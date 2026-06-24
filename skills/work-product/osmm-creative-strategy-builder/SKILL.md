---
name: osmm-creative-strategy-builder
description: >-
  Build the creative direction for an offering or campaign as a structured OSMM Creative Strategy Object (canonical JSON) — the big idea / creative platform, the creative themes and emotional strategy, the creative system & experience concepts, and channel-specific creative requirements. Inputs include creative briefs, creative platform docs, brand campaign decks, art-direction notes, experience-design concepts, or a creative director's notes. Use this skill whenever the user wants to structure HOW the brand expresses its message: "build a creative strategy object," set a creative direction, define a big idea or creative platform, lay out creative themes or territories, define an emotional strategy, capture a creative system or experience concepts, or spell out channel creative requirements. This captures the creative direction — how we express the message, distinct from the message itself — and absorbs the former Experience Design object.
object: Creative Strategy Object
object_type: creative_strategy
category: Work Product
phase: 5
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Creative Strategy Builder

Build a valid **OSMM Creative Strategy Object** from any source describing *how* a brand expresses
its message for an offering or campaign.

A Creative Strategy Object is the **creative direction** — the structured record of *how we express
the message*: the central **creative platform** (the big idea everything ladders up to), the
**creative themes** / territories it explores, the **emotional strategy** (the feeling it evokes),
the **creative system & experience concepts** that bring the platform to life, and the
**channel-specific creative requirements** that translate it per medium. It is a Phase 5 Work
Product resolving sub-processes **5.2** (creative themes, emotional strategy), **5.6**
(channel-specific creative requirements), and **5.8** (confirm the final creative direction).

It **absorbs the former Experience Design object** (sub-process **5.5**, *creative system &
experience concepts*): that work now lives here in `experience_concepts[]` rather than in a separate
object. Creative system thinking and experience ideas are part of the same creative direction, so
they travel with it.

This object is the creative *dressing* of the message. It does not set the message (that cascades
from Brand Context, Product Context, and the Journey — see below) or plan the content (Content
Strategy) or redefine the brand (Brand Context). It expresses the message within the brand, in a way
the channels can execute.

## Core design rule — express the message, don't restate or redefine it

Creative Strategy sits one layer down from the message itself. The message is not a single object —
it cascades in three layers, each with its own home:

- **Brand level** → **Brand Context** (`brand_promise`, `messaging_pillars`, voice/tone).
- **Product/solution level** → **Product Context** (`product_messaging`: primary message, value
  pillars, proof points).
- **Persona × journey-stage level** → the **Journey** object's
  `stages[].persona_tracks[].key_messages`.

Creative Strategy takes *what we say* (that cascade) and decides *how we say it* — the big idea, the
themes, the feeling, the experience, the channel treatments. It draws the message from
`linked_brand_context` (brand promise/pillars) and `linked_product` (`product_messaging` value
pillars), resolves it per persona/stage via the Journey, and operates inside `linked_brand_context`'s
voice and identity.

- It **does not** restate the brand promise/pillars, product value pillars, or persona/stage
  key messages — it references the Brand Context, Product Context, and Journey that own them and
  builds expression on top.
- It **does not** redefine the brand voice, palette, or identity — those are durable Brand Context.
  Creative Strategy applies them to a specific offering/campaign and may extend them creatively, but
  the durable definition stays in Brand Context.
- It **does not** plan which content gets produced or in what sequence — that is Content Strategy.

## Boundaries — what this object is and is NOT

| Object | Owns | This object's relationship |
|--------|------|----------------------------|
| **Brand Context** | The brand-level message — `brand_promise`, `messaging_pillars` — plus the durable brand voice, identity, and guardrails (who the brand is, across everything). | **Source + referenced** via `linked_brand_context`. Creative Strategy expresses the brand promise/pillars and operates inside the voice; `creative_principles` and `emotional_strategy` apply that identity to this work, they don't redefine it. |
| **Product Context** | The product-level message — `product_messaging`: the primary message, value pillars, and proof points for the offering. | **Source.** Referenced via `linked_product`. Creative Strategy expresses these value pillars; it does not restate them. Stop dressing once you start rewriting the message. |
| **Journey** | The persona × stage message — `stages[].persona_tracks[].key_messages`, what each persona needs to hear at each stage. | **Source.** Creative Strategy resolves expression per persona/stage against these key messages; it does not author them. |
| **Creative Strategy** (this) | *How we express the message* — the big idea / creative platform, creative themes, emotional strategy, creative system & experience concepts, and channel creative requirements (5.2/5.5/5.6/5.8). | — |
| **Content Strategy** | *The content plan* — content priorities, types, and sequencing (5.3). | **Downstream peer.** It plans what content to make; this sets the creative direction that content executes against. Don't list content deliverables here. |

Rules of thumb:

- **Express, don't restate.** Themes, emotion, and experience concepts *interpret* the message —
  they don't repeat the pillars. Reference the message cascade (Brand Context, Product Context,
  Journey); build on it.
- **Apply the brand, don't author it.** Voice and identity live in Brand Context. Use
  `creative_principles` for creative-strategy-scoped guardrails only.
- **The platform is the apex.** `creative_platform` is the single big idea; `creative_themes[]` are
  the territories beneath it; `experience_concepts[]` and `channel_creative[]` are how it lives.
  Keep those layers distinct.
- **Experience concepts belong here now.** The former Experience Design object is absorbed —
  creative system and experience ideas go in `experience_concepts[]`, not a separate object.

## The output schema

> **Canonical schema:** [`schemas/creative_strategy.schema.json`](../../../schemas/creative_strategy.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "creative_strategy",        // const — always "creative_strategy"
  "osmm_version": "0.1.0",                    // schema version this conforms to
  "creative_strategy_id": "CRS-<slug>",       // stable, human-readable id (see ID rules)
  "version": "1.0",                           // instance version; bump on revision
  "status": "draft",                          // draft | proposed | stable | deprecated

  "name": "",                                 // readable label (e.g. "IBM watsonx Creative Strategy")
  "creative_platform": "",                    // the central creative idea — the big idea everything ladders up to

  "creative_themes": [],                       // the themes / territories the platform explores (5.2) — ≥1

  "emotional_strategy": "",                    // OPTIONAL — the feeling the creative evokes and how (5.2)

  "experience_concepts": [                     // OPTIONAL — creative system & experience concepts (5.5, absorbed Experience Design)
    {
      "concept": "",                          // the concept's name
      "description": ""                       // what it is and how it expresses the platform
    }
  ],

  "channel_creative": [                        // OPTIONAL — channel-specific creative requirements (5.6)
    {
      "channel": "",                          // the channel / medium
      "requirements": ""                      // the creative treatment / requirements for that channel
    }
  ],

  "creative_principles": [],                   // OPTIONAL — creative guardrails / do's that keep execution on platform

  "linked_brand_context": "BRC-<slug>",        // OPTIONAL — the brand promise/pillars + voice/identity it expresses and operates within
  "linked_product": "PRD-<slug>",              // OPTIONAL — the offering this creative is for (product_messaging value pillars it expresses)
  "linked_personas": [],                       // OPTIONAL — PER- ids this creative speaks to
  "linked_campaign_strategy": "CMS-<slug>",    // OPTIONAL — if scoped to a campaign
  "linked_business_context": "BIZ-<slug>",     // OPTIONAL — the owning business
  "source": ""                                 // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"creative_strategy"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `creative_strategy_id` | string | yes | `CRS-<slug>`. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Readable label, usually entity + offering or campaign. |
| `creative_platform` | string | yes | The big idea / creative platform — the single central creative concept everything ladders up to. |
| `creative_themes` | string[] | yes | ≥1. The themes / territories the platform explores (5.2). 2-4 is usually right. |
| `emotional_strategy` | string | no | The emotional approach — the feeling the creative evokes and how it gets there (5.2). |
| `experience_concepts` | object[] | no | The creative system & experience concepts — **the former Experience Design object, absorbed here** (5.5). Each `{ concept, description }`. |
| `experience_concepts[].concept` | string | yes (within entry) | The concept's name — a creative-system element or experience idea. |
| `experience_concepts[].description` | string | yes (within entry) | What it is and how it expresses the platform. |
| `channel_creative` | object[] | no | Channel-specific creative requirements (5.6). Each `{ channel, requirements }`. |
| `channel_creative[].channel` | string | yes (within entry) | The channel / medium (social, OOH, web, email, video, in-store…). |
| `channel_creative[].requirements` | string | yes (within entry) | What the creative must do / look like in that channel. |
| `creative_principles` | string[] | no | Creative guardrails / do's that keep execution on platform. |
| `linked_brand_context` | string | no | `BRC-<slug>` whose brand promise/pillars this expresses and whose voice/identity it operates within. `BRC-PLACEHOLDER-<slug>` ok. |
| `linked_product` | string | no | `PRD-<slug>` of the offering, whose `product_messaging` value pillars this expresses. `PRD-PLACEHOLDER-<slug>` ok. |
| `linked_personas` | string[] | no | `PER-` ids this creative speaks to. `PER-PLACEHOLDER-<slug>` ok. |
| `linked_campaign_strategy` | string | no | `CMS-<slug>` if scoped to a campaign. `CMS-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning business. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`creative_strategy_id` = `CRS-` + a lowercase, hyphen-delimited slug. Scope it to the **entity plus
the offering (or campaign)** the creative direction is for, so strategies stay distinct across a
portfolio:

- IBM watsonx → `CRS-ibm-watsonx` (expresses `BRC-ibm` + `PRD-ibm-watsonx`)
- Wendy's Baconator → `CRS-wendys-baconator` (expresses `BRC-wendys` + `PRD-wendys-baconator`)

If a creative strategy is scoped to a specific campaign rather than the durable offering, name it for
the campaign (`CRS-wendys-baconator-launch`) and set `linked_campaign_strategy`. Keep the id stable
once assigned — downstream Content/Experience objects and the creative brief composer reference it.
Bump `version` on revision.

## Extraction principles

1. **Express the message, don't restate it.** Draw from the message cascade — the Brand Context's
   brand promise/pillars, the Product Context's `product_messaging` value pillars, and the Journey's
   per persona/stage key messages — then decide *how* to express them: the big idea, themes, feeling,
   experience. If a line just repeats a message pillar, it belongs upstream, not here.
2. **One platform, then themes beneath it.** `creative_platform` is the single big idea;
   `creative_themes[]` are the territories it explores. Keep the layers distinct — a theme is an
   angle the platform takes, not a second big idea.
3. **Experience concepts are creative system, absorbed from Experience Design.** Use
   `experience_concepts[]` for the creative system and experiential ideas (signature interactions,
   visual systems, experiential motifs) — this is where the former Experience Design work lives now.
4. **Channel creative is the translation, not a media plan.** `channel_creative[]` captures the
   *creative* requirements per channel (what the creative must do/look like), not flighting, budget,
   or audience targeting — those are Campaign Strategy.
5. **Apply the brand; don't redefine it.** Set `linked_brand_context`; use `creative_principles` and
   `emotional_strategy` for creative-strategy-scoped guidance, not a parallel brand voice.
6. **Don't plan content here.** Content priorities, types, and sequencing are Content Strategy. If a
   sentence is about *which assets to produce and when*, it belongs downstream.
7. **Keep arrays signal-bearing.** A tight set of real themes, concepts, and channel treatments
   beats a long generic list. Resist padding.

## Output rules

- Emit valid JSON (no comments in the actual output — the `jsonc` above is illustrative).
- One object per offering-or-campaign creative direction. Save using the OSMM instance-naming
  convention: `CREATIVE-STRATEGY_<entity-slug>.json` (e.g. `CREATIVE-STRATEGY_ibm-watsonx.json`),
  with an optional instance slug when one entity has multiple creative strategies — uppercase object
  name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The
  `creative_strategy_id` (`CRS-<slug>`) remains the id *inside* the object; it is not the filename.
- Set `linked_brand_context` to the real `BRC-<slug>` if it exists; otherwise use
  `BRC-PLACEHOLDER-<slug>` and tell the user to resolve it. Do the same for `linked_product`
  (`PRD-`), `linked_personas` (`PER-`), `linked_campaign_strategy` (`CMS-`), and
  `linked_business_context` (`BIZ-`).
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin (especially the
  emotional strategy and experience concepts) so they can fill gaps. If you find message content
  ("our pillar is X") note it belongs upstream in the cascade — Brand Context (brand promise/pillars),
  Product Context (`product_messaging`), or the Journey (persona/stage key messages); if you find
  content-plan or media-flighting detail, point the user to Content Strategy / Campaign Strategy
  rather than smuggling it in here.

## Starter prompts

**From a creative brief or creative platform doc:**
> Build an OSMM Creative Strategy Object for [Offering] by [Brand]. Set the big idea
> (`creative_platform`), 2-4 creative themes, and the emotional strategy. Capture any creative
> system / experience concepts in `experience_concepts`, and any channel-specific creative
> requirements in `channel_creative`. Link the Brand Context (`BRC-[brand-slug]`) whose
> promise/pillars it expresses and operates within, and the Product Context
> (`PRD-[offering-slug]`) whose `product_messaging` value pillars it expresses. Leave the content
> plan to Content Strategy.

**From brand campaign work (no Brand/Product Context resolved yet):**
> Build an OSMM Creative Strategy Object for [Brand]/[Offering] from this campaign deck. Capture the
> creative platform, themes, emotional strategy, and any experience concepts; set
> `linked_brand_context` to `BRC-PLACEHOLDER-<slug>` and `linked_product` to
> `PRD-PLACEHOLDER-<slug>`, and flag that the message it expresses should be confirmed against the
> Brand Context (brand promise/pillars), Product Context (`product_messaging`), and Journey
> (persona/stage key messages).

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below
illustrate the shape; both validate against the canonical schema.

### Example 1 — B2B platform creative (IBM watsonx)

Built from IBM's public watsonx brand and "Let's create" campaign work. Expresses the message
cascade — `BRC-ibm`'s brand promise/pillars and `PRD-ibm-watsonx`'s `product_messaging` value
pillars — operates within `BRC-ibm`'s voice, and exercises `experience_concepts` and
`channel_creative`.

```json
{
  "object_type": "creative_strategy",
  "osmm_version": "0.1.0",
  "creative_strategy_id": "CRS-ibm-watsonx",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Creative Strategy",
  "creative_platform": "Put AI to work — show enterprise AI as practical, governed, and already in production, not a sci-fi promise.",
  "creative_themes": [
    "AI for business outcomes, shown through real enterprise work",
    "Trust made visible — governance and control as the hero, not a footnote",
    "Open and yours — your data, your models, your cloud"
  ],
  "emotional_strategy": "Earn confidence, not awe: replace AI anxiety with grounded reassurance. The feeling is 'a capable partner who has done this in regulated industries before' — measured, credible, quietly ambitious rather than hyped.",
  "experience_concepts": [
    {
      "concept": "Proof-in-the-product demos",
      "description": "Lead experiences with working, hands-on demos of watsonx on real enterprise tasks (code, customer service, data governance) so the creative system shows the platform doing the job rather than describing it."
    },
    {
      "concept": "Governance dashboard motif",
      "description": "A recurring visual system built around the watsonx.governance view — drift, bias, and audit signals rendered as clean, legible UI — making 'trust' a tangible, repeatable creative element across formats."
    }
  ],
  "channel_creative": [
    {
      "channel": "Enterprise web / product pages",
      "requirements": "Lead with interactive product demos and architecture clarity; technical depth expected; every claim links to documentation or proof."
    },
    {
      "channel": "LinkedIn / B2B social",
      "requirements": "Customer-proof and analyst-recognition led; thought-leadership tone; no inflated claims — peer-validated outcomes over adjectives."
    }
  ],
  "creative_principles": [
    "Show governed AI in production — never abstract 'AI magic'",
    "Let customer proof and analyst recognition carry the boast",
    "Apply the IBM brand identity from Brand Context; do not invent a parallel visual voice"
  ],
  "linked_brand_context": "BRC-ibm",
  "linked_product": "PRD-ibm-watsonx",
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-it-decision-maker"],
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx and IBM 'Let's create' brand campaign (2024). Message expressed draws from BRC-ibm (brand promise/pillars) and PRD-ibm-watsonx (product_messaging value pillars). Experience concepts and channel requirements inferred from public creative; the linked persona is a placeholder until that object ships."
}
```

### Example 2 — B2C product creative (Wendy's Baconator)

Built from Wendy's public brand and social creative. Expresses the message cascade —
`BRC-wendys`'s brand promise/pillars and `PRD-wendys-baconator`'s `product_messaging` value
pillars — operates within `BRC-wendys`'s voice, and exercises `experience_concepts` and
`channel_creative`.

```json
{
  "object_type": "creative_strategy",
  "osmm_version": "0.1.0",
  "creative_strategy_id": "CRS-wendys-baconator",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's Baconator Creative Strategy",
  "creative_platform": "The flex of the fully-loaded burger — celebrate the unapologetic, six-strips-of-bacon payoff with Wendy's sharp, confident swagger.",
  "creative_themes": [
    "Stacked and proud — the visible meat-and-bacon payoff as the hero shot",
    "Sharp-tongued confidence — Wendy's signature wit aimed at thin, frozen competitors",
    "Worth-it indulgence — premium that still feels smart, not just cheap"
  ],
  "emotional_strategy": "Crave-then-grin: trigger appetite with bold, glistening product, then reward with a smirk. The feeling is bold satisfaction with a wink — indulgent confidence, never apologetic.",
  "experience_concepts": [
    {
      "concept": "The bacon count callout",
      "description": "A recurring creative system that literally counts the six strips on screen / on pack — turning the proof point into a repeatable, ownable visual device across formats."
    }
  ],
  "channel_creative": [
    {
      "channel": "X / social (real-time)",
      "requirements": "Lean into Wendy's sharp, reactive voice; punchy, conversational, willing to spar with competitors; product still the visible hero in any image."
    },
    {
      "channel": "Out-of-home / digital billboards",
      "requirements": "One bold product hero shot, minimal copy, maximum bacon; the payoff legible at a glance and from a distance."
    }
  ],
  "creative_principles": [
    "Make the product the hero — let the visible payoff do the bragging",
    "Be witty, never generic fast-food; apply the Wendy's brand voice from Brand Context",
    "Punch up at quality, not down at price"
  ],
  "linked_brand_context": "BRC-wendys",
  "linked_product": "PRD-wendys-baconator",
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: wendys.com and Wendy's brand social creative (2024). Message expressed draws from BRC-wendys (brand promise/pillars) and PRD-wendys-baconator (product_messaging value pillars). Experience concept and channel requirements inferred from public creative."
}
```
