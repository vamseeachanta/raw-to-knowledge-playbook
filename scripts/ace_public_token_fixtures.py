"""Fixture-only public token and placeholder helpers for ACE issue 66."""
from __future__ import annotations

import importlib.util
import json
import re
import secrets
import sys
from pathlib import Path
from typing import Callable, Iterable


REPO_ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = Path("config/ace-public-token-fixture-contract.json")
SCHEMA_PATH = Path("artifacts/ace-wave0-ledger-schema.json")
GOOD_FIXTURE_PATH = Path("tests/fixtures/ace-public-token-fixtures/good-request.json")
WORKFLOW_PATH = Path(".github/workflows/validate.yml")
PLAN_PATH = Path("docs/plans/2026-06-30-issue-66-ace-public-token-fixtures-private-field-placeholders.md")
APPROVAL_MARKER_PATH = Path(".planning/plan-approved/66.md")
PARENT_VALIDATOR_PATH = REPO_ROOT / "scripts" / "validate_ace_epic_wave_coordination.py"
TOKEN_PREFIX = "pst_"
TOKEN_HEX_CHARS = 32
TOKEN_RE = re.compile(rf"^{TOKEN_PREFIX}[0-9a-f]{{{TOKEN_HEX_CHARS}}}$")
TOKEN_LITERAL_RE = re.compile(rf"\b{TOKEN_PREFIX}[0-9a-f]{{{TOKEN_HEX_CHARS}}}\b")
ROW_ID_RE = re.compile(r"^fixture_row_\d{3}$")
SEMVER_RE = re.compile(r"^1\.0\.\d+$")
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
HEX_DIGEST_RE = re.compile(r"^[0-9a-f]{32,128}$", re.IGNORECASE)
PRIVATE_SOURCE_TERMS = [
    "source_" + "id",
    "source_" + "sha256",
    "private_" + "lookup_key",
    "private_" + "lookup_map",
    "share_" + "relative_path_private_only",
]
SOURCE_DIGEST_TERMS = ["source_" + "hash", "provenance_" + "pointer"]
PLACEHOLDER_VALUES = [
    "ACE_PRIVATE_PLACEHOLDER_IDENTITY",
    "ACE_PRIVATE_PLACEHOLDER_DIGEST",
    "ACE_PRIVATE_PLACEHOLDER_LOOKUP_KEY",
    "ACE_PRIVATE_PLACEHOLDER_LOOKUP_MAP",
    "ACE_PRIVATE_PLACEHOLDER_PATH",
]
FORBIDDEN_REQUEST_KEYS = [
    "source_" + "name",
    "source_" + "path",
    "source_" + "hash",
    "source_" + "key",
    "lookup_alias",
    "display_name",
    "original_name",
    "raw_provenance",
    "deterministic_seed",
]
REQUEST_KEYS = ["fixture_set_id", "fixture_row_id", "count"]
FIXTURE_SET_IDS = ["wave0_public_token_good"]
ALLOWED_FIXTURE_KEYS = {"fixture_kind", "public_source_token_request", "private_field_placeholders"}


def repo_path(path: Path) -> Path:
    return path if path.is_absolute() else REPO_ROOT / path


def load_contract(path: Path = CONTRACT_PATH) -> dict:
    return json.loads(repo_path(path).read_text())


def load_schema(path: Path = SCHEMA_PATH) -> dict:
    return json.loads(repo_path(path).read_text())


def validate_contract_file(path: Path = CONTRACT_PATH) -> list[str]:
    try:
        contract = load_contract(path)
    except FileNotFoundError:
        return [f"missing fixture contract: {path}"]
    except json.JSONDecodeError as exc:
        return [f"fixture contract JSON is invalid: {exc}"]
    return validate_contract(contract, load_schema())


def validate_fixture_file(path: Path = GOOD_FIXTURE_PATH) -> list[str]:
    try:
        fixture = json.loads(repo_path(path).read_text())
    except FileNotFoundError:
        return [f"missing fixture request: {path}"]
    except json.JSONDecodeError as exc:
        return [f"fixture request JSON is invalid: {exc}"]
    return validate_fixture(fixture, load_contract())


