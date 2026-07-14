---
name: osmm-product-context-builder
description: >-
  Convert any product, service, or solution source into a structured OSMM Product Context Object
  (canonical JSON). Inputs include product pages, datasheets, solution briefs, sales decks, spec
  sheets, menu/SKU descriptions, demo scripts, analyst write-ups, or a product marketer's notes.
  Use this skill whenever the user wants to capture what an offering *is* — its features, how it
  works, its benefits, and its product-level messaging — as a reusable Context object: "build a
  product context object," "structure this product," "objectify our solution," "capture the
  product details," extract a product/service/solution into JSON, or prepare structured product
  context for downstream campaigns, messaging, and offers. This object describes the *thing being
  marketed* — it is NOT the Offer (the value exchange/CTA) and NOT the Business Context (the
  company). Trigger even if the user only says "turn this datasheet into our format" or hands over
  a product brief and asks what to do with it.
object: Product Context Object
object_type: product_context
category: Context Object
phase: 1
wave: 2
osmm_version: 0.1.0
status: draft
---

# OSMM Product Context Builder

Build a valid **OSMM Product Context Object** from any source describing a product, service, or
solution that a business markets.

A Product Context Object is durable, foundational Context — the structured understanding of **the
thing being marketed**: what it is, what it does, how it works, what the customer gets, and the
product-level messaging that carries it — **layer 2 of the message cascade** (brand → product →
persona/journey). Campaigns, creative, content, journeys, and offers all reference an offering;
making that offering explicit and structured means agents and humans frame the *same* product the
same way instead of each re-deriving it from a datasheet.

This is the lean v0.1 builder. It captures the marketing-relevant substance of an offering and
nothing more. Engineering specs, internal roadmaps, and operational detail that don't inform
marketing decisions are out of scope — distill their *marketing implications* into the fields
instead.

## Boundaries — what this object is and is NOT

Product Context sits between two neighbors that are easy to confuse. Keeping the lines clean is the
whole point of giving the offering its own object:

| Object | Answers | Example (IBM) | Example (Wendy's) |
|--------|---------|---------------|-------------------|
| **Business Context** | Who is the *company*? | IBM | Wendy's |
| **Product Context** (this) | What is the *thing* we market — its features, how it works, benefits, product messaging? | watsonx (the AI & data platform) | The Baconator (the burger) |
| **Offer** | What's the *value exchange / CTA* we extend to act now? | "Start a free watsonx trial" / "Book a demo" | "$5 Biggie Bag" / "Free Baconator with app order" |

Rules of thumb:

- **Business Context lists the portfolio; Product Context structures one offering.** Business
  Context's `products_and_services` is a lightweight list of what a company sells. Each entry that
  warrants depth gets its own Product Context Object. One business → many products.
- **Product Context is the durable "what it is"; the Offer is the time-bound "why act now."** A
  discount, trial, demo, financing deal, or bundle promotion is an **Offer** and belongs in the
  Offer Object — it *references* a Product Context but does not live here. Pricing *model* (how the
  thing is priced at all) is product context; a *promotion on* that price is an Offer.
- **Product messaging ≠ campaign/creative messaging.** `product_messaging` here is the durable,
  product-level story (the primary message, value pillars, proof points) that downstream Messaging
  Framework and Creative objects draw from and adapt per campaign. It is the source, not the
  campaign execution.

## The output schema

> **Canonical schema:** [`schemas/product_context.schema.json`](../../schemas/product_context.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "product_context",     // const — always "product_context"
  "osmm_version": "0.1.0",              // schema version this conforms to
  "product_id": "PRD-<slug>",           // stable, human-readable id (see ID rules)
  "version": "1.0",                     // instance version; bump on revision
  "status": "draft",                    // draft | proposed | stable | deprecated

  "name": "",                           // the offering's name as it goes to market
  "offering_type": "",                  // controlled enum — product | service | solution | platform | bundle
  "offering_category": "",              // plain-language category (e.g. "enterprise AI & data platform", "QSR menu item")
  "tagline": "",                        // OPTIONAL — the offering's own short line, if it has one

  "description": "",                    // 2-3 sentences: what it is, who it's for, the job it does (neutral/factual)

  "what_it_does": "",                   // the core function — the job the offering performs for the customer
  "how_it_works": [],                   // key mechanics / components / steps — how it delivers its value
  "key_features": [],                   // notable capabilities — array of { "feature": "", "description": "" }
  "benefits": [],                       // customer outcomes (benefits, not features); phrase as what the customer gets
  "use_cases": [],                      // primary jobs-to-be-done / scenarios it addresses
  "differentiators": [],                // what makes THIS offering distinct vs alternatives (product-level, grounded)

  "product_messaging": {                // durable product-level messaging — the source for downstream creative/messaging
    "primary_message": "",              // the one thing to land about this offering
    "value_pillars": [],               // 2-4 supporting message pillars
    "proof_points": [],                // evidence substantiating the claims (stats, certifications, named customers, awards)
    "objections": []                   // OPTIONAL — array of { "objection": "", "response": "" } for known buyer pushback
  },

  "pricing_model": "",                  // OPTIONAL — how it's priced at all (subscription, per-seat, tiered, menu price). NOT a promo — that's an Offer
  "tiers_or_variants": [],              // OPTIONAL — editions, sizes, configurations, or SKUs if relevant
  "target_segments": [],                // plain descriptions of who it's for (structure lives in Audience/Persona objects)
  "lifecycle_stage": "",                // OPTIONAL — new | growth | mature | sunset

  "linked_business_context": "",        // BIZ-<slug> of the business that offers it (placeholder ok)
  "linked_brand_context": "",           // OPTIONAL — BRC-<slug> if marketed under a specific brand
  "related_offerings": [],              // OPTIONAL — PRD-ids of complementary, parent, or bundled offerings
  "source": ""                          // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"product_context"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `product_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Go-to-market name of the offering. |
| `offering_type` | enum | yes | Controlled vocabulary — see below. Pick the single closest. |
| `offering_category` | string | yes | Plain-language "what kind of thing it is." Not a taxonomy code. |
| `tagline` | string | no | The offering's own line, if it has a recognizable one. Omit if none. |
| `description` | string | yes | 2-3 sentences, neutral and factual. The "what/who/job" — distinct from the message (which is claim-oriented). |
| `what_it_does` | string | yes | One to three sentences on the core function — the job it performs. |
| `how_it_works` | string[] | yes | The mechanics/components/steps that deliver the value. 2-6 items. Substance, not brochure copy. |
| `key_features` | object[] | yes | Each `{ "feature": "", "description": "" }`. 3-8 items. The notable capabilities/attributes. |
| `benefits` | string[] | yes | Outcomes the customer gets, phrased as benefits not features. Tie to a feature where natural. 3-6 items. |
| `use_cases` | string[] | yes | Primary jobs-to-be-done / scenarios. 2-6 items. |
| `differentiators` | string[] | yes | Product-level distinction vs. alternatives — grounded in evidence, not generic claims. |
| `product_messaging` | object | yes | The durable product story. See sub-fields. |
| `product_messaging.primary_message` | string | yes | The single thing to land about the offering. |
| `product_messaging.value_pillars` | string[] | yes | 2-4 supporting pillars. |
| `product_messaging.proof_points` | string[] | yes | Evidence: stats, certifications, named customers, awards, analyst recognition. Ground them. |
| `product_messaging.objections` | object[] | no | Each `{ "objection": "", "response": "" }`. Known buyer pushback and the counter. Omit if thin. |
| `pricing_model` | string | no | How it's priced *at all*. A promotion on the price is an Offer, not this. Omit if unknown/irrelevant. |
| `tiers_or_variants` | string[] | no | Editions, sizes, configurations, SKUs. |
| `target_segments` | string[] | no | Plain descriptions; structure lives in linked Audience/Persona objects. |
| `lifecycle_stage` | enum | no | `new` \| `growth` \| `mature` \| `sunset`. |
| `linked_business_context` | string | yes | Id of the Business Context that offers it. Use `BIZ-PLACEHOLDER-<slug>` if none exists yet. |
| `linked_brand_context` | string | no | Id of the Brand Context if marketed under a specific brand. `BRC-PLACEHOLDER-<slug>` ok; omit if not relevant. |
| `related_offerings` | string[] | no | `PRD-` ids of complementary/parent/bundled offerings. `PRD-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Document-level provenance and approximate date. |

## Offering type vocabulary

`offering_type` is a controlled, governed enum — a stored snake_case token mapped to a
human-readable label.

| Stored value | Label | Use when |
|---|---|---|
| `product` | Product | A discrete, packaged good or app — the Baconator, a SaaS app, a device. |
| `service` | Service | Work delivered for the customer — consulting, managed services, a subscription service. |
| `solution` | Solution | A bundled answer to a problem, often product + service, sold as an outcome. |
| `platform` | Platform | An extensible base others build/run on — watsonx, an app platform, a marketplace. |
| `bundle` | Bundle | A deliberately packaged set of offerings sold together (the offering itself, not a promo bundle). |

Pick the single closest value. If an offering legitimately spans types (a platform sold as a
managed solution), choose the dominant go-to-market framing and note the nuance in `description`.

## ID rules

`product_id` = `PRD-` + a lowercase, hyphen-delimited slug. Prefer a slug that namespaces the
offering under its business so ids stay unique across a portfolio:

- IBM watsonx → `PRD-ibm-watsonx`
- Wendy's Baconator → `PRD-wendys-baconator`
- ACME Rocket Skates → `PRD-acme-rocket-skates`

Keep it stable: once assigned, Offers and Work Products reference it. On revision bump `version`,
never the id.

## Extraction principles

1. **Stay on the offering, not the company.** If a fact is about the business at large (revenue,
   competitive set, corporate strategy), it belongs in Business Context. Here, only what describes
   *this* offering.
2. **Features vs. benefits is the core discipline.** `key_features` is what the offering *has/does*
   (a capability); `benefits` is what the customer *gets* (an outcome). "256-bit encryption" is a
   feature; "your data stays compliant in regulated industries" is the benefit. Keep them in the
   right bucket.
3. **`how_it_works` is substance, not slogans.** Capture the actual mechanics a buyer would need to
   understand the offering — components, steps, the model of delivery — distilled from spec/brochure
   copy, not the copy itself.
4. **`product_messaging` is durable, not a campaign.** Capture the product's standing story — the
   message you'd lead with regardless of campaign. Campaign- and persona-specific angles live
   downstream in the Journey's `persona_tracks.key_messages` and the Creative/Content objects, which
   draw from this.
5. **Ground proof points.** Prefer stated, verifiable evidence (published stats, certifications,
   named customers, analyst placements). If a claim is asserted without evidence, either omit it or
   note the thinness rather than laundering it into a proof point.
6. **Keep the Offer out.** Discounts, trials, demos, financing, limited-time bundles, and any "act
   now" value exchange are Offers — leave them for the Offer Object. Pricing *model* can stay;
   promotions cannot.
7. **One object per distinct offering.** A platform and a service sold around it are usually two
   Product Context Objects linked via `related_offerings`, not one blended object — unless they go
   to market as a single named solution.
8. **Keep arrays signal-bearing.** 3-8 items is usually right. Resist padding to a number.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per offering. Save using the OSMM instance-naming convention:
  `PRODUCT-CONTEXT_<entity-slug>.json` (e.g. `PRODUCT-CONTEXT_ibm-watsonx.json`) — uppercase object
  name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The
  `product_id` (`PRD-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially
  `differentiators` and `proof_points`) so they can fill gaps.
- If you find Offer-like material (promos, trials, discounts) in the source, note it and point the
  user to the Offer Object rather than smuggling it into this one.

## Starter prompts

**B2B platform/solution:**
> Build an OSMM Product Context Object for [Offering Name] by [Company]. Use the product/solution
> page and datasheet for features and how it works; the solution brief or analyst write-up for
> differentiation and proof points; and the pricing page for the pricing model. Keep promotions and
> trials out — those are Offers. Link it to `BIZ-[company-slug]`.

**B2C product:**
> Build an OSMM Product Context Object for [Product Name] by [Brand]. Use the brand's product/menu
> page for what it is, ingredients/components, and any standing tagline. Capture the durable product
> message, not a current promotion. Link it to `BIZ-[brand-slug]` and `BRC-[brand-slug]`.

---

## Worked examples

### Example 1 — B2B platform (IBM watsonx)

Input: ibm.com/watsonx product and solution pages, watsonx datasheets, analyst coverage.

```json
{
  "object_type": "product_context",
  "osmm_version": "0.1.0",
  "product_id": "PRD-ibm-watsonx",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx",
  "offering_type": "platform",
  "offering_category": "Enterprise AI and data platform",
  "tagline": "AI for business",
  "description": "IBM watsonx is an enterprise-grade AI and data platform for training, deploying, and governing AI models — including foundation models — across hybrid cloud environments. It is built for organizations that need to scale generative and traditional AI with the security, compliance, and data control regulated industries require. It comprises three integrated components spanning model development, data, and governance.",
  "what_it_does": "Lets enterprises build, tune, and deploy AI models on their own data and run them in production with governance and oversight — so AI initiatives move from experiment to trusted, scaled deployment without surrendering control of data or models.",
  "how_it_works": [
    "watsonx.ai — a studio to build, tune, and deploy machine-learning and foundation models, including IBM Granite and select open models",
    "watsonx.data — a fit-for-purpose data store (lakehouse) that lets models run on governed enterprise data across hybrid cloud",
    "watsonx.governance — toolkit to direct, manage, and monitor AI for risk, compliance, and explainability across the lifecycle",
    "Deploys across hybrid cloud (on-prem, IBM Cloud, other clouds) rather than locking workloads to a single environment"
  ],
  "key_features": [
    { "feature": "Foundation model library", "description": "IBM-built Granite models plus curated open-source models, tunable on enterprise data." },
    { "feature": "Hybrid-cloud deployment", "description": "Runs where the data lives — on-prem or any cloud — instead of forcing data movement." },
    { "feature": "Lakehouse data store", "description": "watsonx.data unifies and governs data so models train and run on trusted enterprise data." },
    { "feature": "AI governance toolkit", "description": "watsonx.governance monitors models for drift, bias, and compliance with documentation for audit." },
    { "feature": "Indemnified IP", "description": "IBM provides contractual IP protection for its Granite models, lowering enterprise legal risk." }
  ],
  "benefits": [
    "Scale AI from pilot to production without losing control of proprietary data",
    "Meet regulatory and audit requirements with built-in governance and explainability",
    "Reduce legal exposure on generative AI through indemnified, transparent models",
    "Avoid hyperscaler lock-in by running AI across existing hybrid-cloud infrastructure"
  ],
  "use_cases": [
    "Customer service automation with enterprise-grade virtual agents",
    "Code generation and application modernization",
    "Document summarization and knowledge retrieval over proprietary data",
    "Regulatory and risk reporting with governed, auditable AI"
  ],
  "differentiators": [
    "Governance and explainability built into the platform, positioned for regulated industries rather than bolted on",
    "Hybrid-cloud-native — runs on the customer's data wherever it lives, unlike single-cloud AI services",
    "IP-indemnified Granite models reduce the legal risk that blocks enterprise generative-AI adoption",
    "Backed by IBM Consulting for deployment, a flywheel pure-software AI vendors lack"
  ],
  "product_messaging": {
    "primary_message": "Enterprise AI you can trust to scale — on your data, with governance, across any cloud.",
    "value_pillars": [
      "Open: build on IBM and curated open models, not a single black box",
      "Targeted: tuned to enterprise use cases and run on your governed data",
      "Trusted: governance, explainability, and IP indemnification for regulated scale"
    ],
    "proof_points": [
      "Three integrated components (watsonx.ai, watsonx.data, watsonx.governance) span the AI lifecycle",
      "IBM Granite models ship with contractual IP indemnification",
      "Adopted across regulated sectors (financial services, government, healthcare) where compliance is a gate"
    ],
    "objections": [
      { "objection": "Hyperscalers already offer AI services we use.", "response": "watsonx runs on your governed data across hybrid cloud with built-in governance and IP indemnification — built for regulated scale, not just access to a model API." },
      { "objection": "Is IBM still relevant in AI vs. newer entrants?", "response": "watsonx pairs IBM's enterprise security and governance heritage with current foundation models and IBM Consulting deployment muscle." }
    ]
  },
  "pricing_model": "Subscription / consumption-based by component (watsonx.ai, watsonx.data, watsonx.governance); enterprise agreements",
  "tiers_or_variants": ["watsonx.ai", "watsonx.data", "watsonx.governance"],
  "target_segments": [
    "Enterprise data and AI leaders (CDO, CIO, heads of AI/ML)",
    "Regulated-industry organizations with compliance and data-residency constraints",
    "Line-of-business leaders driving AI automation"
  ],
  "lifecycle_stage": "growth",
  "linked_business_context": "BIZ-ibm",
  "linked_brand_context": "BRC-ibm",
  "related_offerings": ["PRD-PLACEHOLDER-ibm-consulting", "PRD-PLACEHOLDER-red-hat-openshift"],
  "source": "ibm.com/watsonx product and solution pages, watsonx component datasheets, analyst coverage (2024)"
}
```

---

### Example 2 — B2C product (Wendy's Baconator)

Input: wendys.com menu pages and public product/nutrition information.

```json
{
  "object_type": "product_context",
  "osmm_version": "0.1.0",
  "product_id": "PRD-wendys-baconator",
  "version": "1.0",
  "status": "draft",
  "name": "Baconator",
  "offering_type": "product",
  "offering_category": "QSR premium hamburger (menu item)",
  "tagline": "More meat, more bacon, no filler.",
  "description": "The Baconator is Wendy's flagship premium cheeseburger: two quarter-pound fresh-beef patties stacked with six strips of Applewood-smoked bacon, American cheese, ketchup, and mayonnaise on a toasted bun. It anchors the brand's 'meat-forward, no shortcuts' positioning and is a signature item that drives premium-burger traffic and brand recognition.",
  "what_it_does": "Delivers a high-protein, indulgent burger that satisfies a serious hunger occasion — Wendy's most meat-and-bacon-forward menu item for customers who want a substantial, premium fast-food burger.",
  "how_it_works": [
    "Two fresh (never frozen) quarter-pound beef patties as the base",
    "Six strips of Applewood-smoked bacon for the signature bacon-forward profile",
    "Two slices of American cheese, ketchup, and mayonnaise",
    "Served on a toasted bun; available as a combo with fries and a drink, and in variants (Son of Baconator, Breakfast Baconator)"
  ],
  "key_features": [
    { "feature": "Fresh, never-frozen beef", "description": "Two quarter-pound patties of fresh beef, a core Wendy's quality claim." },
    { "feature": "Six strips of bacon", "description": "A deliberately heavy bacon load that defines the product and its name." },
    { "feature": "No filler", "description": "Meat-and-bacon forward build with no vegetable filler — squarely an indulgence item." },
    { "feature": "Variant lineup", "description": "Son of Baconator (smaller) and Breakfast Baconator extend the line across hunger levels and dayparts." }
  ],
  "benefits": [
    "Satisfies a big-hunger craving with a substantial, high-protein burger",
    "Delivers a premium, indulgent fast-food experience that feels worth the spend",
    "Reinforces trust through Wendy's fresh-beef quality cue",
    "Offers a recognizable, orderable signature that anchors the visit"
  ],
  "use_cases": [
    "Big-hunger lunch or dinner occasion",
    "Premium-burger craving when a value menu won't satisfy",
    "Combo purchase that lifts average ticket"
  ],
  "differentiators": [
    "Fresh, never-frozen beef vs. frozen-patty QSR competitors",
    "Bacon load (six strips) heavier than typical fast-food bacon cheeseburgers",
    "Strong, ownable brand name and identity within the Wendy's menu"
  ],
  "product_messaging": {
    "primary_message": "When you're seriously hungry, the Baconator brings two fresh-beef patties and six strips of bacon — no filler.",
    "value_pillars": [
      "Meat-forward: two quarter-pound fresh-beef patties",
      "Bacon you can count: six strips, not a token slice",
      "Quality cue: fresh, never frozen"
    ],
    "proof_points": [
      "Two quarter-pound fresh-beef patties and six strips of Applewood-smoked bacon",
      "Long-running signature item central to Wendy's premium-burger identity",
      "Sustained menu staple with multiple line extensions (Son of, Breakfast)"
    ]
  },
  "pricing_model": "Menu price (à la carte or combo); premium tier of the burger menu",
  "tiers_or_variants": ["Baconator", "Son of Baconator", "Breakfast Baconator", "Baconator combo"],
  "target_segments": [
    "Big-hunger value-and-quality seekers",
    "Premium-burger fast-food buyers",
    "Younger adults drawn to indulgent, brand-led menu items"
  ],
  "lifecycle_stage": "mature",
  "linked_business_context": "BIZ-wendys",
  "linked_brand_context": "BRC-wendys",
  "source": "wendys.com menu and product pages, public nutrition information (2024)"
}
```
