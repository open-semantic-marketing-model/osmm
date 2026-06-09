# OSMM™ Governance

**Open Semantic Marketing Model — how the standard is governed**
Status: Draft v0.1

This document describes how decisions get made in OSMM: who maintains the
standard, how objects move from idea to stable, how the schema is versioned,
and how breaking changes are handled. It makes concrete the model the
[README](README.md) summarizes — *maintainer-led, not consensus-driven*.

---

## Governing principle

Open standards fragment when consensus becomes the goal. OSMM is therefore
**maintainer-led**: the community proposes, a small maintainer core decides.
The aim is a coherent, opinionated model that stays internally consistent as it
grows — not a superset of every contributor's preferences.

This is a deliberate trade. Contributors get a low barrier to *propose* and a
high bar to *merge*. Maintainers carry the obligation to keep the model lean
(see "Design tenets") and to say no clearly and with reasons.

## Roles

| Role | Who | Can |
|------|-----|-----|
| **Maintainer** | A small core of practicing marketing operators | Approve and merge changes; assign object lifecycle states; cut releases; own the controlled vocabularies and the object registry. |
| **Contributor** | Anyone | Open issues, propose objects, submit pull requests, comment on proposals. |

Maintainers are listed in `MAINTAINERS.md` (to be added as the core is named).
Until then, the repository owner acts as sole maintainer.

## Design tenets

Every governance decision is measured against these. They are the tie-breakers
when a proposal is reasonable but the answer is still "no, not like this."

1. **Lean over over-engineered.** Minimal cores with optional extensions. A new
   field must earn its place; a new object must do work the existing 35 cannot.
2. **Grounded in real assets.** Objects and examples are validated against real
   marketing artifacts, not invented to round out a model.
3. **Identity is stable; everything else can be re-debated.** An object's
   identity (and therefore its `object_type` and builder slug) does not change
   once assigned. Phase, category, and wave can be revisited.
4. **Distillation, not lossless compression.** The canonical JSON is the
   interoperability contract; richer source assets are referenced, not replaced.
5. **Machine-facetable over free text.** Governed enums (controlled
   vocabularies) are preferred to open strings wherever a field will be queried
   or segmented.

## The object lifecycle

Every object — and the builder skill that constructs it — carries a lifecycle
state in its `SKILL.md` frontmatter (`status`). Maintainers assign and advance
it.

| State | Meaning | Stability promise |
|-------|---------|-------------------|
| **draft** | Under exploration; schema unstable. | None. May change or be removed without notice. |
| **proposed** | Open for community review. | Shape is stabilizing; feedback actively sought. |
| **stable** | Safe to implement against. | Changes follow semantic versioning and the deprecation policy below. |
| **deprecated** | Scheduled for retirement. | Honored through a formal deprecation period; never silently broken. |

Promotion is a maintainer decision, not an automatic graduation. The typical
path is `draft → proposed → stable`, with `proposed` requiring at least one
validated instance built from a real asset.

## Versioning

OSMM versions the **schema** (the `osmm_version` field carried in every object
and every builder's frontmatter) under **semantic versioning**:

- **PATCH** (`0.1.0 → 0.1.1`) — clarifications and additive, non-breaking fixes
  that don't change the meaning of existing fields.
- **MINOR** (`0.1.0 → 0.2.0`) — backward-compatible additions: new optional
  fields, new objects, new controlled-vocabulary values.
- **MAJOR** (`0.x → 1.0`, `1.x → 2.0`) — backward-incompatible changes: removing
  or renaming a field, making an optional field required, changing a field's
  type or semantics, or removing a vocabulary value.

While the standard is pre-1.0, minor versions may carry larger changes than they
will post-1.0, but the deprecation policy still applies to anything marked
`stable`.

Note: documents in this repo (`CONVENTION.md`, `TAXONOMY.md`, this file) carry
their own draft version in their header, independent of the schema
`osmm_version`. The schema version is the one external implementers depend on.

## Deprecation policy

Anything marked `stable` is **never silently broken.** A breaking change to a
stable object or field proceeds only through this path:

1. The field/object is marked `deprecated` in the schema and its builder
   `SKILL.md`, with the replacement (if any) named and the target removal
   version stated.
2. The deprecation is recorded in `CHANGELOG.md`.
3. The element is retained, functional, for at least one **minor** release after
   it is marked deprecated.
4. Removal happens only in a subsequent **major** release.

A `-migrator` skill (see `CONVENTION.md` → "Future verb slots") may be provided
to upgrade existing instances across a breaking change.

## Controlled vocabularies

Governed enums (e.g. Persona `persona_type`, Business Context `business_type`)
are part of the standard, not per-project free text. New values are added
**deliberately by maintainers** — never invented in a single contribution and
left to fragment. Proposing a new vocabulary value follows the same PR flow as
any other change (see [CONTRIBUTING.md](CONTRIBUTING.md)) and is evaluated
against tenet 5. Stored values are snake_case tokens mapped to human-readable
labels in the owning skill.

## How decisions are made

1. A proposal arrives as an issue or pull request (see
   [CONTRIBUTING.md](CONTRIBUTING.md)).
2. Maintainers review against the design tenets and the existing object model.
3. Discussion happens in the open, on the issue or PR.
4. A maintainer makes the call. Approval requires maintainer sign-off; for
   changes to `stable` objects or to the object registry, two maintainers where
   a core of that size exists.
5. The decision and its rationale are recorded on the issue/PR. A "no" comes
   with reasons tied to the tenets, so the boundary stays legible.

## Changing this document

Governance changes are themselves maintainer decisions and follow the same flow.
Material changes are noted in `CHANGELOG.md`.
