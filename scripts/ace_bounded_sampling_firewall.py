"""Bounded metadata-only sampling firewall for ACE issue 67."""
from __future__ import annotations
import importlib.util
import json
import os
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-bounded-sampling-firewall-contract.json")
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
MANIFEST_CONTRACT_PATH = Path("config/ace-manifest-evidence-contract.json")
GOOD_FIXTURE_PATH = Path("tests/fixtures/ace-bounded-sampling-firewall/good-request.json")
SHAPE_FIXTURE_PATH = Path("tests/fixtures/ace-bounded-sampling-firewall/metadata-shape-only-evidence-request.json")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
PLAN_PATH = Path("docs/plans/2026-06-30-issue-67-ace-wave-0-bounded-sampling-firewall.md")
APPROVAL_MARKER_PATH = Path(".planning/plan-approved/67.md")
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
SOURCE_ROOT_ERROR = "ACE_SOURCE_ROOT_ACCESS_FORBIDDEN"
MISSING_EVIDENCE = "MISSING_62_EVIDENCE_CONTRACT"
PLACEHOLDER_TERMS = ("pending", "not-run", "expected", "todo", "tbd", "missing", "forged")
SORT_KEYS = {"strategy", "term_refs", "direction", "tie_breaker"}
DENIED_OPERATION_TOKENS = {
    "recursive_traversal": ["find", "du", "os" + ".walk", "rglob", "glob"],
    "broad_source_root_search": ["rg", "fd", "grep", "ls " + "-R"],
    "manifest_query": ["jq", "select", "query"],
    "raw_manifest_read": ["cat", "read_text", "open"],
    "full_file_count": ["wc", "count"],
    "full_file_digest": ["sha256sum", "digest"],
    "materialization": ["materialize", "copy", "export", "cp", "rsync", "tar", "sqlite", ".dump"],
}
@dataclass
class FirewallResult:
    allowed: bool = False
    authorized: bool = False
    reason_code: str = ""
    errors: list[str] = field(default_factory=list)
    blocked_by_issue: int | None = None
    follow_on_issue: int | None = None
class SourceRootAccessForbidden(RuntimeError): pass
def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path
def load_contract(path: Path = CONTRACT_PATH) -> dict:
    return json.loads(repo_path(path).read_text())
def load_schema(path: Path = SCHEMA_PATH) -> dict:
    return json.loads(repo_path(path).read_text())
def load_manifest_contract(path: Path = MANIFEST_CONTRACT_PATH) -> dict:
    return json.loads(repo_path(path).read_text())
