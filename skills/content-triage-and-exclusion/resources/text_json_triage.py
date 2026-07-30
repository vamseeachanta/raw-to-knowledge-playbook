"""Synthetic wave-1 text/markup/code/small-JSON triage helper."""
from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


JSON_SUFFIXES = {".json"}
MARKUP_SUFFIXES = {".md", ".markdown", ".rst", ".txt"}
CODE_SUFFIXES = {".py", ".js", ".ts", ".jsx", ".tsx"}
EXCLUDED_ROUTE = "excluded_no_ingest"
KEPT_PRIVATE_ROUTE = "private_sidecar"
METADATA_ROUTE = "metadata_only"
REPO_ROOT = Path(__file__).resolve().parents[3]
SCHEMA_PATH = REPO_ROOT / "artifacts" / "ace-wave0-ledger-schema.json"


def classify_candidate(file_path: str | Path, public_clearance: bool = False) -> dict[str, Any]:
    path = Path(file_path)
    text = path.read_text(errors="replace")
    suffix = path.suffix.lower()
    base = _base_record(path, public_clearance)
    if suffix in JSON_SUFFIXES:
        return _classify_json(path, text, base)
    if suffix in MARKUP_SUFFIXES:
        if _has_markup_value(text, suffix):
            return _kept(base, "hand_authored_markup", _route_for_text(public_clearance), ["markup_heading", "prose_density"])
        return _excluded(base, "source_tree_noise", "empty_or_low_value_markup", ["low_prose_density"])
    if suffix in CODE_SUFFIXES:
        return _classify_code(path, text, base)
    return _excluded(base, "source_tree_noise", "unsupported_wave1_type", ["unsupported_suffix"])


def _base_record(path: Path, public_clearance: bool) -> dict[str, Any]:
    return {
        "candidate_id": f"fixture-{path.stem}",
        "parse_status": "synthetic_fixture",
        "visibility": "public" if public_clearance else "private",
        "public_clearance": public_clearance,
    }


def _classify_json(path: Path, text: str, base: dict[str, Any]) -> dict[str, Any]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return _excluded(base, "source_tree_noise", "invalid_json", ["json_decode_error"])
    signals = json_signals(payload, path.name, text)
    if "lockfile" in signals:
        return _excluded(base, "generated_lockfile_like_json", "generated_lockfile_like_json", signals)
    if _is_generated_json(signals):
        return _excluded(base, "generated_repetitive_json", "generated_repetitive_noise", signals)
    return _kept(base, "small_config_json", METADATA_ROUTE, signals or ["small_config_shape"])


def _classify_code(path: Path, text: str, base: dict[str, Any]) -> dict[str, Any]:
    if path.suffix.lower() == ".py" and _has_module_docstring(text):
        return _kept(base, "code_documentation", METADATA_ROUTE, ["module_docstring", "source_tree_metadata_only"])
    if _looks_minified(text):
        return _excluded(base, "source_tree_noise", "minified_or_vendored_code", ["minified_source_tree_noise"])
    if _has_code_comment(text):
        return _kept(base, "code_documentation", METADATA_ROUTE, ["code_comments", "source_tree_metadata_only"])
    return _excluded(base, "source_tree_noise", "undocumented_source_tree_code", ["source_tree_noise"])


def json_signals(payload: Any, filename: str = "", raw_text: str = "") -> list[str]:
    signals: list[str] = []
    lowered = filename.lower()
    if "lock" in lowered or _has_lockfile_shape(payload):
        signals.append("lockfile")
    if _has_package_cache_shape(payload):
        signals.append("package_cache_shape")
    if _has_key(payload, "generated_at"):
        signals.append("generated_timestamp")
    if _has_high_cardinality_list(payload):
        signals.append("high_cardinality_list")
    if _has_high_cardinality_keys(payload):
        signals.append("high_cardinality_keys")
    if _has_repeated_object_templates(payload):
        signals.append("near_duplicate_object_templates")
    if _looks_minified_json_payload(payload, raw_text):
        signals.append("minified_bulk_array")
    return signals


def _has_lockfile_shape(value: Any) -> bool:
    return isinstance(value, dict) and (
        "lockfileVersion" in value
        or ("packages" in value and "dependencies" in value)
        or ("packages" in value and _nested_key_contains(value.get("packages"), "node_modules"))
    )


def _has_package_cache_shape(value: Any) -> bool:
    if not isinstance(value, dict):
        return False
    cache = value.get("cache")
    if isinstance(cache, dict) and isinstance(cache.get("packages"), list):
        return any(_looks_package_record(item) for item in cache["packages"])
    packages = value.get("packages")
    if isinstance(packages, list):
        return any(_looks_package_record(item) for item in packages)
    return False


def _looks_package_record(value: Any) -> bool:
    return isinstance(value, dict) and "version" in value and any(key in value for key in ["integrity", "resolved", "name"])


def _has_key(value: Any, target: str) -> bool:
    if isinstance(value, dict):
        return target in value or any(_has_key(child, target) for child in value.values())
    if isinstance(value, list):
        return any(_has_key(child, target) for child in value)
    return False


