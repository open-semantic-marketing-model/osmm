# Changelog

All notable changes to OSMM™ are recorded here. The format is based on
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/). The **schema** is
versioned via the `osmm_version` field under semantic versioning; see
[GOVERNANCE.md](GOVERNANCE.md#versioning) for what counts as a major, minor, or
patch change, and the deprecation policy that governs breaking changes.

This changelog tracks the standard as a whole (objects, builders, conventions,
governance). The current schema version is **0.1.0**.

## [Unreleased]

### Added
- **`osmm-measurement-framework-builder`** — the sixth object builder and second
  Work Product (Phase 1). Builds a Measurement Framework Object: a tiered KPI set
  (`primary` | `supporting` | `guardrail` governed enum) with per-metric
  definition, target, cadence, and data source, plus an optional
  `north_star_metric` and measurement approach. Introduces the first
  **bidirectional Work Product ↔ Work Product** edge via `linked_marketing_strategy`
  (inverse of the strategy's `linked_measurement_framework`); ratifies the `MEF-`
  prefix.
- **Measurement Framework example instances** — `examples/work-product/MEASUREMENT-FRAMEWORK_ibm-2026.json`
  and `MEASUREMENT-FRAMEWORK_wendys-2026.json` (public-sourced FY2026), paired with
  the Marketing Strategy instances. Resolving the link swapped both Marketing
  Strategy instances' `MEF-PLACEHOLDER-*` for the real framework ids and bumped them
  to v1.1, demonstrating the placeholder-resolution rule. With Marketing Strategy +
  Measurement Framework + Business/Brand Context now present for IBM and Wendy's, the
  Strategy Brief composer (C03) is fully sourced.
- **`osmm-marketing-strategy-builder`** — the fifth object builder and **first
  Work Product** (Phase 1 · Work Product). Builds a Marketing Strategy Object:
  business/marketing objectives, strategy-level `success_criteria`, a
  `positioning_statement` and `differentiation_strategy`, `priority_audiences`,
  and `growth_priorities`, scoped to a `time_horizon`. Introduces the first
  **Work Product → Context** reference edges (`linked_business_context`,
  `linked_brand_context`, `priority_audiences`) plus a
  `linked_measurement_framework` placeholder pending B04. Ratifies the `MKS-`
  prefix and records the edges in `RELATIONSHIPS.md`.
- **Marketing Strategy example instances** — `examples/work-product/MARKETING-STRATEGY_ibm-2026.json`
  and `MARKETING-STRATEGY_wendys-2026.json` (public-sourced, FY2026), the first
  instances in `examples/work-product/`. Both resolve real ids (`BIZ-`, `BRC-`,
  `AUD-`) and are promoted because `osmm-creative-brief-composer` lists
  `marketing_strategy` as an optional input.
- **`design_system_reference` on the Brand Context Object** — an optional pointer
  to a brand's external design system / design language (a design-token source,
  design-language site, or component library), if one exists. OSMM references the
  upstream system rather than modeling it; the full visual identity system stays
  out of scope. The IBM example links IBM Design Language / Carbon
  (`BRAND-CONTEXT_ibm.json` bumped to v1.1).
- **`osmm-audience-builder`** — the fourth object builder (Phase 2 · Context).
  Builds an Audience Object: OSMM's **addressable segment** — membership
  `inclusion_criteria`/`exclusion_criteria`, a governed `segmentation_basis` enum
  (demographic, behavioral, firmographic, value-based, lifecycle, intent,
  lookalike, …), an optional `lifecycle_stage` enum, value characterization, and
  `linked_personas` (realizing the Persona ↔ Audience bidirectional edge).
- **Clarified that "Segment" is the Audience Object**, not a separate object.
  Documented in `TAXONOMY.md` (Phase 2 note) and `RELATIONSHIPS.md`: sub-processes
  2.2/2.3/2.6 resolve to the Audience Object; `segmentation_basis` records the
  segment lens; a Persona *describes* while an Audience *selects*; prioritization
  is the Targeting Strategy Object's job. A distinct Segment object would only be
  warranted later for activation modeling (an edge/delivery concern).
- **Audience example instances** — `examples/context/AUDIENCE_wendys-value-seekers.json`
  (B2C, value-based; linked to the Wendy's persona) and
  `AUDIENCE_ibm-enterprise-it.json` (B2B, firmographic). The Wendy's persona's
  `linked_audiences` placeholder is now resolved to the real id (bumped to v1.1),
  demonstrating referential integrity.
- **`osmm-brand-context-builder`** — the third object builder (Phase 1 · Context).
  Builds a Brand Context Object: brand promise, personality, voice/tone
  principles, messaging pillars, vocabulary, and the must-say/must-not-say
  guardrails and mandatories. Includes an optional 12-archetype `brand_archetype`
  enum and a `linked_business_context` back-reference (realizing the
  Business ↔ Brand Context bidirectional edge). This was the missing *required*
  input of the shipped Creative Brief composer.
- **Brand Context example instances** — `examples/context/BRAND-CONTEXT_wendys.json`
  and `BRAND-CONTEXT_ibm.json` (public-sourced, guardrails inferred). With these,
  the Wendy's Context set (Business + Brand + Persona) covers the composer's
  required inputs, so `osmm-creative-brief-composer` is now runnable end-to-end.
- **`roadmap/` project tracker** — a Kanban backlog (`roadmap/BACKLOG.md`:
  To Do / In Progress / Done across all 34 builders, composer candidates, and
  infrastructure) and a sequenced milestone plan (`roadmap/ROADMAP.md`), plus a
  `roadmap/README.md`. Surfaces the inventory (2 of 34 builders, 1 composer
  shipped) and the critical path (Brand Context builder is the missing required
  input of the shipped Creative Brief composer).
- **`CLAUDE.md`** — project guide and working agreements, including the standing
  rule to update the roadmap tracker in the same commit/PR as any shipped OSMM work.
- **`examples/` instance library** — the first validated, public-sourced object
  instances: `context/BUSINESS-CONTEXT_ibm.json` (enterprise B2B, public
  filings), `context/BUSINESS-CONTEXT_wendys.json` (consumer QSR, public
  information), and `context/PERSONA_wendys-deal-savvy-craver.json`
  (illustrative persona synthesized from public market knowledge), plus an
  `examples/README.md`. The corpus is anchored on two public reference brands
  (IBM, Wendy's) so instances interlink and exercise both `business_type`
  paths of the composer.
- **"Where worked examples live"** rule in `CONVENTION.md` — examples follow the
  same promotion rule as schemas: one or two real worked examples stay inline in
  the builder; an instance is promoted to `examples/` when a second tool needs to
  read it independently.
- **Artifact-composer skill class** — `CONVENTION.md` adds a `-composer` verb
  slot and an "Artifact-composer skills" section: non-normative accelerator
  skills that read several objects and compose a human-readable artifact, keyed
  to the artifact name and living under `skills/artifacts/`. They consume objects
  by `object_type` (enforcing the standard as a pull-through) and select
  variants from object data.
- `osmm-creative-brief-composer` — the first artifact-composer skill. Composes a
  Creative Brief from a three-tier input set: Business/Brand Context + Persona
  are required (enough for a useful first draft), the Phase 5 strategy objects
  are optional and synthesized-and-flagged when absent, and add-on objects (offer,
  campaign, metrics, keyword) are dropped when absent. B2C/B2B variant is driven
  by Business Context `business_type`; missing objects are reported with the
  builder that produces each.
- `RELATIONSHIPS.md` — the object reference model: how ids and reference fields
  work, the category-level reference graph, established reference edges, and a
  proposed id-prefix table for the remaining objects.
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
- Added the examples confidentiality/public-source rule to `CONVENTION.md`
  (examples must be public-sourced; client work never enters the repo) and
  replaced all illustrative ButcherBox references across the docs and skills with
  public-brand examples (Wendy's / IBM), since client content can't be
  published.
- Resolved the `CONVENTION.md` "Creative Brief" open item: Creative Brief is an
  **artifact** (the rendered view of the Creative Strategy + Messaging Framework
  objects), not an OSMM object. No object, `object_type`, or builder is added;
  the model stands at 34 objects. Fixed a stale "Creative Brief object"
  reference in the business-context builder.
- Amended the Creative Brief resolution to add the skill-layer consequence: the
  standard stays objects-only, but OSMM now ships an `osmm-creative-brief-composer`
  artifact-composer skill as a non-normative accelerator.
- README status refreshed to reflect both shipped builders (was "first
  validated builder is `osmm-persona-builder`"), with the versioning policy
  now pointing to `GOVERNANCE.md` and the reference model to `RELATIONSHIPS.md`.
- Builder Output rules aligned with the v0.3 instance-naming convention
  (`<OBJECT-NAME>_<entity-slug>.json`).
- Renamed `brand/logo.md` → `brand/LOGO.md` to match the README references.

### Removed
- `.DS_Store` (macOS artifact) untracked from the repository.