def validate_contract(contract: dict, schema: dict) -> list[str]:
    errors: list[str] = []
    _validate_contract_metadata(contract, errors)
    _validate_schema_imports(contract, schema, errors)
    _validate_contract_grammar(contract, errors)
    _validate_private_term_placement(contract, errors)
    _validate_optional_public_output_contract(contract, errors)
    return errors


def validate_fixture(fixture: dict, contract: dict) -> list[str]:
    errors: list[str] = []
    _validate_fixture_top_level(fixture, errors)
    _validate_request_marker(fixture.get(contract["generation_request_marker"]), contract, errors)
    _validate_placeholder_rows(fixture.get("private_field_placeholders"), contract, errors)
    _validate_no_leaky_values(fixture, contract, errors, allow_schema_terms=True)
    return errors


def generate_fixture_tokens(
    request_marker: dict,
    *,
    random_hex: Callable[[], str] | None = None,
) -> list[str]:
    contract = load_contract()
    errors: list[str] = []
    _validate_request_marker(request_marker, contract, errors)
    if errors:
        raise ValueError("; ".join(errors))
    random_hex = random_hex or (lambda: secrets.token_hex(TOKEN_HEX_CHARS // 2))
    return _unique_tokens(request_marker["count"], random_hex)


def public_scan_paths() -> list[Path]:
    paths = [
        PLAN_PATH,
        Path("docs/plans/README.md"),
        Path("docs/plans/ace-share-ingestion-wave-coordination.md"),
        CONTRACT_PATH,
        GOOD_FIXTURE_PATH,
        Path("scripts/ace_public_token_fixtures.py"),
        Path("scripts/validate_ace_public_token_fixtures.py"),
        Path("tests/test_validate_ace_public_token_fixtures.py"),
        Path("tests/test_validate_ace_wave0_schema_contract.py"),
        WORKFLOW_PATH,
        APPROVAL_MARKER_PATH,
    ]
    paths.extend(_plan_review_artifacts())
    return paths


def validate_public_surfaces(paths: list[Path] | None = None) -> list[str]:
    parent = _load_parent_validator()
    scan_paths = paths or public_scan_paths()
    return parent.validate_public_artifact_paths([repo_path(path) for path in scan_paths])


def _validate_contract_metadata(contract: dict, errors: list[str]) -> None:
    expected = {
        "contract_id": "ace-public-token-fixture-contract",
        "owner_issue": 66,
        "mode": "fixture_only",
        "depends_on_schema_issue": 65,
        "schema_path": SCHEMA_PATH.as_posix(),
        "durable_lookup_owner_issue": 61,
        "publication_certification_owner_issue": 63,
        "public_surface_scanner_consumer_issue": 68,
    }
    for key, value in expected.items():
        if contract.get(key) != value:
            errors.append(f"fixture contract must set {key} to {value!r}")
    if not SEMVER_RE.fullmatch(str(contract.get("contract_version", ""))):
        errors.append("fixture contract_version must use 1.0.x semver")


def _validate_schema_imports(contract: dict, schema: dict, errors: list[str]) -> None:
    token = schema.get("downstream_contracts", {}).get("public_token", {})
    if contract.get("public_token_field_name") != token.get("field_name"):
        errors.append("fixture contract must import #65 public token field")
    if contract.get("public_token_policy_owner_issues") != token.get("owner_issues"):
        errors.append("fixture contract must preserve #65 public token policy owners")
    if contract.get("private_source_terms") != schema.get("private_source_field_terms"):
        errors.append("fixture contract must import #65 private source terms")
    if contract.get("source_like_raw_digest_terms") != schema.get("source_like_raw_digest_terms"):
        errors.append("fixture contract must import #65 source-like digest terms")
    for forbidden in ["route_targets", "logical_target_stores", "route_store_matrix"]:
        if forbidden in contract:
            errors.append(f"fixture contract must not redefine #65 {forbidden}")


def _validate_contract_grammar(contract: dict, errors: list[str]) -> None:
    grammar = contract.get("public_token_grammar", {})
    if grammar != {"prefix": TOKEN_PREFIX, "hex_characters": TOKEN_HEX_CHARS}:
        errors.append("fixture token grammar must be pst_ plus 32 lowercase hex characters")
    if contract.get("generation_request_marker") != "public_source_token_request":
        errors.append("fixture contract must use public_source_token_request marker")
    if contract.get("generation_request_required_keys") != REQUEST_KEYS:
        errors.append("generation request required keys must stay closed")
    if contract.get("fixture_set_ids") != FIXTURE_SET_IDS:
        errors.append("fixture set enum must contain only the #66 v1 value")
    if contract.get("forbidden_request_keys") != FORBIDDEN_REQUEST_KEYS:
        errors.append("forbidden request keys must match the #66 closed set")
    if contract.get("placeholder_values") != PLACEHOLDER_VALUES:
        errors.append("private placeholder value enum must stay closed")
    _validate_placeholder_rows(contract.get("private_placeholder_mapping"), contract, errors)


def _validate_private_term_placement(contract: dict, errors: list[str]) -> None:
    keys = _collect_keys(contract)
    for term in PRIVATE_SOURCE_TERMS + SOURCE_DIGEST_TERMS:
        if term in keys:
            errors.append(f"private/source-like schema term must not be a JSON key: {term}")


def _validate_optional_public_output_contract(contract: dict, errors: list[str]) -> None:
    path = repo_path(Path("config/ace-public-output-contract.json"))
    if not path.exists():
        if contract.get("provisional_fixture_contract") is not True:
            errors.append("fixture contract must remain provisional until #63 config exists")
        return
    if contract.get("provisional_fixture_contract") is not False:
        errors.append("fixture contract must not remain provisional when #63 config exists")
    try:
        output_contract = json.loads(path.read_text())
    except json.JSONDecodeError as exc:
        errors.append(f"#63 public output contract JSON is invalid: {exc}")
        return
    _validate_public_output_token_policy(contract, output_contract, errors)
    _validate_public_output_field_policy(contract, output_contract, errors)


def _validate_public_output_token_policy(contract: dict, output_contract: dict, errors: list[str]) -> None:
    if output_contract.get("public_token_field_name") != contract.get("public_token_field_name"):
        errors.append("#66 fixture field must match #63 public output contract")
    grammar = output_contract.get("public_token_grammar", {})
    if grammar != {"prefix": TOKEN_PREFIX, "hex_characters": TOKEN_HEX_CHARS}:
        errors.append("#63 public output contract token grammar must match #66 fixture grammar")


def _validate_public_output_field_policy(contract: dict, output_contract: dict, errors: list[str]) -> None:
    public_refs = _consistent_alias_list(
        output_contract,
        ["public_safe_source_reference_fields", "public_source_reference_fields"],
    )
    private_terms = _consistent_alias_list(
        output_contract,
        ["private_only_provenance_fields", "private_only_fields", "banned_public_fields"],
    )
    digest_terms = _consistent_alias_list(
        output_contract,
        ["source_like_raw_digest_terms", "source_hash_private_terms"],
    )
    if public_refs != [contract["public_token_field_name"]]:
        errors.append("#63 public output contract public source references must match #66 fixture field")
    if private_terms != contract["private_source_terms"]:
        errors.append("#63 public output contract private provenance fields must match #66 private terms")
    if digest_terms != contract["source_like_raw_digest_terms"]:
        errors.append("#63 public output contract source-like digest fields must match #66 digest terms")


def _consistent_alias_list(record: dict, names: list[str]):
    values = [record[name] for name in names if name in record]
    if not values:
        return None
    return values[0] if all(value == values[0] for value in values) else "__alias_conflict__"


def _validate_fixture_top_level(fixture: dict, errors: list[str]) -> None:
    if set(fixture) != ALLOWED_FIXTURE_KEYS:
        errors.append("fixture must contain only kind, request marker, and placeholders")
    if fixture.get("fixture_kind") != "synthetic_good_public_token_request":
        errors.append("fixture_kind must identify the synthetic good request")


def _validate_request_marker(marker, contract: dict, errors: list[str]) -> None:
    if not isinstance(marker, dict):
        errors.append("public token request marker must be an object")
        return
    if set(marker) != set(contract["generation_request_required_keys"]):
        errors.append("public token request marker keys must be exactly fixture_set_id, fixture_row_id, count")
    if marker.get("fixture_set_id") not in contract["fixture_set_ids"]:
        errors.append("fixture_set_id must use the closed #66 v1 enum")
    if not ROW_ID_RE.fullmatch(str(marker.get("fixture_row_id", ""))):
        errors.append("fixture_row_id must match fixture_row_<three digits>")
    count = marker.get("count")
    if not isinstance(count, int) or not 1 <= count <= 100:
        errors.append("fixture token count must be an integer from 1 through 100")
    for key in marker:
        if key in contract["forbidden_request_keys"] or key in PRIVATE_SOURCE_TERMS:
            errors.append(f"request marker must not contain source-derived key: {key}")
    _validate_no_leaky_values(marker, contract, errors, allow_schema_terms=False)


def _validate_placeholder_rows(rows, contract: dict, errors: list[str]) -> None:
    if not isinstance(rows, list):
        errors.append("private placeholder mapping must be an array")
        return
    expected = [
        {"schema_term": term, "placeholder_value": placeholder}
        for term, placeholder in zip(contract["private_source_terms"], PLACEHOLDER_VALUES)
    ]
    if rows != expected:
        errors.append("private placeholder mapping must match #65 terms and #66 placeholders")
    for row in rows:
        if not isinstance(row, dict) or set(row) != {"schema_term", "placeholder_value"}:
            errors.append("private placeholder rows must use neutral keys")


def _validate_no_leaky_values(
    value,
    contract: dict,
    errors: list[str],
    *,
    allow_schema_terms: bool,
) -> None:
    for key, item in _walk_items(value):
        if key in contract["forbidden_request_keys"] or key in PRIVATE_SOURCE_TERMS + SOURCE_DIGEST_TERMS:
            errors.append(f"fixture/request key is not allowed: {key}")
        if isinstance(item, str):
            _validate_string_value(key, item, contract, errors, allow_schema_terms=allow_schema_terms)


def _validate_string_value(
    key: str,
    value: str,
    contract: dict,
    errors: list[str],
    *,
    allow_schema_terms: bool,
) -> None:
    if TOKEN_LITERAL_RE.search(value):
        errors.append("fixture values must not contain concrete public token literals")
    if any(part in value for part in ["/", "\\", ".."]) or EMAIL_RE.search(value):
        errors.append("fixture values must not contain path-like or email-like markers")
    if HEX_DIGEST_RE.fullmatch(value):
        errors.append("fixture values must not contain raw digest-like values")
    schema_terms = contract["private_source_terms"] + contract["source_like_raw_digest_terms"]
    if value in schema_terms and allow_schema_terms and key == "schema_term":
        return
    if any(re.search(rf"\b{re.escape(term)}\b", value) for term in schema_terms):
        errors.append("fixture values must not contain private/source-like terms")


def _unique_tokens(count: int, random_hex: Callable[[], str]) -> list[str]:
    tokens: list[str] = []
    seen: set[str] = set()
    attempts = 0
    while len(tokens) < count and attempts < count * 20:
        attempts += 1
        candidate = TOKEN_PREFIX + random_hex()
        if not TOKEN_RE.fullmatch(candidate):
            raise ValueError("random source must return exactly 32 lowercase hex characters")
        if candidate in seen:
            continue
        seen.add(candidate)
        tokens.append(candidate)
    if len(tokens) != count:
        raise ValueError("could not generate unique fixture tokens")
    return tokens


def _plan_review_artifacts() -> list[Path]:
    review_root = REPO_ROOT / "scripts" / "review" / "results"
    if not review_root.exists():
        return []
    patterns = ["*plan-66*.md", "*implementation-66*.md"]
    artifacts = {
        path.relative_to(REPO_ROOT)
        for pattern in patterns
        for path in review_root.glob(pattern)
    }
    return sorted(artifacts)


def _load_parent_validator():
    spec = importlib.util.spec_from_file_location("validate_ace_epic_wave_coordination", PARENT_VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def _collect_keys(value) -> set[str]:
    keys: set[str] = set()
    if isinstance(value, dict):
        for key, nested in value.items():
            keys.add(str(key))
            keys.update(_collect_keys(nested))
    elif isinstance(value, list):
        for nested in value:
            keys.update(_collect_keys(nested))
    return keys


def _walk_items(value) -> Iterable[tuple[str, object]]:
    if isinstance(value, dict):
        for key, nested in value.items():
            yield str(key), nested
            yield from _walk_items(nested)
    elif isinstance(value, list):
        for nested in value:
            yield "", nested
            yield from _walk_items(nested)
