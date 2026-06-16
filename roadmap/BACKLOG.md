# OSMM™ Backlog (Kanban)

The single source of truth for **what's done, what's in flight, and what's next**.
For the sequencing rationale and milestones, see [`ROADMAP.md`](ROADMAP.md).

**Last updated:** 2026-06-16

**Progress at a glance**

| Track | Done | In Progress | To Do | Total |
|-------|-----:|------------:|------:|------:|
| Object builders | 8 | 0 | 19 | 27 |
| Artifact composers | 1 | 0 | 6 (candidates) | 7 |
| Infrastructure / docs | 10 | 0 | 5 | 15 |

> **Milestone A (Context foundation) is complete** — all six Context objects
> (Business, Brand, Product, Audience, Persona, Keyword) now have builders.
>
> **v0.5 right-sizing (35 → 27 objects).** Five consolidations removed eight
> speculative, unbuilt objects — Targeting Strategy → Marketing Strategy; Offer
> Strategy → Offer; per-dimension Performance objects → Performance Measurement
> (`dimension` facet); Campaign Measurement → Measurement Framework (`scope` facet);
> Offer/Creative Test Strategy → a single **Experiment Strategy**. See
> [TAXONOMY.md](../TAXONOMY.md). Builder ids below were updated accordingly.

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
| B08 | `osmm-keyword-builder` | Phase 2 · Context. Shipped (`status: draft`). OSMM's addressable unit of **search demand** — one term, its intent, banded metrics, SERP features, and the surfaces it's targeted on (SEO/**AEO**/paid). Ratifies the `KW-` prefix; realizes the Keyword → Persona edge (`linked_personas`). **Completes Milestone A — the Context foundation.** |
| B35 | `osmm-product-context-builder` | Phase 1 · Context. Shipped (`status: draft`). The offering layer (features, how it works, benefits, product-level messaging). Distinct from Business Context (the company) and the Offer (the value exchange / CTA). Ratifies the `PRD-` prefix; realizes Product → Business/Brand Context edges. Id assigned by ship order (appended), not registry position. |
| C01 | `osmm-creative-brief-composer` | Phase 5 artifact-composer. ✅ Required input `brand_context` now built (B02); runnable end-to-end on the Wendy's example set. |
| I01 | `TAXONOMY.md` | 7 phases → 27 objects, object resolution index. |
| I02 | `CONVENTION.md` | Naming, frontmatter contract, full builder registry, composer class, schema/example promotion rules. |
| I03 | `RELATIONSHIPS.md` | Reference model, id prefixes, reference graph. |
| I04 | `GOVERNANCE.md` + `CONTRIBUTING.md` | Decision model, tenets, lifecycle; contribution guide. |
| I05 | `examples/` library | Context instances for IBM + Wendy's (`BUSINESS-CONTEXT`, `BRAND-CONTEXT`, `AUDIENCE`, plus Wendy's `PERSONA`) + README. Public-source rule. |
| I06 | README + licenses | Apache-2.0 (code), CC BY 4.0 (docs). |
| I07 | Roadmap & tracker | This folder. |
| I08 | Consumer reference brand swap (Warby Parker → Wendy's) | Merged in PR #7. |
| I14 | Canonical JSON Schemas + CI validation | Standalone `schemas/<object_type>.schema.json` for all 8 shipped objects (strict); `scripts/validate.py` + `validate` workflow; builders now ship their schema (CONVENTION v0.4, CONTRIBUTING/GOVERNANCE definition-of-done). PRs #18–20. |
| I15 | v0.5 registry right-sizing (35 → 27) | Five consolidations of speculative, unbuilt objects; adopted "prefer a facet over a near-duplicate object; collapse on paper, split at build time." |

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

> ✅ **Milestone A is done.** All six Context objects have builders: Business (B01),
> Brand (B02), Product (B35), Audience (B06), Persona (B07), and Keyword (B08) — see
> Done. The Creative Brief composer runs on fully-real inputs, and Keyword (B08) now
> unblocks Keyword Strategy (B09) in Milestone B. **Next up: Milestone B — Keyword
> Strategy (B09).**

### Milestone B — Strategy layer (Phase 1–2 Work Products)
| ID | Builder | Phase |
|----|---------|------:|
| B09 | `osmm-keyword-strategy-builder` | 2 |

> ✅ B03 `osmm-marketing-strategy-builder` and B04 `osmm-measurement-framework-builder`
> shipped — see Done. **Targeting Strategy (former B05) was folded into Marketing
> Strategy** in the v0.5 right-sizing — audience prioritization is `priority_audiences` /
> `growth_priorities` on MKS, not a separate object. Only **Keyword Strategy (B09)**
> remains here, and it should clear the "earns its own object" bar at build time (it's a
> real plan over many Keyword atoms — intent distribution, AEO/SEO targets, topic→journey).

### Milestone C — Offer & Activation (Phase 3–4)
| ID | Builder | Phase |
|----|---------|------:|
| B11 | `osmm-offer-builder` | 3 |
| B36 | `osmm-experiment-strategy-builder` | 3 (cross-phase) |
| B13 | `osmm-campaign-strategy-builder` | 4 |
| B14 | `osmm-journey-strategy-builder` | 4 |

> Offer Strategy (former B10) folded into **Offer** (B11); Offer Test Strategy (B12) and
> Creative Test Strategy (B20) folded into **Experiment Strategy** (B36, cross-phase);
> Campaign Measurement (B15) folded into **Measurement Framework**. Confirm each surviving
> object earns its own object at build time.

### Milestone D — Content & Creative (Phase 5)
| ID | Builder | Phase |
|----|---------|------:|
| B16 | `osmm-messaging-framework-builder` | 5 |
| B17 | `osmm-creative-strategy-builder` | 5 |
| B18 | `osmm-content-strategy-builder` | 5 |
| B19 | `osmm-experience-design-builder` | 5 |

> Provisional: Content Strategy (B18) and Experience Design (B19) may fold into Creative
> Strategy (B17) — decide at build time.

### Milestone E — Build & Deliver (Phase 6)
| ID | Builder | Phase |
|----|---------|------:|
| B21 | `osmm-experience-specification-builder` | 6 |
| B22 | `osmm-experience-component-builder` | 6 |
| B23 | `osmm-journey-configuration-builder` | 6 |
| B24 | `osmm-personalization-configuration-builder` | 6 |
| B25 | `osmm-experience-delivery-builder` | 6 |
| B26 | `osmm-experience-validation-builder` | 6 |
| B27 | `osmm-campaign-deployment-builder` | 6 |

> Provisional: Experience Validation (B26) may become a state/checklist on Experience
> Delivery, and Personalization Configuration (B24) may merge with Journey Configuration
> (B23) — decide at build time. Experience Performance (former B28) folded into Performance
> Measurement (B29, `dimension: experience`).

### Milestone F — Measure, Learn & Optimize (Phase 7)
| ID | Builder | Phase |
|----|---------|------:|
| B29 | `osmm-performance-measurement-builder` | 7 |
| B30 | `osmm-customer-insight-builder` | 7 |
| B34 | `osmm-optimization-recommendation-builder` | 7 |

> Offer/Creative/Journey Performance (former B31–B33) folded into **Performance
> Measurement** (B29) via a `dimension` facet (offer / creative / journey / channel /
> experience).

> Builder ids are **stable labels, not positions** — they are not renumbered when objects
> are added or consolidated. B01–B34 came from the original registry; **B35** =
> `osmm-product-context-builder` (appended); **B36** = `osmm-experiment-strategy-builder`
> (new in the v0.5 right-sizing). Ids retired by consolidation (B05, B10, B12, B15, B20,
> B28, B31, B32, B33) are not reused.

### Composer candidates (non-normative; gated on their inputs)
*Ship each once its input objects exist. These are accelerators, not standard objects — pick the highest-value ones rather than building all.*

| ID | Composer | Reads | Unlocked after |
|----|----------|-------|----------------|
| C02 | `osmm-campaign-brief-composer` | Campaign Strategy + Journey Strategy (+ Audience, Offer) | Milestone C |
| C03 | `osmm-strategy-brief-composer` | Marketing Strategy + Business/Brand Context + Measurement Framework | Milestone B |
| C04 | `osmm-brand-playbook-composer` | Brand Context (+ Business Context) | Milestone A (B02) |
| C05 | `osmm-audience-strategy-composer` | Marketing Strategy (audience priorities) + Audience + Persona | Milestone B |
| C06 | `osmm-journey-map-composer` | Journey Strategy (+ Campaign Strategy, Persona) | Milestone C |
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
