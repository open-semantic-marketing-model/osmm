---
name: osmm-marketing-strategy-builder
description: >-
  Convert any marketing strategy or annual marketing plan source into a structured OSMM
  Marketing Strategy Object (canonical JSON). Inputs include annual/marketing plans, strategy
  decks, objective frameworks, positioning documents, competitive strategy summaries, growth
  plans, or executive strategy briefs. Use this skill whenever the user wants to capture the
  marketing strategy for a planning horizon — "build a marketing strategy object," "structure
  our annual marketing plan," "objectify our marketing strategy," "capture our marketing
  objectives and positioning," or hands over a strategy deck and asks what to do with it. This
  is the strategic spine that downstream campaign, creative, and measurement work references.
object: Marketing Strategy Object
object_type: marketing_strategy
category: Work Product Object
phase: 1
wave: 2
osmm_version: 0.1.0
status: draft
---

# OSMM Marketing Strategy Builder

Build a valid **OSMM Marketing Strategy Object** from any source describing a brand's marketing strategy for a planning horizon.

A Marketing Strategy Object is the structured record of the **strategic choices** a marketing organization makes for a defined period — the business and marketing objectives it will pursue, how it will position and differentiate, and which audiences and growth bets it will prioritize. It is OSMM's first **Work Product**: a typed output of a decision that today lives in an annual plan, a strategy deck, or an executive brief. Downstream Work Products — Targeting Strategy, Campaign Strategy, Creative Strategy — and the Measurement Framework all reference this strategic spine, so making it explicit means every later decision is anchored to the same objectives and positioning instead of re-deriving them.

This is the lean v0.1 builder. It captures the strategic decisions a marketing workflow needs to stay aligned, and nothing more. The detailed KPI framework, metric definitions, and targets are deliberately out of scope — they belong to the **Measurement Framework Object** (Phase 1, sub-process 1.7); capture only strategy-level `success_criteria` here and link the framework via `linked_measurement_framework`.

The Marketing Strategy resolves workflow sub-processes **1.3–1.6 and 1.8** (`TAXONOMY.md`): business & marketing objectives, market & competitive strategy, customer & growth priorities, positioning & value proposition, and confirmed strategic direction. It is also the object the Phase 7 learning loop revises (7.7/7.8) — an Optimization Recommendation feeds the next horizon's strategy.

**Key difference from Business Context:** the Business Context Object is durable *fact* — what the business is, sells, and competes on, plus its standing `marketing_objectives` as enduring facts. The Marketing Strategy Object is a **time-boxed set of decisions** — the specific, prioritized objectives, positioning, and bets chosen for a planning horizon. It draws on Business Context but sharpens and commits; it never restates it. A Marketing Strategy belongs to a business and points back via `linked_business_context`.

**Key difference from Brand Context:** Brand Context carries the *durable* brand promise and voice (who the brand is). The Marketing Strategy's `positioning_statement` is the **competitive market positioning chosen for this horizon** (how the brand will compete this period) — distinct from the brand's identity core and from the Business Context `value_proposition` (a standing competitive claim). Strategy *applies* the brand and value proposition into a period's positioning; it does not duplicate them.

**Key difference from Measurement Framework (Phase 1):** objectives and strategy-level success criteria live here; the **KPI framework, metric definitions, and numeric targets** live in the Measurement Framework Object and are referenced via `linked_measurement_framework`. Durable "what we'll achieve and how we'll compete" lives here; "exactly how we'll measure it" lives there.

