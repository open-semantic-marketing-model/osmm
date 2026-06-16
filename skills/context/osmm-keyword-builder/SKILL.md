---
name: osmm-keyword-builder
description: >-
  Convert any keyword, topic, or search-intent source into a structured OSMM Keyword Object
  (canonical JSON). Inputs include keyword research exports (Semrush, Ahrefs, Google Keyword
  Planner, Search Console), topic/cluster maps, SERP analyses, People-Also-Ask and AI-overview
  captures, paid-search term reports, or a search strategist's notes. Use this skill whenever the
  user wants to capture a single search term or topic as a reusable Context object — "build a
  keyword object," "structure this keyword/topic," "objectify this search term," "turn this keyword
  research into our format," map intent and journey stage for a term, or capture an AEO/answer-engine
  question. The Keyword Object is OSMM's addressable unit of search demand: one term, its intent, its
  metrics, the personas who search it, and the surfaces (SEO/AEO/paid) it is targeted on. It is NOT
  the Keyword *Strategy* Object — that prioritizes and organizes many keywords into a plan.
object: Keyword Object
object_type: keyword
category: Context Object
phase: 2
wave: 1
osmm_version: 0.1.0
status: draft
---

# OSMM Keyword Builder

Build a valid **OSMM Keyword Object** from any source describing a search term, query, or topic.

A Keyword Object is durable, foundational Context — the structured understanding of **one unit of
search demand**: the term itself, what the searcher wants (intent), where they are in the journey,
how competitive and voluminous it is, the personas who search it, and the surfaces it's optimized
for (organic SEO, answer-engine/AEO, and paid). Campaigns, content, and the Keyword Strategy all
reference these atoms; making each term explicit and addressable means content and agents target the
*same* demand the same way instead of re-deriving it from a spreadsheet each time.

This is the lean v0.1 builder. One object = one term (or one topic). It captures the
marketing-relevant attributes of that term and nothing more. Full rank-tracking histories, raw
crawl data, and per-URL position tables stay in the SEO tool; distill their *decision-relevant*
signal into the fields.

## Boundaries — what this object is and is NOT

| Object | Answers | Example |
|--------|---------|---------|
| **Keyword** (this) | What is this *one* term — its intent, metrics, personas, surfaces? | "hybrid cloud" |
| **Keyword Strategy** (`osmm-keyword-strategy-builder`, B09) | Across many terms, what do we *prioritize*, and how do topics map to the journey and to AEO/SEO targets? | The plan over a portfolio of Keyword Objects |
| **Persona** | *Who* searches the term? | Enterprise IT decision-maker |

Rules of thumb:

- **One term per object.** A topic cluster is modeled as a parent topic (a Keyword Object with
  `term_type: topic`) plus its member terms, linked via `parent_topic` / `related_keywords` — not
  one blended object.
- **Keyword Object is the atom; Keyword Strategy is the plan.** Prioritization, intent distribution
  across a portfolio, and topic-to-journey *targets* are the Strategy's job. The per-term
  `journey_stage` and `search_intent` here are attributes of the atom, not the portfolio plan.
- **SEO and AEO are both first-class.** `optimization_channels` and the `questions` field make a
  term's answer-engine (AEO) relevance explicit — the conversational/question form that AI overviews
  and voice surfaces reward — alongside classic organic SEO and paid.

## The output schema

