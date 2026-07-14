---
name: osmm-performance-measurement-builder
description: >-
  Convert any performance data source into a structured OSMM Performance Measurement Object
  (canonical JSON) that records actuals against a Measurement Framework's plan for a period.
  Inputs include analytics exports, KPI dashboards, campaign performance reports, scorecard
  actuals, and MMM/lift study outputs. Use this skill whenever the user wants to record what
  actually happened against a measurement plan — "record performance against our measurement
  framework," "structure our Q1 KPI actuals," "log offer/creative/journey performance," or
  "build a performance measurement object." This is the append-only Phase 7 Measurement Object
  that reports the readings, their variance to target, and a narrative readout for one period.
object: Performance Measurement Object
object_type: performance_measurement
category: Measurement Object
phase: 7
wave: 7
osmm_version: 0.1.0
status: draft
---

# OSMM Performance Measurement Builder

Build a valid **OSMM Performance Measurement Object** from any source reporting how a marketing strategy actually performed in a period.

A Performance Measurement Object is the structured record of **what actually happened** for a measurement period — the readings for each KPI, how each fared against its target, and a narrative readout. It is the Phase 7 Measurement object that records **actuals** against a **Measurement Framework**'s plan: where the framework says "breakfast daypart sales and repeat rate, targeted directionally up, reported monthly," this object says "breakfast daypart sales up mid-single digits, repeat rate ahead of plan — on track." It references the framework via `linked_measurement_framework` and reports against its metric **names**; it never re-defines the metrics.

This is the lean v0.1 builder. It captures the period's readings, variance, governed status, and a summary — and nothing more. It is **append-only**: each period is a *new instance*, not a new version of a prior one. A version bump corrects a recorded reading; a new period creates a new object.

One object type serves four Phase 7 sub-processes via the `dimension` facet. The Performance Measurement resolves workflow sub-processes **7.1** (overall performance), **7.3** (offer performance), **7.4** (creative performance), and **7.5** (journey/channel performance) (`TAXONOMY.md`): `overall` is the strategy-level rollup, and the other dimensions scope a reading to one subject — folding in the former per-dimension Offer, Creative, and Journey Performance objects so they need not exist as separate types.

**Key difference from Measurement Framework (Phase 1):** the Measurement Framework is the durable *plan* — what will be measured and the targets. The Performance Measurement Object records the *actuals* against it and is append-only. "What we'll measure and the goal" lives there; "what actually happened" lives here. The framework defines and names each metric; this object reports its reading and **must not redefine it** — it points back via `linked_measurement_framework` and echoes the metric names.

**Key difference from Customer Insight (Phase 7):** a Performance Measurement reports **the number — what happened**; a Customer Insight explains **the 'why' — the interpreted meaning behind the numbers**. The Performance Measurement is the measured reading ("breakfast repeat rate landed behind plan"); the Customer Insight is the interpretation drawing on one or more Performance Measurements ("breakfast repeat lags because the value bundle skews to existing lunch customers"). Record the reading here; interpret it there.

## The output schema