## The output schema

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "marketing_strategy",     // const — always "marketing_strategy"
  "osmm_version": "0.1.0",                  // schema version this conforms to
  "marketing_strategy_id": "MKS-<slug>",    // stable, human-readable id (see ID rules)
  "version": "1.0",                         // instance version; bump on revision
  "status": "draft",                        // draft | proposed | stable | deprecated

  "name": "",                               // the strategy's name (e.g. "IBM 2026 Marketing Strategy")
  "linked_business_context": "",            // id of the owning Business Context (BIZ-<slug>; placeholder ok)
  "linked_brand_context": "",               // OPTIONAL — id of the Brand Context this applies (BRC-<slug>)
  "time_horizon": "",                       // the planning period this strategy covers (e.g. "FY2026", "FY2026 Q1")

  "business_objectives": [],                // the business goals marketing is in service of (1.3)
  "marketing_objectives": [],               // marketing's own prioritized goals for the horizon (1.3) — outcomes, not activities
  "success_criteria": [],                   // OPTIONAL — strategy-level "what success looks like"; KPI detail lives in the Measurement Framework

  "positioning_statement": "",              // the competitive positioning chosen for this horizon (1.6)
  "differentiation_strategy": [],           // OPTIONAL — how the brand will win vs. its competitive set (1.4)

  "priority_audiences": [],                 // OPTIONAL — ids of the prioritized Audience objects (AUD-<slug>) (1.5)
  "growth_priorities": [],                  // OPTIONAL — the growth bets / where the brand will lean in (1.5)

  "linked_measurement_framework": "",       // OPTIONAL — id of the Measurement Framework (MEF-<slug>; placeholder ok)
  "source": ""                              // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"marketing_strategy"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `marketing_strategy_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | A readable label for the strategy, usually entity + horizon: "Wendy's 2026 Marketing Strategy". |
| `linked_business_context` | string | yes | `BIZ-<slug>` of the owning Business Context. Use `BIZ-PLACEHOLDER-<slug>` if it doesn't exist yet. |
| `linked_brand_context` | string | no | `BRC-<slug>` of the Brand Context this strategy applies. Omit if not relevant; use `BRC-PLACEHOLDER-<slug>` if it's expected but unbuilt. |
| `time_horizon` | string | yes | The planning period the strategy covers — a year, half, quarter, or named initiative window ("FY2026", "FY2026 H1", "Always-on 2026"). This is what scopes the instance. |
| `business_objectives` | string[] | yes | The business goals marketing serves. 2–5 items. Outcomes the business cares about, drawn from (not a copy of) Business Context `strategic_priorities`. |
| `marketing_objectives` | string[] | yes | Marketing's own prioritized goals for the horizon. 3–6 items. **Outcomes, not activities** — "grow breakfast trial," not "run breakfast ads." |
| `success_criteria` | string[] | no | Strategy-level description of what success looks like. Keep qualitative/directional — the metric definitions and numeric targets belong to the Measurement Framework (link it). |
| `positioning_statement` | string | yes | One to three sentences: how the brand chooses to compete this horizon. Distinct from the durable `brand_promise` (identity) and `value_proposition` (standing claim). |
| `differentiation_strategy` | string[] | no | The concrete ways the brand will win vs. its competitive set. Derived from Business Context `competitive_differentiators`, expressed as *what marketing will lead with*. |
| `priority_audiences` | string[] | no | Ids of the Audience objects (`AUD-<slug>`) the strategy prioritizes. References, not restated definitions. Use `AUD-PLACEHOLDER-<slug>` for an unbuilt audience. |
| `growth_priorities` | string[] | no | The growth bets — dayparts, segments, products, or motions the brand will lean into. 2–5 items. |
| `linked_measurement_framework` | string | no | `MEF-<slug>` of the Measurement Framework that operationalizes these objectives into KPIs. Use `MEF-PLACEHOLDER-<slug>` until that object is built. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`marketing_strategy_id` = `MKS-` + a lowercase, hyphen-delimited slug. Scope it to the **owning business plus the horizon**, so multiple strategies for the same business across periods stay distinct and obvious:

- IBM, FY2026 → `MKS-ibm-2026` (pairs with `BIZ-ibm`)
- Wendy's, FY2026 → `MKS-wendys-2026` (pairs with `BIZ-wendys`)

