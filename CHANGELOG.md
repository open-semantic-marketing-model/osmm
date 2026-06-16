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
- **Phase 3–4 activation layer — three Work Product builders** (`status: draft`),
  taking the model to **11 of 27 builders shipped**:
  - **`osmm-offer-builder`** (B11, Phase 3) — the Offer Object: the time-bound **value
    exchange / call to action** (financial, free trial, demo, discount, bundle, BOGO,
    financing, …) with a governed `offer_type` enum. Folds in the former *Offer Strategy*
    (`behavior_change_objective`, `strategic_rationale`). Ratifies `OFR-`; realizes the
    first **Work Product → Product Context** edge (`linked_product`) plus Offer → Audience /
    Business Context.
  - **`osmm-campaign-strategy-builder`** (B13, Phase 4) — the activation plan:
    `campaign_objective`, `scope`, the `audience_offer_mapping[]` matrix (4.3),
    `channel_strategy[]` (4.4), and personalization (4.6). Ratifies `CMS-`; references
    Marketing Strategy, Journey Strategy, Audiences, Offers, Business Context, and
    campaign-scope Measurement Framework.
  - **`osmm-journey-strategy-builder`** (B14, Phase 4) — the orchestrated customer path:
    `journey_goal`, `stages[]`, `triggers[]`, sequencing/cadence (4.2, 4.5), with a
    governed `journey_type` enum. May serve a campaign or run always-on (optional
    `linked_campaign_strategy`). Ratifies `JNS-`; distinct from Journey Configuration
    (Phase 6 implementation).
  - Each ships its strict canonical schema (`schemas/{offer,campaign_strategy,journey_strategy}.schema.json`)
    per the definition-of-done; `RELATIONSHIPS.md` records the new realized edges and ratifies
    the three prefixes; `GRAPH.md`/SVG regenerated (11 built nodes, 25 realized edges).

### Changed
- **Right-sized the object model from 35 to 27 objects** (v0.5) — five consolidations
  removed eight speculative, *unbuilt* objects, applying "prefer a facet over a
  near-duplicate object; a new object must do work the others can't; collapse on paper
  and split only when building reveals the need":
  - **Targeting Strategy → Marketing Strategy** (audience prioritization is
    `priority_audiences` / `growth_priorities`, not a separate object).
  - **Offer Strategy → Offer** (incentive philosophy / behavior-change objective are
    fields on the Offer).
  - **Offer/Creative/Journey/Experience Performance → Performance Measurement** via a
    `dimension` facet.
  - **Campaign Measurement → Measurement Framework** via a `scope` facet.
  - **Offer Test Strategy + Creative Test Strategy → a single cross-phase Experiment
    Strategy.**
  Reconciled across `TAXONOMY.md` (Phase 2/3/4/5/6/7 re-pointing + resolution index +
  a consolidation note), `CONVENTION.md` (registry → 27, v0.5 changes note),
  `RELATIONSHIPS.md` (proposed-prefix appendix, count), the roadmap tracker, README,
  CLAUDE.md, and the `GOVERNANCE.md` design tenet (added the facet-over-object rule).
  Remaining unbuilt boundaries are provisional, confirmed at build time.

### Added
- **`GRAPH.md` — a whole-model object-graph view.** A rendered graph-database picture
  of all 27 objects (built + backlog) by category, with realized (solid) vs envisioned
  (dashed) reference edges and the learning loop, plus an inline Mermaid version that
  renders on GitHub. Generated from a single source — `scripts/gen_object_graph.py`
  (object + edge tables; `dot` renders the committed `osmm-object-graph.svg`) — so it
  regenerates as builders ship and edges become real. Linked from README and RELATIONSHIPS.
- **Canonical schemas for the remaining 7 shipped objects** — `schemas/` now holds
  all 8: `brand_context`, `product_context`, `persona`, `audience`, `keyword`
  (Context) and `marketing_strategy`, `measurement_framework` (Work Product), each
  a strict JSON Schema (`additionalProperties: false`) derived from its builder's
  inline spec, with id/reference patterns (`PLACEHOLDER` allowed on cross-object
  refs), governed enums (e.g. `persona_type`, `segmentation_basis`, `offering_type`,
  the keyword search/intent vocabularies, the measurement `tier` enum), and nested
  shapes (persona `demographics`, product `product_messaging`/`key_features`,
  measurement `metrics[]`). Each builder's `SKILL.md` now references its canonical
  schema and marks the inline block illustrative. All 11 example instances validate
  against their schemas.
