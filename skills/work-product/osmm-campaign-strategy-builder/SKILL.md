---
name: osmm-campaign-strategy-builder
description: >-
  Convert any campaign brief, campaign plan, or activation plan source into a structured OSMM
  Campaign Strategy Object (canonical JSON). Inputs include campaign briefs, campaign charters,
  activation plans, channel plans, media plans, audience-to-offer matrices, go-to-market launch
  plans, or a marketer's notes on how a campaign will run. Use this skill whenever the user wants
  to capture how a campaign activates — its objective and scope, which audiences get which offers
  (audience-to-offer mapping), the channel and touchpoint strategy, and the personalization
  approach: "build a campaign strategy object," "structure this campaign brief," "objectify our
  activation plan," "map audiences to offers," "build a channel plan," or "capture our
  personalization strategy." This is the activation plan that turns strategy into a coordinated
  campaign. It is NOT the customer path/sequencing (that's Journey) and it does NOT
  restate audiences or offers — it references them.
object: Campaign Strategy Object
object_type: campaign_strategy
category: Work Product
phase: 4
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Campaign Strategy Builder

Build a valid **OSMM Campaign Strategy Object** from any source describing how a campaign will be
activated.

A Campaign Strategy Object is the **activation plan** — the typed record of the choices that turn a
marketing strategy into a coordinated campaign: the campaign's objective and scope, *which audiences
get which offers* (the audience-to-offer mapping), the channel and touchpoint strategy, and the
personalization approach. It is a Work Product that references the strategic spine it executes (the
**Marketing Strategy**), the customer path it uses (the **Journey**), and the
**Audiences** and **Offers** it activates. Making it explicit means every downstream creative,
content, and delivery decision is anchored to the same activation plan instead of re-deriving it.

This is the lean v0.1 builder. It captures the activation decisions a marketing workflow needs to
coordinate a campaign, and nothing more. It deliberately does **not** model the customer path,
triggering, or sequencing — that is the **Journey Object** (sub-processes 4.2/4.5) — and
it does **not** restate audience criteria or offer mechanics, which live in their own objects and
are referenced here.

The Campaign Strategy resolves workflow sub-processes **4.1, 4.3, 4.4, 4.6, and 4.8** (`TAXONOMY.md`):
campaign objective & scope, audience-to-offer mapping, channel & touchpoint strategy, personalization
strategy, and the confirmed campaign direction. It is the activation counterpart to the Journey
Strategy, with which it is confirmed jointly at 4.8.

## Boundaries — what this object is and is NOT

Campaign Strategy sits among three neighbors that are easy to confuse. Keeping the lines clean is
the whole point of giving the activation plan its own object:

| Object | Answers | Example (Wendy's) | Example (IBM) |
|--------|---------|-------------------|---------------|
| **Marketing Strategy** | What are we trying to achieve this *horizon*, and how do we position/compete? | "Wendy's 2026 Marketing Strategy" — grow breakfast, digital, loyalty | "IBM 2026 Marketing Strategy" — establish watsonx as enterprise AI of record |
| **Campaign Strategy** (this) | How does *this campaign* activate — objective, who gets which offer, on what channels, personalized how? | "Biggie Bag Value Campaign" — value-seekers get the Biggie Bag via app/paid social/OOH | "watsonx Enterprise AI Launch" — enterprise IT gets a trial/demo via paid search/LinkedIn/events |
| **Journey** | What is the *customer path* — the sequence, triggers, and cadence across touchpoints? | The value-seeker's path from social impression → app open → redemption | The buyer's path from search → content → demo request → sales |
| **Offer** | What's the *value exchange / CTA*? | "$5 Biggie Bag" | "Start a free watsonx trial" / "Book a demo" |

Rules of thumb:

- **Campaign Strategy is the activation plan; Journey is the path.** The *what gets
  activated, for whom, on which channels* lives here. The *order, triggers, and cadence* a customer
  moves through lives in the Journey. A campaign references the journey it uses
  (`linked_journey`); it does not encode the sequence in `channel_strategy`.
- **Reference audiences and offers; never restate them.** `audience_offer_mapping` holds `AUD-` and
  `OFR-` ids. The audience's criteria live in the Audience Object and the offer's mechanics in the
  Offer Object — the campaign only says *which audience gets which offer, and why*.
- **The Campaign Strategy executes a Marketing Strategy.** It points back via
  `linked_marketing_strategy`. The horizon-level objectives and positioning live there; the
  campaign sharpens them into one activation.
- **Campaign measurement is a scope facet of the Measurement Framework.** Keep `success_criteria`
  directional here and link the campaign-scope Measurement Framework
  (`linked_measurement_framework`) for KPI definitions and targets.

## The output schema

> **Canonical schema:** [`schemas/campaign_strategy.schema.json`](../../../schemas/campaign_strategy.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "campaign_strategy",      // const — always "campaign_strategy"
  "osmm_version": "0.1.0",                  // schema version this conforms to
  "campaign_strategy_id": "CMS-<slug>",     // stable, human-readable id (see ID rules)
  "version": "1.0",                         // instance version; bump on revision
  "status": "draft",                        // draft | proposed | stable | deprecated

  "name": "",                               // the campaign's name (e.g. "Wendy's Biggie Bag Value Campaign")
  "campaign_objective": "",                 // what the campaign is trying to achieve (4.1) — an outcome
  "success_criteria": [],                   // how success is judged, directional (4.1); KPI detail → Measurement Framework
  "scope": "",                              // what's in / out of scope (4.1)
  "campaign_window": {                      // OPTIONAL — the campaign's timing
    "start": "",                            //   when it starts
    "end": "",                              //   when it ends
    "duration": ""                          //   human-readable duration
  },

  "audience_offer_mapping": [               // the core 4.3 matrix — array of { audience, offer, rationale }
    { "audience": "AUD-<slug>", "offer": "OFR-<slug>", "rationale": "" }
  ],
  "channel_strategy": [                     // the 4.4 channel/touchpoint strategy — array of { channel, role, priority }
    { "channel": "", "role": "", "priority": "" }   // priority: primary | secondary | supporting
  ],
  "personalization_strategy": [],           // OPTIONAL — the 4.6 personalization rules/approach

  "linked_marketing_strategy": "",          // OPTIONAL — MKS-<slug> of the strategy this executes (placeholder ok)
  "linked_journey": "",            // OPTIONAL — JNY-<slug> of the journey it uses (placeholder ok)
  "linked_audiences": [],                   // OPTIONAL — AUD-<slug> ids this campaign activates
  "linked_offers": [],                      // OPTIONAL — OFR-<slug> ids this campaign activates
  "linked_business_context": "",            // OPTIONAL — BIZ-<slug> of the owning Business Context (placeholder ok)
  "linked_measurement_framework": "",       // OPTIONAL — MEF-<slug> of the campaign-scope Measurement Framework
  "source": ""                              // OPTIONAL — one line: source(s) and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"campaign_strategy"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `campaign_strategy_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | A readable label for the campaign, usually entity + campaign theme: "Wendy's Biggie Bag Value Campaign". |
| `campaign_objective` | string | yes | What the campaign is trying to achieve (4.1). An **outcome** ("drive Biggie Bag trial and app redemption among value-seekers"), not an activity list. |
| `success_criteria` | string[] | yes | How success is judged, kept directional. 2–5 items. Metric definitions and numeric targets belong to the campaign-scope Measurement Framework — link it. |
| `scope` | string | yes | What's in and out of scope (4.1) — markets, products, dayparts, and explicit exclusions. |
| `campaign_window` | object | no | `{ start, end, duration }`. Omit if undated/always-on; or set `duration` only. |
| `audience_offer_mapping` | object[] | yes | The 4.3 matrix. Each `{ audience: "AUD-<slug>", offer: "OFR-<slug>", rationale }`. 1+ rows. References, not restatements. |
| `channel_strategy` | object[] | yes | The 4.4 strategy. Each `{ channel, role, priority }`. 1+ items. `priority` ∈ `primary` \| `secondary` \| `supporting`. Channels/roles, not sequence. |
| `personalization_strategy` | string[] | no | The 4.6 approach — the rules/dimensions used to tailor the campaign. Executable rule config lives in Personalization Configuration. |
| `linked_marketing_strategy` | string | no | `MKS-<slug>` of the strategy this executes. Use `MKS-PLACEHOLDER-<slug>` until built. |
| `linked_journey` | string | no | `JNY-<slug>` of the journey this campaign uses. Use `JNY-PLACEHOLDER-<slug>` until built. |
| `linked_audiences` | string[] | no | `AUD-<slug>` ids the campaign activates. `AUD-PLACEHOLDER-<slug>` ok. |
| `linked_offers` | string[] | no | `OFR-<slug>` ids the campaign activates. `OFR-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` ok. |
| `linked_measurement_framework` | string | no | `MEF-<slug>` of the campaign-scope Measurement Framework. `MEF-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`campaign_strategy_id` = `CMS-` + a lowercase, hyphen-delimited slug. Scope it to the **owning
entity plus the campaign**, so multiple campaigns for the same business stay distinct and obvious:

- Wendy's Biggie Bag value campaign → `CMS-wendys-biggie-bag` (pairs with `BIZ-wendys`)
- IBM watsonx enterprise AI launch → `CMS-ibm-watsonx-launch` (pairs with `BIZ-ibm`)

Keep it stable once assigned: downstream Journey, Experience Delivery, and Campaign
Deployment objects reference it. A **materially different campaign is a new instance** (a new id),
not an edit of the old one.

## Extraction principles

1. **A campaign strategy is an activation plan, not a restatement.** Capture the choices —
   objective, who-gets-what, on which channels, personalized how. If a fact is a horizon-level
   choice (positioning, annual objectives), it belongs in the Marketing Strategy and is referenced,
   not copied.
2. **The objective is an outcome.** `campaign_objective` is what the campaign drives ("grow
   breakfast trial via the app"), not the tactics ("run app push notifications"). Keep
   `success_criteria` directional and defer the KPI table to the Measurement Framework.
3. **Reference audiences and offers; don't restate them.** `audience_offer_mapping` is the heart of
   the object — it holds `AUD-` and `OFR-` ids plus the rationale for the pairing. The audience's
   criteria and the offer's mechanics live in their own objects.
4. **The journey/sequencing lives in Journey.** Channels and their roles/priority belong
   here; the *order, triggers, and cadence* a customer moves through do not — link the Journey
   Strategy via `linked_journey` rather than encoding the path in `channel_strategy`.
5. **Personalization here is the approach, not the rule engine.** `personalization_strategy`
   captures the dimensions and rules-of-thumb for tailoring; the executable rules live downstream in
   the Personalization Configuration object.
6. **Scope to one campaign.** Every instance names one campaign with a clear `scope`. A materially
   different campaign is a new instance.
7. **Keep arrays signal-bearing.** A tight, real set of audience-offer pairs and channels beats a
   padded list. Resist filler.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per campaign. Save using the OSMM instance-naming convention:
  `CAMPAIGN-STRATEGY_<entity-slug>.json` (e.g. `CAMPAIGN-STRATEGY_wendys-biggie-bag.json`) —
  uppercase object name, underscore join, lowercase entity slug. Append an instance slug only if
  one entity has multiple campaign strategies. See `CONVENTION.md` → "Instance file naming". The
  `campaign_strategy_id` (`CMS-<slug>`) remains the id *inside* the object; it is not the filename.
- Set reference fields to the real ids if they exist (`AUD-`, `OFR-`, `MKS-`, `JNY-`, `BIZ-`,
  `MEF-`); otherwise use a `…-PLACEHOLDER-<slug>` id and tell the user to resolve it once that
  object is built.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially missing
  audience-offer pairs or an unscoped campaign) so they can fill gaps.

## Starter prompts

**From a campaign brief or activation plan:**
> Build an OSMM Campaign Strategy Object for [Brand]'s [campaign name]. Sources: [campaign brief /
> activation plan / channel plan / media plan]. Capture the objective and scope, the
> audience-to-offer mapping, the channel/touchpoint strategy, and the personalization approach. Link
> the Marketing Strategy it executes, the Journey it uses, and the Audiences and Offers it
> activates.

**From public signals (no internal brief):**
> Build an OSMM Campaign Strategy Object for [Brand]'s [observed campaign] from public signals — the
> brand's public marketing, press, and channel activity. Synthesize the likely objective, audience-
> to-offer mapping, and channel mix; flag what is inferred and should be confirmed against the
> internal brief. Use PLACEHOLDER ids for any unbuilt Audience/Offer/Journey objects.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). Both validate against
`schemas/campaign_strategy.schema.json`. They reference shipped ids where they exist (`BIZ-wendys`,
`MKS-wendys-2026`, `AUD-wendys-value-seekers`, `BIZ-ibm`, `MKS-ibm-2026`, `AUD-ibm-enterprise-it`)
and PLACEHOLDER ids where the target object doesn't exist yet (Offers, Journey Strategies).

### Example 1 — B2C value campaign (Wendy's Biggie Bag)

Built from Wendy's public marketing. Maps the value-seeker audience to the Biggie Bag offer across
app, paid social, and OOH; executes the Wendy's 2026 Marketing Strategy.

```json
{
  "object_type": "campaign_strategy",
  "osmm_version": "0.1.0",
  "campaign_strategy_id": "CMS-wendys-biggie-bag",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's Biggie Bag Value Campaign",
  "campaign_objective": "Drive trial and repeat purchase of the Biggie Bag among value-seeking, mobile-first customers, converting Wendy's cultural attention into measured app-led visits during the value-menu price war.",
  "success_criteria": [
    "Growth in Biggie Bag transactions and attach rate",
    "Higher share of redemptions through the Wendy's app and loyalty program",
    "Social engagement translating into measured visit lift, not just impressions"
  ],
  "scope": "U.S. system-wide lunch and late-night value occasions, app-first. In scope: the Biggie Bag value bundle promoted via app, paid social, and OOH. Out of scope: breakfast daypart, premium-burger messaging, and non-U.S. markets.",
  "campaign_window": {
    "start": "FY2026 Q1",
    "end": "FY2026 Q2",
    "duration": "12 weeks"
  },
  "audience_offer_mapping": [
    {
      "audience": "AUD-wendys-value-seekers",
      "offer": "OFR-PLACEHOLDER-wendys-biggie-bag",
      "rationale": "Value-seeking, mobile-first customers are most responsive to a bundled price offer surfaced in the app, where redemption and loyalty can be measured."
    }
  ],
  "channel_strategy": [
    {
      "channel": "Mobile app",
      "role": "Primary redemption and loyalty surface — deliver the offer and capture measured visits",
      "priority": "primary"
    },
    {
      "channel": "Paid social",
      "role": "Convert the brand's cultural voice into reach and offer awareness",
      "priority": "primary"
    },
    {
      "channel": "Out-of-home (OOH)",
      "role": "Broad value-message awareness in high-traffic occasions",
      "priority": "supporting"
    }
  ],
  "personalization_strategy": [
    "Surface the Biggie Bag offer in-app to lapsed and value-seeking segments based on visit recency and frequency",
    "Tailor late-night vs lunch creative by time-of-day and prior daypart behavior",
    "Prioritize loyalty enrollment prompts for first-time app redeemers"
  ],
  "linked_marketing_strategy": "MKS-wendys-2026",
  "linked_journey": "JNY-PLACEHOLDER-wendys-value-redemption",
  "linked_audiences": ["AUD-wendys-value-seekers"],
  "linked_offers": ["OFR-PLACEHOLDER-wendys-biggie-bag"],
  "linked_business_context": "BIZ-wendys",
  "linked_measurement_framework": "MEF-PLACEHOLDER-wendys-biggie-bag",
  "source": "Built from public information: wendys.com, the Wendy's app, and public reporting on the brand's value-menu marketing (2024). Audience-offer mapping and channel mix synthesized from public signals; the Offer and Journey are placeholders until those objects are built."
}
```

### Example 2 — B2B launch campaign (IBM watsonx Enterprise AI Launch)

Built from IBM's public strategic priorities. Maps the enterprise-IT audience to a watsonx
trial/demo offer across paid search, LinkedIn, and events; executes the IBM 2026 Marketing Strategy.

```json
{
  "object_type": "campaign_strategy",
  "osmm_version": "0.1.0",
  "campaign_strategy_id": "CMS-ibm-watsonx-launch",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Enterprise AI Launch Campaign",
  "campaign_objective": "Drive watsonx consideration and qualified trial/demo requests among enterprise AI buyers evaluating hyperscaler alternatives, establishing watsonx as the governed enterprise AI platform of record.",
  "success_criteria": [
    "Volume and quality of watsonx trial and demo requests from target accounts",
    "Pipeline influenced among regulated-industry enterprise accounts",
    "Share of voice and consideration lift among enterprise AI buyers"
  ],
  "scope": "Global enterprise and regulated-industry accounts (financial services, government, healthcare). In scope: watsonx trial and demo activation across paid search, LinkedIn, and events. Out of scope: SMB segments, Red Hat-only modernization deals, and IBM Consulting services campaigns.",
  "campaign_window": {
    "start": "FY2026 H1",
    "duration": "two quarters"
  },
  "audience_offer_mapping": [
    {
      "audience": "AUD-ibm-enterprise-it",
      "offer": "OFR-PLACEHOLDER-ibm-watsonx-trial",
      "rationale": "Enterprise IT and data leaders evaluating AI platforms convert best on a low-risk trial or guided demo that proves governance and hybrid-cloud fit on their own data."
    }
  ],
  "channel_strategy": [
    {
      "channel": "Paid search",
      "role": "Capture high-intent enterprise AI demand and route to trial/demo",
      "priority": "primary"
    },
    {
      "channel": "LinkedIn",
      "role": "Reach and nurture enterprise IT decision-makers with proof-led content",
      "priority": "primary"
    },
    {
      "channel": "Events",
      "role": "Deepen consideration and demo conversion with target accounts",
      "priority": "secondary"
    }
  ],
  "personalization_strategy": [
    "Tailor messaging by industry (financial services, government, healthcare) to lead with the relevant governance and compliance proof",
    "Adapt the offer ask by funnel stage — content for early intent, guided demo for evaluating accounts",
    "Account-based prioritization for named enterprise target accounts"
  ],
  "linked_marketing_strategy": "MKS-ibm-2026",
  "linked_journey": "JNY-PLACEHOLDER-ibm-enterprise-evaluation",
  "linked_audiences": ["AUD-ibm-enterprise-it"],
  "linked_offers": ["OFR-PLACEHOLDER-ibm-watsonx-trial"],
  "linked_business_context": "BIZ-ibm",
  "linked_measurement_framework": "MEF-PLACEHOLDER-ibm-watsonx-launch",
  "source": "Built from public information: ibm.com/watsonx, IBM earnings commentary, and public marketing (2024). Audience-offer mapping and channel mix synthesized from public strategic priorities; the Offer and Journey are placeholders until those objects are built."
}
```
