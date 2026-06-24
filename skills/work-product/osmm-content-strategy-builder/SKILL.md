---
name: osmm-content-strategy-builder
description: >-
  Build the content plan for an offering or campaign as a structured OSMM Content Strategy Object (canonical JSON) — the content goal, the content pillars/themes and the formats under each, the content priorities, the content types/formats in scope, how content is sequenced across the journey/funnel, and the publishing cadence. Inputs include editorial plans, content calendars, content briefs, channel plans, SEO/topic plans, or a content strategist's notes. Use this skill whenever the user wants to structure what content we produce and in what order: "build a content strategy object," "structure our content strategy," lay out a content plan or editorial plan, set content priorities or content pillars, plan a content calendar, define content sequencing, or list content types/formats. This is the content plan — NOT the Creative Strategy (creative direction) and NOT the Journey (the path it supports).
object: Content Strategy Object
object_type: content_strategy
category: Work Product
phase: 5
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Content Strategy Builder

Build a valid **OSMM Content Strategy Object** from any source describing what content a brand
plans to produce for an offering or campaign and in what order.

A Content Strategy Object is the **content plan** — the structured record of *what content we
produce and in what order*: the content goal it drives, the content pillars/themes the plan is
organized around (and the formats under each), what to produce first, the content types in scope,
how content is sequenced across the journey/funnel, and the cadence at which it ships. It is a
Phase 5 Work Product resolving sub-process **5.3** (content priorities, content sequencing).
Downstream production and channel work reference this so every piece ladders up to one plan
instead of being commissioned ad hoc.

This is the lean v0.1 builder. It captures the content plan and its sequencing, and nothing more.
Creative direction (look, feel, emotional strategy), the messages the content conveys, and the
journey mechanics are deliberately out of scope — they belong to neighboring objects; this object
stays at the level of *what gets produced and when*. The message the content conveys cascades from
Brand Context (`brand_promise`/`messaging_pillars`), Product Context (`product_messaging`), and the
Journey's per-persona, per-stage `key_messages`; the questions and topics the content answers live
in the Journey's `persona_tracks[].key_questions`. Reference the Journey via `linked_journey`.

## Boundaries — what this object is and is NOT

Content Strategy sits among two Phase 5 / Phase 4 neighbors that are easy to blur. Keeping the
lines clean is the whole point of giving the content plan its own object:

| Object | Owns | This object's relationship |
|--------|------|----------------------------|
| **Content Strategy** (this) | The content plan: content goal, pillars/themes, formats, priorities, sequencing across the funnel, cadence (5.3) — *what content we produce and in what order*. | — |
| **Creative Strategy** | The creative direction — themes, emotional strategy, look and feel, channel creative requirements (5.2/5.6) — *how it looks and feels*. | **Referenced** via `linked_creative_strategy`. Content is produced *within* that direction; this object does not set look/feel. |
| **Journey** | The orchestrated path — stages, triggers, sequencing of the experience, and per-persona, per-stage `key_messages` and `key_questions` (4.x) — *the path the customer takes, the messages it conveys, and the questions it answers*. | **Referenced** via `linked_journey`. `journey_mapping` maps content *to* journey stages; it does not redesign the path. The messages the content conveys and the questions/topics it answers come *from* the Journey's `persona_tracks`. |

Rules of thumb:

- **This object is the *what and when of content*, not the *how it looks* or *what it says*.** If a
  line is about visual direction or tone, it is Creative Strategy. If it is the message itself or the
  question the content answers, it belongs to the Journey's `persona_tracks` (`key_messages` /
  `key_questions`). Keep this object to the plan.
- **`content_pillars` are themes the content organizes around, not messages or questions.** A content
  pillar is a recurring topic/theme that generates many pieces (with `formats` under it); the
  messages the content conveys cascade from Brand Context, Product Context `product_messaging`, and
  the Journey's `key_messages`, and the questions/topics it answers live in the Journey's
  `key_questions`. Pillars can align with those, but they are different objects.
- **`journey_mapping` maps content onto an existing path; it does not author the path.** Reference
  the Journey via `linked_journey` and place content against its stages. Stage definitions, triggers,
  and cadence of the *experience* live in the Journey Object.
- **Sequencing here is content sequencing (5.3), not journey orchestration.** `sequencing` is the
  order/pacing in which content is produced and released across the funnel — leave trigger logic and
  branching to the Journey.

## The output schema

