# OSMM Skill Naming Convention

**Open Semantic Marketing Model — builder skills**
Status: Draft v0.3

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

In v0.1, a builder's object schema is defined **inline in its `SKILL.md` body** — a lean field list with types, requirements, and a worked example — not as a separate file. This keeps the standard shippable and avoids over-engineering a formal JSON Schema before the object has been exercised against real inputs.

A schema is promoted to a standalone `schemas/<object_type>.schema.json` **only when a second tool needs to read it independently of the builder** — a validator, a third-party importer, another implementation. Until that moment the skill is the single source of truth, and the frontmatter `osmm_version` records which schema version the builder conforms to. (Reference proven out by `osmm-persona-builder`, the first built skill.)

---

## Repository structure

Skills are grouped by **object category** — the five stable buckets that map to the read/write and governance profiles in the model. Category is a more durable axis than workflow phase, so it drives the folder layout; phase and wave live in frontmatter.

```
osmm/
├── skills/
│   ├── context/
│   │   ├── osmm-business-context-builder/SKILL.md
│   │   ├── osmm-brand-context-builder/SKILL.md
│   │   ├── osmm-audience-builder/SKILL.md
│   │   ├── osmm-persona-builder/SKILL.md
│   │   └── osmm-keyword-builder/SKILL.md
│   ├── work-product/
│   │   ├── osmm-marketing-strategy-builder/SKILL.md
│   │   └── ...
│   ├── configuration/
│   │   ├── osmm-journey-configuration-builder/SKILL.md
│   │   └── osmm-personalization-configuration-builder/SKILL.md
│   ├── measurement/
│   │   ├── osmm-experience-performance-builder/SKILL.md
│   │   └── osmm-performance-measurement-builder/SKILL.md
│   └── learning/
│       ├── osmm-customer-insight-builder/SKILL.md
│       └── ...
├── schemas/          # added per-object only when a schema is promoted out of its skill
└── examples/         # validated example instances (e.g. PERSONA_butcherbox-jesse.json)
```

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

---

## Object lifecycle states

Mirrors the OSMM object lifecycle so a builder's maturity tracks its object's:

- **draft** — under exploration; schema unstable.
- **proposed** — open for community review.
- **stable** — safe to implement against.
- **deprecated** — scheduled for retirement; evolves under a formal deprecation period, never a silent break.

---

## Full builder registry

All 34 objects in the OSMM object model, mapped to their builder skill names.

| Phase | Object | Category | Skill name |
|------:|--------|----------|------------|
| 1 | Business Context | Context | `osmm-business-context-builder` |
| 1 | Brand Context | Context | `osmm-brand-context-builder` |
| 1 | Marketing Strategy | Work Product | `osmm-marketing-strategy-builder` |
| 1 | Measurement Framework | Work Product | `osmm-measurement-framework-builder` |
| 2 | Targeting Strategy | Work Product | `osmm-targeting-strategy-builder` |
| 2 | Audience | Context | `osmm-audience-builder` |
| 2 | Persona | Context | `osmm-persona-builder` |
| 2 | Keyword | Context | `osmm-keyword-builder` |
| 2 | Keyword Strategy | Work Product | `osmm-keyword-strategy-builder` |
| 3 | Offer Strategy | Work Product | `osmm-offer-strategy-builder` |
| 3 | Offer | Work Product | `osmm-offer-builder` |
| 3 | Offer Test Strategy | Work Product | `osmm-offer-test-strategy-builder` |
| 4 | Campaign Strategy | Work Product | `osmm-campaign-strategy-builder` |
| 4 | Journey Strategy | Work Product | `osmm-journey-strategy-builder` |
| 4 | Campaign Measurement | Work Product | `osmm-campaign-measurement-builder` |
| 5 | Messaging Framework | Work Product | `osmm-messaging-framework-builder` |
| 5 | Creative Strategy | Work Product | `osmm-creative-strategy-builder` |
| 5 | Content Strategy | Work Product | `osmm-content-strategy-builder` |
| 5 | Experience Design | Work Product | `osmm-experience-design-builder` |
| 5 | Creative Test Strategy | Work Product | `osmm-creative-test-strategy-builder` |
| 6 | Experience Specification | Work Product | `osmm-experience-specification-builder` |
| 6 | Experience Component | Work Product | `osmm-experience-component-builder` |
| 6 | Journey Configuration | Configuration | `osmm-journey-configuration-builder` |
| 6 | Personalization Configuration | Configuration | `osmm-personalization-configuration-builder` |
| 6 | Experience Delivery | Work Product | `osmm-experience-delivery-builder` |
| 6 | Experience Validation | Work Product | `osmm-experience-validation-builder` |
| 6 | Campaign Deployment | Work Product | `osmm-campaign-deployment-builder` |
| 6 | Experience Performance | Measurement | `osmm-experience-performance-builder` |
| 7 | Performance Measurement | Measurement | `osmm-performance-measurement-builder` |
| 7 | Customer Insight | Learning | `osmm-customer-insight-builder` |
| 7 | Offer Performance | Learning | `osmm-offer-performance-builder` |
| 7 | Creative Performance | Learning | `osmm-creative-performance-builder` |
| 7 | Journey Performance | Learning | `osmm-journey-performance-builder` |
| 7 | Optimization Recommendation | Learning | `osmm-optimization-recommendation-builder` |

