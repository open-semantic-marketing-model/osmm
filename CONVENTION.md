# OSMM™ Skill Naming Convention

**Open Semantic Marketing Model — builder skills**
Status: Draft v0.11

This document defines how skills that build OSMM objects are named, organized, and described. Every object in the model gets exactly one builder skill, and the name of that skill is keyed to the one thing about the object that never changes: its identity. Phase, category, and release wave can all be re-debated over the life of the standard. The object's identity cannot, so it — and only it — drives the name.

---

## The pattern

```
osmm-<object-slug>-builder
```

Three parts, each with one job:

- **`osmm-`** — namespace prefix. Clusters every standard-related skill and reads as "this builds an OSMM-conformant object."
- **`<object-slug>`** — the object's stable identity. Lowercase, hyphen-delimited, derived from the canonical object name with the trailing word "Object" dropped.
- **`-builder`** — the verb slot. Signals that the skill constructs and emits a valid instance of the object. Kept as a suffix so skills sort by object, and reserved for sibling verbs later (`-validator`, `-reader`, `-migrator`).

The verb is uniform across all categories. A Learning or Measurement object is *derived* rather than authored, but `-builder` still reads correctly as "constructs a valid instance," and uniformity is worth more than semantic precision here. If a category-specific distinction is ever needed, it goes in the verb slot (e.g. `-synthesizer`), not in a new naming scheme.

---

## Slug rules

1. Lowercase, hyphens only. No spaces, no underscores in the skill/folder name.
2. Drop the trailing "Object" from the canonical object name.
3. Keep every other word. Full slugs are what disambiguate the multiple `…strategy` and `…measurement` objects from each other.
4. The frontmatter `name` and the folder name are identical — both equal the slug.
5. **Slug uses hyphens; `object_type` uses underscores.** The skill slug (`osmm-business-context-builder`) and the JSON schema field (`"object_type": "business_context"`) are deliberately different notations so a skill name is never confused with an object type.

---

## Where the schema lives

Every object's canonical schema is a standalone **JSON Schema** file at
`schemas/<object_type>.schema.json` (e.g. `schemas/business_context.schema.json`).
**That file is the single source of truth for the object's shape** — types,
required fields, governed enums, id patterns, and cardinality. Schemas are strict
(`additionalProperties: false`) so typos and stray fields fail loudly.

A builder **ships with its schema file** — authoring the schema is part of the
definition of done for an object, not a later promotion. The `SKILL.md` does
**not** carry a parallel field spec; it *references* the schema file and keeps
only a short, explicitly *illustrative* excerpt plus one or two worked examples to
teach the shape at the point of use, alongside the human guidance (extraction
principles, vocabularies, ID rules) that a schema can't capture. The excerpt is
teaching material, not a second source of truth — **if it ever disagrees with the
schema, the schema wins.**

Every instance in `examples/` **must validate** against its object's schema; this
is enforced by `scripts/validate.py` in CI (see the `validate` workflow). That is
the reconciliation guarantee: examples cannot drift from schemas without CI going
red.

This rule applies to an object **when its builder ships**. Objects without a
builder yet do not get a schema — we don't formalize contracts that don't exist.
During the migration of already-shipped builders, an object whose schema hasn't
landed yet is *skipped* by the validator rather than failing it.

> **Why standalone, not inline?** OSMM is an interoperability *standard*, and for a
> standard the machine-readable schema is the product, not a supporting artifact —
> implementers, validators, and IDEs expect `schemas/<name>.schema.json`, and a
> consumer can adopt the contract without adopting the skills. Drift is avoided by
> keeping a *single* source of truth (the schema file) rather than hand-maintaining
> two. This supersedes the v0.1–v0.3 "inline until a second tool needs it" rule.

---

## Where worked examples live

Examples follow the **same promotion rule as schemas**, because they answer the
same question — "is a second tool reading this?" — and the answer should drive
where the artifact lives.

