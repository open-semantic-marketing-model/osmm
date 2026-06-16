#!/usr/bin/env python3
"""OSMM schema validation.

Single source of truth = the canonical JSON Schema files in `schemas/`. This
script enforces two guarantees on every run (and in CI):

  1. Every schema in `schemas/*.schema.json` is itself a valid JSON Schema
     (2020-12 meta-schema).
  2. Every instance in `examples/**/*.json` validates against the schema for
     its `object_type`.

Migration-aware: an example whose `object_type` has no schema yet is SKIPPED
(reported, not failed), so CI stays green while schemas are added object by
object. Once every shipped object has a schema, flip STRICT_REQUIRE_SCHEMA to
True to make a missing schema a hard error.

Usage:  python scripts/validate.py
Exit:   0 = all good, 1 = one or more failures.

Requires: jsonschema  (pip install jsonschema)
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError:
    sys.exit("ERROR: this script needs 'jsonschema' — run: pip install jsonschema")

REPO_ROOT = Path(__file__).resolve().parent.parent
SCHEMA_DIR = REPO_ROOT / "schemas"
EXAMPLES_DIR = REPO_ROOT / "examples"

# Flip to True once every shipped object has a schema (post full migration).
STRICT_REQUIRE_SCHEMA = False


def load_json(path: Path):
    with path.open(encoding="utf-8") as fh:
        return json.load(fh)


def load_schemas() -> dict[str, dict]:
    """Map object_type -> schema dict, keyed by filename stem before '.schema'."""
    schemas: dict[str, dict] = {}
    if not SCHEMA_DIR.is_dir():
        return schemas
    for path in sorted(SCHEMA_DIR.glob("*.schema.json")):
        object_type = path.name[: -len(".schema.json")]
        schemas[object_type] = load_json(path)
    return schemas


def main() -> int:
    errors: list[str] = []
    skipped: list[str] = []
    passed = 0

    schemas = load_schemas()

    # 1) Meta-validate each schema.
    for object_type, schema in schemas.items():
        try:
            Draft202012Validator.check_schema(schema)
            print(f"  schema OK    schemas/{object_type}.schema.json")
        except Exception as exc:  # noqa: BLE001 - report any meta-schema failure
            errors.append(f"schemas/{object_type}.schema.json is not a valid JSON Schema: {exc}")

    # 2) Validate each example against its object_type schema.
    if not EXAMPLES_DIR.is_dir():
        print("No examples/ directory found; nothing to validate.")
    for path in sorted(EXAMPLES_DIR.rglob("*.json")):
        rel = path.relative_to(REPO_ROOT)
        try:
            instance = load_json(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{rel}: invalid JSON ({exc})")
            continue

        object_type = instance.get("object_type")
        if not object_type:
            errors.append(f"{rel}: missing 'object_type'")
            continue

        schema = schemas.get(object_type)
        if schema is None:
            msg = f"{rel}: no schema for object_type '{object_type}'"
            if STRICT_REQUIRE_SCHEMA:
                errors.append(msg)
            else:
                skipped.append(msg + " (skipped — schema not yet migrated)")
            continue

        validator = Draft202012Validator(schema)
        problems = sorted(validator.iter_errors(instance), key=lambda e: list(e.path))
        if problems:
            for err in problems:
                loc = "/".join(str(p) for p in err.path) or "(root)"
                errors.append(f"{rel}: {loc}: {err.message}")
        else:
            passed += 1
            print(f"  example OK   {rel}")

    print()
    for line in skipped:
        print(f"  SKIP  {line}")
    print(
        f"\nSummary: {passed} example(s) valid, "
        f"{len(skipped)} skipped, {len(errors)} error(s)."
    )

    if errors:
        print("\nFAILURES:")
        for err in errors:
            print(f"  - {err}")
        return 1
    print("All good.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