---

## Future verb slots

The convention reserves the verb suffix for sibling skills that operate on the same object. When those are needed, they follow the identical pattern:

| Verb | Purpose |
|------|---------|
| `-builder` | Constructs and emits a valid instance of the object. |
| `-validator` | Checks an instance against the object schema. |
| `-reader` | Parses an existing instance into working context. |
| `-migrator` | Upgrades an instance from one schema version to the next. |

Example: `osmm-persona-builder`, `osmm-persona-validator`, `osmm-persona-reader`.

A `-validator` is also the trigger condition for promoting a schema out of its builder (see "Where the schema lives") — the moment two skills need the same schema, it becomes a standalone file.

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
| Persona | ButcherBox | Jesse | `PERSONA_butcherbox-jesse.json` |
| Business Context | IBM | — | `BUSINESS-CONTEXT_ibm.json` |
| Business Context | ButcherBox | — | `BUSINESS-CONTEXT_butcherbox.json` |
| Campaign Strategy | ButcherBox | Summer Winback | `CAMPAIGN-STRATEGY_butcherbox-summer-winback.json` |
| Keyword | — | Marketing Operating Model | `KEYWORD_marketing-operating-model.json` |
| Journey Performance | ButcherBox | Lapsed Buyer | `JOURNEY-PERFORMANCE_butcherbox-lapsed-buyer.json` |

### Where instance files live

Validated example instances live in the `examples/` folder at the repo root, organized by object category — mirroring the `skills/` structure:

```
examples/
├── context/
│   ├── BUSINESS-CONTEXT_ibm.json
│   ├── BUSINESS-CONTEXT_butcherbox.json
│   └── PERSONA_butcherbox-jesse.json
├── work-product/
│   └── CAMPAIGN-STRATEGY_butcherbox-summer-winback.json
├── configuration/
├── measurement/
└── learning/
```

Instances produced during client work or internal testing that are not yet validated against the schema live outside the repo until they are reviewed and promoted.

---

## Controlled vocabularies

Some object fields are governed enums, not free text (e.g. Persona `persona_type`). These follow the same governance logic as the object model itself: a small, opinionated starter vocabulary, extended deliberately by maintainers — never invented per-project. Stored values use snake_case tokens (consistent with `object_type`) mapped to human-readable labels in the owning skill. This keeps fields machine-facetable instead of fragmenting into near-duplicate variants.

---

## Resolved: "Creative Brief" is an artifact, not an object

The concept papers and the L1 summary reference a **Creative Brief** *object*
(Wave 1 / Phase 5 work product), but the detailed object registry has no object
by that name — it carries Messaging Framework, Creative Strategy, Content
Strategy, Experience Design, and Creative Test Strategy instead.

**Resolution:** the Creative Brief is a **human-readable artifact, not an OSMM
object.** It is the rendered view of the underlying objects — specifically the
output of sub-process 5.8 (*Confirm Content & Creative Direction*), which
resolves to the **Creative Strategy Object + Messaging Framework Object** (see
[`TAXONOMY.md`](TAXONOMY.md)). This is the same object-vs-rendering split that
runs through the rest of OSMM: the "Creative Brief" a person reads is a
presentation of structured objects, just as a Strategic Brief renders the
Marketing Strategy Object. The concept papers used "Creative Brief" as the
colloquial name for the deliverable before the detailed model decomposed it into
typed objects.

Consequences: there is no Creative Brief object, no `object_type:
creative_brief`, and no `osmm-creative-brief-builder`. The object model stands at
**34 objects**; nothing is added or removed by this resolution. "Creative Brief"
remains valid only as an artifact label (e.g. in the TAXONOMY artifact column).

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
