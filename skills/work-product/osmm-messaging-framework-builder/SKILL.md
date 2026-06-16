---
name: osmm-messaging-framework-builder
description: >-
  Build the message architecture for an offering or campaign as a structured OSMM Messaging
  Framework Object (canonical JSON) — the message hierarchy, value framing, message pillars,
  proof points, and message variations differentiated by persona. Inputs include product
  messaging, positioning docs, message houses, value-proposition frameworks, persona research,
  or a strategist's notes. Use this skill whenever the user wants to structure what the brand
  says and how it's prioritized: "build a messaging framework object," "structure our
  messaging," define a message hierarchy or message architecture, set value framing, lay out
  message pillars and proof points, or produce message variations by persona. The message
  architecture — what we say and how it's prioritized — differentiated by persona.
object: Messaging Framework Object
object_type: messaging_framework
category: Work Product
phase: 5
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Messaging Framework Builder

Build a valid **OSMM Messaging Framework Object** from any source describing what a brand says
about an offering and how that message is prioritized.

A Messaging Framework Object is the **message architecture** — the structured record of *what we
say and in what order of priority*: the single overarching message (the apex of the hierarchy),
the supporting message pillars that hold it up, the evidence that substantiates it, and — at its
core — the **message variants differentiated by Persona**. It is a Phase 5 Work Product resolving
sub-processes **5.1** (define messaging strategy: message hierarchy, value framing) and **5.4**
(message hierarchy & variations: message prioritization). Downstream Creative, Content, and
Experience work reference this so every execution ladders up to the same architecture instead of
re-inventing the message per channel.

This is the lean v0.1 builder. It captures the message architecture and its persona variations,
and nothing more. Creative themes, emotional strategy, and channel execution are deliberately out
of scope — they belong to the **Creative Strategy Object**; this object stays at the level of
*the message*, not its dressing.

## Core design rule — differentiated by Persona, delivered by Audience

This object embodies the Phase 5 rule from `TAXONOMY.md`:

> **Messaging is differentiated by Persona, delivered by Audience.**

The message — its angle, value framing, and variations — is tuned to what *moves* a reader:
`motivations`, `pain_points`, `decision_criteria`, and `messaging_preferences`, which are
**Persona** attributes (a Persona carries `messaging_preferences` — that is the differentiation
hook). So this framework's per-variant differentiation **keys to a Persona**
(`persona_variants[].linked_persona`, and the framework-level `linked_personas`), and it
**sources its raw material** from the linked Product Context's `product_messaging`
(`primary_message`, `value_pillars`, `proof_points`).