def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_contract(path)
    except FileNotFoundError:
        return [f"missing bounded sampling firewall contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"bounded sampling firewall contract JSON is invalid: {exc}"]
    return validate_contract(contract, load_schema(), load_manifest_contract())
def validate_request_file(path: Path, contract: dict | None = None) -> list[str]:
    try:
        request = json.loads(repo_path(path).read_text())
    except FileNotFoundError:
        return [f"missing bounded sampling request: {path}"]
    except json.JSONDecodeError as exc:
        return [f"bounded sampling request JSON is invalid: {exc}"]
    result = validate_sampling_request(request, contract or load_contract())
    return result.errors if result.authorized else result.errors or [result.reason_code]
def validate_contract(contract: dict, schema: dict, manifest_contract: dict) -> list[str]:
    errors: list[str] = []
    expected = {
        "contract_id": "ace-bounded-sampling-firewall",
        "owner_issue": 67,
        "depends_on_schema_issue": 65,
        "schema_path": SCHEMA_PATH.as_posix(),
        "manifest_evidence_contract_path": MANIFEST_CONTRACT_PATH.as_posix(),
        "method_issue_bindings": [1, 12],
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"contract must set {key} to {value!r}")
    if not re.fullmatch(r"1\.0\.\d+", str(contract.get("contract_version", ""))):
        errors.append("contract_version must use 1.0.x semver")
    if contract.get("allowed_manifest_sources") != manifest_contract.get("manifest_source_keys"):
        errors.append("allowed manifest sources must import #62 manifest source keys")
    if contract.get("output_shape_route_store", {}).get("logical_target_store") != schema["route_store_matrix"]["metadata_only"]:
        errors.append("metadata-only route/store must import #65 schema matrix")
    for forbidden in ["route_store_matrix", "private_source_field_terms", "source_like_raw_digest_terms"]:
        if forbidden in contract:
            errors.append(f"contract must not redefine #65 {forbidden}")
    if contract.get("request_classes") != [
        "control_plane_proof",
        "downstream_manifest_backed_sampling",
        "metadata_only_fixture",
    ]:
        errors.append("request_classes must match the closed #67 set")
    if set(contract.get("required_sampling_fields", [])) != _base_request_keys():
        errors.append("required sampling fields must match the closed base key set")
    if contract.get("maximum_caps") != {
        "per_bucket_row_cap": 200,
        "max_files_touched": 25,
        "max_bytes_touched": 1048576,
    }:
        errors.append("maximum caps must match the coordination bounded-read contract")
    if not contract.get("public_safety_notes"):
        errors.append("contract must include public_safety_notes")
    return errors
def validate_sampling_request(request: dict, contract: dict | None = None, env: dict[str, str] | None = None) -> FirewallResult:
    contract = contract or load_contract()
    guarded = _guard_result("validate_sampling_request", env)
    if guarded:
        return guarded
    context_result = _scan_json_context_fields(request, contract, env)
    if context_result:
        return FirewallResult(False, False, context_result.reason_code, context_result.errors)
    errors: list[str] = []
    _validate_key_shape(request, contract, errors)
    _validate_common_fields(request, contract, errors)
    if errors:
        return FirewallResult(False, False, "INVALID_SAMPLING_REQUEST", errors)
    issue = request["target_issue"]
    if issue in contract["non_target_issues"]:
        return FirewallResult(False, False, "NON_TARGET_SAMPLING_ISSUE", ["target issue is not a #67 sampling target"])
    if issue == 67:
        return _validate_metadata_fixture(request, contract)
    if 52 <= issue <= 60:
        return _validate_downstream_request(request, contract)
    if str(issue) in contract["control_plane_issue_classes"]:
        return _validate_control_plane_request(request, contract)
    return FirewallResult(False, False, "UNKNOWN_SAMPLING_TARGET", [f"unknown target issue: {issue}"])
def classify_executable_context(
    text: str,
    trigger: str,
    contract: dict | None = None,
    env: dict[str, str] | None = None,
) -> FirewallResult:
    contract = contract or load_contract()
    if trigger not in contract["executable_context_triggers"]:
        return FirewallResult(False, False, "UNKNOWN_EXECUTABLE_CONTEXT", ["unknown executable context trigger"])
    if _looks_source_root_capable(text, contract):
        guarded = _guard_result("classify_executable_context", env)
        if guarded:
            return guarded
    if trigger == "markdown_policy_prose" and not _has_command_like_token(text):
        return FirewallResult(True, False)
    if _is_denied_text(text, contract):
        return FirewallResult(False, False, "DENIED_EXECUTABLE_CONTEXT", ["denied executable source-root context"])
    return FirewallResult(True, False)
def validate_manifest_operation(
    manifest_source: str,
    operation_name: str,
    contract: dict | None = None,
    env: dict[str, str] | None = None,
) -> FirewallResult:
    contract = contract or load_contract()
    guarded = _guard_result("validate_manifest_operation", env)
    if guarded:
        return guarded
    if manifest_source not in contract["allowed_manifest_sources"]:
        return FirewallResult(False, False, "UNKNOWN_MANIFEST_SOURCE", ["manifest source is not allowed"])
    if operation_name in contract["denied_token_matrix"]["manifest_operations"]:
        return FirewallResult(False, False, "DENIED_MANIFEST_OPERATION", ["unbounded manifest operation denied"])
    if operation_name == "bounded_sample_selection":
        gate = contract["downstream_evidence_gate"]
        return FirewallResult(False, False, MISSING_EVIDENCE, [MISSING_EVIDENCE], gate["blocked_by_issue"], gate["follow_on_issue"])
    allowed = {"bounded_metadata_probe", "snapshot_evidence_check"}
    return FirewallResult(operation_name in allowed, False, "" if operation_name in allowed else "UNKNOWN_MANIFEST_OPERATION")
def build_runtime_deny_fixture(
    operation_name: str,
    manifest_source: str,
    contract: dict | None = None,
    env: dict[str, str] | None = None,
) -> str:
    guarded = _guard_result("build_runtime_deny_fixture", env)
    if guarded:
        return guarded.reason_code
    source_root = "ACE_" + "SHARE_ROOT"
    command = {
        "recursive_traversal": "find",
        "broad_source_root_search": "rg",
        "manifest_query": "jq",
        "raw_manifest_read": "cat",
        "full_file_count": "wc -l",
        "full_file_digest": "sha256sum",
        "materialization": "materialize",
    }.get(operation_name, operation_name)
    return "```sh\n" + command + " ${" + source_root + "}/" + manifest_source + "\n```"
def guard_no_source_root_access(operation_name: str, env: dict[str, str] | None = None) -> None:
    active_env = env if env is not None else os.environ
    if active_env.get("ACE_SHARE_ROOT"):
        raise SourceRootAccessForbidden(f"{SOURCE_ROOT_ERROR}: {operation_name}")
def review_artifact_paths(root: Path | None = None) -> list[Path]:
    default_root = REPO_ROOT / "scripts" / "review" / "results"
    artifact_root = root or default_root
    if not artifact_root.exists():
        return []
    prefix = Path() if root else Path("scripts/review/results")
    return [prefix / path.name for path in sorted(artifact_root.glob("*67*.md"))]
def validate_review_sidecars(root: Path | None = None) -> list[str]:
    artifact_root = root or REPO_ROOT / "scripts" / "review" / "results"
    if not artifact_root.exists():
        return []
    sidecars = list(artifact_root.glob("*67*.stderr")) + list(artifact_root.glob("*67*.err"))
    return [f"review sidecar must be normalized or deleted before retention: {path.name}" for path in sidecars]
def public_scan_paths() -> list[Path]:
    paths = [
        PLAN_PATH,
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        Path("artifacts/ace-wave0-ledger-schema.json"),
        CONTRACT_PATH,
        Path("scripts/ace_bounded_sampling_firewall.py"),
        Path("scripts/validate_ace_bounded_sampling_firewall.py"),
        Path("tests/test_validate_ace_bounded_sampling_firewall.py"),
        GOOD_FIXTURE_PATH,
        SHAPE_FIXTURE_PATH,
        WORKFLOW_PATH,
        APPROVAL_MARKER_PATH,
    ]
    paths.extend(review_artifact_paths())
    return paths
def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    parent = _load_parent_validator()
    scan_paths = paths or public_scan_paths()
    return parent.validate_public_artifact_paths([repo_path(path) for path in scan_paths])
def _base_request_keys() -> set[str]:
    return {
        "target_issue",
        "manifest_source",
        "seed_id",
        "sort_rule",
        "per_bucket_row_cap",
        "max_files_touched",
        "max_bytes_touched",
        "request_class",
        "requires_manifest_snapshot_id",
        "output_shape",
        "route_target",
        "logical_target_store",
    }
def _guard_result(operation_name: str, env: dict[str, str] | None) -> FirewallResult | None:
    try:
        guard_no_source_root_access(operation_name, env)
    except SourceRootAccessForbidden:
        return FirewallResult(False, False, SOURCE_ROOT_ERROR, [SOURCE_ROOT_ERROR])
    return None
def _scan_json_context_fields(request: dict, contract: dict, env: dict[str, str] | None) -> FirewallResult | None:
    for field_name in contract["json_executable_context_fields"]:
        if field_name not in request:
            continue
        result = classify_executable_context(str(request[field_name]), "json_request_field", contract, env)
        if not result.allowed:
            return result
    return None
def _validate_key_shape(request: dict, contract: dict, errors: list[str]) -> None:
    expected = set(contract["required_sampling_fields"])
    if "target_wave_class" in request:
        expected.add("target_wave_class")
    if "fixture_scope" in request:
        expected.add("fixture_scope")
    if "snapshot_evidence" in request:
        expected.add("snapshot_evidence")
    missing = _base_request_keys() - set(request)
    extra = set(request) - expected
    if missing:
        errors.append(f"missing required sampling field(s): {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"unknown sampling field(s): {', '.join(sorted(extra))}")
    if ("target_wave_class" in request) == ("fixture_scope" in request):
        errors.append("request must carry exactly one target_wave_class or fixture_scope")
def _validate_common_fields(request: dict, contract: dict, errors: list[str]) -> None:
    if not isinstance(request.get("target_issue"), int):
        errors.append("target_issue must be a JSON integer")
    if request.get("manifest_source") not in contract["allowed_manifest_sources"]:
        errors.append("manifest_source must use the closed manifest source enum")
    for field_name, limit in contract["maximum_caps"].items():
        value = request.get(field_name)
        if not isinstance(value, int) or value <= 0 or value > limit:
            errors.append(f"{field_name} cap must be a positive integer no greater than {limit}")
    _validate_seed(request.get("seed_id"), contract, errors)
    _validate_sort_rule(request.get("sort_rule"), errors)
    expected_route = contract["output_shape_route_store"]
    for field_name, expected in expected_route.items():
        if request.get(field_name) != expected:
            errors.append(f"{field_name} must stay on the metadata_only route/store boundary")
    if request.get("request_class") not in contract["request_classes"]:
        errors.append("request_class must use the closed #67 enum")
    _validate_snapshot_placeholders(request.get("snapshot_evidence"), errors)
def _validate_seed(seed_id: object, contract: dict, errors: list[str]) -> None:
    if not isinstance(seed_id, str) or not seed_id.startswith(contract["seed_rule"]["prefix"]):
        errors.append("seed_id must be fixed and reviewable")
        return
    lowered = seed_id.lower()
    if any(fragment in lowered for fragment in contract["seed_rule"]["forbidden_fragments"]):
        errors.append("seed_id must not be random, clock-derived, user-local, or unstated")
def _validate_sort_rule(sort_rule: object, errors: list[str]) -> None:
    schema_terms = set(load_schema()["private_source_field_terms"])
    if not isinstance(sort_rule, dict) or set(sort_rule) != SORT_KEYS:
        errors.append("sort_rule must use exactly strategy, term_refs, direction, and tie_breaker")
        return
    if sort_rule.get("strategy") != "stable_private_term_order":
        errors.append("sort_rule strategy must be stable_private_term_order")
    if sort_rule.get("direction") not in {"ascending", "descending"}:
        errors.append("sort_rule direction must be ascending or descending")
    if sort_rule.get("tie_breaker") != "public_manifest_row_ordinal":
        errors.append("sort_rule tie_breaker must be public_manifest_row_ordinal")
    refs = sort_rule.get("term_refs")
    if not isinstance(refs, list) or not refs:
        errors.append("sort_rule term_refs must be a non-empty array")
        return
    for ref in refs:
        if ref not in schema_terms or any(token in str(ref) for token in [":", "=", "/", "\\"]):
            errors.append("sort_rule term_refs must contain only #65 private schema terms as values")
def _validate_metadata_fixture(request: dict, contract: dict) -> FirewallResult:
    errors: list[str] = []
    if request.get("request_class") != "metadata_only_fixture":
        errors.append("#67 fixture must use metadata_only_fixture")
    if request.get("fixture_scope") != contract["metadata_fixture_scope"]:
        errors.append("#67 fixture_scope must be firewall_validator_self_check")
    if request.get("requires_manifest_snapshot_id") is not False:
        errors.append("#67 metadata fixture requires_manifest_snapshot_id must be false")
    evidence = request.get("snapshot_evidence")
    if evidence is not None:
        _validate_shape_only_evidence(evidence, errors)
    return FirewallResult(not errors, not errors, "AUTHORIZED_METADATA_ONLY_FIXTURE" if not errors else "INVALID_METADATA_FIXTURE", errors)
def _validate_downstream_request(request: dict, contract: dict) -> FirewallResult:
    errors: list[str] = []
    if request.get("request_class") != "downstream_manifest_backed_sampling":
        errors.append("ingestion waves must use downstream_manifest_backed_sampling")
    if request.get("target_wave_class") != "ingestion_wave":
        errors.append("ingestion waves must import target_wave_class=ingestion_wave")
    if request.get("requires_manifest_snapshot_id") is not True:
        errors.append("ingestion waves must import requires_manifest_snapshot_id=true from #65")
    _validate_blocked_evidence(request.get("snapshot_evidence"), errors)
    gate = contract["downstream_evidence_gate"]
    return FirewallResult(False, False, MISSING_EVIDENCE, errors or [MISSING_EVIDENCE], gate["blocked_by_issue"], gate["follow_on_issue"])
def _validate_control_plane_request(request: dict, contract: dict) -> FirewallResult:
    errors: list[str] = []
    expected_class = contract["control_plane_issue_classes"][str(request["target_issue"])]
    if request.get("request_class") != "control_plane_proof":
        errors.append("control-plane targets must use control_plane_proof")
    if request.get("target_wave_class") != expected_class:
        errors.append("control-plane target_wave_class does not match #65 registry")
    if "snapshot_evidence" in request:
        errors.append("control-plane proof forbids snapshot_evidence")
    return FirewallResult(False, False, "CONTROL_PLANE_PROOF_NOT_SAMPLING_REQUEST", errors)
def _validate_shape_only_evidence(evidence: object, errors: list[str]) -> None:
    if not isinstance(evidence, dict):
        errors.append("snapshot_evidence must be an object")
        return
    required = {"evidence_mode", "source_issue", "recorded_at"}
    optional = {"shape_only_artifact_ref"}
    if evidence.get("evidence_mode") != "shape_only_fixture" or evidence.get("source_issue") != 62:
        errors.append("shape-only evidence must name issue 62 and evidence_mode=shape_only_fixture")
    if missing := required - set(evidence):
        errors.append(f"shape-only evidence missing field(s): {', '.join(sorted(missing))}")
    if extra := set(evidence) - required - optional:
        errors.append(f"shape-only evidence forbids field(s): {', '.join(sorted(extra))}")
def _validate_blocked_evidence(evidence: object, errors: list[str]) -> None:
    required = {"evidence_mode", "source_issue", "blocked_by_issue", "follow_on_issue", "reason_code", "recorded_at"}
    if not isinstance(evidence, dict):
        errors.append("downstream sampling requires blocked_pending_62_contract snapshot_evidence")
        return
    if evidence.get("evidence_mode") != "blocked_pending_62_contract":
        errors.append("operational evidence parser is owned by #70; #67 fails closed")
        return
    expected = {"source_issue": 62, "blocked_by_issue": 62, "follow_on_issue": 70, "reason_code": MISSING_EVIDENCE}
    for key, value in expected.items():
        if evidence.get(key) != value:
            errors.append(f"blocked evidence must set {key} to {value!r}")
    if missing := required - set(evidence):
        errors.append(f"blocked evidence missing field(s): {', '.join(sorted(missing))}")
    if extra := set(evidence) - required:
        errors.append(f"blocked evidence forbids field(s): {', '.join(sorted(extra))}")
def _validate_snapshot_placeholders(evidence: object, errors: list[str]) -> None:
    if not isinstance(evidence, dict):
        return
    for key, value in evidence.items():
        if key == "evidence_mode" and value == "blocked_pending_62_contract":
            continue
        if key == "reason_code" and value == MISSING_EVIDENCE:
            continue
        if isinstance(value, str) and any(term in value.lower() for term in PLACEHOLDER_TERMS):
            errors.append("placeholder snapshot evidence is not allowed")
def _looks_source_root_capable(text: str, contract: dict) -> bool:
    source_root = "ACE_" + "SHARE_ROOT"
    return source_root in text or any(source in text for source in contract["allowed_manifest_sources"])
def _has_command_like_token(text: str) -> bool:
    lowered = text.lower()
    return any(token.lower() in lowered for tokens in DENIED_OPERATION_TOKENS.values() for token in tokens)
def _is_denied_text(text: str, contract: dict) -> bool:
    if not _looks_source_root_capable(text, contract):
        return False
    return _has_command_like_token(text)
def _load_parent_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_epic_wave_coordination_for_67_runtime", PARENT_VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module
