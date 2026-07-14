---
name: osmm-business-context-builder
description: >-
  Convert any business source into a structured OSMM Business Context Object (canonical JSON).
  Inputs include pitch decks, investor presentations, brand strategy documents, discovery call
  transcripts, annual reports, website copy, company one-pagers, competitive briefs, or a
  strategist's raw notes. Use this skill whenever the user wants to turn a business document,
  discovery transcript, or strategy asset into a standardized Business Context Object, "build
  a business context object," "objectify this company," "structure this client context," extract
  business attributes into JSON, or prepare structured context for downstream AI workflows.
  Trigger even if the user only says "turn this into our format," "structure this company
  context," or hands over a business asset and asks what to do with it.
object: Business Context Object
object_type: business_context
category: Context Object
phase: 1
wave: 2
osmm_version: 0.1.0
status: draft
---

# OSMM Business Context Builder

Build a valid **OSMM Business Context Object** from any source describing a company and its marketing context.

A Business Context Object is durable, foundational Context — the structured understanding of who a business is, what it sells, who it competes with, and what marketing is trying to accomplish for it. Every downstream Work Product object — Marketing Strategy, Campaign Strategy, Creative Strategy — implicitly references this foundation. Making it explicit and structured means agents and humans operate against the same baseline instead of each reinventing it from scratch.

This is the lean v0.1 builder. It captures the essential business facts a marketing workflow needs and nothing more. Financial details, org charts, and operational data that don't inform marketing decisions are deliberately out of scope — distill their *marketing implications* into the fields instead.

**Key difference from Persona:** a Persona Object is typically distilled from a single artifact (a persona deck). Business Context usually requires **synthesis across multiple sources** — a pitch deck for positioning, a website for product detail, a discovery transcript for strategic priorities, public sources for competitive context. When multiple sources are available, synthesize across all of them rather than transcribing any one.

## The output schema