> **Canonical schema:** [`schemas/keyword.schema.json`](../../../schemas/keyword.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "keyword",             // const — always "keyword"
  "osmm_version": "0.1.0",              // schema version this conforms to
  "keyword_id": "KW-<slug>",            // stable, human-readable id (see ID rules)
  "version": "1.0",                     // instance version; bump on revision
  "status": "draft",                    // draft | proposed | stable | deprecated

  "term": "",                           // the keyword / topic / query phrase, as searched
  "term_type": "",                      // controlled enum — keyword | topic | question
  "branded": false,                     // does the term include the brand or product name?
  "search_intent": "",                  // controlled enum — informational | navigational | commercial | transactional
  "intent_notes": "",                   // OPTIONAL — what the searcher actually wants; nuance on the intent

  "journey_stage": "",                  // OPTIONAL — controlled enum — awareness | consideration | decision | retention | advocacy
  "optimization_channels": [],          // surfaces this term is targeted on — enum array: seo | aeo | paid_search | social
  "serp_features": [],                  // OPTIONAL — enum array: featured_snippet | people_also_ask | ai_overview | knowledge_panel | local_pack | shopping | video | image_pack

  "metrics": {                          // OPTIONAL — directional and banded; never presented as precise vendor truth
    "monthly_search_volume": "",        // order-of-magnitude band: "<100" | "100-1K" | "1K-10K" | "10K-100K" | "100K+"
    "keyword_difficulty": "",           // low | medium | high  (or a 0-100 score if a tool provides one)
    "cpc_usd": "",                      // OPTIONAL — typical paid cost-per-click band, if paid is in play
    "trend": ""                         // OPTIONAL — rising | stable | declining | seasonal
  },

  "variations": [],                     // close variants / synonyms / common phrasings of the same intent
  "questions": [],                      // OPTIONAL — natural-language questions for this term (AEO / People-Also-Ask / voice)
  "parent_topic": "",                   // OPTIONAL — KW- id of the topic cluster this term rolls up to (placeholder ok)
  "related_keywords": [],               // OPTIONAL — KW- ids of semantically related terms (clustering)

  "linked_personas": [],                // PER- ids of the personas who search this term (placeholder ok)
  "linked_business_context": "",        // OPTIONAL — BIZ- id whose search strategy this term belongs to (placeholder ok)
  "source": ""                          // one line: what source(s)/tool this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"keyword"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `keyword_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `term` | string | yes | The phrase as a person searches it. Lowercase unless the term is a proper noun. |
| `term_type` | enum | yes | `keyword` (a query), `topic` (a cluster theme), or `question` (a natural-language query). |
| `branded` | boolean | yes | `true` if the term contains the brand/product name. Drives SEO vs. demand-capture treatment. |
| `search_intent` | enum | yes | The classic four — see vocabulary. Pick the single dominant intent. |
| `intent_notes` | string | no | One line on what the searcher is really after. |
| `journey_stage` | enum | no | Where this demand sits in the funnel. See vocabulary. |
| `optimization_channels` | enum[] | yes | Which surfaces the term is targeted on. At least one. See vocabulary. |
| `serp_features` | enum[] | no | Observed SERP features — what winning the term actually requires. |
| `metrics` | object | no | Banded, directional signal. Omit the block, or any sub-field, when unknown. |
| `metrics.monthly_search_volume` | string | no | Order-of-magnitude band, not a precise figure. |
| `metrics.keyword_difficulty` | string | no | `low` \| `medium` \| `high`, or a 0-100 score if a tool provides it. |
| `metrics.cpc_usd` | string | no | Paid cost-per-click band; include only if paid is in play. |
| `metrics.trend` | enum | no | `rising` \| `stable` \| `declining` \| `seasonal`. |
| `variations` | string[] | no | Close variants and synonyms that share this intent (don't create separate objects for these). 2-8. |
| `questions` | string[] | no | The question forms of this demand — for AEO, People-Also-Ask, and voice. Strongly recommended for `term_type: topic`/`question`. |
| `parent_topic` | string | no | `KW-` id of the topic this rolls up to. `KW-PLACEHOLDER-<slug>` ok. |
| `related_keywords` | string[] | no | `KW-` ids of semantically related terms (the cluster). |
| `linked_personas` | string[] | no | `PER-` ids of who searches it. Use `PER-PLACEHOLDER-<slug>` until built. Realizes the Keyword → Persona edge. |
| `linked_business_context` | string | no | `BIZ-` id whose search strategy this belongs to. `BIZ-PLACEHOLDER-<slug>` ok; omit for a brand-agnostic term. |
| `source` | string | no | One line. Tool/source provenance and approximate date. |

## Controlled vocabularies

Stored values are snake_case tokens mapped to human-readable labels (per `CONVENTION.md` →
"Controlled vocabularies"). Pick the single closest value for scalar enums.

**`term_type`**

| Stored value | Label | Use when |
|---|---|---|
| `keyword` | Keyword | A discrete search query — "hybrid cloud pricing". |
| `topic` | Topic | A cluster theme that groups many queries — "hybrid cloud". |
| `question` | Question | A natural-language question — "what is hybrid cloud?". AEO-relevant. |

**`search_intent`** — the classic four. Pick the dominant one; note secondary intent in `intent_notes`.

| Stored value | Label | The searcher wants to&hellip; |
|---|---|---|
| `informational` | Informational | Learn / understand something. |
| `navigational` | Navigational | Reach a specific site, brand, or page. |
| `commercial` | Commercial investigation | Compare options before deciding. |
| `transactional` | Transactional | Act now — buy, sign up, visit, order. |

**`journey_stage`**: `awareness` · `consideration` · `decision` · `retention` · `advocacy`.

**`optimization_channels`** (array — a term can be targeted on several):

| Stored value | Label | Surface |
|---|---|---|
| `seo` | Organic SEO | Classic organic ranking. |
| `aeo` | Answer-Engine Optimization | AI overviews, featured snippets, voice, generative answers. |
| `paid_search` | Paid Search | SEM / PPC bidding. |
| `social` | Social Search | In-platform search (TikTok, YouTube, Pinterest, etc.). |

**`serp_features`** (array): `featured_snippet` · `people_also_ask` · `ai_overview` ·
`knowledge_panel` · `local_pack` · `shopping` · `video` · `image_pack`.

## ID rules

`keyword_id` = `KW-` + a lowercase, hyphen-delimited slug derived from the term. The slug is the
term itself, not a brand (keywords are often shared demand, not brand-owned):

- "hybrid cloud" → `KW-hybrid-cloud`
- "fast food deals near me" → `KW-fast-food-deals-near-me`
- "what is hybrid cloud" → `KW-what-is-hybrid-cloud`

For a branded term, include the brand in the slug (`KW-ibm-watsonx`) and set `branded: true`. Keep
ids stable; on revision bump `version`, never the id.

## Extraction principles

1. **One intent per object.** If a "term" actually spans two intents (informational *and*
   transactional), it's two queries — model the dominant one and capture the other phrasing in
   `variations` or split into a second object.
2. **Don't manufacture metrics.** Use bands and only when you have a real source. A made-up volume or
   difficulty is worse than an omitted one — leave the sub-field out and say so.
3. **Branded vs. non-branded changes everything.** Branded terms are demand you already own (defend
   cheaply); non-branded terms are demand you compete for. Get `branded` right — it drives strategy
   downstream.
4. **Make AEO explicit.** If the term has a natural question form or triggers AI overviews / PAA,
   populate `questions` and add `aeo` to `optimization_channels`. Answer-engine demand is easy to
   miss when you only look at head-term volume.
5. **`serp_features` is "what winning requires."** A term with a `local_pack` is won differently than
   one with a `featured_snippet`. Capture observed features so content targets the right format.
6. **Personas are who, not what.** `linked_personas` connects the term to the people who search it —
   the bridge that lets a campaign resolve audience ↔ demand. Use placeholders until personas exist.
7. **Cluster with ids, don't nest.** Relate terms via `parent_topic` and `related_keywords` (ids),
   keeping each term addressable — never embed a list of full keyword objects inside another.
8. **Keep arrays signal-bearing.** A handful of strong variations/questions beats an exhaustive dump
   from a tool.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per term. Save using the OSMM instance-naming convention:
  `KEYWORD_<term-slug>.json` (e.g. `KEYWORD_hybrid-cloud.json`) — uppercase object name, underscore
  join, lowercase term slug. See `CONVENTION.md` → "Instance file naming". The `keyword_id`
  (`KW-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you extracted vs. inferred, flag any metric you could not source, and
  note whether the term has untapped AEO (question) potential.

## Starter prompts

**From keyword research:**
> Build OSMM Keyword Objects from this [Semrush/Ahrefs/Search Console] export for [Company]. For each
> term capture intent, journey stage, banded volume/difficulty, SERP features, and which surfaces
> (SEO/AEO/paid) it's targeted on. Flag branded vs. non-branded and link the personas who search it.

**From a topic / AEO angle:**
> Build an OSMM Keyword Object for the topic "[topic]" for [Company]. Set `term_type: topic`, capture
> the natural-language `questions` people ask (for AEO / AI overviews), the member `related_keywords`,
> and the personas it serves.

---

## Worked examples

### Example 1 — B2B non-branded topic (IBM · "hybrid cloud")

Input: keyword research export + SERP/AI-overview capture for IBM's hybrid cloud topic.

```json
{
  "object_type": "keyword",
  "osmm_version": "0.1.0",
  "keyword_id": "KW-hybrid-cloud",
  "version": "1.0",
  "status": "draft",
  "term": "hybrid cloud",
  "term_type": "topic",
  "branded": false,
  "search_intent": "informational",
  "intent_notes": "Mostly top-of-funnel understanding, but a meaningful commercial slice compares vendors and platforms; the topic spans awareness into consideration.",
  "journey_stage": "consideration",
  "optimization_channels": ["seo", "aeo"],
  "serp_features": ["ai_overview", "featured_snippet", "people_also_ask"],
  "metrics": {
    "monthly_search_volume": "10K-100K",
    "keyword_difficulty": "high",
    "trend": "stable"
  },
  "variations": [
    "hybrid cloud computing",
    "hybrid cloud architecture",
    "hybrid cloud solutions",
    "what is hybrid cloud"
  ],
  "questions": [
    "What is hybrid cloud?",
    "How does hybrid cloud work?",
    "Hybrid cloud vs. multicloud — what's the difference?",
    "What are the benefits of a hybrid cloud strategy?"
  ],
  "parent_topic": "",
  "related_keywords": ["KW-PLACEHOLDER-multicloud", "KW-PLACEHOLDER-red-hat-openshift", "KW-PLACEHOLDER-hybrid-cloud-security"],
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-it-decision-maker"],
  "linked_business_context": "BIZ-ibm",
  "source": "Keyword research export + Google AI-overview/SERP capture (2024)"
}
```

---

### Example 2 — B2C non-branded transactional/local (Wendy's · "fast food deals near me")

Input: keyword research + mobile SERP capture for Wendy's value/deals demand.

```json
{
  "object_type": "keyword",
  "osmm_version": "0.1.0",
  "keyword_id": "KW-fast-food-deals-near-me",
  "version": "1.0",
  "status": "draft",
  "term": "fast food deals near me",
  "term_type": "keyword",
  "branded": false,
  "search_intent": "transactional",
  "intent_notes": "High-intent, mobile-dominant, local: the searcher wants a deal they can act on right now at a nearby location.",
  "journey_stage": "decision",
  "optimization_channels": ["seo", "paid_search"],
  "serp_features": ["local_pack", "people_also_ask", "ai_overview"],
  "metrics": {
    "monthly_search_volume": "100K+",
    "keyword_difficulty": "medium",
    "cpc_usd": "$0.50-1.50",
    "trend": "rising"
  },
  "variations": [
    "fast food deals",
    "cheap fast food near me",
    "best fast food deals today",
    "fast food coupons"
  ],
  "questions": [
    "What fast food deals are near me right now?",
    "Which fast food app has the best deals?"
  ],
  "parent_topic": "KW-PLACEHOLDER-fast-food-value",
  "related_keywords": ["KW-PLACEHOLDER-baconator", "KW-PLACEHOLDER-wendys-app-deals"],
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_business_context": "BIZ-wendys",
  "source": "Keyword research export + mobile SERP capture (2024)"
}
```