Keep it stable once assigned: downstream objects reference it. A **new planning period is a new instance** (a new id), not an edit of the old one — the prior strategy becomes history, and the learning loop revises forward.

## Extraction principles

1. **A strategy is a set of choices, not a summary.** Capture the decisions — what the brand *will and won't* do this horizon — not a restatement of the Business Context. If a sentence is true every year regardless of plan, it's durable fact and belongs in Context, not here.
2. **Objectives are outcomes, not activities.** "Grow the breakfast daypart's repeat visits" is an objective; "launch a breakfast campaign" is an activity. Keep `marketing_objectives` at the outcome level so downstream campaigns can be measured against them.
3. **Keep success criteria strategy-level.** Describe what winning looks like directionally; defer metric definitions and numeric targets to the Measurement Framework and link it. Don't smuggle a KPI table into `success_criteria`.
4. **Positioning is a period choice.** `positioning_statement` is how the brand competes *this horizon* — distinct from the durable `brand_promise` (Brand Context) and the standing `value_proposition` (Business Context). Apply them; don't duplicate them.
5. **Reference audiences, don't restate them.** `priority_audiences` holds Audience ids. The audience's criteria live in the Audience Object; the strategy only says *which* audiences are prioritized.
6. **Scope to a horizon.** Every strategy names its `time_horizon`. A new period is a new instance.
7. **Keep arrays signal-bearing.** A tight set of real objectives and bets beats a long generic list. Resist padding.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per business-and-horizon. Save using the OSMM instance-naming convention: `MARKETING-STRATEGY_<entity-slug>-<horizon-slug>.json` (e.g. `MARKETING-STRATEGY_ibm-2026.json`) — uppercase object name, underscore join, lowercase entity + horizon. See `CONVENTION.md` → "Instance file naming". The `marketing_strategy_id` (`MKS-<slug>`) remains the id *inside* the object; it is not the filename.
- Set `linked_business_context` to the real `BIZ-<slug>` if it exists; otherwise use a `BIZ-PLACEHOLDER-<slug>` and tell the user to resolve it once that object is built. Do the same for `priority_audiences` (`AUD-`) and `linked_measurement_framework` (`MEF-`).
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin in the source (especially missing objectives or positioning) so they can fill gaps.

## Starter prompts

**From an annual plan or strategy deck:**
> Build an OSMM Marketing Strategy Object for [Brand], horizon [FY2026]. Sources: [annual marketing plan / strategy deck / objective framework / positioning doc]. Capture the business and marketing objectives, the positioning and differentiation, and the priority audiences and growth bets. Link the owning Business Context and any Brand Context.

**From public strategic signals (no internal plan):**
> Build an OSMM Marketing Strategy Object for [Brand] from its public strategy signals — earnings commentary, investor materials, and public marketing. Synthesize the likely objectives, positioning, and priorities; flag that objectives and success criteria are inferred and should be confirmed against the internal plan.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical instances live in `examples/work-product/` (`MARKETING-STRATEGY_ibm-2026.json`, `MARKETING-STRATEGY_wendys-2026.json`) — they are read independently by the `osmm-creative-brief-composer` (which lists `marketing_strategy` as an optional input), so they are promoted there; the blocks below illustrate the shape.

### Example 1 — B2C challenger with a distinctive voice (Wendy's, FY2026)

Built from Wendy's public filings and marketing. References the shipped `BIZ-wendys`, `BRC-wendys`, and `AUD-wendys-value-seekers`; the Measurement Framework is a placeholder until that builder ships.