- **Inline in the `SKILL.md`** — every builder keeps **one or two real worked
  examples** in its body. They travel with the builder (loaded into context when
  the skill runs) and are human-readable, so they teach the output shape at the
  point of use. This is the default home for an example.
- **Promoted to `examples/`** — an instance becomes a standalone
  `examples/<FILENAME>.json` **only when a second tool needs to read
  it independently of the builder** — the composer that consumes it
  (`osmm-creative-brief-composer` reads `business_context` + `persona`
  instances), a future `-validator` that checks it, a third-party importer. At
  that point `examples/` holds the canonical, machine-consumable instance and the
  inline copy is the readable illustration.

The two are deliberately **not the same artifact**, so they don't drift into
conflict: the inline example shows shape (and may be abbreviated), while the
`examples/` file is the full, canonical instance. Once a real instance is
promoted, a long inline example may be trimmed to an excerpt plus a pointer to
the file, leaving one full canonical copy.

**Examples must be real and publicly sourced** (see "Where instance files live"
for the confidentiality rule): inline examples shed the "fictional placeholder"
status as the model matures — prefer a real, public-company example over an
invented one.

---

## Repository structure

Skills live **directly under `skills/`, one folder per skill** — a flat layout
that matches how Claude discovers plugin skills (each `skills/<skill-name>/SKILL.md`
is a direct child of `skills/`). **Object category** — the five stable buckets
that map to the read/write and governance profiles in the model — is captured in
each builder's frontmatter (`category:`), not in the folder structure. Category is
a more durable axis than workflow phase, but both live in frontmatter; the folder
is keyed only to the skill's own identity.

```
osmm/
├── skills/
│   ├── osmm-business-context-builder/SKILL.md   # category: Context Object
│   ├── osmm-brand-context-builder/SKILL.md       # category: Context Object
│   ├── osmm-audience-builder/SKILL.md            # category: Context Object
│   ├── osmm-persona-builder/SKILL.md             # category: Context Object
│   ├── osmm-marketing-strategy-builder/SKILL.md  # category: Work Product Object
│   ├── ...
│   ├── osmm-performance-measurement-builder/SKILL.md  # category: Measurement Object
│   ├── osmm-customer-insight-builder/SKILL.md    # category: Learning Object
│   └── osmm-creative-brief-composer/SKILL.md     # artifact-composer (NOT an object builder)
├── schemas/          # canonical JSON Schema per object — schemas/<object_type>.schema.json (single source of truth)
├── examples/         # validated example instances (e.g. PERSONA_wendys-deal-savvy-craver.json)
└── scripts/          # validate.py — checks every example against its object's schema (run in CI)
```

