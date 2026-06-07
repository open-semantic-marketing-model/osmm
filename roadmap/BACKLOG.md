# OSMM Backlog (Kanban)

The single source of truth for **what's done, what's in flight, and what's next**.
For the sequencing rationale and milestones, see [`ROADMAP.md`](ROADMAP.md).

**Last updated:** 2026-06-07

**Progress at a glance**

| Track | Done | In Progress | To Do | Total |
|-------|-----:|------------:|------:|------:|
| Object builders | 4 | 0 | 30 | 34 |
| Artifact composers | 1 | 0 | 6 (candidates) | 7 |
| Infrastructure / docs | 8 | 0 | 5 | 13 |

Item ids: `B##` = object builder, `C##` = composer, `I##` = infrastructure/docs.

---

## ✅ Done

| ID | Item | Notes |
|----|------|-------|
| B01 | `osmm-business-context-builder` | Phase 1 · Context. Shipped (`status: draft`). |
| B02 | `osmm-brand-context-builder` | Phase 1 · Context. Shipped (`status: draft`). Unblocks C01's required `brand_context` input. |
| B06 | `osmm-audience-builder` | Phase 2 · Context. Shipped (`status: draft`). OSMM's addressable **segment** (clarified Segment ≈ Audience). Realizes Persona ↔ Audience. |
| B07 | `osmm-persona-builder` | Phase 2 · Context. Shipped (`status: draft`). First built skill. |
| C01 | `osmm-creative-brief-composer` | Phase 5 artifact-composer. ✅ Required input `brand_context` now built (B02); runnable end-to-end on the Wendy's example set. |
| I01 | `TAXONOMY.md` | 7 phases → 34 objects, object resolution index. |
| I02 | `CONVENTION.md` | Naming, frontmatter contract, full builder registry, composer class, schema/example promotion rules. |
| I03 | `RELATIONSHIPS.md` | Reference model, id prefixes, reference graph. |
| I04 | `GOVERNANCE.md` + `CONTRIBUTING.md` | Decision model, tenets, lifecycle; contribution guide. |
| I05 | `examples/` library | Context instances for IBM + Wendy's (`BUSINESS-CONTEXT`, `BRAND-CONTEXT`, `AUDIENCE`, plus Wendy's `PERSONA`) + README. Public-source rule. |
| I06 | README + licenses | Apache-2.0 (code), CC BY 4.0 (docs). |
| I07 | Roadmap & tracker | This folder. |
| I08 | Consumer reference brand swap (Warby Parker → Wendy's) | Merged in PR #7. |

---

## 🚧 In Progress

| ID | Item | Notes |
|----|------|-------|
| — | (nothing in flight) | |

---

## 📋 To Do

Grouped by milestone (see [`ROADMAP.md`](ROADMAP.md)). Within a milestone, order is a suggestion, not a hard gate.

### Milestone A — Finish the Context foundation
*Context objects are referenced by every Work Product and consumed by composers. Completing this layer unblocks everything downstream.*

| ID | Builder | Phase | Why it's prioritized |
|----|---------|------:|----------------------|
| B08 | `osmm-keyword-builder` | 2 | Search/intent Context; feeds Keyword Strategy (B09). **Next up — last item in Milestone A.** |

> ✅ B02 `osmm-brand-context-builder` and B06 `osmm-audience-builder` shipped — see Done. Milestone A is **2 of 3 complete**; only Keyword (B08) remains to finish the Context foundation.

### Milestone B — Strategy layer (Phase 1–2 Work Products)
| ID | Builder | Phase |
|----|---------|------:|
| B03 | `osmm-marketing-strategy-builder` | 1 |
| B04 | `osmm-measurement-framework-builder` | 1 |
| B05 | `osmm-targeting-strategy-builder` | 2 |
| B09 | `osmm-keyword-strategy-builder` | 2 |

### Milestone C — Offer & Activation (Phase 3–4)
| ID | Builder | Phase |
|----|---------|------:|
| B10 | `osmm-offer-strategy-builder` | 3 |
| B11 | `osmm-offer-builder` | 3 |
| B12 | `osmm-offer-test-strategy-builder` | 3 |
| B13 | `osmm-campaign-strategy-builder` | 4 |
| B14 | `osmm-journey-strategy-builder` | 4 |
| B15 | `osmm-campaign-measurement-builder` | 4 |

### Milestone D — Content & Creative (Phase 5)
| ID | Builder | Phase |
|----|---------|------:|
| B16 | `osmm-messaging-framework-builder` | 5 |
| B17 | `osmm-creative-strategy-builder` | 5 |
| B18 | `osmm-content-strategy-builder` | 5 |
| B19 | `osmm-experience-design-builder` | 5 |
| B20 | `osmm-creative-test-strategy-builder` | 5 |

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
| B28 | `osmm-experience-performance-builder` | 6 |

### Milestone F — Measure, Learn & Optimize (Phase 7)
| ID | Builder | Phase |
|----|---------|------:|
| B29 | `osmm-performance-measurement-builder` | 7 |
| B30 | `osmm-customer-insight-builder` | 7 |
| B31 | `osmm-offer-performance-builder` | 7 |
| B32 | `osmm-creative-performance-builder` | 7 |
| B33 | `osmm-journey-performance-builder` | 7 |
| B34 | `osmm-optimization-recommendation-builder` | 7 |

> Builder ids B01–B34 follow the registry order in `CONVENTION.md`; B01 and B07 are Done (above).

### Composer candidates (non-normative; gated on their inputs)
*Ship each once its input objects exist. These are accelerators, not standard objects — pick the highest-value ones rather than building all.*

| ID | Composer | Reads | Unlocked after |
|----|----------|-------|----------------|
| C02 | `osmm-campaign-brief-composer` | Campaign Strategy + Journey Strategy (+ Audience, Offer) | Milestone C |
| C03 | `osmm-strategy-brief-composer` | Marketing Strategy + Business/Brand Context + Measurement Framework | Milestone B |
| C04 | `osmm-brand-playbook-composer` | Brand Context (+ Business Context) | Milestone A (B02) |
| C05 | `osmm-audience-strategy-composer` | Targeting Strategy + Audience + Persona | Milestone B |
| C06 | `osmm-journey-map-composer` | Journey Strategy (+ Campaign Strategy, Persona) | Milestone C |
| C07 | `osmm-optimization-plan-composer` | Optimization Recommendation + Phase 7 performance objects | Milestone F |

### Infrastructure / cross-cutting
| ID | Item | Notes |
|----|------|-------|
| I09 | Example instance per new builder | One public-sourced instance per builder as it ships (IBM and/or Wendy's where natural), per the examples promotion rule. |
| I10 | `osmm-<object>-validator` skills | First validator triggers schema promotion to `schemas/<object_type>.schema.json` (see CONVENTION "Where the schema lives"). Start with the most-consumed objects. |
| I11 | Ratify id prefixes | Confirm the proposed prefixes in `RELATIONSHIPS.md` appendix object-by-object as builders land. |
| I12 | Controlled-vocabulary expansion | Extend governed enums (e.g. `persona_type`, `business_type`) as real inputs demand. |
| I13 | Reference-edge tracking | Keep `RELATIONSHIPS.md` "Established reference fields" table updated as each builder introduces links. |

---

### How to update this board
When work ships, move its row to the correct column, update the **Progress at a
glance** counts, and bump **Last updated**. Add new rows for newly-scoped items.
Keep it in the same commit/PR as the work it describes.
