# OSMM™ Roadmap

The sequenced plan for building OSMM out from its current state (17 of 18 object
builders, 1 composer) to a complete, connected model. For live status see
[`BACKLOG.md`](BACKLOG.md).

**Last updated:** 2026-06-19

## Guiding principles

The build order follows three rules, in priority order:

1. **Context before Work Product.** Context objects are high-read and referenced
   by everything downstream; Work Products and composers are nearly useless
   without them. Finish the Context layer first.
2. **Unblock what's already shipped.** The Creative Brief composer already ships
   but lists `brand_context` as a *required* input — so Brand Context is the
   single highest-priority builder.
3. **Walk the phases in order after that.** Phases 1→7 are a dependency chain
   (strategy → audience → offer → campaign → creative → build → measure), so
   building in phase order keeps every new builder's references resolvable.

Each builder is a self-contained PR (one object, per `CONTRIBUTING.md`), shipped
at `status: draft`, ideally with one public-sourced example instance.

## The milestones

```mermaid
flowchart TD
  A["Milestone A ✅<br/>Finish Context foundation<br/>(Brand Context, Audience, Product)"]
  B["Milestone B ✅<br/>Strategy layer · Ph 1-2<br/>(Marketing Strategy,<br/>Measurement Framework)"]
  C["Milestone C ✅<br/>Offer & Activation · Ph 3-4<br/>(Offer, Campaign, Journey)"]
  D["Milestone D ✅<br/>Content & Creative · Ph 5<br/>(Creative, Content)"]
  E["Milestone E ✅<br/>Build & Deliver · Ph 6<br/>(Experience, Experience Component)"]
  F["Milestone F ✅<br/>Measure, Learn & Optimize · Ph 7<br/>(Performance, Insight, Optimization)"]
  A --> B --> C --> D --> E --> F
  A -. "unblocks" .-> C01["Creative Brief composer (shipped)"]
```

### Milestone A — Finish the Context foundation ✅ COMPLETE
**Objects:** ~~Brand Context (B02)~~ ✅, ~~Audience (B06)~~ ✅ (plus ~~Product Context
(B35)~~ ✅, added out of band).
**Why first:** Context is the foundation the whole model references. **All five Context
objects now have builders** (Business, Brand, Product, Audience, Persona) — the Creative
Brief composer runs end-to-end on the Wendy's set and the Persona ↔ Audience edge is
realized. (Keyword was later dissolved into the Journey in v0.8.)
**Exit state (met):** Business, Brand, Product, Audience, Persona all have builders.
**Composer unlocked:** Brand Playbook (C04).

### Milestone B — Strategy layer (Phase 1–2 Work Products) ✅ COMPLETE
**Objects:** ~~Marketing Strategy (B03)~~ ✅, ~~Measurement Framework (B04)~~ ✅.
**Why next:** these are the first Work Products and they reference the Context
layer from Milestone A. **Both shipped** — the MKS ↔ MEF edge is realized, so the
Strategy Brief composer (C03) is fully sourced. *Right-sized: Targeting Strategy folded
into Marketing Strategy (v0.5); Keyword Strategy dissolved into the Journey (v0.8).*
**Composers unlocked:** Strategy Brief (C03), Audience Strategy (C05).

### Milestone C — Offer & Activation (Phase 3–4) ✅ shipped
**Objects:** ~~Offer (B11)~~ ✅, ~~Campaign Strategy (B13)~~ ✅, ~~Journey (B14)~~ ✅.
**Why:** turns strategy into activatable plans. **Offer, Campaign Strategy, and Journey
shipped** — realizing the Phase 3–4 activation edges (Campaign → Marketing/Journey/Audience/
Offer; Offer → Product Context). *Right-sized: Offer Strategy folded into Offer; Campaign
Measurement → Measurement Framework; Journey Strategy + Journey Configuration → the single
Journey Object (v0.6).* Experiment Strategy (B36) is **parked** (deprioritized).
**Composers unlocked:** Campaign Brief (C02), Journey Map (C06).