Object builders and artifact-composers sit side by side in the same flat `skills/`
directory; they are told apart by frontmatter, not location — a composer carries
`skill_class: artifact-composer` and *composes human-readable artifacts from
objects* rather than building an object. See
[Artifact-composer skills](#artifact-composer-skills).

---

## Frontmatter schema

Because the skill name carries no taxonomy, every builder's `SKILL.md` frontmatter carries it instead:

```yaml
name: osmm-business-context-builder
description: >-                    # trigger-rich: what it builds + when to use it (required for skill discovery)
  Convert any business/strategy source into a structured OSMM Business Context Object...
object: Business Context Object
object_type: business_context
category: Context Object           # Context | Work Product | Configuration | Measurement | Learning
phase: 1                           # 1–7, workflow phase
wave: 2                            # 1–4, release wave
osmm_version: 0.1.0                # OSMM schema version this builder targets
status: draft                      # draft | proposed | stable | deprecated
```

The `description` is not decorative — it is what makes the skill discoverable/triggerable, so it should name the object it builds and the situations that should invoke it.

**Length cap:** the `description` field must be **≤ 1024 characters** — the plugin-packaging validator rejects any skill whose description exceeds it. Keep it trigger-rich but within budget; if it grows past the cap, tighten the trigger list rather than dropping the object/boundary framing. Quick check across the repo:

```
python3 -c "import glob,yaml; [print(len(yaml.safe_load(open(f).read().split('---',2)[1])['description']), f) for f in glob.glob('skills/**/SKILL.md', recursive=True) if len(yaml.safe_load(open(f).read().split('---',2)[1]).get('description','')) > 1024]"
```

---

## Object lifecycle states

Mirrors the OSMM object lifecycle so a builder's maturity tracks its object's:

- **draft** — under exploration; schema unstable.
- **proposed** — open for community review.
- **stable** — safe to implement against.
- **deprecated** — scheduled for retirement; evolves under a formal deprecation period, never a silent break.

---

## Full builder registry

All 18 objects in the OSMM object model, mapped to their builder skill names.
(Speculative objects were consolidated in the v0.5/v0.6 right-sizing — see
[TAXONOMY.md](TAXONOMY.md) → the note under the object resolution index.)

| Phase | Object | Category | Skill name |
|------:|--------|----------|------------|
| 1 | Business Context | Context | `osmm-business-context-builder` |
| 1 | Brand Context | Context | `osmm-brand-context-builder` |
| 1 | Product Context | Context | `osmm-product-context-builder` |
| 1 | Marketing Strategy | Work Product | `osmm-marketing-strategy-builder` |
| 1 | Measurement Framework | Work Product | `osmm-measurement-framework-builder` |
| 2 | Audience | Context | `osmm-audience-builder` |
| 2 | Persona | Context | `osmm-persona-builder` |
| 3 | Offer | Work Product | `osmm-offer-builder` |
| 3 | Experiment Strategy | Work Product | `osmm-experiment-strategy-builder` |
| 4 | Campaign Strategy | Work Product | `osmm-campaign-strategy-builder` |
| 4 | Journey | Work Product | `osmm-journey-builder` |
| 5 | Creative Strategy | Work Product | `osmm-creative-strategy-builder` |
| 5 | Content Strategy | Work Product | `osmm-content-strategy-builder` |
| 6 | Experience | Work Product | `osmm-experience-builder` |
| 6 | Experience Component | Work Product | `osmm-experience-component-builder` |
| 7 | Performance Measurement | Measurement | `osmm-performance-measurement-builder` |
| 7 | Customer Insight | Learning | `osmm-customer-insight-builder` |
| 7 | Optimization Recommendation | Learning | `osmm-optimization-recommendation-builder` |

The **Experiment Strategy** object is cross-phase (it serves the test sub-processes
3.7, 4.7, and 5.7); it is listed once, at its earliest phase. Performance
Measurement absorbs the former per-dimension performance objects via a `dimension`
facet, and Measurement Framework absorbs campaign-scope measurement via a `scope`
facet.

---

## Future verb slots

The convention reserves the verb suffix for sibling skills that operate on the same object. When those are needed, they follow the identical pattern:

| Verb | Operates on | Purpose |
|------|-------------|---------|
| `-builder` | one object | Constructs and emits a valid instance of the object. |
| `-validator` | one object | Checks an instance against the object schema. |
| `-reader` | one object | Parses an existing instance into working context. |
| `-migrator` | one object | Upgrades an instance from one schema version to the next. |
| `-composer` | many objects → one artifact | Composes a human-readable artifact (a brief, a deck, a summary) from a set of objects. See [Artifact-composer skills](#artifact-composer-skills). |

The first four verbs are **object verbs** — each operates on a single object and
its schema, so they share the `osmm-<object-slug>-<verb>` form (e.g.
`osmm-persona-builder`, `osmm-persona-validator`, `osmm-persona-reader`).

`-composer` is different in kind: it does not operate on a single object, it
*reads several objects and emits an artifact*. It therefore keys to the
**artifact** name, not an object — `osmm-<artifact-slug>-composer` (e.g.
`osmm-creative-brief-composer`) — and lives directly under `skills/`, alongside
the object builders, distinguished by its `skill_class` frontmatter.

A `-validator` is also the trigger condition for promoting a schema out of its builder (see "Where the schema lives") — the moment two skills need the same schema, it becomes a standalone file.

---

## Artifact-composer skills

OSMM standardizes **objects** (the machine-readable interoperability contract).
It deliberately does **not** standardize **artifacts** — the human-readable
briefs, decks, and summaries rendered from those objects — because rendering is a
client/edge concern, and prescribing it would overreach the standard (see the
[Creative Brief resolution](#resolved-creative-brief-is-an-artifact-not-an-object)).

An **artifact-composer skill** sits at the skill layer, not the data-standard
layer. It is a **non-normative accelerator**: it reads a set of OSMM objects and
composes a useful first-draft artifact a client can then tailor. It does not
define a schema or an `object_type`, and the artifact it emits is not an OSMM
object.

Two properties make it OSMM-conformant rather than just a document generator:

1. **It consumes objects, by `object_type`.** A composer declares the object
   types it requires (and which strengthen the output if present) in its
   frontmatter `consumes` list, and resolves them as inputs. This is what makes
   the composer *enforce the standard*: you cannot get the accelerator without
   first having the structured objects — so the artifact becomes a pull-through
   for object adoption. Missing required objects are reported, with a pointer to
   the builder that produces each, rather than silently invented.

2. **It is data-driven, not hand-toggled.** Template/variant selection is driven
   by object data (e.g. a B2C vs B2B brief follows the Business Context
   `business_type`), not a manual switch.

### Naming and location

- Name: `osmm-<artifact-slug>-composer`. The slug is the artifact's name
  (`creative-brief`), lowercase, hyphen-delimited.
- Folder: `skills/<skill-name>/SKILL.md` — flat, alongside the object builders.
  The frontmatter `name` equals the folder name, as with every skill; a composer
  is told apart from a builder by its `skill_class`, not its location.

### Frontmatter

Composers carry artifact-oriented frontmatter instead of the object keys:

```yaml
name: osmm-creative-brief-composer
description: >-                     # trigger-rich: what it composes + when to use it
  ...
skill_class: artifact-composer     # distinguishes it from object builders
artifact: Creative Brief           # the human-readable artifact produced (NOT an object)
consumes:                          # the object_types it reads as input
  required: [business_context, brand_context, persona]
  optional: [marketing_strategy, creative_strategy, content_strategy, product_context,
             journey, audience, offer, campaign_strategy, measurement_framework]
phase: 5                           # workflow phase the artifact belongs to
osmm_version: 0.1.0                # OSMM schema version the consumed objects target
status: draft                      # draft | proposed | stable | deprecated
```

Note the absence of `object`, `object_type`, and `category` — a composer has no
object identity. `skill_class: artifact-composer` is the explicit marker.

### Output

A composer emits a human-readable artifact (typically Markdown), not JSON. Since
artifacts are non-normative, OSMM does not mandate the artifact's internal
format; the composer ships a sensible default template that clients tailor. If a
filename convention is wanted for consistency, mirror the instance pattern with
the artifact name in uppercase: `CREATIVE-BRIEF_<entity-slug>.md`.

---

## Instance file naming

Every JSON object instance produced by a builder follows a single filename pattern. The filename is the canonical identity of the instance — readable without opening the file, sortable by object type, and unambiguous when instances of different object types share the same entity slug.

### The pattern

```
<OBJECT-NAME>_<entity-slug>.json
<OBJECT-NAME>_<entity-slug>-<instance-slug>.json
```

Two parts separated by a single underscore:

- **`<OBJECT-NAME>`** — the canonical object name in uppercase, with hyphens between words. Derived directly from the object name with no abbreviation. Multi-word objects use hyphens: `BUSINESS-CONTEXT`, `CAMPAIGN-STRATEGY`, `JOURNEY-PERFORMANCE`.
- **`<entity-slug>`** — lowercase, hyphen-delimited slug identifying the entity the instance describes. For a second disambiguating segment (e.g. multiple personas for the same brand), append a hyphen and an instance slug.

### Rules

1. **No abbreviation.** The full object name is always spelled out. `PERSONA` not `PER`; `BUSINESS-CONTEXT` not `BIZ`. Abbreviations require a lookup; full names do not.
2. **Uppercase object name, lowercase entity slug.** The visual break between the two parts is immediate — no separator ambiguity.
3. **Underscore is the join between object name and entity; hyphens are used within each part.** The underscore appears exactly once per filename.
4. **Instance slug is optional.** Use it only when multiple instances of the same object type exist for the same entity (e.g. two personas for the same brand). When an entity has only one instance of a given type, omit the instance slug.
5. **Filenames are lowercase after the object name prefix** — entity and instance slugs follow the same slug rules as skill folder names.

### Examples

| Object | Entity | Instance | Filename |
|--------|--------|----------|----------|
| Persona | Wendy's | Deal-savvy craver | `PERSONA_wendys-deal-savvy-craver.json` |
| Business Context | IBM | — | `BUSINESS-CONTEXT_ibm.json` |
| Business Context | Wendy's | — | `BUSINESS-CONTEXT_wendys.json` |
| Campaign Strategy | Wendy's | Baconator Launch | `CAMPAIGN-STRATEGY_wendys-baconator-launch.json` |
| Journey | Wendy's | App Habit | `JOURNEY_wendys-app-habit.json` |
| Performance Measurement | Wendy's | FY2026 Q1 | `PERFORMANCE-MEASUREMENT_wendys-2026-q1.json` |
| Customer Insight | Wendy's | Checkout fee friction | `CUSTOMER-INSIGHT_wendys-checkout-fee-friction.json` |
| Optimization Recommendation | Wendy's | Checkout fee transparency | `OPTIMIZATION-RECOMMENDATION_wendys-checkout-fee-transparency.json` |

### Where instance files live

Validated example instances live **flat** in the `examples/` folder at the repo
root — one file per instance, no category subfolders. The object-prefixed
filename already carries the type, so the folder needs no further grouping:

```
examples/
├── BUSINESS-CONTEXT_ibm.json
├── BUSINESS-CONTEXT_wendys.json
├── PERSONA_wendys-deal-savvy-craver.json
├── CAMPAIGN-STRATEGY_wendys-baconator-launch.json
└── ...
```

**Examples must derive from public, non-confidential sources.** The repo is
openly licensed, so every committed instance has to be built from public
material (public-company filings, published research, the brand's own public
site) — IBM and Wendy's here are public companies. **Client work never
enters the repo**, even after validation: it is real but confidential, which is a
different category from "real but not yet promoted." Instances produced during
client or internal work stay outside the repo permanently; only public-sourced
instances are promoted into `examples/`.

---

## Controlled vocabularies

Some object fields are governed enums, not free text (e.g. Persona `persona_type`). These follow the same governance logic as the object model itself: a small, opinionated starter vocabulary, extended deliberately by maintainers — never invented per-project. Stored values use snake_case tokens (consistent with `object_type`) mapped to human-readable labels in the owning skill. This keeps fields machine-facetable instead of fragmenting into near-duplicate variants.

---

## Resolved: "Creative Brief" is an artifact, not an object

The concept papers and the L1 summary reference a **Creative Brief** *object*
(Wave 1 / Phase 5 work product), but the detailed object registry has no object
by that name — it carries Creative Strategy and Content Strategy, with the message
itself cascading from Brand Context, Product Context `product_messaging`, and the
Journey's `persona_tracks`.

**Resolution:** the Creative Brief is a **human-readable artifact, not an OSMM
object.** It is the rendered view of the underlying objects — specifically the
output of sub-process 5.8 (*Confirm Content & Creative Direction*), which
resolves to the **Creative Strategy Object** plus the cascaded message (Brand
Context + Product Context `product_messaging` + the Journey's `persona_tracks`; see
[`TAXONOMY.md`](TAXONOMY.md)). This is the same object-vs-rendering split that
runs through the rest of OSMM: the "Creative Brief" a person reads is a
presentation of structured objects, just as a Strategic Brief renders the
Marketing Strategy Object. The concept papers used "Creative Brief" as the
colloquial name for the deliverable before the detailed model decomposed it into
typed objects.

Consequences at the **data-standard layer**: there is no Creative Brief object,
no `object_type: creative_brief`, and no `osmm-creative-brief-builder` (an object
*builder* has no object to build). The object model stands at **18 objects**;
nothing is added or removed by this resolution. "Creative Brief" remains valid
only as an artifact label (e.g. in the TAXONOMY artifact column).

At the **skill layer**, this does not preclude an accelerator. OSMM ships an
`osmm-creative-brief-composer` — an [artifact-composer
skill](#artifact-composer-skills) that *reads* the underlying objects (Creative
Strategy, the Journey, and the Context objects behind them) and composes
a first-draft brief a client can tailor. The composer is non-normative: it
defines no schema and emits an artifact, not an object. So the standard stays
pure (objects only) while the skill library still delivers the brief as an
accelerator.

---

## Changes in v0.11

- **Journey gains a required `scope` facet and the Campaign↔Journey edge is set to one
  direction.** A journey is now explicitly either the durable, persona-anchored **`lifecycle`**
  backbone (the end-to-end view of how a persona experiences the brand — high-read, low-write,
  referenced by many campaigns) or a **`campaign`**-scoped slice that runs within it. This keeps
  the Journey a Work Product (it is a *designed* path, not observed Context — the observed truth
  already lives in Persona + Customer Insight) while capturing its durable, backbone nature as a
  property rather than a recategorization. The journey's downward `linked_campaign_strategy`
  reference is **removed**: the canonical edge is **Campaign Strategy → Journey** (the campaign's
  `linked_journey`), so a journey never points at a campaign. A `lifecycle` journey **must** anchor
  to ≥1 Persona and ≥1 Audience (its spine), enforced by a conditional `if/then` in the schema.
  Reconciled across the Journey schema + builder, RELATIONSHIPS (reference table + realized-edge
  narrative), the graph (regenerated — the `JNY-→CMS-` edge dropped), and CHANGELOG.

---

## Changes in v0.10

- **Built the Phase 7 Measure-Learn-Optimize layer — three objects, completing the model
  to 17 of 18 builders shipped.** `osmm-performance-measurement-builder` (Measurement
  category, prefix `PFM-`) records actuals against a Measurement Framework, faceted by a
  `dimension` field (overall / offer / creative / journey / channel / experience / campaign)
  so one object serves sub-processes 7.1/7.3/7.4/7.5 and absorbs the former per-dimension
  Performance objects; it is append-only (each period a new instance). `osmm-customer-insight-builder`
  (Learning category, prefix `CIN-`) is the interpreted *why*, drawn from Performance
  Measurements plus external research, and proposes durable updates back into Context
  (`proposes_updates_to[]`, sub-process 7.7). `osmm-optimization-recommendation-builder`
  (Learning category, prefix `OPR-`) is the prescription derived from insight + measurement,
  writing forward into Work Products/Strategy (`targets[]`) and carrying a `disposition`
  (proposed → accepted/rejected/implemented) distinct from the lifecycle `status`. The
  write-back is **lean pointer-plus-prose**, not a field-level patch: applying a change
  produces a new *version* of the target object. This populates the previously-empty
  **Measurement** and **Learning** categories and closes the learning loop. Only
  **Experiment Strategy** remains unbuilt (parked).

---

## Changes in v0.9

- **Collapsed Phase 6's Experience-\* family into a single `experience` object** (22 → 18).
  Experience Specification (6.1, `specification`), Experience Delivery (6.5), Personalization
  Configuration (6.4, `personalization_rules`), and Experience Validation (6.6, `validation`
  status) are one **Experience** decision object — the rendered asset lives in the production
  tool, referenced via `delivery_reference`. **Campaign Deployment → Campaign Strategy
  `launch_plan`** (6.7; per-experience go-live on the Experience's `deployment`). Only
  **Experience Component** stays separate (reusable building blocks the Experience references).
  The **Configuration** category is now empty (its members folded into the Journey's
  `delivery_logic` and the Experience's `personalization_rules`).

---

## Changes in v0.8

- **Dissolved Keyword, Keyword Strategy, and Messaging Framework into the Journey** (25 →
  22). Directional keywords are now a journey stage's `persona_tracks.key_questions` ("just
  enough to point downstream teams, not an SEO database"); messaging is a three-layer cascade
  — Brand Context (`brand_promise`/`messaging_pillars`) → Product Context (`product_messaging`)
  → the Journey's `persona_tracks.key_messages` — rendered as an artifact, not authored as an
  object. Each journey stage now carries per-persona tracks (`buyer_goal`, `milestones`,
  `key_activities`, `key_questions`, `key_messages`). Creative/Content Strategy dropped their
  `linked_messaging_framework`/`linked_keywords` references.

---

## Changes in v0.7

- **Folded Experience Design → Creative Strategy** (26 → 25). The creative system &
  experience concepts (sub-process 5.5) are creative direction, captured as the Creative
  Strategy's `experience_concepts`; no separate Experience Design object. Shipped the
  **Creative Strategy** (`CRS-`) and **Content Strategy** (`CTS-`) builders.

---

## Changes in v0.6

- **Merged Journey Strategy + Journey Configuration → a single `journey` object**
  (27 → 26). The designed path (stages, triggers, cadence) and its operational build
  are two views of one thing; the operational specifics live in the Journey Object's
  optional `delivery_logic` (resolving sub-process 6.3). Renamed the builder to
  `osmm-journey-builder` (prefix `JNY-`); Campaign Strategy now references it via
  `linked_journey`.
- **Deprioritized** the Keyword Strategy and Experiment Strategy builders (parked in
  the backlog) — no change to the object model, a sequencing decision.

---

## Changes in v0.5

- **Right-sized the registry from 35 to 27 objects** — five consolidations removed
  eight speculative (unbuilt) objects, applying "prefer a facet over a near-duplicate
  object; a new object must do work the others can't": Targeting Strategy → Marketing
  Strategy; Offer Strategy → Offer; per-dimension Performance objects (Offer/Creative/
  Journey/Experience) → Performance Measurement (`dimension` facet); Campaign
  Measurement → Measurement Framework (`scope` facet); Offer Test Strategy + Creative
  Test Strategy → a single cross-phase **Experiment Strategy**. Details in
  [TAXONOMY.md](TAXONOMY.md). Remaining unbuilt boundaries are provisional and confirmed
  at build time.

---

## Changes in v0.4

- Rewrote **"Where the schema lives"** — the canonical schema is now a standalone,
  strict JSON Schema file at `schemas/<object_type>.schema.json` (single source of
  truth), shipped with each builder; the `SKILL.md` references it and keeps only an
  illustrative excerpt + guidance. This **supersedes** the v0.2 inline-until-promoted
  rule. Reflects OSMM's positioning as an interoperability standard (the schema is
  the product) and removes drift by keeping one source of truth.
- Added **`scripts/validate.py`** + a `validate` CI workflow: every `examples/`
  instance must validate against its object's schema; migration-aware (objects
  without a schema yet are skipped, not failed).
- Updated the **repository structure** example: `schemas/` is canonical-per-object;
  added `scripts/`.

---

## Changes in v0.3

- Added **"Instance file naming"** — full object name in uppercase + entity slug pattern (`BUSINESS-CONTEXT_ibm.json`); no abbreviations, underscore as the single join between object name and entity, hyphens within each part. Includes examples table and `examples/` folder structure.
- Updated **repository structure** example to reflect new instance filename convention.

---

## Changes in v0.2

- Added **"Where the schema lives"** — schemas are embedded in the builder's `SKILL.md` and promoted to standalone files only when a second tool needs them.
- Added `description` to the **frontmatter schema** (required for skill discovery; surfaced while building `osmm-persona-builder`).
- Added **"Controlled vocabularies"** — governance rule for enum fields like `persona_type`.
- Expanded the **repository structure** to show `schemas/` and `examples/` alongside `skills/`.
