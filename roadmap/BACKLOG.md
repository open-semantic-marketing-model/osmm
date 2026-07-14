# OSMM™ Backlog (Kanban)

The single source of truth for **what's done, what's in flight, and what's next**.
For the sequencing rationale and milestones, see [`ROADMAP.md`](ROADMAP.md).

**Last updated:** 2026-07-14 (docs: split plugin install instructions by product — Claude Cowork app UI vs. Claude Code CLI — in README, GETTING-STARTED, and PLUGIN)

**Prior:** 2026-06-19 (v0.10: Phase 7 Measure-Learn-Optimize layer built — Performance Measurement, Customer Insight, Optimization Recommendation → Milestone F complete)

**Progress at a glance**

| Track | Done | In Progress | To Do | Total |
|-------|-----:|------------:|------:|------:|
| Object builders | 17 | 0 | 1 (parked) | 18 |
| Artifact composers | 1 | 0 | 6 (candidates) | 7 |
| Infrastructure / docs | 11 | 0 | 5 | 16 |

> **Milestones A–F complete** — Context foundation, Strategy layer, Offer & Activation,
> Content & Creative, Build & Deliver, and Measure-Learn-Optimize all have builders.
> **17 of 18 object builders ship**; only the parked **Experiment Strategy (B36)** remains.
> The Phase 7 layer closes the learning loop: Performance Measurement records actuals against
> the framework (faceted by `dimension`), Customer Insight is the interpreted *why*, and
> Optimization Recommendation is the prescription that writes back into Context/Strategy (7.7).
>
> **Right-sizing → 18 objects.** v0.5–v0.7 (see below); **v0.8** dissolved **Keyword (B08),
> Keyword Strategy (B09), and Messaging Framework (B16) into the Journey**; **v0.9** collapsed
> **Phase 6's Experience-\* family (Experience Specification B21, Personalization Configuration
> B24, Experience Delivery B25, Experience Validation B26) into a single Experience object**,
> with **Campaign Deployment (B27) → Campaign Strategy `launch_plan`**. Only **Experience
> Component** stays separate. The **Configuration** category is now empty. See [TAXONOMY.md](../TAXONOMY.md).
>
> **Deprioritized (parked):** Experiment Strategy (B36) — a sequencing decision.

Item ids: `B##` = object builder, `C##` = composer, `I##` = infrastructure/docs.

---

## ✅ Done