It **must not** carry audience-membership logic. *Which* segment receives *which* variant is a
**delivery** decision — that targets an **Audience** (a Persona isn't addressable) and lives in
the **Campaign Strategy** (personalization + `audience_offer_mapping`) via the Persona ↔ Audience
link. Putting "this segment gets variant B" here would duplicate the Audience Object and blur the
describe-vs-select line that runs through OSMM. Keep this object to the message; leave the
delivery routing to Campaign Strategy.

## Boundaries — what this object is and is NOT

| Object | Owns | This object's relationship |
|--------|------|----------------------------|
| **Product Context** `product_messaging` | The durable, product-level story (primary message, value pillars, proof points) regardless of campaign. | **Source.** This framework draws raw material from it and adapts it — it does not restate it. |
| **Messaging Framework** (this) | The message architecture: hierarchy, value framing, pillars, proof, and **persona-differentiated variants** (5.1/5.4). | — |
| **Creative Strategy** | Creative themes, emotional strategy, channel creative requirements, execution (5.2/5.6). | **Downstream.** It dresses the message; it does not set it. Stop at *what we say*; leave *how it looks/feels* to Creative. |
| **Brand Context** | Durable brand voice and guardrails (who the brand is). | **Referenced** via `linked_brand_context`. Per-variant `tone` and `tone_principles` apply that voice; they don't redefine it. |
| **Audience** | The addressable segment and its selection rules — *who is targeted*. | **Out of scope here.** Delivery (which segment gets which variant) is a Campaign Strategy decision, not a message decision. |

Rules of thumb:

- **Persona differentiates the message; Audience delivers it.** Variants key to `PER-` ids, never
  `AUD-` ids. There is no audience-membership field in this object on purpose.
- **Source from `product_messaging`, don't duplicate it.** The Product Context holds the durable
  product story; this framework adapts it into a prioritized architecture with per-persona angles.
- **Pillars are the hierarchy.** `primary_message` is the apex; `message_pillars[]` is the tier
  beneath it; `persona_variants[]` re-expresses the apex per reader. Keep those three layers
  distinct.
- **Voice lives in Brand Context.** Reference it; `tone`/`tone_principles` are framework-scoped
  notes, not a second voice definition.

## The output schema

> **Canonical schema:** [`schemas/messaging_framework.schema.json`](../../../schemas/messaging_framework.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "messaging_framework",      // const — always "messaging_framework"
  "osmm_version": "0.1.0",                   // schema version this conforms to
  "messaging_framework_id": "MSF-<slug>",    // stable, human-readable id (see ID rules)
  "version": "1.0",                          // instance version; bump on revision
  "status": "draft",                         // draft | proposed | stable | deprecated

  "name": "",                                // readable label (e.g. "IBM watsonx Messaging Framework")
  "primary_message": "",                     // the single overarching message — the hierarchy's apex (5.1)

  "message_pillars": [                        // the supporting pillars — the hierarchy's middle tier (5.1/5.4)
    {
      "pillar": "",                          // the pillar's name / theme
      "support": "",                         // how it substantiates the primary message
      "proof_points": []                     // OPTIONAL — pillar-level evidence
    }
  ],
  "proof_points": [],                         // OPTIONAL — framework-level evidence substantiating the messaging
  "value_framing": "",                        // OPTIONAL — how value is framed overall

  "persona_variants": [                       // THE CORE — message variants differentiated BY persona
    {
      "linked_persona": "PER-<slug>",        // the Persona this variant is tuned to (the differentiation key)
      "angle": "",                           // which of their motivations/pains/criteria the message leans into
      "key_message": "",                     // the primary message, re-expressed for this persona
      "tone": "",                            // OPTIONAL — how to sound, within the brand voice
      "emphasis": []                         // OPTIONAL — which pillars/proof points to foreground
    }
  ],

  "tone_principles": [],                      // OPTIONAL — framework-level tone notes; brand voice lives in Brand Context
  "linked_product": "PRD-<slug>",             // OPTIONAL — Product Context whose product_messaging this draws from
  "linked_personas": [],                      // OPTIONAL — PER- ids this framework serves
  "linked_brand_context": "BRC-<slug>",       // OPTIONAL — voice / guardrails
  "linked_campaign_strategy": "CMS-<slug>",   // OPTIONAL — if scoped to a campaign
  "linked_business_context": "BIZ-<slug>",    // OPTIONAL — the owning business
  "source": ""                                // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"messaging_framework"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `messaging_framework_id` | string | yes | `MSF-<slug>`. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Readable label, usually entity + offering. |
| `primary_message` | string | yes | The single overarching message — the apex of the hierarchy. One line everything ladders up to. |
| `message_pillars` | object[] | yes | ≥1. Each `{ pillar, support, proof_points? }`. 2-4 is usually right. The supporting tier of the hierarchy. |
| `message_pillars[].pillar` | string | yes | The pillar's name / theme. |
| `message_pillars[].support` | string | yes | The argument this pillar makes for the primary message. |
| `message_pillars[].proof_points` | string[] | no | Pillar-level evidence. Omit if thin. |
| `proof_points` | string[] | no | Framework-level evidence (stats, certifications, named customers, awards). |
| `value_framing` | string | no | The lens through which value is communicated overall. |
| `persona_variants` | object[] | yes | ≥1. **The core of this object.** One entry per Persona; differentiation keys to the persona, never to an audience. |
| `persona_variants[].linked_persona` | string | yes | `PER-<slug>` (or `PER-PLACEHOLDER-<slug>`). The differentiation key. |
| `persona_variants[].angle` | string | yes | Which of the persona's motivations / pain points / decision criteria the message leans into. |
| `persona_variants[].key_message` | string | yes | The primary message re-expressed for this persona. |
| `persona_variants[].tone` | string | no | How to sound for them, within the brand voice. |
| `persona_variants[].emphasis` | string[] | no | Which pillars / proof points to foreground for this persona. |
| `tone_principles` | string[] | no | Framework-scoped tone notes. Brand voice lives in Brand Context — reference it, don't redefine it. |
| `linked_product` | string | no | `PRD-<slug>` of the Product Context this sources `product_messaging` from. `PRD-PLACEHOLDER-<slug>` ok. |
| `linked_personas` | string[] | no | `PER-` ids this framework serves. Each variant keys to one. `PER-PLACEHOLDER-<slug>` ok. |
| `linked_brand_context` | string | no | `BRC-<slug>` owning voice and guardrails. `BRC-PLACEHOLDER-<slug>` ok. |
| `linked_campaign_strategy` | string | no | `CMS-<slug>` if scoped to a campaign. `CMS-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning business. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`messaging_framework_id` = `MSF-` + a lowercase, hyphen-delimited slug. Scope it to the **entity
plus the offering (or campaign)** it carries the message for, so frameworks stay distinct across a
portfolio:

- IBM watsonx → `MSF-ibm-watsonx` (sources `PRD-ibm-watsonx`)
- Wendy's Baconator → `MSF-wendys-baconator` (sources `PRD-wendys-baconator`)

If a framework is scoped to a specific campaign rather than the durable offering, name it for the
campaign (`MSF-wendys-baconator-launch`) and set `linked_campaign_strategy`. Keep the id stable
once assigned — downstream Creative/Content objects reference it. Bump `version` on revision.

## Extraction principles

1. **Differentiate by Persona, never by Audience.** Each `persona_variants` entry keys to a `PER-`
   id. Tune `angle`/`key_message` to that persona's `motivations`, `pain_points`,
   `decision_criteria`, and `messaging_preferences`. Do **not** record which segment receives which
   variant — that delivery decision is Campaign Strategy's, and recording it here would duplicate
   the Audience Object.
2. **Source from `product_messaging`; don't restate it.** Draw the raw material — primary message,
   value pillars, proof points — from the linked Product Context, then *prioritize and adapt* it
   into an architecture. If a line is identical to the Product Context, you're copying, not framing.
3. **Pillars are the hierarchy.** `primary_message` is the apex; `message_pillars[]` are the
   supports beneath it; `persona_variants[].key_message` re-expresses the apex per reader. Keep the
   layers distinct — a pillar is a theme, not a persona variant.
4. **Stop at the message.** Creative themes, emotional strategy, look-and-feel, and channel rules
   are Creative Strategy. If a sentence is about *how it looks or feels* rather than *what we say*,
   it belongs downstream.
5. **Voice is referenced, not redefined.** Set `linked_brand_context`; use `tone`/`tone_principles`
   only for framework-scoped guidance. Don't author a parallel brand voice here.
6. **Ground the proof.** Prefer stated, verifiable evidence. If a claim is asserted without
   evidence, omit it or flag the thinness rather than laundering it into a proof point.
7. **Keep arrays signal-bearing.** A tight set of real pillars and persona variants beats a long
   generic list. One variant per persona that genuinely needs a distinct angle — resist padding.

## Output rules

- Emit valid JSON (no comments in the actual output — the `jsonc` above is illustrative).
- One object per offering-or-campaign message architecture. Save using the OSMM instance-naming
  convention: `MESSAGING-FRAMEWORK_<entity-slug>.json` (e.g. `MESSAGING-FRAMEWORK_ibm-watsonx.json`),
  with an optional instance slug when one entity has multiple frameworks — uppercase object name,
  underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The
  `messaging_framework_id` (`MSF-<slug>`) remains the id *inside* the object; it is not the filename.
- Set `linked_product` to the real `PRD-<slug>` if it exists; otherwise use `PRD-PLACEHOLDER-<slug>`
  and tell the user to resolve it. Do the same for `linked_personas`/`linked_persona` (`PER-`),
  `linked_brand_context` (`BRC-`), `linked_campaign_strategy` (`CMS-`), and
  `linked_business_context` (`BIZ-`).
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin (especially
  proof points and the per-persona angles) so they can fill gaps. If you find delivery/targeting
  logic in the source ("send variant B to high-value segment"), note it and point the user to the
  Campaign Strategy Object rather than smuggling it into this one.

## Starter prompts

**From product messaging and persona research:**
> Build an OSMM Messaging Framework Object for [Offering] by [Brand]. Source the raw material from
> the Product Context `product_messaging` (`PRD-[offering-slug]`), set a primary message and 2-4
> pillars with proof points, and write a persona variant for each priority persona — keying each to
> its `PER-` id and tuning the angle to that persona's motivations and pain points. Link the Brand
> Context for voice. Leave delivery/targeting to Campaign Strategy.

**From a positioning doc or message house (no persona research yet):**
> Build an OSMM Messaging Framework Object for [Brand]/[Offering] from this positioning document.
> Capture the message hierarchy and value framing; create persona variants with placeholder
> `PER-PLACEHOLDER-<slug>` ids and flag that the per-persona angles are inferred and should be
> confirmed against persona research.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below
illustrate the shape; both validate against the canonical schema.

### Example 1 — B2B platform messaging (IBM watsonx)

Built from IBM's public watsonx messaging. Sources `PRD-ibm-watsonx`'s `product_messaging`,
differentiates by the enterprise-IT decision-maker persona, and references `BRC-ibm` for voice.

```json
{
  "object_type": "messaging_framework",
  "osmm_version": "0.1.0",
  "messaging_framework_id": "MSF-ibm-watsonx",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Messaging Framework",
  "primary_message": "Enterprise AI you can trust to scale — on your data, with governance, across any cloud.",
  "message_pillars": [
    {
      "pillar": "Open",
      "support": "Build on IBM Granite and curated open models, not a single black box — so you keep choice and avoid lock-in.",
      "proof_points": [
        "IBM Granite models plus curated open-source models, tunable on enterprise data",
        "Runs across hybrid cloud (on-prem, IBM Cloud, other clouds)"
      ]
    },
    {
      "pillar": "Targeted",
      "support": "Tuned to enterprise use cases and run on your governed data, so AI moves from pilot to production.",
      "proof_points": [
        "watsonx.data lakehouse unifies and governs the data models run on",
        "Adopted for code generation, customer-service automation, and knowledge retrieval over proprietary data"
      ]
    },
    {
      "pillar": "Trusted",
      "support": "Governance, explainability, and IP indemnification make AI safe to scale in regulated industries.",
      "proof_points": [
        "watsonx.governance monitors models for drift, bias, and compliance with audit documentation",
        "IBM Granite models ship with contractual IP indemnification",
        "Adopted across financial services, government, and healthcare where compliance is a gate"
      ]
    }
  ],
  "proof_points": [
    "Three integrated components (watsonx.ai, watsonx.data, watsonx.governance) span the AI lifecycle",
    "Backed by IBM Consulting for deployment"
  ],
  "value_framing": "Frame value as trusted scale: not access to a model, but the ability to put governed AI into production on your own data without surrendering control.",
  "persona_variants": [
    {
      "linked_persona": "PER-PLACEHOLDER-ibm-enterprise-it-decision-maker",
      "angle": "De-risk enterprise AI: lead with governance, data control, and IP indemnification — the things that protect a career and pass an audit.",
      "key_message": "Put AI into production on your governed data, with the security, compliance, and indemnification a regulated enterprise requires — without locking workloads to one cloud.",
      "tone": "Credible, precise, peer-validated — technical depth expected, no inflated claims.",
      "emphasis": ["Trusted", "Open"]
    }
  ],
  "tone_principles": [
    "Enterprise-credible and evidence-led; let analyst recognition and customer proof carry weight",
    "Apply the IBM brand voice defined in Brand Context — do not invent a parallel voice here"
  ],
  "linked_product": "PRD-ibm-watsonx",
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-it-decision-maker"],
  "linked_brand_context": "BRC-ibm",
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx messaging and the PRD-ibm-watsonx Product Context (2024). Persona angle inferred from public enterprise-buyer research; the linked persona is a placeholder until that object ships."
}
```

### Example 2 — B2C product messaging (Wendy's Baconator)

Built from Wendy's public product messaging. Sources `PRD-wendys-baconator`, differentiates by the
shipped deal-savvy craver persona, and references `BRC-wendys`.

```json
{
  "object_type": "messaging_framework",
  "osmm_version": "0.1.0",
  "messaging_framework_id": "MSF-wendys-baconator",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's Baconator Messaging Framework",
  "primary_message": "More meat, more bacon, real value — no filler.",
  "message_pillars": [
    {
      "pillar": "Meat-forward",
      "support": "Two quarter-pound fresh-beef patties answer a serious-hunger craving a value menu won't satisfy.",
      "proof_points": ["Two quarter-pound patties of fresh, never-frozen beef"]
    },
    {
      "pillar": "Bacon you can count",
      "support": "Six strips of Applewood-smoked bacon, not a token slice — the thing the name promises.",
      "proof_points": ["Six strips of Applewood-smoked bacon per Baconator"]
    },
    {
      "pillar": "Real value",
      "support": "A premium, indulgent burger that still feels worth the spend against the biggest chains.",
      "proof_points": ["Long-running signature item; variants (Son of, Breakfast) span hunger levels and price points"]
    }
  ],
  "proof_points": [
    "Fresh, never-frozen beef as a core Wendy's quality claim",
    "Signature menu staple central to the brand's premium-burger identity"
  ],
  "value_framing": "Frame value as quality-you-can-see for the money: substantial, premium ingredients at a price that competes head-on — not cheapness.",
  "persona_variants": [
    {
      "linked_persona": "PER-wendys-deal-savvy-craver",
      "angle": "Indulgence that still feels smart: lead with the visible meat-and-bacon payoff and the sense of getting real value, not just a low price.",
      "key_message": "When you're seriously hungry, the Baconator stacks two fresh-beef patties and six strips of bacon — a premium burger that's actually worth it.",
      "tone": "Bold, confident, culturally fluent — Wendy's signature sharp personality.",
      "emphasis": ["Meat-forward", "Bacon you can count", "Real value"]
    }
  ],
  "tone_principles": [
    "Sharp, witty, confident — apply the Wendy's brand voice from Brand Context",
    "Let the product's visible payoff do the bragging; avoid generic fast-food claims"
  ],
  "linked_product": "PRD-wendys-baconator",
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_brand_context": "BRC-wendys",
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: wendys.com menu/product messaging and the PRD-wendys-baconator Product Context (2024). Persona angle inferred from the PER-wendys-deal-savvy-craver persona."
}
```
