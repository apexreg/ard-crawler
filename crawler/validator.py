from __future__ import annotations
import jsonschema
from typing import Any, Dict, List, Tuple

# Minimal ARD-like schema for ai-catalog.json entries
ARD_ENTRY_SCHEMA = {
    "type": "object",
    "required": ["name", "description"],
    "properties": {
        "name": {"type": "string"},
        "description": {"type": "string"},
        "protocols": {
            "type": "array",
            "items": {"type": "string"}
        },
        "endpoints": {
            "type": "object"
        }
    }
}

def validate_entry(entry: Dict[str, Any]) -> Tuple[bool, str]:
    """
    Validate a single ARD catalog entry.
    Returns (is_valid, error_message).
    """
    try:
        jsonschema.validate(instance=entry, schema=ARD_ENTRY_SCHEMA)
        return True, ""
    except jsonschema.ValidationError as e:
        return False, str(e.message)

def validate_catalog(catalog: Dict[str, Any]) -> Tuple[bool, List[str]]:
    """
    Validate an ai-catalog.json catalog.
    Assumes catalog has a top-level 'entries' list or is itself a list of entries.
    Returns (all_valid, list_of_errors).
    """
    errors = []
    entries = catalog.get("entries", [])
    if not entries and isinstance(catalog, list):
        entries = catalog
    for i, entry in enumerate(entries):
        ok, msg = validate_entry(entry)
        if not ok:
            errors.append(f"Entry {i}: {msg}")
    return len(errors) == 0, errors