def _has_high_cardinality_list(value: Any) -> bool:
    if isinstance(value, list):
        return len(value) >= 8 or any(_has_high_cardinality_list(child) for child in value)
    if isinstance(value, dict):
        return any(_has_high_cardinality_list(child) for child in value.values())
    return False


def _has_high_cardinality_keys(value: Any) -> bool:
    if isinstance(value, dict):
        keys = [str(key) for key in value]
        path_like_keys = [key for key in keys if _looks_generated_path_key(key)]
        if len(path_like_keys) >= 8:
            return True
        return any(_has_high_cardinality_keys(child) for child in value.values())
    if isinstance(value, list):
        return any(_has_high_cardinality_keys(child) for child in value)
    return False


def _looks_generated_path_key(key: str) -> bool:
    if "/" not in key and "\\" not in key:
        return False
    suffix = Path(key).suffix.lower()
    if suffix not in {".json", ".xml", ".csv", ".txt", ".log", ".dat", ".out"}:
        return False
    return any(char.isdigit() for char in key)


def _has_repeated_object_templates(value: Any) -> bool:
    if isinstance(value, list) and len(value) >= 5:
        key_sets = [tuple(sorted(item)) for item in value if isinstance(item, dict)]
        return len(key_sets) >= 5 and len(set(key_sets)) == 1
    if isinstance(value, dict):
        return any(_has_repeated_object_templates(child) for child in value.values())
    if isinstance(value, list):
        return any(_has_repeated_object_templates(child) for child in value)
    return False


def _is_generated_json(signals: list[str]) -> bool:
    signal_set = set(signals)
    return bool(
        "high_cardinality_list" in signal_set
        or "high_cardinality_keys" in signal_set
        or "near_duplicate_object_templates" in signal_set
        or "package_cache_shape" in signal_set
        or {"generated_timestamp", "minified_bulk_array"} & signal_set
    )


def _looks_minified_json_payload(payload: Any, raw_text: str) -> bool:
    compact = raw_text.strip()
    return isinstance(payload, list) and len(payload) >= 5 and "\n" not in compact and len(compact) >= 80


def _nested_key_contains(value: Any, fragment: str) -> bool:
    if isinstance(value, dict):
        return any(fragment in str(key) or _nested_key_contains(child, fragment) for key, child in value.items())
    if isinstance(value, list):
        return any(_nested_key_contains(child, fragment) for child in value)
    return False


def _has_module_docstring(text: str) -> bool:
    try:
        module = ast.parse(text)
    except SyntaxError:
        return False
    return bool(ast.get_docstring(module))


def _looks_minified(text: str) -> bool:
    lines = [line for line in text.splitlines() if line.strip()]
    if not lines:
        return False
    longest = max(len(line) for line in lines)
    return len(lines) <= 3 and longest >= 100 and text.count(";") >= 2


def _has_code_comment(text: str) -> bool:
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#!"):
            continue
        if stripped.startswith("#") and _has_wordy_comment(stripped[1:]):
            return True
        if stripped.startswith("//") and _has_wordy_comment(stripped[2:]):
            return True
        if stripped.startswith(("/*", "/**")) and _has_wordy_comment(stripped.lstrip("/*")):
            return True
    return False


def _has_markup_value(text: str, suffix: str) -> bool:
    stripped = text.strip()
    if not stripped:
        return False
    words = [word for word in stripped.replace("\n", " ").split(" ") if word.strip()]
    if len(words) < 8:
        return False
    if suffix == ".rst":
        return "====" in stripped or "----" in stripped
    return "#" in stripped or len(words) >= 12


def _has_wordy_comment(text: str) -> bool:
    return len([word for word in text.strip().split() if word]) >= 4


def _route_for_text(public_clearance: bool) -> str:
    return "public_llm_wiki" if public_clearance else KEPT_PRIVATE_ROUTE


def _kept(base: dict[str, Any], candidate_class: str, route_target: str, signals: list[str]) -> dict[str, Any]:
    base.update(
        {
            "candidate_class": candidate_class,
            "route_target": route_target,
            "logical_target_store": _route_store(route_target),
            "visibility": _visibility_for_route(route_target),
            "signals": signals,
            "extraction_estimate": {"unit": "logical_sections", "expected_count": 1},
            "extraction_yield": {"unit": "logical_sections", "observed_count": 1},
        }
    )
    return base


def _excluded(base: dict[str, Any], candidate_class: str, reason: str, signals: list[str]) -> dict[str, Any]:
    base.update(
        {
            "candidate_class": candidate_class,
            "route_target": EXCLUDED_ROUTE,
            "logical_target_store": _route_store(EXCLUDED_ROUTE),
            "visibility": "none",
            "signals": signals,
            "hard_exclusion_reason": reason,
        }
    )
    return base


def _route_store(route_target: str) -> str:
    schema = json.loads(SCHEMA_PATH.read_text())
    return schema["route_store_matrix"][route_target]


def _visibility_for_route(route_target: str) -> str:
    if route_target == "public_llm_wiki":
        return "public"
    if route_target in {"private_sidecar", "metadata_only"}:
        return "private"
    return "none"