> **Canonical schema:** [`schemas/content_strategy.schema.json`](../../../schemas/content_strategy.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "content_strategy",         // const — always "content_strategy"
  "osmm_version": "0.1.0",                   // schema version this conforms to
  "content_strategy_id": "CTS-<slug>",       // stable, human-readable id (see ID rules)
  "version": "1.0",                          // instance version; bump on revision
  "status": "draft",                         // draft | proposed | stable | deprecated

  "name": "",                                // readable label (e.g. "IBM watsonx Content Strategy")
  "content_goal": "",                        // the outcome the content plan drives (5.3)

  "content_pillars": [                        // THE SPINE — content themes and the formats under each
    {
      "pillar": "",                          // the content theme's name
      "description": "",                     // what it covers and why it advances the goal
      "formats": []                          // OPTIONAL — formats produced under this pillar
    }
  ],

  "content_priorities": [],                   // OPTIONAL — what to produce first / where to concentrate
  "content_types": [],                        // OPTIONAL — formats/types in scope (blog, video, webinar, …)
  "sequencing": "",                           // OPTIONAL — how content is sequenced across the journey/funnel (5.3)
  "cadence": "",                              // OPTIONAL — publishing frequency / pacing
  "channels": [],                             // OPTIONAL — channels content is published to/through

  "journey_mapping": [                        // OPTIONAL — which content supports which journey stage
    {
      "stage": "",                           // the journey/funnel stage
      "content": ""                          // the content serving that stage
    }
  ],

  "linked_creative_strategy": "CRS-<slug>",   // OPTIONAL — the creative direction this is produced within
  "linked_personas": [],                      // OPTIONAL — PER- ids this content is written for
  "linked_journey": "JNY-<slug>",             // OPTIONAL — the journey whose persona_tracks carry the messages this conveys and the questions it answers
  "linked_campaign_strategy": "CMS-<slug>",   // OPTIONAL — if scoped to a campaign
  "linked_business_context": "BIZ-<slug>",    // OPTIONAL — the owning business
  "source": ""                                // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"content_strategy"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `content_strategy_id` | string | yes | `CTS-<slug>`. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Readable label, usually entity + offering. |
| `content_goal` | string | yes | The outcome the content plan drives — an outcome, not a deliverables list. |
| `content_pillars` | object[] | yes | ≥1. Each `{ pillar, description, formats? }`. 2-5 is usually right. The spine of the plan. |
| `content_pillars[].pillar` | string | yes | The content theme's name. |
| `content_pillars[].description` | string | yes | What the pillar covers and why it advances the content goal. |
| `content_pillars[].formats` | string[] | no | Formats produced under this pillar (blog, video, webinar, …). Omit if thin. |
| `content_priorities` | string[] | no | What to produce first / where to concentrate effort. |
| `content_types` | string[] | no | Formats/types in scope overall. |
| `sequencing` | string | no | How content is sequenced across the journey/funnel (5.3). |
| `cadence` | string | no | Publishing frequency / pacing. |
| `channels` | string[] | no | Channels content is published to/through. |
| `journey_mapping` | object[] | no | Each `{ stage, content }`. Maps content onto journey/funnel stages — does not author the path. |
| `journey_mapping[].stage` | string | yes (within item) | The journey/funnel stage. |
| `journey_mapping[].content` | string | yes (within item) | The content serving that stage. |
| `linked_creative_strategy` | string | no | `CRS-<slug>`. `CRS-PLACEHOLDER-<slug>` ok. |
| `linked_personas` | string[] | no | `PER-` ids this content is written for. `PER-PLACEHOLDER-<slug>` ok. |
| `linked_journey` | string | no | `JNY-<slug>`. The Journey's `persona_tracks` carry the `key_messages` this content conveys and the `key_questions` it answers. `JNY-PLACEHOLDER-<slug>` ok. |
| `linked_campaign_strategy` | string | no | `CMS-<slug>` if scoped to a campaign. `CMS-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning business. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`content_strategy_id` = `CTS-` + a lowercase, hyphen-delimited slug. Scope it to the **entity plus
the offering (or campaign)** the content plan serves, so strategies stay distinct across a
portfolio:

- IBM watsonx → `CTS-ibm-watsonx`
- Wendy's Baconator launch → `CTS-wendys-baconator-launch`

If a content strategy is scoped to a specific campaign rather than the durable offering, name it for
the campaign and set `linked_campaign_strategy`. Keep the id stable once assigned — downstream
production references it. Bump `version` on revision, never the id.

## Extraction principles

1. **Capture *what* and *when*, not *how it looks* or *what it says*.** Visual direction and tone are
   Creative Strategy; the messages the content conveys cascade from Brand Context, Product Context
   `product_messaging`, and the Journey's per-persona, per-stage `key_messages`, and the questions it
   answers live in the Journey's `key_questions`. If a sentence is about look/feel, the wording of a
   claim, or the question a piece answers, it belongs in a linked object, not here.
2. **Pillars are themes that generate many pieces.** Each `content_pillars` entry is a recurring topic
   the plan organizes around, with the `formats` produced under it. Keep pillars distinct from the
   Journey's `key_messages` and `key_questions` — align them, don't duplicate them.
3. **Sequencing is content sequencing (5.3).** `sequencing` describes the order and pacing in which
   content is produced/released across the funnel. Don't smuggle in trigger logic or branching — that
   is the Journey's.
4. **`journey_mapping` places content on an existing path.** Reference the Journey via
   `linked_journey` and map content to its stages. If you find yourself defining stages, entry/exit
   criteria, or triggers, that's the Journey Object, not this one.
5. **Priorities are an emphasis order, not a backlog.** `content_priorities` says what to lead with
   and where to concentrate — keep it short and decisive rather than an exhaustive list.
6. **Keep arrays signal-bearing.** A tight set of real pillars, types, and mappings beats a long
   generic list. 2-5 pillars is usually right; resist padding to a number.

## Output rules

- Emit valid JSON (no comments in the actual output — the `jsonc` above is illustrative).
- One object per offering-or-campaign content plan. Save using the OSMM instance-naming convention:
  `CONTENT-STRATEGY_<entity-slug>.json` (e.g. `CONTENT-STRATEGY_ibm-watsonx.json`), with an optional
  instance slug when one entity has multiple strategies — uppercase object name, underscore join,
  lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The `content_strategy_id`
  (`CTS-<slug>`) remains the id *inside* the object; it is not the filename.
- Set each reference to the real id if it exists; otherwise use the `PLACEHOLDER-` form
  (`CRS-PLACEHOLDER-<slug>`, `PER-PLACEHOLDER-<slug>`, `JNY-PLACEHOLDER-<slug>`,
  `CMS-PLACEHOLDER-<slug>`, `BIZ-PLACEHOLDER-<slug>`) and tell the user to resolve it.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially the
  per-stage `journey_mapping` and `sequencing`) so they can fill gaps. If you find creative direction
  or message/question wording in the source, note it and point the user to the Creative Strategy
  Object or the Journey's `persona_tracks` (`key_messages` / `key_questions`) rather than smuggling
  it into this one.

## Starter prompts

**From an editorial plan / content calendar:**
> Build an OSMM Content Strategy Object for [Offering] by [Brand] from this editorial plan. Set a
> content goal, 2-5 content pillars with the formats under each, the content types in scope, and the
> cadence. Map the priority content to the journey stages and describe how it's sequenced across the
> funnel. Link the Journey it supports (whose `persona_tracks` carry the messages it conveys and the
> questions it answers) and the Creative Strategy it's produced within.

**From a topic/SEO plan (no journey mapped yet):**
> Build an OSMM Content Strategy Object for [Brand]/[Offering] from this topic plan. Capture the
> content pillars, set priorities and cadence, and link the Journey via `linked_journey` (use
> `JNY-PLACEHOLDER-<slug>` if it doesn't exist yet) — the topics/questions this content answers live
> in the Journey's `persona_tracks[].key_questions`. Flag that the journey_mapping is inferred and
> should be confirmed against the Journey Object.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below
illustrate the shape; both validate against the canonical schema.

### Example 1 — B2B platform content plan (IBM watsonx)

Built from IBM's public watsonx content footprint. Organized around enterprise-AI themes, mapped to
a B2B funnel, and linked to the watsonx acquisition Journey (whose persona tracks carry the messages
this conveys and the questions it answers).

```json
{
  "object_type": "content_strategy",
  "osmm_version": "0.1.0",
  "content_strategy_id": "CTS-ibm-watsonx",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Content Strategy",
  "content_goal": "Move enterprise data and AI leaders from awareness to qualified pipeline by making watsonx the trusted reference for putting governed AI into production.",
  "content_pillars": [
    {
      "pillar": "Trusted enterprise AI",
      "description": "Governance, explainability, and IP indemnification — the proof that AI can scale safely in regulated industries.",
      "formats": ["thought-leadership blog", "analyst report", "whitepaper", "webinar"]
    },
    {
      "pillar": "Hybrid-cloud AI in practice",
      "description": "How enterprises run AI on their own governed data across any cloud, without lock-in.",
      "formats": ["solution brief", "reference architecture", "technical blog"]
    },
    {
      "pillar": "Production use cases",
      "description": "Concrete deployments — code generation, customer-service automation, knowledge retrieval — that show watsonx beyond pilots.",
      "formats": ["case study", "demo video", "customer story"]
    }
  ],
  "content_priorities": [
    "Lead with Trusted enterprise AI to clear the governance/compliance objection that gates adoption",
    "Back every claim with a production use case before pushing top-of-funnel reach"
  ],
  "content_types": ["blog", "whitepaper", "webinar", "case study", "video", "solution brief", "analyst report"],
  "sequencing": "Open the funnel with trust and category education, deepen with hybrid-cloud how-to in consideration, then convert with use-case proof and product deep-dives; release pillar anchors quarterly with supporting blog/social between.",
  "cadence": "2-3 long-form assets per month; weekly blog; daily LinkedIn social distribution.",
  "channels": ["IBM.com", "LinkedIn", "email nurture", "webinar platform", "YouTube"],
  "journey_mapping": [
    { "stage": "Awareness", "content": "Thought-leadership blog and analyst reports on trusted, governed enterprise AI" },
    { "stage": "Consideration", "content": "Hybrid-cloud reference architectures, solution briefs, and how-to webinars" },
    { "stage": "Decision", "content": "Production case studies, demo videos, and watsonx component deep-dives" }
  ],
  "linked_creative_strategy": "CRS-PLACEHOLDER-ibm-watsonx",
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-it-decision-maker"],
  "linked_journey": "JNY-PLACEHOLDER-ibm-watsonx-acquisition",
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx content footprint (2024). The messages this conveys and the questions it answers cascade from IBM Brand/Product Context and the watsonx Journey's persona/stage tracks. Creative, journey, and persona links are placeholders until those objects ship."
}
```

### Example 2 — B2C product content plan (Wendy's Baconator launch)

Built from Wendy's public social-led content style. Organized around culturally-fluent food content,
mapped to a B2C funnel, and linked to the deal-savvy craver persona and the Baconator launch Journey
(whose persona tracks carry the messages this conveys and the questions it answers).

```json
{
  "object_type": "content_strategy",
  "osmm_version": "0.1.0",
  "content_strategy_id": "CTS-wendys-baconator-launch",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's Baconator Launch Content Strategy",
  "content_goal": "Drive craving and app-order traffic for the Baconator by flooding social with bold, shareable meat-and-bacon content during the launch window.",
  "content_pillars": [
    {
      "pillar": "Meat-and-bacon hero",
      "description": "Mouth-watering product hero content that makes the two-patty, six-strip payoff impossible to ignore.",
      "formats": ["short-form video", "hero photography", "social post"]
    },
    {
      "pillar": "Sharp social banter",
      "description": "Wendy's signature witty, culturally-fluent replies and posts that turn the launch into a conversation.",
      "formats": ["X/Twitter reply", "meme", "social post"]
    },
    {
      "pillar": "Deal and app nudge",
      "description": "Content that pushes the value angle and the app order as the way to act on the craving.",
      "formats": ["app-promo video", "email", "in-app banner"]
    }
  ],
  "content_priorities": [
    "Front-load hero video in the first launch week to spike craving",
    "Sustain reach with daily social banter rather than more produced assets"
  ],
  "content_types": ["short-form video", "social post", "photography", "email", "meme"],
  "sequencing": "Tease, then a hero-video launch burst, then sustained daily banter and deal/app nudges through the promo window; ramp banter as hero content tapers.",
  "cadence": "Daily social across the launch window; 1-2 produced video drops per week; weekly email.",
  "channels": ["X/Twitter", "Instagram", "TikTok", "Wendy's app", "email"],
  "journey_mapping": [
    { "stage": "Awareness", "content": "Hero product video and bold photography across social" },
    { "stage": "Consideration", "content": "Sharp social banter and craving-driving meme content" },
    { "stage": "Conversion", "content": "App-order promo video, in-app banner, and value/deal email" }
  ],
  "linked_creative_strategy": "CRS-PLACEHOLDER-wendys-baconator",
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_journey": "JNY-PLACEHOLDER-wendys-baconator-launch",
  "linked_campaign_strategy": "CMS-PLACEHOLDER-wendys-baconator-launch",
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: Wendy's social content style (2024). The messages this conveys and the questions it answers cascade from Wendy's Brand/Product Context and the Baconator launch Journey's persona/stage tracks. Creative, journey, and campaign links are placeholders until those objects ship."
}
```