> **Canonical schema:** [`schemas/business_context.schema.json`](../../schemas/business_context.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "business_context",    // const — always "business_context"
  "osmm_version": "0.1.0",              // schema version this conforms to
  "business_id": "BIZ-<slug>",          // stable, human-readable id (see ID rules)
  "version": "1.0",                     // instance version; bump on revision
  "status": "draft",                    // draft | proposed | stable | deprecated

  "name": "",                           // company name
  "industry": "",                       // primary industry / sector
  "business_type": "",                  // controlled enum — see vocabulary below
  "founded": "",                        // year founded (string; omit if unknown)
  "hq_location": "",                    // city, state/country (omit if irrelevant)

  "description": "",                    // 2-3 sentences: what the company does, who it serves, how it's distinctive

  "products_and_services": [],          // key offerings — what they actually sell (names/types, not brochure copy)
  "value_proposition": "",              // the core "why us" — what they claim sets them apart
  "target_customers": [],               // the customer types this business serves (plain descriptions; Persona/Audience objects carry the structure)
  "revenue_model": "",                  // how the business makes money (e.g. subscription, DTC e-commerce, B2B SaaS, licensing)
  "scale_context": {                    // OPTIONAL — marketing-relevant scale signal; never a precise financial filing
    "revenue_range": "",                // order-of-magnitude band: e.g. "<$10M", "$10–50M", "$50–250M", "$250M–1B", "$1–10B", "$10B+"
    "revenue_mix_notes": "",            // OPTIONAL — segment or channel mix if it shapes marketing's mandate
    "growth_trajectory": ""            // OPTIONAL — directional characterization (e.g. "mid-single digit growth; double-digit software growth")
  },
  "business_model_notes": "",           // OPTIONAL — anything structurally distinctive about how the business operates

  "market_position": "",                // where they sit in the market: challenger, category leader, premium niche, etc.
  "competitors": [],                    // primary competitive set (names only; competitive strategy lives elsewhere)
  "competitive_differentiators": [],    // what makes them meaningfully different from competitors — grounded in evidence

  "marketing_objectives": [],           // what marketing is trying to accomplish for this business right now
  "marketing_challenges": [],           // the structural or situational obstacles marketing faces
  "strategic_priorities": [],           // the broader business priorities that shape marketing's mandate

  "brand_tone_notes": "",               // OPTIONAL — brief characterization of brand voice/tone if evident in sources
  "key_markets": [],                    // OPTIONAL — geographies or segments that matter (if not obvious from description)

  "linked_brand_context": "",           // id of the Brand Context Object for this business (placeholder ok)
  "source": ""                          // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"business_context"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `business_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | |
| `industry` | string | yes | Use plain language, not a taxonomy code. |
| `business_type` | enum | yes | Controlled vocabulary — see below. |
| `founded` | string | no | Year as string. Omit if unknown and not relevant. |
| `hq_location` | string | no | Omit if not provided or not relevant to marketing context. |
| `description` | string | yes | 2-3 sentences. The concise "what/who/how" — distinct from value proposition (which is claim-oriented). |
| `products_and_services` | string[] | yes | What they actually sell. Names/types, not marketing copy. 3-10 items. |
| `value_proposition` | string | yes | One sentence: the core claim of differentiation. Extract from source if stated; synthesize from evidence if not. |
| `target_customers` | string[] | yes | Plain descriptions of who they serve. Structure lives in linked Persona/Audience objects. |
| `revenue_model` | string | yes | How the business makes money. One phrase or sentence. |
| `scale_context` | object | no | Marketing-relevant scale signal. Use `revenue_range` as an order-of-magnitude band, not a precise figure. `revenue_mix_notes` and `growth_trajectory` are optional sub-fields — include only when they directly inform the marketing mandate. Omit the whole block for early-stage or private companies where revenue isn't known. |
| `business_model_notes` | string | no | Structural distinctives worth noting (e.g. vertically integrated supply chain, marketplace model, franchise). |
| `market_position` | string | yes | Plain characterization: category leader, challenger, premium niche, volume player, etc. |
| `competitors` | string[] | yes | Names of primary competitors. 3-8. Competitive strategy lives in other objects. |
| `competitive_differentiators` | string[] | yes | What makes them meaningfully different — grounded in what the source actually claims or evidences. |
| `marketing_objectives` | string[] | yes | What marketing is actively trying to accomplish. Specific > generic. |
| `marketing_challenges` | string[] | yes | Structural or situational obstacles. The "hard parts." |
| `strategic_priorities` | string[] | yes | The broader business priorities shaping marketing's mandate. |
| `brand_tone_notes` | string | no | Brief characterization if tone/voice is evident and relevant. Omit if thin. Full brand identity lives in the Brand Context Object. |
| `key_markets` | string[] | no | Geographies or segments if the business is not obviously single-market. |
| `linked_brand_context` | string | no | Id of the Brand Context Object. Use `BRC-PLACEHOLDER-<slug>` if none exists yet. |
| `source` | string | no | One line. Document-level provenance and approximate date. |

## Business type vocabulary

`business_type` is a controlled, governed enum — a stored snake_case token that maps to a human-readable label.

| Stored value | Label |
|---|---|
| `b2c` | B2C |
| `b2b` | B2B |
| `b2b2c` | B2B2C |
| `dtc` | Direct-to-Consumer |
| `marketplace` | Marketplace |
| `saas` | SaaS |
| `enterprise_software` | Enterprise Software |
| `media` | Media / Publishing |
| `nonprofit` | Nonprofit |
| `professional_services` | Professional Services |
| `retail` | Retail |
| `ecommerce` | E-commerce |

Pick the single closest value. For businesses that span types (e.g. a DTC brand that also sells wholesale), choose the dominant model and note the nuance in `business_model_notes`.

## Multi-source synthesis

Unlike Persona, Business Context is routinely built from multiple sources with different fidelity:

- **Pitch deck / investor presentation** — best source for positioning, differentiation, and strategic priorities. Often overstates competitive advantages; calibrate.
- **Website / product pages** — best source for products/services and current value proposition. Tends toward marketing copy; distill to substance.
- **Discovery transcript** — best source for marketing objectives and challenges as actually stated by stakeholders. Raw and honest — weight this highly.
- **Annual report / earnings materials** — best source for market position and competitive context at scale. May lag current strategy.
- **Public enrichment (news, Crunchbase, LinkedIn)** — useful for founding date, HQ, funding stage, competitive set. Treat as directional, not authoritative.

When sources conflict, **weight the discovery transcript most heavily for objectives and challenges** (it's what they actually said), and the pitch/website for positioning claims. Note significant conflicts in `business_model_notes` or `source`.

## ID rules

`business_id` = `BIZ-` + a lowercase, hyphen-delimited slug derived from the company name. Keep it stable: once assigned, downstream objects reference it.

- Acme Corp → `BIZ-acme`
- IBM → `BIZ-ibm`
- Acme Financial Services → `BIZ-acme-financial`

## Extraction principles

1. **Synthesize across sources, don't transcribe any one.** The quality signal in a multi-source build is whether the output resolves tensions between sources (pitch deck claims vs. discovery transcript realities) into a coherent structured picture.
2. **Extract before you infer.** Pull what sources actually state. Most business assets state products, competitors, and value propositions fairly directly.
3. **Infer conservatively, flag gaps.** `marketing_challenges` and `competitive_differentiators` are often the hardest to extract cleanly — implied by what they emphasize and what they avoid. Infer from adjacent evidence; flag thin areas.
4. **`marketing_objectives` ≠ `strategic_priorities`.** Strategic priorities are business-level (grow in new segments, defend margin, expand internationally). Marketing objectives are what marketing is doing about them (drive trial in X segment, increase brand consideration, grow organic acquisition). Both belong here; keep them in the right bucket.
5. **`value_proposition` is a single synthesized claim.** Not a list of features. One sentence that captures the core "why us" — extract from source if clearly stated, synthesize if implicit.
6. **`competitive_differentiators` must be grounded.** Avoid generic claims ("great quality," "customer focus") unless the source provides evidence for them. If the source only asserts without evidence, note that in the field: "Claims [X]; evidence thin in source materials."
7. **`description` is neutral and factual.** The value proposition is where the claim lives; the description should be something a neutral observer would write, not marketing copy.
8. **`target_customers` is a bridge, not a destination.** Plain descriptions that point to the human segments — the structured treatment lives in linked Persona and Audience objects. Don't over-elaborate here.
9. **Keep arrays to signal-bearing items.** 3-8 items per array is usually right. Resist padding to hit a number.
10. **One object per business entity.** If a conglomerate has distinct business units with different marketing mandates, consider a separate object per unit (with a shared parent reference in `business_model_notes`).

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per business entity. Save using the OSMM instance-naming convention: `BUSINESS-CONTEXT_<entity-slug>.json` (e.g. `BUSINESS-CONTEXT_ibm.json`) — uppercase object name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The `business_id` (`BIZ-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin in the source so they can fill gaps.
- Note which sources were available and which fields would benefit from additional source material.

## Starter prompts

Use these as your starting point when invoking the builder. Swap in the company name and available sources — the prompt does the sourcing setup so you don't have to reconstruct it each time.

**Public company:**
> Build an OSMM Business Context Object for [Company Name] ([TICKER]). Use their most recent 10-K for business description, competitive landscape, and risk factors; their most recent earnings call transcript for current strategic priorities and challenges; and their IR site or Investor Day deck if available for positioning. Supplement with website copy for products and value proposition.

**Private company:**
> Build an OSMM Business Context Object for [Company Name]. Sources available: [list what you have — e.g. pitch deck, website, discovery transcript, one-pager]. Weight the discovery transcript most heavily for marketing objectives and challenges; use the pitch deck for positioning and differentiation claims; supplement with website for products and services.

---

## Worked examples

### Example 1 — B2C consumer brand (fictional)

Input: a website, a brand one-pager, and discovery call notes for a fictional home goods company.

```json
{
  "object_type": "business_context",
  "osmm_version": "0.1.0",
  "business_id": "BIZ-acme-wile-e-coyote-corp",
  "version": "1.0",
  "status": "draft",
  "name": "ACME Wile E. Coyote Corp",
  "industry": "Consumer goods / home and outdoor",
  "business_type": "b2c",
  "founded": "1949",
  "hq_location": "Desert Springs, AZ",
  "description": "ACME Wile E. Coyote Corp is a direct-to-consumer brand selling household, outdoor, and problem-solving products to everyday consumers. The company is known for its broad catalog of inventive gadgets and gear, sold primarily through its own e-commerce channel and select retail partners. It targets value-oriented buyers who want creative solutions to everyday challenges.",
  "products_and_services": [
    "Outdoor and adventure gear",
    "Home problem-solving gadgets",
    "Seasonal and novelty product lines",
    "Extended warranty and support plans"
  ],
  "value_proposition": "Ingenious products that solve real problems — built for people who refuse to give up.",
  "target_customers": [
    "Value-oriented adult consumers seeking practical household solutions",
    "Outdoor enthusiasts looking for gear that performs under pressure",
    "Gift buyers drawn to inventive, novelty-adjacent products"
  ],
  "revenue_model": "E-commerce (DTC) and wholesale retail; supplemented by warranty and service plans",
  "scale_context": {
    "revenue_range": "$50–250M"
  },
  "market_position": "Mid-market challenger; strong brand recognition; competes on product breadth and personality",
  "competitors": ["As Seen on TV brands", "Harbor Freight", "Amazon Basics", "Sharper Image"],
  "competitive_differentiators": [
    "Distinctive brand personality with high unaided awareness in target segments",
    "Broad catalog depth gives consumers a one-stop destination for problem-solving products",
    "Loyal repeat buyer base driven by product reliability and brand affinity"
  ],
  "marketing_objectives": [
    "Grow DTC e-commerce share vs. wholesale channel",
    "Increase repeat purchase rate among existing buyers",
    "Expand brand consideration among 25–44 homeowner segment"
  ],
  "marketing_challenges": [
    "Brand awareness skews toward an aging cohort; limited resonance with younger buyers",
    "Product breadth creates positioning diffusion — hard to own a single category narrative",
    "Rising customer acquisition costs in paid search and social"
  ],
  "strategic_priorities": [
    "Shift revenue mix toward higher-margin DTC",
    "Develop a content and community strategy to deepen brand engagement",
    "Rationalize the product catalog to improve margin and marketing focus"
  ],
  "brand_tone_notes": "Clever, optimistic, and slightly self-aware — the brand leans into its own mythology without taking itself too seriously",
  "linked_brand_context": "BRC-PLACEHOLDER-acme-wile-e-coyote-corp",
  "source": "ACME brand one-pager, acmecorp.com, discovery call notes (Q1 2025)"
}
```

---

### Example 2 — Large public company (IBM)

Input: IBM 2023 Annual Report, Q4 2023 earnings call transcript, ibm.com.

```json
{
  "object_type": "business_context",
  "osmm_version": "0.1.0",
  "business_id": "BIZ-ibm",
  "version": "1.0",
  "status": "draft",
  "name": "IBM",
  "industry": "Enterprise technology / hybrid cloud and AI",
  "business_type": "enterprise_software",
  "founded": "1911",
  "hq_location": "Armonk, NY",
  "description": "IBM is a global enterprise technology company focused on hybrid cloud infrastructure and AI-powered business automation. Following the 2021 spinoff of its managed infrastructure business (Kyndryl), IBM has repositioned around software and consulting, with Red Hat as its hybrid cloud platform anchor. It serves large enterprises and governments across more than 175 countries.",
  "products_and_services": [
    "Red Hat OpenShift and hybrid cloud platform",
    "IBM watsonx AI and data platform",
    "IBM Cloud",
    "IBM Consulting (strategy, technology, and operations services)",
    "IBM Z mainframe systems and storage",
    "Automation software (IBM Business Automation, AIOps)"
  ],
  "value_proposition": "The hybrid cloud and AI platform built for enterprise-grade security, compliance, and scale — so organizations can modernize without rearchitecting everything.",
  "target_customers": [
    "Large enterprise IT and technology buyers (CIO, CTO, infrastructure leads)",
    "Line-of-business executives driving AI and automation initiatives (COO, CFO, CMO)",
    "Government and regulated-industry organizations requiring security and compliance at scale",
    "Mid-market companies scaling on Red Hat open-source infrastructure"
  ],
  "revenue_model": "Software licensing and subscription (recurring); consulting and services engagements; hardware sales (mainframe, storage)",
  "scale_context": {
    "revenue_range": "$10B+",
    "revenue_mix_notes": "~45% software, ~33% consulting, ~15% infrastructure (hardware/mainframe). Software is the growth engine; consulting supports platform adoption.",
    "growth_trajectory": "Mid-single digit overall growth; double-digit growth in software; consulting growing modestly; infrastructure declining as mix shifts"
  },
  "business_model_notes": "Post-Kyndryl spinoff, IBM operates as a software-led, consulting-amplified model. Consulting is a platform adoption flywheel — it deploys Red Hat and watsonx rather than competing as a standalone services business. Acquisition strategy (HashiCorp, Apptio, others) is building out the hybrid cloud and FinOps platform.",
  "market_position": "Established leader in enterprise hybrid cloud and mainframe; challenger in AI platform vs. hyperscalers; strong position in regulated industries",
  "competitors": ["Microsoft (Azure + Copilot)", "AWS", "Google Cloud", "Accenture", "Salesforce", "ServiceNow"],
  "competitive_differentiators": [
    "Red Hat is the dominant open-source enterprise Linux and Kubernetes platform — embedded in most Fortune 500 hybrid environments",
    "Mainframe franchise provides locked-in, high-margin revenue and unmatched security/compliance credibility in regulated industries",
    "watsonx positions IBM as an enterprise-safe AI alternative to hyperscaler models — with governance, explainability, and data privacy as differentiators",
    "Consulting arm accelerates platform adoption in ways pure-software competitors cannot match"
  ],
  "marketing_objectives": [
    "Drive watsonx platform consideration among enterprise AI buyers alongside hyperscaler alternatives",
    "Grow Red Hat adoption in hybrid cloud modernization deals",
    "Expand IBM Consulting pipeline tied to AI and automation transformation engagements",
    "Strengthen brand relevance with a younger generation of enterprise technology buyers"
  ],
  "marketing_challenges": [
    "Brand perception lag — IBM is associated with legacy tech by buyers who don't track its portfolio evolution",
    "Competing for AI mindshare against AWS, Microsoft, and Google who have larger developer and consumer brand presence",
    "Complex portfolio makes it hard to lead with a single, clear narrative across segments",
    "Consulting and software go-to-market motions require tight alignment to avoid channel conflict"
  ],
  "strategic_priorities": [
    "Grow software revenue to represent the majority of total revenue",
    "Establish watsonx as the enterprise AI platform of record for regulated industries",
    "Deepen Red Hat ecosystem and partner network to extend hybrid cloud reach",
    "Continue selective M&A to fill hybrid cloud and automation platform gaps"
  ],
  "brand_tone_notes": "Authoritative and pragmatic — IBM leads with business outcomes and enterprise credibility rather than aspiration or disruption narrative",
  "key_markets": ["North America", "Europe", "Asia-Pacific", "regulated industries globally (financial services, healthcare, government)"],
  "linked_brand_context": "BRC-PLACEHOLDER-ibm",
  "source": "IBM 2023 Annual Report, Q4 2023 earnings call transcript, ibm.com (2024)"
}
```