> **Canonical schema:** [`schemas/performance_measurement.schema.json`](../../schemas/performance_measurement.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "performance_measurement",      // const — always "performance_measurement"
  "osmm_version": "0.1.0",                        // schema version this conforms to
  "performance_measurement_id": "PFM-<slug>",    // stable id, scoped to subject + period (see ID rules)
  "version": "1.0",                              // instance version; bump only to correct a reading
  "status": "draft",                             // draft | proposed | stable | deprecated

  "name": "",                                    // readable label, usually subject + period ("Wendy's FY2026 Q1 Performance")
  "linked_measurement_framework": "",            // id of the framework this reports against (MEF-<slug>; placeholder ok)
  "dimension": "overall",                        // overall | offer | creative | journey | channel | experience | campaign
  "subject_reference": "",                       // OPTIONAL — the measured object when dimension != overall (OFR-/CRS-/JNY-/EXP-/CMS-)

  "period": {                                    // the window these readings cover
    "start": "",                                 // period start (ISO date or readable label, e.g. "2026-01-01" or "FY2026 Q1")
    "end": "",                                   // OPTIONAL — period end
    "label": ""                                  // OPTIONAL — human label ("FY2026 Q1")
  },

  "metrics": [                                   // the readings — one per KPI measured (>= 1)
    {
      "name": "",                                // metric name — should match a metric in the linked framework
      "actual": "",                              // the recorded reading (value or banded/directional; keep public examples honest)
      "target": "",                              // OPTIONAL — echo of the framework's target
      "variance": "",                            // OPTIONAL — actual vs. target, directional or quantified ("+4 pts", "below plan")
      "status": "",                              // OPTIONAL — ahead | on_track | behind | met | missed | no_target (governed enum)
      "note": ""                                 // OPTIONAL — short context on the reading (data caveat, driver)
    }
  ],

  "summary": "",                                 // OPTIONAL — narrative readout: what performed and the headline takeaways
  "linked_business_context": "",                 // OPTIONAL — owning Business Context (BIZ-<slug>; placeholder ok)
  "linked_marketing_strategy": "",               // OPTIONAL — the Marketing Strategy this period evaluates (MKS-<slug>; placeholder ok)
  "source": ""                                   // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"performance_measurement"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `performance_measurement_id` | string | yes | `PFM-<slug>`, scoped to subject + period. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. Bump only to correct a recorded reading. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Readable label, usually subject + period: "Wendy's FY2026 Q1 Performance". |
| `linked_measurement_framework` | string | yes | `MEF-<slug>` of the framework these readings report against. `MEF-PLACEHOLDER-<slug>` if unbuilt. Reference the framework; never redefine its metrics. |
| `dimension` | enum | yes | `overall` \| `offer` \| `creative` \| `journey` \| `channel` \| `experience` \| `campaign` — see vocabulary below. |
| `subject_reference` | string | no | The specific object measured when `dimension` is not `overall` (e.g. `OFR-`, `CRS-`, `JNY-`, `EXP-`, `CMS-`). Omit for `overall`. Use `<PREFIX>-PLACEHOLDER-<slug>` until the subject exists. |
| `period` | object | yes | `{ start (required), end?, label? }` — the window these readings cover. |
| `period.start` | string | yes | ISO date or readable label (e.g. `2026-01-01` or `FY2026 Q1`). |
| `period.end` | string | no | Period end. Omit for an open or single-label period. |
| `period.label` | string | no | Human label for the period (e.g. `FY2026 Q1`). |
| `metrics` | object[] | yes | The readings, one per KPI measured (≥ 1). Each requires `name` and `actual`; `target`, `variance`, `status`, `note` are optional. |
| `metrics[].name` | string | yes | Should match a metric defined in the linked Measurement Framework. |
| `metrics[].actual` | string | yes | The recorded reading — value or banded/directional result. Keep public examples honest. |
| `metrics[].target` | string | no | Echo of the framework's target being measured against. |
| `metrics[].variance` | string | no | Actual vs. target, directional or quantified ("+4 pts", "below plan"). |
| `metrics[].status` | enum | no | `ahead` \| `on_track` \| `behind` \| `met` \| `missed` \| `no_target` — see vocabulary below. |
| `metrics[].note` | string | no | Short context on the reading (data caveat, driver). |
| `summary` | string | no | Narrative readout for the period — what performed and the headline takeaways. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` if unbuilt. |
| `linked_marketing_strategy` | string | no | `MKS-<slug>` of the Marketing Strategy this period evaluates. `MKS-PLACEHOLDER-<slug>` if unbuilt. |
| `source` | string | no | One line. Provenance and approximate date. |

## Governed vocabularies

### `dimension` — the lens of the measurement

`dimension` is a governed enum. Exactly one per object. It is what lets one object type serve four sub-processes: pick `overall` for the strategy-level rollup, or scope the reading to a single subject with one of the others and set `subject_reference`.

| Stored value | Use when measuring… | Sub-process | `subject_reference` |
|---|---|---|---|
| `overall` | The strategy-level rollup across all metrics | 7.1 | Omit. |
| `offer` | One offer's performance | 7.3 | `OFR-<slug>` |
| `creative` | One creative strategy / asset's performance | 7.4 | `CRS-<slug>` |
| `journey` | One customer journey's performance | 7.5 | `JNY-<slug>` |
| `channel` | One channel's performance | 7.5 | (channel object id) |
| `experience` | One experience's performance | 7.x | `EXP-<slug>` |
| `campaign` | One campaign's performance | 7.x | `CMS-<slug>` |

### `metrics[].status` — the read of a metric vs. its target

`status` is a governed enum giving each reading a one-token verdict against its target. Optional per metric; use `no_target` when the framework set none.

| Stored value | Use for |
|---|---|
| `ahead` | Reading is beating its target with the period still open. |
| `on_track` | Reading is pacing to plan for an in-progress target. |
| `behind` | Reading is lagging its target with the period still open. |
| `met` | A closed-period target that was achieved. |
| `missed` | A closed-period target that was not achieved. |
| `no_target` | The framework set no target for this metric — record the reading without a verdict. |

## ID rules

`performance_measurement_id` = `PFM-` + a lowercase, hyphen-delimited slug. Scope it to the **subject plus the period** so each reading is uniquely addressable:

- Wendy's, FY2026 Q1, overall → `PFM-wendys-2026-q1` (reports against `MEF-wendys-2026`)
- IBM, FY2026 Q1, overall → `PFM-ibm-2026-q1` (reports against `MEF-ibm-2026`)
- A scoped reading folds the subject into the slug, e.g. `PFM-ibm-watsonx-offer-2026-q1` for a `dimension: "offer"` reading.

Keep it stable once assigned. Each period is a **new instance** (append-only), never an overwrite — the next quarter is `PFM-wendys-2026-q2`, not a new version of Q1. The `version` field bumps only to **correct a recorded reading** within a period.

## Extraction principles

1. **Record actuals, never redefine metrics.** The metric `name` and definition live in the Measurement Framework. Echo each framework metric `name` exactly and report its `actual`; do not invent new metrics here. If the source has a reading with no matching framework metric, flag it rather than smuggling a new metric into the framework's scope.
2. **One instance per period — append, don't overwrite.** Each measurement period is a fresh `PFM-` instance scoped by ID. Never edit last period's object to hold this period's numbers. Reserve `version` bumps for correcting a mis-recorded reading.
3. **Pick the dimension, then scope it.** Use `overall` for the strategy rollup. For a single offer, creative, journey, channel, experience, or campaign, set the matching `dimension` and point `subject_reference` at that object — this is how 7.3/7.4/7.5 are served without separate object types.
4. **Keep readings honest.** When building from public sources, record directional or banded actuals ("up mid-single digits," "ahead of plan") rather than inventing precise figures. Echo the framework's `target`, set `variance` directionally, and give a governed `status`. Note any data caveat in the metric `note`.
5. **Status is a verdict, not a vibe.** Use the `status` enum deliberately: `ahead`/`on_track`/`behind` for in-flight targets, `met`/`missed` for closed ones, `no_target` where the framework set none. Don't mark `met` on a target the framework never defined.
6. **Summarize, don't interpret.** The `summary` is a readout of what the numbers say. The *why* — the causal interpretation — belongs in a Customer Insight that draws on this object, not here.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One instance per subject-and-period. Save using the OSMM instance-naming convention: `PERFORMANCE-MEASUREMENT_<subject-slug>-<period-slug>.json` (e.g. `PERFORMANCE-MEASUREMENT_wendys-2026-q1.json`). The `performance_measurement_id` (`PFM-<slug>`) is the id *inside* the object, not the filename.
- Set `linked_measurement_framework` to the real `MEF-<slug>` if it exists; otherwise use `MEF-PLACEHOLDER-<slug>`. Do the same `BIZ-`/`MKS-`/placeholder handling for `linked_business_context` and `linked_marketing_strategy`.
- When `dimension` is not `overall`, set `subject_reference` to the measured object's id (placeholder form until it exists); omit it for `overall`.
- Validate it parses and conforms to the schema before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out any reading that lacks a matching framework metric or a clear target so they can reconcile it.

## Starter prompts

**From an analytics export or KPI dashboard:**
> Build an OSMM Performance Measurement Object for [Brand], period [FY2026 Q1], reporting actuals against [framework / MEF id]. Sources: [analytics export / KPI dashboard / scorecard actuals]. For each framework metric record the actual, echo its target, set variance and a governed status, and write a short summary of what performed.

**From a campaign or per-dimension performance report:**
> Build an OSMM Performance Measurement Object for [Brand]'s [offer / creative / journey] [name], period [FY2026 Q1]. Set the right `dimension` and `subject_reference`, report the actuals against the linked framework's metrics, and flag any reading that has no matching framework metric.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical instances would live in `examples/measurement/`; the blocks below illustrate the shape and validate against the schema. Each reports against the corresponding Measurement Framework worked example (`MEF-wendys-2026`, `MEF-ibm-2026`) and echoes its metric names.

### Example 1 — B2C challenger (Wendy's, FY2026 Q1, overall)

Reports against `MEF-wendys-2026`. `dimension: "overall"` — the strategy-level rollup, so no `subject_reference`. Actuals are directional/banded and honest, with governed `status` reads and a `summary`.

```json
{
  "object_type": "performance_measurement",
  "osmm_version": "0.1.0",
  "performance_measurement_id": "PFM-wendys-2026-q1",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's FY2026 Q1 Performance",
  "linked_measurement_framework": "MEF-wendys-2026",
  "dimension": "overall",
  "period": {
    "start": "2026-01-01",
    "end": "2026-03-31",
    "label": "FY2026 Q1"
  },
  "metrics": [
    {
      "name": "Social-attributed visit lift",
      "actual": "Positive, measurable visit lift on the two largest social moments; smaller moments inconclusive",
      "target": "Positive, measurable visit lift per major social moment",
      "variance": "On plan for major moments; below plan on minor ones",
      "status": "on_track",
      "note": "Lift-study read; minor moments below the modeling detectability threshold"
    },
    {
      "name": "Breakfast daypart sales and repeat rate",
      "actual": "Breakfast sales up mid-single digits year-over-year; repeat rate up slightly",
      "target": "Breakfast sales and repeat up year-over-year",
      "variance": "Sales ahead of plan; repeat roughly on plan",
      "status": "ahead"
    },
    {
      "name": "Digital sales mix and loyalty enrollment",
      "actual": "Digital sales mix up year-over-year; net new Wendy's Rewards enrollments grew double digits",
      "target": "Digital mix and loyalty base up year-over-year",
      "variance": "Ahead of plan on loyalty enrollment",
      "status": "ahead"
    },
    {
      "name": "Quality-plus-value perception",
      "actual": "Quality and value scores held steady vs. key burger-QSR competitors",
      "target": "Sustain quality-plus-value perception",
      "variance": "Holding; no erosion during the value-menu cycle",
      "status": "on_track",
      "note": "Quarterly brand-tracker read; single quarter, directional"
    },
    {
      "name": "Franchisee value-menu margin health",
      "actual": "Franchisee value-menu contribution margin down slightly as value promotions scaled",
      "target": "Hold or improve vs. prior year",
      "variance": "Modestly below plan",
      "status": "behind",
      "note": "Guardrail under mild pressure — watch as value promotions continue"
    }
  ],
  "summary": "Q1 was on track to ahead overall: social moments drove measurable visit lift, breakfast and digital/loyalty ran ahead of plan, and brand perception held. The one watch item is the franchisee value-menu margin guardrail, which dipped slightly as value promotions scaled — flagged for the next review.",
  "linked_business_context": "BIZ-wendys",
  "linked_marketing_strategy": "MKS-wendys-2026",
  "source": "Built from public information: The Wendy's Company public filings and public reporting on the brand's marketing (2024). Readings are illustrative and directional, inferred from public strategic priorities; not internal actuals."
}
```

### Example 2 — B2B enterprise (IBM, FY2026 Q1, offer-scoped, abbreviated)

Reports against `MEF-ibm-2026`. Shown as a scoped reading — `dimension: "offer"` with `subject_reference` pointing at the watsonx offer (placeholder until built). Abbreviated, like the framework's Example 2.

```json
{
  "object_type": "performance_measurement",
  "osmm_version": "0.1.0",
  "performance_measurement_id": "PFM-ibm-watsonx-offer-2026-q1",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Offer — FY2026 Q1 Performance",
  "linked_measurement_framework": "MEF-ibm-2026",
  "dimension": "offer",
  "subject_reference": "OFR-PLACEHOLDER-ibm-watsonx",
  "period": {
    "start": "FY2026 Q1",
    "label": "FY2026 Q1"
  },
  "metrics": [
    {
      "name": "watsonx consideration / shortlist rate",
      "actual": "Shortlist rate up year-over-year; gap to hyperscaler shortlist rates narrowed modestly",
      "target": "Up year-over-year; closing the gap to hyperscaler shortlist rates",
      "variance": "On plan",
      "status": "on_track",
      "note": "Quarterly consideration tracker; directional read"
    },
    {
      "name": "Red Hat-attached hybrid cloud pipeline",
      "actual": "Marketing-sourced Red Hat / OpenShift-attached pipeline grew quarter-over-quarter",
      "variance": "No framework target set",
      "status": "no_target"
    }
  ],
  "summary": "watsonx offer performance was on plan in Q1: consideration ticked up and Red Hat-attached pipeline grew, though the framework set no explicit pipeline target to grade against.",
  "linked_business_context": "BIZ-ibm",
  "linked_marketing_strategy": "MKS-ibm-2026",
  "source": "Built from public information: IBM 2023 Annual Report, earnings commentary, and ibm.com (2024). Readings are illustrative and directional; not internal actuals."
}
```
