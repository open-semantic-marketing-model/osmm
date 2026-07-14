---
name: osmm-customer-insight-builder
description: >-
  Turn analysis into a structured OSMM Customer Insight Object (canonical JSON): a durable,
  interpreted finding about why customers behaved or responded the way they did. Inputs include
  analytics readouts, voice-of-customer (VoC) research, survey results, support/CSAT logs, churn
  analyses, A/B test learnings, and Performance Measurement objects. Use this skill whenever the
  user wants to capture the why behind the numbers — "capture a customer insight," "structure what
  we learned about our audience," "turn this analysis into an insight object," "record why
  customers behaved this way," or "build a customer insight object." This is the Phase 7 Learning
  object that closes the loop, proposing durable updates back into the Context layer.
object: Customer Insight Object
object_type: customer_insight
category: Learning Object
phase: 7
wave: 7
osmm_version: 0.1.0
status: draft
---

# OSMM Customer Insight Builder

Build a valid **OSMM Customer Insight Object** from any source describing what was learned about customer behavior or response.

A Customer Insight Object is the structured record of a **durable, interpreted finding** about how customers behave or respond — the *why* behind the numbers. Where a Performance Measurement says "checkout abandonment rose 9 points in Q1," the Customer Insight says "deal-savvy cravers abandon at the payment step because of surprise fees, not price sensitivity." It is interpretation, not measurement: one insight typically draws on **several Performance Measurements** (via `evidence.linked_performance_measurements`) plus **external research** (`evidence.external_sources`) and reconciles them into a single conclusion.

This is the lean v0.1 builder. It captures the finding, its evidence, who it is about, and the durable changes it proposes back into the Context layer — and nothing more. The `insight_statement` is an **interpreted conclusion, not a metric**. Numbers live in Performance Measurement; the Customer Insight is the reading of them.

The Customer Insight resolves workflow sub-process **7.2** (`TAXONOMY.md`): structuring durable learnings about the customer. It also **closes the loop**, contributing to sub-process **7.7** — the Context-layer write-back — via its `proposes_updates_to[]` pointers.

**Key difference from Performance Measurement (Phase 7):** the Performance Measurement is the *number* — append-only actuals against a Measurement Framework. The Customer Insight is the *interpreted why* drawn from those numbers. "Abandonment rose 9 points" is a Performance Measurement; "they abandon over surprise fees, not price" is a Customer Insight. The insight points back at the measurements that evidence it via `evidence.linked_performance_measurements`; the measurements do not know about the insight.

**Key difference from Optimization Recommendation (Phase 7):** an insight is a **diagnosis**; a recommendation is a **prescription**. The Customer Insight is the durable *finding* — it stays true and is referenced over time. An Optimization Recommendation is the proposed *action* — it gets actioned, then closed. One durable insight can spawn many recommendations. Keep the finding here; keep the proposed actions there. (Note the narrow exception: `proposes_updates_to[]` carries durable *Context-layer* changes the finding implies — a new version of a Persona or Strategy — not tactical campaign actions, which belong to a recommendation.)

## The output schema

