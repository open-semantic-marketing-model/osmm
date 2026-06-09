---
name: osmm-measurement-framework-builder
description: >-
  Convert any measurement plan or KPI framework source into a structured OSMM Measurement
  Framework Object (canonical JSON). Inputs include measurement plans, KPI frameworks,
  scorecards, OKR/objective-metric mappings, dashboard specs, or analytics/measurement decks.
  Use this skill whenever the user wants to capture how a marketing strategy will be measured —
  "build a measurement framework object," "structure our KPI framework," "define our marketing
  metrics and targets," "objectify our measurement plan," or hands over a scorecard and asks
  what to do with it. This is the Work Product that operationalizes a Marketing Strategy's
  objectives into measurable KPIs, definitions, targets, and cadence.
object: Measurement Framework Object
object_type: measurement_framework
category: Work Product Object
phase: 1
wave: 2
osmm_version: 0.1.0
status: draft
---

# OSMM Measurement Framework Builder

Build a valid **OSMM Measurement Framework Object** from any source describing how a marketing strategy will be measured.

A Measurement Framework Object is the structured record of **how success is measured** for a planning horizon — the KPI set, each metric's definition and target, and the cadence and approach for reporting. It is the Work Product that operationalizes a **Marketing Strategy**'s objectives into something measurable: where the strategy says "grow the breakfast daypart," the framework says "breakfast daypart sales and repeat rate, defined as X, targeted directionally up, reported monthly." Downstream Phase 7 Performance Measurement records actuals against this framework, and the Strategy Brief composer reads the two together.

This is the lean v0.1 builder. It captures the metrics, definitions, targets, and cadence a marketing workflow needs to measure its strategy, and nothing more. It does **not** record results — actual performance data is the job of the Phase 7 Performance Measurement Object (append-only). The framework is the *plan*; performance is the *outcome*.

The Measurement Framework resolves workflow sub-process **1.7** (`TAXONOMY.md`): the KPI framework and success metrics.

**Key difference from Marketing Strategy (Phase 1):** the Marketing Strategy sets the objectives and describes, directionally, what success looks like (`success_criteria`). The Measurement Framework defines the **KPIs, their precise definitions, targets, and cadence** that make those objectives measurable. They are a pair: the strategy points forward via `linked_measurement_framework`, and the framework points back via `linked_marketing_strategy`. Objectives live in the strategy; metrics live here.

**Key difference from Performance Measurement (Phase 7):** the Measurement Framework is the durable *plan* — what will be measured and the targets. The Performance Measurement Object records the *actuals* against it and is append-only. "What we'll measure and the goal" lives here; "what actually happened" lives there.

## The output schema

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "measurement_framework",   // const — always "measurement_framework"
  "osmm_version": "0.1.0",                   // schema version this conforms to
  "measurement_framework_id": "MEF-<slug>",  // stable, human-readable id (see ID rules)
  "version": "1.0",                          // instance version; bump on revision
  "status": "draft",                         // draft | proposed | stable | deprecated

  "name": "",                                // the framework's name (e.g. "IBM 2026 Measurement Framework")
  "linked_business_context": "",             // id of the owning Business Context (BIZ-<slug>; placeholder ok)
  "linked_marketing_strategy": "",           // id of the Marketing Strategy this measures (MKS-<slug>; placeholder ok)
  "time_horizon": "",                        // the period measured — should match the strategy's horizon

  "north_star_metric": "",                   // OPTIONAL — the single most important measure for the horizon

  "metrics": [                               // the KPI set
    {
      "name": "",                            // metric name
      "tier": "",                            // primary | supporting | guardrail (governed enum)
      "definition": "",                      // what it counts / how it is calculated — unambiguous
      "supports_objective": "",              // OPTIONAL — the strategy objective this measures (text echo)
      "target": "",                          // OPTIONAL — directional or banded goal (keep public examples honest)
      "cadence": "",                         // OPTIONAL — measurement frequency (monthly, quarterly, per-campaign)
      "data_source": ""                      // OPTIONAL — where the data comes from
    }
  ],

  "measurement_cadence": "",                 // OPTIONAL — overall reporting/review cadence
  "measurement_approach": "",                // OPTIONAL — attribution method / measurement design notes
  "source": ""                               // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"measurement_framework"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `measurement_framework_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Readable label, usually entity + horizon: "Wendy's 2026 Measurement Framework". |