- **Validation is now strict** — `scripts/validate.py` flips `STRICT_REQUIRE_SCHEMA`
  to `True`: every shipped object has a schema, so an example whose `object_type`
  lacks one is a hard error rather than a skip. New builders ship their schema with
  their first example.

### Changed
- **Contributor rules updated for the schema-canonical model** — `CONTRIBUTING.md`
  now makes shipping the canonical `schemas/<object_type>.schema.json` part of a
  builder's definition of done (replacing the stale "schema lives inline" step),
  requires committed instances to validate via `scripts/validate.py`, and notes the
  CI check on `schemas/`/`examples/` changes. `GOVERNANCE.md`'s object lifecycle
  records that every object ships with its schema from `draft` onward.
- **Schemas are now standalone, canonical JSON Schema files** under `schemas/`
  (`schemas/<object_type>.schema.json`), the single source of truth for each
  object's shape — superseding the v0.1–v0.3 "schema inline in `SKILL.md` until a
  second tool needs it" rule. Reflects OSMM's positioning as an interoperability
  standard (the machine-readable schema is the product), and lets a consumer adopt
  the contract without the skills. Builders now ship with their schema; the
  `SKILL.md` references it and keeps only an illustrative excerpt + guidance. Drift
  is avoided by keeping one source of truth rather than two hand-maintained copies.
  Documented in `CONVENTION.md` (v0.4).

### Added
- **First canonical schema + validation harness (Foundation):**
  `schemas/business_context.schema.json` (strict, `additionalProperties: false`) as
  the reference implementation; `scripts/validate.py` and a `validate` GitHub
  Actions workflow that check every `examples/` instance against its object's
  schema and meta-validate each schema. Migration-aware: objects whose schema
  hasn't been written yet are skipped, not failed, so CI stays green while the
  remaining shipped objects are migrated. The two Business Context examples (IBM,
  Wendy's) validate clean.
- **`osmm-keyword-builder`** — the eighth object builder (Phase 2 · Context), **completing
  Milestone A, the Context foundation** (all six Context objects now have builders). Builds a
  Keyword Object: OSMM's addressable unit of search demand — one `term` with its `term_type`
  (keyword | topic | question), `branded` flag, governed `search_intent` (informational |
  navigational | commercial | transactional), `journey_stage`, banded `metrics`
  (volume/difficulty/cpc/trend), `serp_features`, `variations`, and `questions`. Treats **AEO
  (answer-engine optimization) as first-class** alongside SEO and paid via `optimization_channels`
  and the natural-language `questions` field. Ratifies the `KW-` prefix (moved out of the proposed
  appendix); realizes the **Keyword → Persona** edge via `linked_personas` (the Wendy's example
  resolves the real `PER-wendys-deal-savvy-craver`), plus `parent_topic`/`related_keywords` for
  clustering. Worked examples: IBM "hybrid cloud" (B2B topic) and Wendy's "fast food deals near me"
  (B2C transactional/local). Keyword unblocks `osmm-keyword-strategy-builder` (B09) in Milestone B.
- **`osmm-product-context-builder`** — the seventh object builder and the model's
  **35th object** (Phase 1 · Context). Builds a Product Context Object: the durable
  description of a product, service, or solution being marketed — `what_it_does`,
  `how_it_works`, `key_features`, `benefits`, `use_cases`, `differentiators`, and a
  structured `product_messaging` block (primary message, value pillars, proof points,
  objections), with a governed `offering_type` enum (`product` | `service` | `solution`
  | `platform` | `bundle`). Closes the gap between **Business Context** (the company)
  and the **Offer** (the time-bound value exchange / CTA): the offering itself now has
  a home, and an Offer will reference it rather than restate it. Ratifies the `PRD-`
  prefix; realizes Product Context → Business/Brand Context edges (the watsonx example
  resolves real `BIZ-ibm` / `BRC-ibm`); adds `related_offerings` for product-to-product
  links. Worked examples: IBM watsonx (B2B platform) and Wendy's Baconator (B2C product).
- **Model expanded from 34 to 35 objects.** Reconciled across `TAXONOMY.md` (new Phase 1
  sub-process 1.3 *Define Product Context*; Phase 1 renumbered 1.4–1.9; resolution index
  and the 7.7 durable-context loop updated; new Offer-vs-offering and Product-Context
  boundary notes), `CONVENTION.md` (registry + object count), `RELATIONSHIPS.md` (`PRD-`
  prefix, reference-field edges, graph), the roadmap tracker, README, and the design-tenet
  phrasing in `GOVERNANCE.md`/`CONTRIBUTING.md`.
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
