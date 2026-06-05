# Changelog

All notable changes to OSMM are recorded here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The **schema** is
versioned via the `osmm_version` field under semantic versioning; see
[GOVERNANCE.md](GOVERNANCE.md#versioning) for what counts as a major, minor, or
patch change, and the deprecation policy that governs breaking changes.

This changelog tracks the standard as a whole (objects, builders, conventions,
governance). The current schema version is **0.1.0**.

## [Unreleased]

### Added
- `GOVERNANCE.md` — maintainer-led decision model, design tenets, object
  lifecycle, semantic-versioning and deprecation policy.
- `CONTRIBUTING.md` — how to propose objects, author builder skills, and
  contribute example instances.
- `LICENSE-docs` — CC BY 4.0 license text for documentation, as referenced by
  the README.
- `.gitignore` — ignores OS/editor cruft and unvalidated root-level instance
  JSON.
- `osmm-business-context-builder` and `osmm-persona-builder` — the first two
  builder skills, under `skills/context/`.

### Changed
- Builder Output rules aligned with the v0.3 instance-naming convention
  (`<OBJECT-NAME>_<entity-slug>.json`).
- Renamed `brand/logo.md` → `brand/LOGO.md` to match the README references.

### Removed
- `.DS_Store` (macOS artifact) untracked from the repository.
