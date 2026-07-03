"""Documented utility fixture.

This module carries a durable explanation in its docstring. The code body is
not a bulk-ingestion target; only metadata and documentation signals are kept.
"""


def normalize_label(value: str) -> str:
    """Return a normalized label for synthetic examples."""
    return value.strip().lower().replace(" ", "-")
