---
name: osmm-offer-builder
description: >-
  Convert any promotion, deal, or incentive source into a structured OSMM Offer Object (canonical JSON). Inputs include promo pages, pricing/trial pages, "book a demo" or "request a consultation" CTAs, value-meal and combo deals, BOGO and gift-with-purchase mechanics, financing and lease offers, freemium tiers, samples, sweepstakes, loyalty rewards, or a marketer's notes on an incentive. Use this skill whenever the user wants to capture the value exchange / call to action — the time-bound reason to act now — as a reusable object: "build an offer object," "structure this promotion," "objectify this deal/trial/demo," "capture the offer," extract a promotion into JSON, or prepare a structured offer for downstream campaigns and creative. Trigger on offers, promotions, incentives, deals, discounts, free trials, demos, consultations, financial offers, BOGO, gift-with-purchase, bundles, freemium, samples, sweepstakes, financing, and loyalty rewards. An Offer references the Product Context it promotes.
object: Offer Object
object_type: offer
category: Work Product
phase: 3
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Offer Builder

Build a valid **OSMM Offer Object** from any source describing a promotion, incentive, trial, demo,
or other value exchange a business extends to get an audience to act.

An Offer Object is the **intended value exchange extended to an audience in exchange for a call to
action** — the time-bound, promotional reason to act *now*. A free trial ("30 days, no risk"), a
demo ("book a test drive"), a financial offer ("no money down, low lease payments"), a discount
("$5 Biggie Bag"), a bundle, a BOGO — each is an Offer. Campaigns, journeys, and creative all
activate offers; making the offer explicit and structured means agents and humans frame the *same*
deal the same way instead of re-deriving it from a promo page.

This object also carries the offer's **behavior-change objective** and **incentive philosophy** —
folded in from the former *Offer Strategy* object in the v0.5 right-sizing (those were a thin
strategy layer above the offer, not a separate thing). So an Offer says both *what the deal is* and
*why this deal, to drive what behavior*.

This is the lean v0.1 builder. It captures the marketing-relevant substance of an offer and nothing
more. It does **not** restate product features — it *references* the Product Context it promotes.

## Boundaries — what this object is and is NOT

The Offer sits between the durable thing it promotes and the campaign that activates it. Keeping the
lines clean is the whole point of giving the value exchange its own object:

| Object | Answers | Example (IBM) | Example (Wendy's) |
|--------|---------|---------------|-------------------|
| **Product Context** | What is the *thing* we market — its features, how it works, product messaging? | watsonx (the AI & data platform) | The Biggie Bag items / a burger (the menu item) |
| **Offer** (this) | What's the *value exchange / CTA* we extend to act now, and what behavior does it drive? | "Start a free watsonx trial" / "Book a demo" | "$5 Biggie Bag" |
| **Campaign Strategy** | How do we *activate* the offer — objective, audience-to-offer mapping, channels, sequencing? | The demand-gen campaign that runs the trial | The value-platform campaign that runs the Biggie Bag |

Rules of thumb:

- **Product Context is the durable "what it is"; the Offer is the time-bound "why act now."** A
  discount, trial, demo, financing deal, or bundle promotion is an Offer. Pricing *model* (how the
  thing is priced at all) is Product Context; a *promotion on* that price is an Offer.
- **Keep product features OUT.** The Offer does not restate what the product does, its capabilities,
  or its product-level messaging — those live in the Product Context the Offer points to via
  `linked_product`. The Offer carries only the value exchange and its mechanics.
- **The Offer is not the campaign.** *Which* audiences get *which* offer, on *which* channels, in
  *what* sequence is Campaign Strategy / Journey (Phase 4). The Offer defines the deal itself and the
  behavior it's meant to drive; the campaign decides how to put it in market.
- **Positioning here frames the deal, not the product.** `positioning` is how the *offer* is sold
  ("a meal for the price of a snack"); product positioning and messaging are Product Context's job.

## The output schema

> **Canonical schema:** [`schemas/offer.schema.json`](../../../schemas/offer.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "offer",                 // const — always "offer"
  "osmm_version": "0.1.0",                // schema version this conforms to
  "offer_id": "OFR-<slug>",               // stable, human-readable id (see ID rules)
  "version": "1.0",                       // instance version; bump on revision
  "status": "draft",                      // draft | proposed | stable | deprecated

  "name": "",                             // the offer's go-to-market name ("$5 Biggie Bag")
  "offer_type": "",                       // controlled enum — see vocabulary table

  "description": "",                      // 2-3 neutral sentences: what the offer is, who it's for, the action asked
  "value_exchange": "",                   // what the customer GETS in return for acting
  "call_to_action": "",                   // the action requested ("Start a free trial", "Book a demo", "Order in the app")
  "incentive_structure": "",              // the mechanics ("30 days free, no card required"; "$5 for a 4-item meal"; "0% APR for 60 months")
  "behavior_change_objective": "",        // the behavior this offer is meant to drive (folded from former Offer Strategy)

  "strategic_rationale": "",              // OPTIONAL — incentive philosophy / why this offer (folded from former Offer Strategy)
  "eligibility": [],                      // OPTIONAL — who qualifies / inclusion rules
  "redemption": "",                       // OPTIONAL — how it's redeemed / fulfilled
  "economics": {                          // OPTIONAL — directional, NOT precise finance
    "cost_basis": "",                     // what it costs to extend, directionally
    "profitability_threshold": "",        // the directional break-even / profitability bar
    "margin_notes": ""                    // directional notes on margin / subsidy / LTV
  },
  "positioning": "",                      // OPTIONAL — how the OFFER is framed to the audience
  "terms_conditions": [],                 // OPTIONAL — key terms / restrictions
  "availability": {                       // OPTIONAL — the time-bound window + channels
    "start": "",                          // when it starts
    "end": "",                            // when it ends
    "duration": "",                       // how long it runs ("limited-time", "30 days", "ongoing")
    "channels": []                        // channels it runs in (app, web, in-store)
  },

  "linked_product": "",                   // OPTIONAL — PRD-id of the Product Context this offer promotes (placeholder ok)
  "linked_audiences": [],                 // OPTIONAL — AUD-ids the offer is for (placeholder ok)
  "linked_business_context": "",          // OPTIONAL — BIZ-id of the business extending the offer (placeholder ok)
  "source": ""                            // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"offer"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `offer_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Go-to-market name of the offer. |
| `offer_type` | enum | yes | Controlled vocabulary — see below. Pick the single closest. |
| `description` | string | yes | 2-3 neutral sentences. The "what/who/action" — distinct from the positioning (which is the framing angle). |
| `value_exchange` | string | yes | What the customer *gets* for acting. The "you receive X." |
| `call_to_action` | string | yes | The single action requested — imperative phrasing ("Start a free trial", "Order in the app"). |
| `incentive_structure` | string | yes | The mechanics of the incentive — the terms that make it concrete ("30 days free, no card required"; "$5 for a 4-item meal"). |
| `behavior_change_objective` | string | yes | The behavior this offer is meant to drive (trial → adoption, lapsed → return, awareness → trial-down-funnel). Folded from the former Offer Strategy. |
| `strategic_rationale` | string | no | The incentive philosophy — why *this* offer is the right value exchange. Folded from the former Offer Strategy. Omit if thin. |
| `eligibility` | string[] | no | Inclusion rules / who qualifies. |
| `redemption` | string | no | How the customer redeems or how it's fulfilled. |
| `economics` | object | no | Directional offer economics only. See sub-fields. Not precise finance — ground it loosely or omit. |
| `economics.cost_basis` | string | no | What the offer costs to extend, directionally. |
| `economics.profitability_threshold` | string | no | Directional break-even / profitability bar. |
| `economics.margin_notes` | string | no | Directional notes on margin, subsidy, or LTV rationale. |
| `positioning` | string | no | How the *offer* is framed to the audience (the angle the deal is sold on). Not product positioning. |
| `terms_conditions` | string[] | no | Key terms, restrictions, limitations. |
| `availability` | object | no | The time-bound window and channels. See sub-fields. |
| `availability.start` | string | no | When the offer starts (date or plain-language). |
| `availability.end` | string | no | When the offer ends. |
| `availability.duration` | string | no | How long it runs ("limited-time", "30 days", "ongoing while in market"). |
| `availability.channels` | string[] | no | Channels it's available through. |
| `linked_product` | string | no | `PRD-` id of the Product Context this offer promotes. `PRD-PLACEHOLDER-<slug>` ok; omit if none. |
| `linked_audiences` | string[] | no | `AUD-` ids the offer is for. `AUD-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-` id of the business extending the offer. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Document-level provenance and approximate date. |

## Offer type vocabulary

`offer_type` is a controlled, governed enum — a stored snake_case token mapped to a human-readable
label. Extended deliberately by maintainers, never invented per-project.

| Stored value | Label | Use when |
|---|---|---|
| `financial` | Financial offer | Money-terms incentive on a purchase — "no money down", low lease/monthly payment, deposit waiver. |
| `discount` | Discount | A price reduction — percent or absolute off, value-meal pricing, promo code. |
| `free_trial` | Free trial | Time-boxed full access at no cost before buying — "30 days free". |
| `freemium` | Freemium | A permanently free tier intended to convert to paid over time. |
| `demo` | Demo | An invitation to experience the product with guidance — "book a demo", "schedule a test drive". |
| `consultation` | Consultation | An invitation to a guided assessment / advisory session — "talk to an expert", "free audit". |
| `bundle` | Bundle | A promotional package of items sold together for a combined incentive (the promo, not a product bundle). |
| `bogo` | Buy one, get one | Buy-one-get-one (free or discounted second unit). |
| `gift_with_purchase` | Gift with purchase | A free add-on item conditioned on a purchase. |
| `loyalty_reward` | Loyalty reward | A reward earned/redeemed via a loyalty or rewards program. |
| `sample` | Sample | A free or token-cost sample of the product to drive first trial. |
| `content_offer` | Content offer | Gated value content (whitepaper, report, tool) exchanged for the action (e.g. a form fill). |
| `sweepstakes` | Sweepstakes | A chance-to-win entry tied to taking an action. |
| `financing` | Financing | Payment-terms incentive — "0% APR for 60 months", deferred or installment financing. |

Pick the single closest value. If an offer legitimately blends types (a free trial that converts to
a freemium tier), choose the dominant act-now framing and note the nuance in `description`.

## ID rules

`offer_id` = `OFR-` + a lowercase, hyphen-delimited slug. Prefer a slug that namespaces the offer
under its business so ids stay unique across a portfolio:

- IBM watsonx trial → `OFR-ibm-watsonx-free-trial`
- Wendy's Biggie Bag → `OFR-wendys-biggie-bag`
- ACME no-money-down lease → `OFR-acme-zero-down-lease`

Keep it stable: once assigned, Campaign and Journey objects reference it. On revision bump
`version`, never the id.

## Extraction principles

1. **Keep product features OUT — reference the Product Context.** The Offer is the value exchange,
   not the thing. Capabilities, how-it-works, and product-level messaging belong in the Product
   Context the Offer points to via `linked_product`. Capture only what the customer *gets* and the
   mechanics of getting it.
2. **Offers are time-bound.** An Offer is a promotional reason to act *now*; capture the window in
   `availability`. If something has no time dimension and is just "how the thing is priced," that's
   the Product Context's `pricing_model`, not an Offer.
3. **Separate value exchange, CTA, and mechanics.** `value_exchange` is what they get;
   `call_to_action` is the single action you ask for; `incentive_structure` is the concrete terms.
   Keep them in the right bucket rather than collapsing all three into one sentence.
4. **Capture the behavior, not just the deal.** `behavior_change_objective` is required because an
   offer exists to move a behavior (try → adopt, lapsed → return, value-seeker → bigger basket). If
   the source only describes mechanics, infer the behavior and flag it as inferred.
5. **Ground economics directionally.** `economics` is for directional rationale — "subsidized to
   acquire trial users", "profitable with a drink attach" — not precise unit economics or
   confidential margins. If you have no public basis, omit it rather than inventing numbers.
6. **Positioning frames the offer, not the product.** Keep `positioning` about the deal's angle. If
   you find yourself writing product benefits, that belongs in the Product Context.
7. **Don't smuggle in the campaign.** Audience-to-offer mapping, channel plans, and sequencing are
   Campaign Strategy / Journey. The Offer may *link* the audiences it's for, but it doesn't decide how
   the campaign deploys it.
8. **Keep arrays signal-bearing.** A few real terms/eligibility rules beat a padded list. Resist
   restating the obvious.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per offer. Save using the OSMM instance-naming convention:
  `OFFER_<entity-slug>.json` (e.g. `OFFER_wendys-biggie-bag.json`) — uppercase object name,
  underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The
  `offer_id` (`OFR-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially
  `behavior_change_objective`, `strategic_rationale`, and `economics`) so they can fill gaps.
- If you find Product-Context material (features, how it works, product messaging) in the source,
  note it and point the user to the Product Context Object rather than restating it here — link to
  it via `linked_product` instead.

## Starter prompts

**B2B trial / demo offer:**
> Build an OSMM Offer Object for [Company]'s [trial/demo] of [Offering]. Use the trial/demo landing
> page for the value exchange, CTA, and mechanics; capture the behavior change it's meant to drive
> (e.g. self-serve trial → qualified pipeline). Keep product features out — link it to
> `PRD-[offering-slug]` and `BIZ-[company-slug]`.

**B2C promotional offer:**
> Build an OSMM Offer Object for [Brand]'s [promotion name]. Use the brand's promo/menu page for the
> deal mechanics, value exchange, and the action it asks for; capture the behavior it drives (e.g.
> drive value-seeker visits and basket size). Note the time window in availability. Link it to
> `BIZ-[brand-slug]` and the audiences it targets.

---

## Worked examples

### Example 1 — B2B free trial / demo (IBM watsonx)

Input: ibm.com/watsonx trial and "book a demo" pages; public watsonx promotion of trial access.

```json
{
  "object_type": "offer",
  "osmm_version": "0.1.0",
  "offer_id": "OFR-ibm-watsonx-free-trial",
  "version": "1.0",
  "status": "draft",
  "name": "watsonx Free Trial & Demo",
  "offer_type": "free_trial",
  "description": "A no-cost way for enterprise data and AI teams to start with IBM watsonx — a free trial of watsonx.ai plus the option to book a guided demo with IBM. It is aimed at technical evaluators who want hands-on proof before committing to an enterprise agreement. The action asked is to start the trial or book a demo.",
  "value_exchange": "Hands-on access to build and test AI models in watsonx.ai at no cost, plus an optional guided demo tailored to the buyer's use case.",
  "call_to_action": "Start a free trial or book a demo",
  "incentive_structure": "Free trial access to watsonx.ai with no upfront purchase; optional scheduled demo with an IBM specialist. Converts to a paid subscription/consumption agreement after evaluation.",
  "behavior_change_objective": "Move enterprise AI evaluators from passive interest to hands-on evaluation, so a self-serve trial or specialist demo seeds qualified pipeline and shortens the path to an enterprise commitment.",
  "strategic_rationale": "Enterprise AI is a high-consideration, evaluation-led purchase; removing cost and friction at the trial stage lets technical buyers prove value on their own terms, which de-risks the later commercial conversation and feeds IBM Consulting-led deployment.",
  "eligibility": [
    "Open to business and enterprise evaluators; trial scope and limits set by IBM",
    "Demo routed to qualified accounts via IBM sales"
  ],
  "redemption": "Sign up on ibm.com/watsonx to activate trial access, or submit the demo-request form to schedule a session with an IBM specialist.",
  "economics": {
    "cost_basis": "Subsidized trial compute and specialist demo time as customer-acquisition cost",
    "profitability_threshold": "Justified by downstream enterprise subscription and consulting attach, not trial-period revenue",
    "margin_notes": "Acquisition investment against high-LTV enterprise agreements"
  },
  "positioning": "Prove watsonx on your own data and use case before you commit — trusted enterprise AI, hands-on and risk-free to start.",
  "terms_conditions": [
    "Trial scope, feature limits, and duration governed by IBM trial terms",
    "Demo availability subject to qualification and scheduling"
  ],
  "availability": {
    "start": "Ongoing",
    "end": "Ongoing while in market",
    "duration": "Ongoing offer; trial period time-boxed per IBM terms",
    "channels": ["ibm.com/watsonx", "IBM sales / specialist demo"]
  },
  "linked_product": "PRD-ibm-watsonx",
  "linked_business_context": "BIZ-ibm",
  "source": "ibm.com/watsonx trial and demo-request pages (2024)"
}
```

---

### Example 2 — B2C value-meal offer (Wendy's $5 Biggie Bag)

Input: wendys.com and public coverage of the $5 Biggie Bag value-meal offer.

```json
{
  "object_type": "offer",
  "osmm_version": "0.1.0",
  "offer_id": "OFR-wendys-biggie-bag",
  "version": "1.0",
  "status": "draft",
  "name": "$5 Biggie Bag",
  "offer_type": "discount",
  "description": "Wendy's $5 Biggie Bag is a bundled value meal that packages a sandwich, junior bacon cheeseburger, nuggets, fries, and a drink for a single low price. It targets budget-conscious quick-service customers comparing value across QSR chains. The action asked is to order the Biggie Bag, primarily through the Wendy's app.",
  "value_exchange": "A complete four-item meal (sandwich, junior bacon cheeseburger, 4-piece nuggets, small fries, and a drink) for $5 — meaningfully below buying the items separately.",
  "call_to_action": "Order a $5 Biggie Bag in the app",
  "incentive_structure": "Four-plus items bundled at a fixed $5 price point; positioned against competitors' value menus and ordered à la carte at higher combined cost otherwise.",
  "behavior_change_objective": "Pull value-seekers away from competing QSR value menus and into a Wendy's visit, lifting traffic and average basket while driving app orders and the data/loyalty engagement that come with them.",
  "strategic_rationale": "In a price-sensitive QSR climate, a clear, memorable price-led bundle is the strongest lever to win the value-seeker occasion; routing it through the app deepens the loyalty and personalization flywheel beyond the single transaction.",
  "eligibility": [
    "Available to all customers; best price typically via the Wendy's app",
    "Participating locations; item lineup may vary by market"
  ],
  "redemption": "Order in the Wendy's app, online, or in-store at participating locations.",
  "economics": {
    "cost_basis": "Thin per-meal margin at the $5 price as a traffic-driving loss-leader-adjacent bundle",
    "profitability_threshold": "Relies on traffic lift, drink/upsize attach, and app-driven repeat visits rather than per-unit margin",
    "margin_notes": "Margin pressure offset by basket attach and loyalty/LTV gains"
  },
  "positioning": "A full meal for the price of a snack — Wendy's answer to the value menu, without giving up the food.",
  "terms_conditions": [
    "At participating locations; prices and availability may vary",
    "Limited-time and market-dependent; lineup subject to change"
  ],
  "availability": {
    "start": "Limited-time value promotion",
    "end": "While in market",
    "duration": "Limited-time / recurring value offer",
    "channels": ["Wendy's app", "wendys.com / online ordering", "in-store"]
  },
  "linked_product": "PRD-PLACEHOLDER-wendys-biggie-bag",
  "linked_audiences": ["AUD-wendys-value-seekers"],
  "linked_business_context": "BIZ-wendys",
  "source": "wendys.com and public coverage of the $5 Biggie Bag value offer (2024)"
}
```