### Milestone D — Content & Creative (Phase 5) ✅ COMPLETE
**Objects:** ~~Creative Strategy (B17)~~ ✅, ~~Content Strategy (B18)~~ ✅.
**Why:** completes the inputs to the Creative Brief composer's *optional* tier, making
that artifact fully-sourced rather than synthesized-and-flagged. **Both shipped** — creative
direction (Creative Strategy) and the content plan (Content Strategy). *Right-sized: Experience
Design folded into Creative Strategy (v0.7, `experience_concepts`); Messaging Framework dissolved
into the message cascade (v0.8 — Brand → Product `product_messaging` → Journey
`persona_tracks.key_messages`).* **Milestone D complete.**

### Milestone E — Build & Deliver (Phase 6) ✅ COMPLETE
**Objects:** ~~Experience (B37)~~ ✅, ~~Experience Component (B22)~~ ✅.
**Why:** the operational layer — the deliverable experiences and the reusable building blocks.
**Shipped as 2 objects** (v0.9 collapse): the **Experience** object absorbs Experience
Specification, Experience Delivery, Personalization Configuration, and Experience Validation
(spec → built → personalized → validated → deployed are *states* of one decision; the rendered
asset is referenced, not stored); **Experience Component** stays as the reusable building blocks.
*Right-sized: Campaign Deployment → Campaign Strategy `launch_plan`; Journey Configuration →
Journey `delivery_logic` (v0.6); Experience Performance → Performance Measurement (v0.5).*

### Milestone F — Measure, Learn & Optimize (Phase 7) ✅ COMPLETE
**Objects:** ~~Performance Measurement (B29)~~ ✅, ~~Customer Insight (B30)~~ ✅, ~~Optimization
Recommendation (B34)~~ ✅.
**Why last:** the Learning objects close the loop — they reference what they
evaluate and *propose updates back into Context* (sub-process 7.7). They are most
valuable once there's a full pipeline producing things to measure. **All three shipped** —
**Performance Measurement** (Measurement category, prefix `PFM-`) records append-only actuals
against the Measurement Framework, faceted by a `dimension` field; **Customer Insight** (`CIN-`)
is the interpreted *why*, proposing durable Context updates; **Optimization Recommendation**
(`OPR-`) is the prescription, writing forward into Work Products/Strategy and tracked to a
`disposition`. The write-back is lean pointer-plus-prose (applying a change produces a new
*version* of the target). This populates the previously-empty Measurement and Learning
categories. *Right-sized: the per-dimension Offer/Creative/Journey/Experience Performance
objects folded into Performance Measurement via the `dimension` facet.* **Only the parked
Experiment Strategy now remains unbuilt.**
**Composer unlocked:** Optimization Plan (C07).

## Parallel tracks (run alongside the milestones)

- **Examples (I09):** ship one public-sourced instance per builder as it lands.
- **Validators (I10):** schemas already ship standalone at
  `schemas/<object_type>.schema.json` and CI validates examples; add
  `osmm-<object>-validator` skill-layer wrappers as needed, starting with the
  most-referenced objects.
- **Id-prefix ratification (I11)** and **reference-edge tracking (I13):** confirm
  each object's prefix and record its reference fields in `RELATIONSHIPS.md` as
  its builder ships.
- **Vocabulary expansion (I12):** extend governed enums as real inputs demand.

## Sizing snapshot

| Milestone | Builders | Cumulative builders done |
|-----------|---------:|-------------------------:|
| (shipped) | 14 | 14 / 18 |
| A–E ✅ complete | 0 | 14 / 18 |
| F ✅ (Measure, Learn & Optimize) | 3 | 17 / 18 |
| Parked (Experiment Strategy) | 1 | 18 / 18 |

Composers and infrastructure are additive on top of the builder count.

## A note on scope discipline

Per the `lean over over-engineered` tenet ([GOVERNANCE.md](../GOVERNANCE.md)):
composers (C-track) are **non-normative accelerators** — build the few that earn
their keep, not all seven. The 18 builders are the standard; the composers are
convenience.