| `linked_business_context` | string | yes | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` if unbuilt. |
| `linked_marketing_strategy` | string | yes | `MKS-<slug>` of the strategy this framework measures. `MKS-PLACEHOLDER-<slug>` if unbuilt. Resolving this realizes the inverse of the strategy's `linked_measurement_framework`. |
| `time_horizon` | string | yes | The period measured; should match the linked strategy's `time_horizon`. |
| `north_star_metric` | string | no | The single most important measure for the horizon, if there is one. |
| `metrics` | object[] | yes | The KPI set. 3–8 metrics. Each requires `name`, `tier`, and `definition`; `supports_objective`, `target`, `cadence`, `data_source` are optional. |
| `metrics[].tier` | enum | yes | `primary` \| `supporting` \| `guardrail` — see vocabulary below. |
| `measurement_cadence` | string | no | Overall reporting/review rhythm (e.g. "Monthly business review; quarterly strategic review"). |
| `measurement_approach` | string | no | Notes on attribution method or measurement design (e.g. "marketing mix modeling + incrementality tests; brand tracker quarterly"). |
| `source` | string | no | One line. Provenance and approximate date. |

## Metric tier vocabulary

`tier` is a governed enum — a stored snake_case token mapping to a human-readable label. Every metric carries exactly one.

| Stored value | Label | Use for |
|---|---|---|
| `primary` | Primary | The few headline KPIs you would report to leadership — the metrics the strategy is judged on. |
| `supporting` | Supporting | Diagnostic metrics that explain movement in the primaries. |
| `guardrail` | Guardrail | Health metrics that must not degrade in pursuit of the primaries (margin, brand trust, churn). |

## ID rules

`measurement_framework_id` = `MEF-` + a lowercase, hyphen-delimited slug. Scope it to the **business plus the horizon**, normally matching the Marketing Strategy it measures so the pair is obvious:

- IBM, FY2026 → `MEF-ibm-2026` (measures `MKS-ibm-2026`)
- Wendy's, FY2026 → `MEF-wendys-2026` (measures `MKS-wendys-2026`)

Keep it stable once assigned. A new planning period is a new instance, paired with that period's Marketing Strategy.

## Extraction principles

1. **Every metric ladders to an objective.** A KPI that doesn't measure a stated marketing or business objective is noise. Tie each to the objective it serves via `supports_objective` (echo the strategy's wording). If the source has a metric with no objective behind it, flag it.
2. **Define the metric, don't just name it.** "App order share" is a label; "share of total transactions placed through the app" is a definition two analysts would count the same way. The definition is the point of structuring this.
3. **Separate primary, supporting, and guardrail.** Primaries are the few you'd report up; supporting metrics diagnose them; guardrails are the health metrics that must not degrade (franchisee margin, brand trust). Use the `tier` enum deliberately — most frameworks over-weight primaries and forget guardrails.
4. **Targets can be directional.** When building from public sources, use directional or banded targets ("up year-over-year," "top-three in category") rather than inventing precise numbers. Keep it honest and flag inferred targets.
5. **Keep it lean.** A tight set of real KPIs beats a sprawling scorecard. 3–8 metrics is usually right for a strategy-level framework.
6. **Don't restate the strategy.** Objectives, positioning, and audiences live in the Marketing Strategy. Reference the strategy and measure it; don't duplicate it.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One framework per business-and-horizon. Save using the OSMM instance-naming convention: `MEASUREMENT-FRAMEWORK_<entity-slug>-<horizon-slug>.json` (e.g. `MEASUREMENT-FRAMEWORK_ibm-2026.json`). The `measurement_framework_id` (`MEF-<slug>`) is the id *inside* the object, not the filename.
- Set `linked_marketing_strategy` to the real `MKS-<slug>` if it exists; otherwise use `MKS-PLACEHOLDER-<slug>`. When you resolve a real strategy, **tell the user to swap that strategy's `linked_measurement_framework` placeholder for this framework's id and bump the strategy's `version`** — that completes the bidirectional edge. Do the same `BIZ-`/placeholder handling for `linked_business_context`.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out metrics that lack a clear objective or target so they can fill gaps.

## Starter prompts

**From a measurement plan or scorecard:**
> Build an OSMM Measurement Framework Object for [Brand], horizon [FY2026], measuring [strategy / MKS id]. Sources: [measurement plan / KPI framework / scorecard]. Capture the primary, supporting, and guardrail metrics with definitions and targets, tie each to the objective it measures, and note the reporting cadence.

**From a strategy with no formal measurement plan:**
> Build an OSMM Measurement Framework Object for [Brand]'s [FY2026] marketing strategy. Derive a lean KPI set from the strategy's objectives — propose primary, supporting, and guardrail metrics with definitions and directional targets, and flag that targets and cadence are inferred and should be confirmed.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical instances live in `examples/work-product/` (`MEASUREMENT-FRAMEWORK_ibm-2026.json`, `MEASUREMENT-FRAMEWORK_wendys-2026.json`) — they are read independently by the Strategy Brief composer (and pair with the Marketing Strategy instances), so they are promoted there; the blocks below illustrate the shape.

### Example 1 — B2C challenger (Wendy's, FY2026)

Measures `MKS-wendys-2026`. Note the guardrail tying value-menu growth to franchisee margin — the health metric the strategy must not break.

```json
{
  "object_type": "measurement_framework",
  "osmm_version": "0.1.0",
  "measurement_framework_id": "MEF-wendys-2026",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's 2026 Measurement Framework",
  "linked_business_context": "BIZ-wendys",
  "linked_marketing_strategy": "MKS-wendys-2026",
  "time_horizon": "FY2026",
  "north_star_metric": "System-wide same-restaurant sales growth",
  "metrics": [
    {
      "name": "Social-attributed visit lift",
      "tier": "primary",
      "definition": "Incremental restaurant visits attributable to social/earned campaigns, measured via lift studies — not impressions or engagement",
      "supports_objective": "Convert the brand's social-media fame into measurable visits and frequency",
      "target": "Positive, measurable visit lift per major social moment",
      "cadence": "Per-campaign and monthly",
      "data_source": "Marketing mix modeling and incrementality/lift studies"
    },
    {
      "name": "Breakfast daypart sales and repeat rate",
      "tier": "primary",
      "definition": "Breakfast-daypart sales and share of breakfast customers who return within the period",
      "supports_objective": "Grow breakfast trial and repeat among value-seeking, mobile-first customers",
      "target": "Breakfast sales and repeat up year-over-year",
      "cadence": "Monthly"
    },
    {
      "name": "Digital sales mix and loyalty enrollment",
      "tier": "primary",
      "definition": "Share of transactions placed through the app plus net new Wendy's Rewards enrollments",
      "supports_objective": "Increase app-led offer redemption and loyalty enrollment",
      "target": "Digital mix and loyalty base up year-over-year",
      "cadence": "Monthly"
    },
    {
      "name": "Quality-plus-value perception",
      "tier": "supporting",
      "definition": "Brand-tracker scores for food quality and value vs. key burger-QSR competitors",
      "supports_objective": "Sustain quality-plus-value perception during value-menu price wars",
      "cadence": "Quarterly",
      "data_source": "Brand tracking study"
    },
    {
      "name": "Franchisee value-menu margin health",
      "tier": "guardrail",
      "definition": "Franchisee contribution margin on value-menu mix — must not degrade as value promotions scale",
      "supports_objective": "Sustain quality-plus-value perception during value-menu price wars",
      "target": "Hold or improve vs. prior year",
      "cadence": "Quarterly"
    }
  ],
  "measurement_cadence": "Monthly business review; quarterly brand and strategic review",
  "measurement_approach": "Marketing mix modeling and incrementality tests for traffic; app/loyalty analytics for digital; quarterly brand tracker for perception. Directional targets pending franchise-system planning.",
  "source": "Built from public information: The Wendy's Company public filings and public reporting on the brand's marketing (2024). Metrics and targets inferred from public strategic priorities; not internal scorecard values."
}
```

### Example 2 — B2B enterprise (IBM, FY2026, abbreviated)

Measures `MKS-ibm-2026`. Shown abbreviated; the full instance is `examples/work-product/MEASUREMENT-FRAMEWORK_ibm-2026.json`.

```json
{
  "object_type": "measurement_framework",
  "osmm_version": "0.1.0",
  "measurement_framework_id": "MEF-ibm-2026",
  "version": "1.0",
  "status": "draft",
  "name": "IBM 2026 Measurement Framework",
  "linked_business_context": "BIZ-ibm",
  "linked_marketing_strategy": "MKS-ibm-2026",
  "time_horizon": "FY2026",
  "north_star_metric": "Marketing-sourced qualified pipeline for the software and AI portfolios",
  "metrics": [
    {
      "name": "watsonx consideration / shortlist rate",
      "tier": "primary",
      "definition": "Share of tracked enterprise AI evaluations in which watsonx is shortlisted",
      "supports_objective": "Drive watsonx consideration among enterprise AI buyers evaluating hyperscaler alternatives",
      "target": "Up year-over-year; closing the gap to hyperscaler shortlist rates",
      "cadence": "Quarterly",
      "data_source": "Brand and consideration tracking studies"
    },
    {
      "name": "Red Hat-attached hybrid cloud pipeline",
      "tier": "primary",
      "definition": "Marketing-sourced pipeline on modernization deals that attach Red Hat / OpenShift",
      "supports_objective": "Grow Red Hat adoption within hybrid cloud modernization deals",
      "cadence": "Monthly"
    },
    {
      "name": "Enterprise-trust perception",
      "tier": "guardrail",
      "definition": "Brand-tracker trust/credibility scores among enterprise buyers — must not erode as AI messaging scales",
      "supports_objective": "Strengthen brand relevance with a younger generation of enterprise technology buyers",
      "cadence": "Quarterly",
      "data_source": "Brand tracking study"
    }
  ],
  "measurement_cadence": "Monthly pipeline review; quarterly brand review",
  "source": "Built from public information: IBM 2023 Annual Report, earnings commentary, and ibm.com (2024). Metrics and targets inferred from public strategic priorities; not internal scorecard values."
}
```