> **Canonical schema:** [`schemas/customer_insight.schema.json`](../../schemas/customer_insight.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "customer_insight",         // const — always "customer_insight"
  "osmm_version": "0.1.0",                    // schema version this conforms to
  "customer_insight_id": "CIN-<slug>",        // stable, human-readable id (see ID rules)
  "version": "1.0",                           // instance version; bump on revision
  "status": "draft",                          // draft | proposed | stable | deprecated

  "name": "",                                 // short readable label (e.g. "Deal-savvy cravers abandon at the payment step")
  "insight_statement": "",                    // the finding as an interpreted conclusion — NOT a metric

  "confidence": "",                           // OPTIONAL — low | medium | high (governed enum)

  "evidence": {                               // OPTIONAL — what the insight is drawn from
    "linked_performance_measurements": [],    //   ids of evidencing Performance Measurements (PFM-<slug>; placeholder ok)
    "external_sources": []                    //   non-OSMM evidence (VoC, support logs, research) as free text
  },

  "affected_personas": [],                    // OPTIONAL — personas the insight is about (PER-<slug>; placeholder ok)
  "affected_audiences": [],                   // OPTIONAL — audiences the insight is about (AUD-<slug>; placeholder ok)
  "segment_note": "",                         // OPTIONAL — free-text scope when the group isn't a modeled Persona/Audience yet

  "implication": "",                          // OPTIONAL — the "so what" for downstream marketing decisions

  "proposes_updates_to": [                    // OPTIONAL — the Context-layer write-back (sub-process 7.7)
    {
      "target_id": "",                        //   id of the object to update (PER-, BRC-, PRC-, BIZ-, MKS-; placeholder ok)
      "recommended_change": ""                //   prose description of the proposed change to that object
    }
  ],

  "linked_business_context": "",              // OPTIONAL — id of the owning Business Context (BIZ-<slug>; placeholder ok)
  "source": ""                                // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"customer_insight"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `customer_insight_id` | string | yes | `CIN-<slug>`. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | `draft` \| `proposed` \| `stable` \| `deprecated`. Default `"draft"`. |
| `name` | string | yes | Short readable label for the finding. |
| `insight_statement` | string | yes | The finding, stated as an interpreted conclusion — **not a metric**. The "why" behind the numbers. |
| `confidence` | enum | no | `low` \| `medium` \| `high` — how well-supported by evidence. See vocabulary below. |
| `evidence` | object | no | What the insight is drawn from. Holds `linked_performance_measurements` and `external_sources`. |
| `evidence.linked_performance_measurements` | string[] | no | `PFM-<slug>` ids of the Performance Measurements that evidence this insight. `PFM-PLACEHOLDER-<slug>` if unbuilt. |
| `evidence.external_sources` | string[] | no | Non-OSMM evidence (VoC studies, support/CSAT logs, surveys, analyst research) as free text. |
| `affected_personas` | string[] | no | `PER-<slug>` ids the insight is about. `PER-PLACEHOLDER-<slug>` if unbuilt. |
| `affected_audiences` | string[] | no | `AUD-<slug>` ids the insight is about. `AUD-PLACEHOLDER-<slug>` if unbuilt. |
| `segment_note` | string | no | Free-text scope when the affected group is not yet a modeled Persona or Audience. |
| `implication` | string | no | The "so what" — why this matters for downstream marketing decisions. |
| `proposes_updates_to` | object[] | no | The Context-layer write-back (sub-process 7.7). Each item is a lean pointer + prose. See ID rules and Extraction principles. |
| `proposes_updates_to[].target_id` | string | yes (within item) | `^[A-Z]{3}-...` — id of the object to update (e.g. `PER-`, `BRC-`, `PRC-`, `BIZ-`, `MKS-`). Placeholder ok. |
| `proposes_updates_to[].recommended_change` | string | yes (within item) | Prose description of the proposed change to that object. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` if unbuilt. |
| `source` | string | no | One line. Provenance and approximate date. |

## Confidence vocabulary

`confidence` is a governed enum — how well-supported the finding is by its evidence. Optional, but worth setting deliberately so downstream consumers know how much weight to put on the insight.

| Stored value | Label | Use for |
|---|---|---|
| `low` | Low | A plausible reading from thin or single-source evidence — one survey, anecdotal support logs, or a directional move not yet corroborated. Treat as a hypothesis to validate. |
| `medium` | Medium | A finding supported by more than one signal that line up, but with gaps — e.g. one Performance Measurement plus qualitative VoC, no controlled test. The working interpretation. |
| `high` | High | A finding triangulated across multiple Performance Measurements and external sources, ideally including a controlled test (A/B, lift study). Safe to act on and to propose Context-layer changes from. |

## ID rules

`customer_insight_id` = `CIN-` + a lowercase, hyphen-delimited slug that **describes the finding**, not just the brand. The slug should let a reader guess the insight from the id alone:

- Wendy's surprise-fee abandonment finding → `CIN-wendys-checkout-fee-friction`
- IBM enterprise trust/governance finding → `CIN-ibm-watsonx-trust-gap`

Keep it stable once assigned. Revising the finding bumps `version`; the id never changes. A genuinely different finding is a new object with its own `CIN-` id.

## Extraction principles

1. **State a conclusion, not a number.** `insight_statement` must read as an interpretation — *why* something happened. If your draft statement is a metric ("abandonment rose 9 points"), you have written a Performance Measurement, not an insight. Restate it as the reading: "they abandon over surprise fees, not price."
2. **Show your evidence.** An insight without evidence is an opinion. Link the Performance Measurements that ground it (`evidence.linked_performance_measurements`) and cite the qualitative sources (`evidence.external_sources`). One insight commonly reconciles several measurements plus research — that triangulation is the value.
3. **Set confidence honestly.** Use the enum to signal how far the evidence actually reaches. A single survey is `low`; a finding triangulated across measurements and a controlled test is `high`. Don't inflate confidence to make the insight sound stronger.
4. **Name who it's about.** Tie the finding to the `affected_personas` or `affected_audiences` it concerns. If the group isn't modeled yet, use `segment_note` rather than forcing a placeholder id that may never resolve.
5. **Separate the finding from the so-what.** `insight_statement` is the durable diagnosis; `implication` is why it matters for the next decision. Keep tactical actions out of both — those are Optimization Recommendations.
6. **Close the loop with lean pointers.** When a finding implies a durable change to a Context-layer object, record it in `proposes_updates_to[]` as `{target_id, recommended_change}` — a pointer plus prose. This is deliberately lean: there is **no structured field-level patch**. The insight only *records* the proposal; **applying** a change is a separate act that produces a **new version of the target object** (a new Persona, Brand/Product/Business Context, or Marketing Strategy version). The insight never patches the target itself.
7. **Don't restate the source.** Personas, strategies, and metric definitions live in their own objects. Reference them by id and interpret them; don't duplicate their content here.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One Customer Insight per finding. Save using the OSMM instance-naming convention: `CUSTOMER-INSIGHT_<finding-slug>.json` (e.g. `CUSTOMER-INSIGHT_wendys-checkout-fee-friction.json`). The `customer_insight_id` (`CIN-<slug>`) is the id *inside* the object, not the filename.
- Set evidence and affected-group ids to real ids if they exist; otherwise use the `PLACEHOLDER` form (`PFM-PLACEHOLDER-<slug>`, `PER-PLACEHOLDER-<slug>`, etc.).
- `proposes_updates_to[]` records proposals only — it does **not** apply them. When the user accepts a proposed change, **tell them to rebuild/revise the target object and bump that object's `version`**; the new version is the result of the write-back. Note that the target object does not gain a back-pointer — this edge is one-directional by design.
- Validate it parses and conforms to the schema before returning it.
- Briefly tell the user what you interpreted vs. extracted, what `confidence` you set and why, and which Context-layer updates you are proposing so they can decide whether to apply them.

## Starter prompts

**From a performance readout plus research:**
> Build an OSMM Customer Insight Object from this analysis of [Brand]'s [metric / behavior]. Evidence: [PFM ids] plus [VoC / survey / support-log / churn / A/B-test source]. State the finding as an interpreted conclusion (the *why*), set confidence honestly, name the affected persona/audience, and propose any durable Context-layer updates it implies.

**From raw voice-of-customer or support logs:**
> Turn these [VoC interviews / CSAT and support logs / survey results] into an OSMM Customer Insight Object for [Brand]. Capture what we learned about [audience], cite the qualitative sources (and any Performance Measurements that corroborate), flag the confidence as low/medium, and note what it implies for our personas or strategy.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below illustrate the shape; validated canonical instances live in `examples/learning/`.

### Example 1 — B2C challenger (Wendy's)

A payment-step abandonment finding for deal-savvy cravers: the cause is surprise fees, not price. Triangulates a Performance Measurement with support-log VoC, and closes the loop with two proposed Context-layer updates — one to the persona, one to the strategy.

```json
{
  "object_type": "customer_insight",
  "osmm_version": "0.1.0",
  "customer_insight_id": "CIN-wendys-checkout-fee-friction",
  "version": "1.0",
  "status": "draft",
  "name": "Deal-savvy cravers abandon at the payment step over surprise fees",
  "insight_statement": "Deal-savvy cravers who add a discounted item to their cart abandon disproportionately at the payment step, not the menu — the trigger is service and delivery fees surfacing late in checkout, which reads as a bait-and-switch on the advertised value, not genuine price sensitivity. They will pay the food price; they balk when the total jumps after they have committed.",
  "confidence": "medium",
  "evidence": {
    "linked_performance_measurements": ["PFM-wendys-2026-q1"],
    "external_sources": [
      "Wendy's app store reviews and public social complaints citing 'hidden fees' and 'sticker shock at checkout' (2025-2026)",
      "Support / CSAT log theme analysis: fee-related abandonment and complaint volume on app and delivery orders (Q1 2026)"
    ]
  },
  "affected_personas": ["PER-wendys-deal-savvy-craver"],
  "segment_note": "Concentrated in app and third-party delivery orders where fees are added after item selection; far weaker on in-store and drive-thru.",
  "implication": "The value message that drives the visit is being undercut at the moment of payment, leaking conversions the marketing spend already paid to create. Fee transparency is a conversion lever, not just a service issue — surfacing the all-in price earlier could recover abandoned deal-led orders.",
  "proposes_updates_to": [
    {
      "target_id": "PER-wendys-deal-savvy-craver",
      "recommended_change": "Add a key friction point: 'late-surfacing service/delivery fees at checkout read as broken value promise and trigger abandonment.' Update purchase triggers to note that all-in price transparency, not just a low headline price, drives conversion for this persona."
    },
    {
      "target_id": "MKS-wendys-2026",
      "recommended_change": "Add a conversion-integrity consideration to the digital/value strategy: advertised deal value must hold through to the order total. Treat early, all-in fee transparency in the app and delivery flows as a strategic lever supporting the value-menu objective."
    }
  ],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: Wendy's app store reviews, public social complaints, and reported app/delivery fee practices (2025-2026), interpreted against a Q1 2026 performance readout. Support-log theme is illustrative of public complaint patterns, not internal data."
}
```

### Example 2 — B2B enterprise (IBM, abbreviated)

An enterprise-trust finding shaping watsonx shortlisting. Cites a Performance Measurement plus analyst research, is about an audience rather than a single persona, and proposes one Brand Context update. Shown abbreviated.

```json
{
  "object_type": "customer_insight",
  "osmm_version": "0.1.0",
  "customer_insight_id": "CIN-ibm-watsonx-trust-gap",
  "version": "1.0",
  "status": "draft",
  "name": "Enterprise buyers shortlist watsonx on trust and governance, not raw capability",
  "insight_statement": "When enterprise IT buyers shortlist enterprise AI platforms, watsonx advances or drops on data governance, security, and IP-indemnification confidence rather than headline model capability — buyers assume baseline capability across vendors and decide on whether they can deploy safely on their own data without legal or compliance exposure. The shortlist gap to hyperscalers is a trust gap, not a feature gap.",
  "confidence": "high",
  "evidence": {
    "linked_performance_measurements": ["PFM-ibm-2026-q1"],
    "external_sources": [
      "Industry analyst research on enterprise generative-AI adoption barriers, citing governance, data privacy, and IP/indemnification as top shortlist criteria (2025-2026)",
      "Public enterprise AI buyer surveys ranking trust and compliance above raw model performance for production deployment"
    ]
  },
  "affected_audiences": ["AUD-ibm-enterprise-it"],
  "implication": "Capability-led messaging competes on a dimension buyers treat as table stakes. Leading with governance, security, and indemnification — IBM's differentiators — addresses the actual shortlist criterion and is more likely to move consideration.",
  "proposes_updates_to": [
    {
      "target_id": "BRC-ibm",
      "recommended_change": "Elevate enterprise trust — data governance, security, and IP indemnification — to a primary, proof-led message pillar for watsonx, ahead of raw model capability, reflecting that this is the decisive shortlist criterion for enterprise AI buyers."
    }
  ],
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: industry analyst commentary on enterprise AI adoption barriers and public enterprise AI buyer surveys (2025-2026), interpreted against a Q1 2026 performance readout. Not based on internal IBM data."
}
```