```json
{
  "object_type": "marketing_strategy",
  "osmm_version": "0.1.0",
  "marketing_strategy_id": "MKS-wendys-2026",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's 2026 Marketing Strategy",
  "linked_business_context": "BIZ-wendys",
  "linked_brand_context": "BRC-wendys",
  "time_horizon": "FY2026",
  "business_objectives": [
    "Drive system-wide traffic and same-restaurant sales across the franchised system",
    "Expand and defend the breakfast daypart against entrenched competitors",
    "Accelerate digital sales, app adoption, and Wendy's Rewards loyalty"
  ],
  "marketing_objectives": [
    "Convert the brand's social-media fame into measurable visits and frequency",
    "Grow breakfast trial and repeat among value-seeking, mobile-first customers",
    "Increase app-led offer redemption and loyalty enrollment",
    "Sustain quality-plus-value perception during value-menu price wars"
  ],
  "success_criteria": [
    "Breakfast daypart share and repeat-visit growth",
    "Higher share of transactions through the app and loyalty program",
    "Social engagement translating into measured visit lift, not just impressions"
  ],
  "positioning_statement": "Higher-quality fast food — fresh, never frozen — with a sharp, culturally fluent personality, at a value that competes head-on with the biggest burger chains.",
  "differentiation_strategy": [
    "Anchor every message in the durable 'fresh, never frozen' quality proof",
    "Win attention through creativity and cultural speed rather than media spend",
    "Use the distinctive social voice as a traffic-driving asset, not just brand fame",
    "Lead value architecture (Biggie Bag / 4 for $4) to compete directly on price"
  ],
  "priority_audiences": ["AUD-wendys-value-seekers"],
  "growth_priorities": [
    "Breakfast daypart expansion",
    "Digital, app, and loyalty adoption",
    "Late-night and high-frequency value occasions"
  ],
  "linked_measurement_framework": "MEF-PLACEHOLDER-wendys",
  "source": "Built from public information: The Wendy's Company public filings, wendys.com, and public reporting on the brand's marketing (2024). Objectives synthesized from public strategic priorities; success criteria illustrative, not internal targets."
}
```

### Example 2 — B2B enterprise strategy (IBM, FY2026, abbreviated)

Built from IBM's public strategic priorities. Shown abbreviated to contrast an enterprise, outcome-led strategy with Example 1; the full instance is `examples/work-product/MARKETING-STRATEGY_ibm-2026.json`.

```json
{
  "object_type": "marketing_strategy",
  "osmm_version": "0.1.0",
  "marketing_strategy_id": "MKS-ibm-2026",
  "version": "1.0",
  "status": "draft",
  "name": "IBM 2026 Marketing Strategy",
  "linked_business_context": "BIZ-ibm",
  "linked_brand_context": "BRC-ibm",
  "time_horizon": "FY2026",
  "business_objectives": [
    "Grow software to the majority of total revenue",
    "Establish watsonx as the enterprise AI platform of record for regulated industries",
    "Deepen the Red Hat ecosystem to extend hybrid cloud reach"
  ],
  "marketing_objectives": [
    "Drive watsonx consideration among enterprise AI buyers evaluating hyperscaler alternatives",
    "Grow Red Hat adoption within hybrid cloud modernization deals",
    "Expand IBM Consulting pipeline tied to AI and automation transformation engagements",
    "Strengthen brand relevance with a younger generation of enterprise technology buyers"
  ],
  "positioning_statement": "The enterprise-grade, governed AI and hybrid cloud platform — modernize without rearchitecting, with security, compliance, and trust built in.",
  "differentiation_strategy": [
    "Lead with Red Hat as the open hybrid cloud standard embedded across Fortune 500 environments",
    "Use mainframe and regulated-industry credibility as proof of enterprise-grade security",
    "Frame watsonx as the governed, explainable AI alternative to hyperscaler models"
  ],
  "priority_audiences": ["AUD-ibm-enterprise-it"],
  "linked_measurement_framework": "MEF-PLACEHOLDER-ibm",
  "source": "Built from public information: IBM 2023 Annual Report, earnings commentary, and ibm.com (2024). Objectives and positioning synthesized from public strategic priorities."
}
```