| ID | Item | Notes |
|----|------|-------|
| B01 | `osmm-business-context-builder` | Phase 1 · Context. Shipped (`status: draft`). |
| B02 | `osmm-brand-context-builder` | Phase 1 · Context. Shipped (`status: draft`). Unblocks C01's required `brand_context` input. |
| B03 | `osmm-marketing-strategy-builder` | Phase 1 · Work Product. Shipped (`status: draft`). **First Work Product object** — realizes the first Work Product → Context edges (Business/Brand Context, priority Audiences). |
| B04 | `osmm-measurement-framework-builder` | Phase 1 · Work Product. Shipped (`status: draft`). Tiered KPI framework (`primary`/`supporting`/`guardrail`) measuring a Marketing Strategy. Realizes the first bidirectional Work Product ↔ Work Product edge (MKS ↔ MEF); resolved the MKS `MEF-PLACEHOLDER` refs (MKS instances → v1.1). |
| B06 | `osmm-audience-builder` | Phase 2 · Context. Shipped (`status: draft`). OSMM's addressable **segment** (clarified Segment ≈ Audience). Realizes Persona ↔ Audience. |
| B07 | `osmm-persona-builder` | Phase 2 · Context. Shipped (`status: draft`). First built skill. |
| B35 | `osmm-product-context-builder` | Phase 1 · Context. Shipped (`status: draft`). The offering layer (features, how it works, benefits, product-level messaging). Distinct from Business Context (the company) and the Offer (the value exchange / CTA). Ratifies the `PRD-` prefix; realizes Product → Business/Brand Context edges. Id assigned by ship order (appended), not registry position. |
| B11 | `osmm-offer-builder` | Phase 3 · Work Product. Shipped (`status: draft`). The value exchange / CTA — the time-bound incentive to act (financial, free trial, demo, discount, bundle, BOGO, financing, etc.). Folds in the former **Offer Strategy** (`behavior_change_objective`, `strategic_rationale`). Ratifies the `OFR-` prefix; realizes Offer → Product Context (`linked_product`), Offer → Audience (`linked_audiences`), and Offer → Business Context edges. First Phase 3 / Milestone C object. |
| B13 | `osmm-campaign-strategy-builder` | Phase 4 · Work Product. Shipped (`status: draft`). The activation plan — objective/scope, the `audience_offer_mapping` matrix (4.3), `channel_strategy` (4.4), and personalization (4.6). Ratifies the `CMS-` prefix; references Marketing Strategy, Journey, Audiences, Offers, Business Context, and (campaign-scope) Measurement Framework. |
| B14 | `osmm-journey-builder` | Phase 4 · Work Product. Shipped (`status: draft`). The **Journey Object** — orchestrated customer path, strategy through delivery: `journey_goal`, `stages[]`, `triggers[]`, sequencing/cadence (4.2, 4.5) plus optional `delivery_logic` (6.3). **Merges the former Journey Strategy + Journey Configuration** (v0.6). Ratifies the `JNY-` prefix; may serve a campaign or run always-on. |
| B17 | `osmm-creative-strategy-builder` | Phase 5 · Work Product. Shipped (`status: draft`). The creative direction — `creative_platform` (big idea), `creative_themes[]`, `channel_creative[]` (5.6), and `experience_concepts[]`. **Absorbs the former Experience Design** (5.5). Ratifies the `CRS-` prefix; references Brand Context, Product Context. |
| B18 | `osmm-content-strategy-builder` | Phase 5 · Work Product. Shipped (`status: draft`). The content plan — `content_goal`, `content_pillars[]` (with formats), sequencing, and `journey_mapping[]` (5.3). Ratifies the `CTS-` prefix; references Creative Strategy, Journey, Personas. **Completes Milestone D.** |
| B22 | `osmm-experience-component-builder` | Phase 6 · Work Product. Shipped (`status: draft`). The reusable building blocks (headline, hero, CTA, copy block, offer card, trust block, wireframe, …) that Experiences are assembled from. Ratifies the `EXC-` prefix; references Brand Context, Product Context, Personas. |
| B37 | `osmm-experience-builder` | Phase 6 · Work Product. Shipped (`status: draft`). The **Experience Object** — a deliverable's *definition* (email, landing page, ad, hero): `specification`, assembled `linked_components`, `variants`, `personalization_rules`, `validation` status, `deployment`. **Collapses Experience Specification (B21), Experience Delivery (B25), Personalization Configuration (B24), Experience Validation (B26)** (v0.9); the rendered asset is referenced via `delivery_reference`. Ratifies the `EXP-` prefix. **Completes Milestone E.** |
| B29 | `osmm-performance-measurement-builder` | Phase 7 · Measurement. Shipped (`status: draft`). Append-only **actuals** against a Measurement Framework — `period`, per-metric `actual`/`target`/`variance`/`status`, faceted by a `dimension` field (overall / offer / creative / journey / channel / experience / campaign) that serves 7.1/7.3/7.4/7.5 and **absorbs the former per-dimension Performance objects (B31–B33, B28)**. Ratifies the `PFM-` prefix; references the Measurement Framework (and optionally the subject measured, Marketing Strategy, Business Context). First **Measurement-category** object. |
| B30 | `osmm-customer-insight-builder` | Phase 7 · Learning. Shipped (`status: draft`). The interpreted **why** (7.2) — `insight_statement`, `confidence`, `evidence` (Performance Measurements + external research), affected personas/audiences, and `proposes_updates_to[]` writing durable changes back into Context (7.7). Ratifies the `CIN-` prefix. First **Learning-category** object. |
| B34 | `osmm-optimization-recommendation-builder` | Phase 7 · Learning. Shipped (`status: draft`). The **prescription** (7.6) — `recommendation`, `rationale`, `derived_from` (insights + measurements), `priority`/`effort`/`expected_impact`, a `disposition` (proposed → accepted/rejected/implemented) distinct from lifecycle `status`, and `targets[]` writing forward into Work Products/Strategy. Lean pointer-plus-prose write-back. Ratifies the `OPR-` prefix. **Completes Milestone F.** Unlocks the Optimization Plan composer (C07). |
| C01 | `osmm-creative-brief-composer` | Phase 5 artifact-composer. ✅ Required input `brand_context` now built (B02); runnable end-to-end on the Wendy's example set. |
| I01 | `TAXONOMY.md` | 7 phases → 18 objects, object resolution index. |
| I02 | `CONVENTION.md` | Naming, frontmatter contract, full builder registry, composer class, schema/example promotion rules. |
| I03 | `RELATIONSHIPS.md` | Reference model, id prefixes, reference graph. |
| I04 | `GOVERNANCE.md` + `CONTRIBUTING.md` | Decision model, tenets, lifecycle; contribution guide. |
| I05 | `examples/` library | Context instances for IBM + Wendy's (`BUSINESS-CONTEXT`, `BRAND-CONTEXT`, `AUDIENCE`, plus Wendy's `PERSONA`) + README. Public-source rule. |
| I06 | README + licenses | Apache-2.0 (code), CC BY 4.0 (docs). |
| I07 | Roadmap & tracker | This folder. |
| I08 | Consumer reference brand swap (Warby Parker → Wendy's) | Merged in PR #7. |
| I14 | Canonical JSON Schemas + CI validation | Standalone `schemas/<object_type>.schema.json` for all 8 shipped objects (strict); `scripts/validate.py` + `validate` workflow; builders now ship their schema (CONVENTION v0.4, CONTRIBUTING/GOVERNANCE definition-of-done). PRs #18–20. |
| I15 | v0.5 registry right-sizing (35 → 27) | Five consolidations of speculative, unbuilt objects; adopted "prefer a facet over a near-duplicate object; collapse on paper, split at build time." |
| I16 | Object-graph view (`GRAPH.md`) | Whole-model graph of all 18 objects (built + backlog), ordered left→right by workflow phase, realized vs envisioned edges + learning loop, with an inline Mermaid version; generated by `scripts/gen_object_graph.py` (committed `osmm-object-graph.svg`). |

---

## 🚧 In Progress

| ID | Item | Notes |
|----|------|-------|
| — | (nothing in flight) | |

---

## 📋 To Do

Grouped by milestone (see [`ROADMAP.md`](ROADMAP.md)). Within a milestone, order is a suggestion, not a hard gate.

### Milestone A — Finish the Context foundation ✅ COMPLETE
*Context objects are referenced by every Work Product and consumed by composers. Completing this layer unblocks everything downstream.*

> ✅ **Milestone A is done.** All five Context objects have builders: Business (B01),
> Brand (B02), Product (B35), Audience (B06), Persona (B07) — see Done. The Creative Brief
> composer runs on fully-real inputs. **Next up: Milestone E — Build & Deliver (Phase 6).**

### Parked / deprioritized
*Sequencing decision — not removed from the model, just not being built now.*

| ID | Builder | Phase | Note |
|----|---------|------:|------|
| B36 | `osmm-experiment-strategy-builder` | 3 (cross-phase) | Experiment/testing work deprioritized. |

### Milestone D — Content & Creative (Phase 5) ✅ COMPLETE

> ✅ **Milestone D shipped** — B17 Creative Strategy, B18 Content Strategy (see Done).
> **Experience Design (former B19) folded into Creative Strategy** (v0.7); **Messaging
> Framework (former B16) dissolved into the message cascade** (v0.8 — Brand Context →
> Product Context `product_messaging` → the Journey's `persona_tracks.key_messages`),
> rendered as an artifact, not authored as an object. **Next up: Milestone E — Build &
> Deliver (Phase 6).**

### Milestone E — Build & Deliver (Phase 6) ✅ COMPLETE

> ✅ **Milestone E shipped as 2 objects** — **Experience (B37)** and **Experience Component
> (B22)** (see Done). v0.9 collapsed the Phase 6 Experience-\* family: Experience Specification
> (B21), Experience Delivery (B25), Personalization Configuration (B24), and Experience
> Validation (B26) became one **Experience** object (the rendered asset lives in the production
> tool, referenced); **Campaign Deployment (B27) → Campaign Strategy `launch_plan`**; Journey
> Configuration (B23) was already merged into the Journey (v0.6); Experience Performance (B28)
> into Performance Measurement (v0.5). **Next up: Milestone F — Measure, Learn & Optimize.**

### Milestone F — Measure, Learn & Optimize (Phase 7) ✅ COMPLETE

> ✅ **Milestone F shipped** — **Performance Measurement (B29)**, **Customer Insight (B30)**,
> and **Optimization Recommendation (B34)** (see Done). This populates the previously-empty
> **Measurement** and **Learning** categories and closes the learning loop (7.7). Offer/Creative/
> Journey Performance (former B31–B33) and Experience Performance (B28) are folded into
> **Performance Measurement** via a `dimension` facet (overall / offer / creative / journey /
> channel / experience / campaign). **All milestones (A–F) are now complete** — only the parked
> Experiment Strategy (B36) remains unbuilt. **Next: the Optimization Plan composer (C07) is now
> unblocked, and a Measurement Framework example pair could be promoted to `examples/`.**

> Builder ids are **stable labels, not positions** — they are not renumbered when objects
> are added or consolidated. B01–B34 came from the original registry; **B35** =
> `osmm-product-context-builder`; **B36** = `osmm-experiment-strategy-builder` (v0.5);
> **B37** = `osmm-experience-builder` (the v0.9 Phase 6 collapse). Ids retired by consolidation
> (B05, B08, B09, B10, B12, B15, B16, B19, B20, B21, B23, B24, B25, B26, B27, B28, B31, B32, B33)
> are not reused — **B23** (Journey Configuration) in v0.6; **B19** (Experience Design) in v0.7;
> **B08/B09/B16** (Keyword, Keyword Strategy, Messaging Framework) in v0.8; and **B21, B24, B25,
> B26** (Experience Specification, Personalization Configuration, Experience Delivery, Experience
> Validation) into the Experience object plus **B27** (Campaign Deployment) into Campaign
> Strategy in v0.9.

### Composer candidates (non-normative; gated on their inputs)
*Ship each once its input objects exist. These are accelerators, not standard objects — pick the highest-value ones rather than building all.*

| ID | Composer | Reads | Unlocked after |
|----|----------|-------|----------------|
| C02 | `osmm-campaign-brief-composer` | Campaign Strategy + Journey (+ Audience, Offer) | Milestone C |
| C03 | `osmm-strategy-brief-composer` | Marketing Strategy + Business/Brand Context + Measurement Framework | Milestone B |
| C04 | `osmm-brand-playbook-composer` | Brand Context (+ Business Context) | Milestone A (B02) |
| C05 | `osmm-audience-strategy-composer` | Marketing Strategy (audience priorities) + Audience + Persona | Milestone B |
| C06 | `osmm-journey-map-composer` | Journey (+ Campaign Strategy, Persona) | Milestone C |
| C07 | `osmm-optimization-plan-composer` | Optimization Recommendation + Phase 7 performance objects | Milestone F |

### Infrastructure / cross-cutting
| ID | Item | Notes |
|----|------|-------|
| I09 | Example instance per new builder | One public-sourced instance per builder as it ships (IBM and/or Wendy's where natural), per the examples promotion rule. |
| I10 | `osmm-<object>-validator` skills | Per-object validator skills that check an instance against its canonical `schemas/<object_type>.schema.json`. (Schemas already ship standalone — I14 — and `scripts/validate.py` covers examples in CI; these are the skill-layer wrappers.) |
| I11 | Ratify id prefixes | Confirm the proposed prefixes in `RELATIONSHIPS.md` appendix object-by-object as builders land. |
| I12 | Controlled-vocabulary expansion | Extend governed enums (e.g. `persona_type`, `business_type`) as real inputs demand. |
| I13 | Reference-edge tracking | Keep `RELATIONSHIPS.md` "Established reference fields" table updated as each builder introduces links. |

---

### How to update this board
When work ships, move its row to the correct column, update the **Progress at a
glance** counts, and bump **Last updated**. Add new rows for newly-scoped items.
Keep it in the same commit/PR as the work it describes.
