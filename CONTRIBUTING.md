# Contributing to OSMM™

Thanks for your interest in the Open Semantic Marketing Model. OSMM is
**maintainer-led** (see [GOVERNANCE.md](GOVERNANCE.md)): anyone can propose,
and a small maintainer core decides. This guide explains how to propose well so
your contribution has the best chance of landing.

Before you start, skim:

- [README.md](README.md) — what OSMM is and the object model at a glance.
- [CONVENTION.md](CONVENTION.md) — the builder-skill naming convention, the
  `SKILL.md` frontmatter contract, slug rules, and instance file naming.
- [TAXONOMY.md](TAXONOMY.md) — the seven workflow phases and the object each
  sub-process resolves to.
- [GOVERNANCE.md](GOVERNANCE.md) — design tenets, the object lifecycle, and how
  decisions get made.

## What you can contribute

| Contribution | Start with |
|--------------|-----------|
| A fix or clarification to docs | A pull request. |
| A **builder skill** for an object already in the registry | An issue (optional) → a pull request. |
| A **new object** not in the registry | An issue first — propose before you build. |
| A new **controlled-vocabulary value** (e.g. a new `persona_type`) | An issue, or a PR that edits the owning skill. |
| A **validated example instance** | A pull request adding it under `examples/`. |

When in doubt, **open an issue first.** It's cheaper to align on whether
something belongs in the model than to write a full builder and have it
declined on scope.

## The design tenets (read these first)

Every contribution is measured against the tenets in
[GOVERNANCE.md](GOVERNANCE.md#design-tenets). The two that decline the most
proposals:

- **Lean over over-engineered.** A new field must earn its place; a new object
  must do work the existing 26 cannot. "It would be nice to also capture X" is
  usually a no unless X changes a decision downstream.
- **Grounded in real assets.** Objects and examples are validated against real
  marketing artifacts, not invented to round out the model.

## Proposing a new object

1. **Open an issue** titled `Object proposal: <Name>`. Include:
   - The decision or artifact it represents (which phase / sub-process in
     [TAXONOMY.md](TAXONOMY.md) does it serve?).
   - Why the existing objects can't carry it.
   - A draft of its core fields and which existing objects it references.
   - A pointer to a real asset it would be built from.
2. A maintainer responds with a direction before you invest in a builder. If
   accepted, the object enters at `status: draft`.

## Contributing a builder skill

Builders follow the convention exactly — read
[CONVENTION.md](CONVENTION.md) in full first. The essentials:

1. **Name and location.** The skill is `osmm-<object-slug>-builder`, the folder
   name equals the frontmatter `name`, and it lives under
   `skills/<category>/` — one of `context`, `work-product`, `configuration`,
   `measurement`, `learning`.
2. **Slug rules.** Lowercase, hyphens only; drop the trailing "Object"; keep
   every other word. The skill slug uses hyphens (`osmm-business-context-builder`)
   while the JSON field uses underscores (`"object_type": "business_context"`).
3. **Frontmatter.** Provide every key in the
   [frontmatter schema](CONVENTION.md#frontmatter-schema): `name`,
   `description` (trigger-rich — this is what makes the skill discoverable),
   `object`, `object_type`, `category`, `phase`, `wave`, `osmm_version`,
   `status`.
4. **Ship the canonical schema.** Each object's contract is a standalone JSON
   Schema at `schemas/<object_type>.schema.json` — the single source of truth for
   its shape, and **strict** (`additionalProperties: false`). A builder is not
   complete without it: your PR adds the schema file, and the `SKILL.md`
   *references* it (keeping only an illustrative excerpt plus the human guidance —
   extraction principles, vocabularies, ID rules). If the inline excerpt ever
   disagrees with the schema, the schema wins. See
   [CONVENTION.md → "Where the schema lives"](CONVENTION.md).
5. **Instance output.** The builder must save instances using the
   [instance file naming](CONVENTION.md#instance-file-naming) pattern
   (`<OBJECT-NAME>_<entity-slug>.json`, e.g. `PERSONA_wendys-deal-savvy-craver.json`),
   and the in-object id (`PER-…`, `BIZ-…`) stays the id, not the filename.
6. **Validate against a real asset.** A builder reaching `proposed` needs at
   least one instance built from a real source — ideally contributed alongside
   it under `examples/` (see below). Any committed instance **must validate
   against its object's schema**: run `python scripts/validate.py` (CI runs it on
   every PR; it is a hard error if an example's `object_type` has no schema).

Use the two shipped Context builders
(`skills/context/osmm-business-context-builder`,
`skills/context/osmm-persona-builder`) as references.

## Contributing an example instance

Validated examples live under `examples/<category>/`, mirroring `skills/`, and
follow the same instance file naming as builder output. Unvalidated instances
produced during client or internal work stay **outside** the repo until
reviewed — the `.gitignore` is configured to keep stray root-level `.json` out
by accident. Submit an example as a PR; include a one-line note on the source it
was built from.

## Pull request flow

1. Branch from `main`.
2. Make your change. Keep PRs focused — one object, one fix, or one example per
   PR where practical. If you touch `schemas/` or `examples/`, run
   `python scripts/validate.py` before pushing (CI runs it too).
3. Open the PR with a clear description: what it changes and why, and which
   tenet(s) it serves. Link any related issue.
4. A maintainer reviews against the tenets and the object model
   ([GOVERNANCE.md](GOVERNANCE.md#how-decisions-are-made)). Expect questions;
   a decline comes with reasons.
5. On approval, a maintainer merges.

## Lifecycle and stability

New objects and builders enter at `draft` and are advanced to `proposed` and
`stable` by maintainers — see the
[object lifecycle](GOVERNANCE.md#the-object-lifecycle). Don't set your own
contribution to `stable`; that's a maintainer call.

## Licensing of contributions

By contributing you agree that your contributions are licensed under the
repository's licenses: **Apache 2.0** for schemas and code
([LICENSE](LICENSE)), **CC BY 4.0** for documentation
([LICENSE-docs](LICENSE-docs)).
