---
name: osmm-optimization-recommendation-builder
description: >-
  Convert any learning-loop output into a structured OSMM Optimization Recommendation Object
  (canonical JSON). Inputs include test readouts, QBR action items, optimization backlogs,
  insight summaries, and performance reviews. Use this skill whenever the user wants to turn
  evidence into a prioritized, actionable change — "turn this insight into a recommendation,"
  "structure our optimization backlog," "what should we change based on these results,"
  "build an optimization recommendation object," or "log a prioritized optimization." This is
  the Learning Object that prescribes a change to a strategy or work product, derived from
  Customer Insights and Performance Measurements, and tracked to a disposition.
object: Optimization Recommendation Object
object_type: optimization_recommendation
category: Learning Object
phase: 7
wave: 7
osmm_version: 0.1.0
status: draft
---

# OSMM Optimization Recommendation Builder

Build a valid **OSMM Optimization Recommendation Object** from any source describing a change that should be made off the back of the learning loop.

An Optimization Recommendation Object is the structured record of **a prioritized, actionable change** — the prescription. Where a **Customer Insight** explains *what is true and why* (the diagnosis), an Optimization Recommendation says *what to do about it* (the prescription), states why, and writes forward into the Work Product / Strategy layer by naming the objects it would change. It is derived from the evidence the learning loop produced: the Customer Insights it acts on (`derived_from.linked_customer_insights[]`, `CIN-`) and the Performance Measurements that motivate it (`derived_from.linked_performance_measurements[]`, `PFM-`).

This is the lean v0.1 builder. It captures the change, the rationale, its priority and effort, the expected impact, where it would land, and whether it has been acted on — and nothing more. It is deliberately **not** a patch format: a `targets[]` entry is a lean pointer plus prose, not a field-level diff. Applying an accepted recommendation produces a **new version of the target object**; this object only records the proposal.

The Optimization Recommendation resolves workflow sub-process **7.6** (`TAXONOMY.md`): turning learning into prioritized, actioned change. It is the input to the non-normative **Optimization Plan** composer, which reads a set of these to render a human optimization plan.

**Key difference from Customer Insight (Phase 7):** the Customer Insight is the **diagnosis** — a durable, evidence-backed finding about what is true. The Optimization Recommendation is the **prescription** — a specific change proposed in response. One insight can spawn many recommendations. The insight stays durable and reusable; the recommendation is actioned and then closed (it reaches a terminal `disposition`). Diagnosis lives there; the prescribed action lives here.

**Key difference from Marketing Strategy (Phase 1):** a recommendation **proposes a change** to a strategy or work product and is **tracked to a disposition** — it does not itself restate the strategy. A Marketing Strategy (or Campaign Strategy, Offer, Creative Strategy, Journey, Experience) is the durable plan; an Optimization Recommendation names that object in `targets[]` and describes, in prose, the change it wants made. Applying an **accepted** recommendation produces a **new version of the target object**. Don't copy the strategy's content into the recommendation; point at it and describe the delta.

## The output schema

> **Canonical schema:** [`schemas/optimization_recommendation.schema.json`](../../schemas/optimization_recommendation.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "optimization_recommendation",      // const — always "optimization_recommendation"
  "osmm_version": "0.1.0",                            // schema version this conforms to
  "optimization_recommendation_id": "OPR-<slug>",     // stable, human-readable id (see ID rules)
  "version": "1.0",                                   // instance version; bump on revision
  "status": "draft",                                  // object lifecycle: draft | proposed | stable | deprecated

  "name": "",                                         // short readable label (e.g. "Add fee transparency to app checkout")
  "recommendation": "",                               // the proposed change, stated as an action — the prescription
  "rationale": "",                                    // why this change — connects the evidence to the action

  "derived_from": {                                   // OPTIONAL — the evidence chain behind the recommendation
    "linked_customer_insights": [],                   // OPTIONAL — Customer Insights this acts on (CIN-<slug>)
    "linked_performance_measurements": []             // OPTIONAL — Performance Measurements that motivate it (PFM-<slug>)
  },

  "priority": "",                                     // OPTIONAL — low | medium | high | critical (governed enum)
  "effort": "",                                       // OPTIONAL — low | medium | high (governed enum)
  "expected_impact": "",                              // OPTIONAL — what improvement is expected; directional or quantified

  "disposition": "",                                  // OPTIONAL — proposed | accepted | rejected | implemented | deferred (NOT status)

  "targets": [                                        // OPTIONAL — the write-forward: objects this change would land in
    {
      "target_id": "",                                // id of the object the change targets (MKS-/CMS-/OFR-/CRS-/JNY-/EXP- …)
      "recommended_change": ""                        // prose description of the change to that object
    }
  ],

  "linked_business_context": "",                      // OPTIONAL — owning Business Context (BIZ-<slug>; placeholder ok)
  "source": ""                                        // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"optimization_recommendation"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `optimization_recommendation_id` | string | yes | `OPR-<slug>`. See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Object lifecycle: `draft` \| `proposed` \| `stable` \| `deprecated`. Default `"draft"`. **Not** `disposition`. |
| `name` | string | yes | Short readable label for the change. |
| `recommendation` | string | yes | The proposed change, stated as an action — the prescription. |
| `rationale` | string | yes | Why this change — the reasoning that connects the evidence to the action. |
| `derived_from` | object | no | The evidence chain. Both arrays optional. |
| `derived_from.linked_customer_insights` | string[] | no | Customer Insights acted on. `CIN-<slug>` (or `CIN-PLACEHOLDER-<slug>`). |
| `derived_from.linked_performance_measurements` | string[] | no | Performance Measurements that motivate it. `PFM-<slug>` (or `PFM-PLACEHOLDER-<slug>`). |
| `priority` | enum | no | `low` \| `medium` \| `high` \| `critical` — see vocabulary below. |
| `effort` | enum | no | `low` \| `medium` \| `high` — see vocabulary below. |
| `expected_impact` | string | no | What improvement is expected if implemented — directional or quantified. Keep public examples honest. |
| `disposition` | enum | no | `proposed` \| `accepted` \| `rejected` \| `implemented` \| `deferred` — whether it was acted on. See vocabulary below. Defaults to `proposed` in practice. |
| `targets` | object[] | no | The write-forward. Each requires `target_id` and `recommended_change`. |
| `targets[].target_id` | string | yes (within a target) | Id of the object the change targets: `^[A-Z]{3}-...` (e.g. `MKS-`, `CMS-`, `OFR-`, `CRS-`, `JNY-`, `EXP-`). Placeholder form allowed. |
| `targets[].recommended_change` | string | yes (within a target) | Prose description of the change to that object — not a field-level patch. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` if unbuilt. |
| `source` | string | no | One line. Provenance and approximate date. |

## Governed vocabularies

Three fields are governed enums. Each stores a lowercase token. `priority` and `effort` size the recommendation; `disposition` tracks whether it has been acted on — and is distinct from the lifecycle `status`.

### `priority` — how urgently to act

| Stored value | Use for |
|---|---|
| `low` | Nice-to-have; act on it when capacity allows. No material downside to waiting. |
| `medium` | Worth doing this planning cycle; meaningful but not blocking. |
| `high` | A clear, evidenced opportunity or problem that should be addressed soon. |
| `critical` | Acute — material revenue, trust, or compliance exposure if left unaddressed. Escalate. |

### `effort` — rough cost to implement

| Stored value | Use for |
|---|---|
| `low` | A small, contained change — copy, a setting, a single screen. Days, not weeks. |
| `medium` | Multi-team or multi-step work — a flow change plus a test, new creative across channels. |
| `high` | Significant build or coordination — new capability, platform work, broad rollout. |

### `disposition` — whether it was acted on (NOT the lifecycle `status`)

| Stored value | Use for |
|---|---|
| `proposed` | Logged and awaiting a decision. The default starting state. |
| `accepted` | Approved to do; the change will be applied to the target(s) in a new version. |
| `rejected` | Decided against. Keep the record — a rejected recommendation is still learning. |
| `implemented` | The change has been applied to the target object(s). |
| `deferred` | Acknowledged but parked — revisit next cycle. |

Keep `status` and `disposition` separate. `status` is the OSMM object's lifecycle (is this *object* a draft or stable record?). `disposition` is about the *real-world decision* (did we accept and ship the change?). A `stable`, well-formed recommendation can carry any disposition; a `draft` record can already be `accepted`.

## ID rules

`optimization_recommendation_id` = `OPR-` + a lowercase, hyphen-delimited slug that **describes the change**, scoped to the business. Make the slug read like the headline of the change, not the insight behind it:

- Wendy's, surface all checkout fees → `OPR-wendys-checkout-fee-transparency`
- IBM, lead with watsonx governance proof → `OPR-ibm-watsonx-governance-proof`

Keep it stable once assigned. A revision bumps `version`, not the id. A genuinely different change — even from the same insight — is a new recommendation with its own id.

## Extraction principles

1. **Prescription, not diagnosis.** The `recommendation` is an action — something a team can do ("surface all fees on the checkout review screen and A/B test it"), not a restatement of the problem. If you find yourself describing what is wrong, that belongs in the Customer Insight; here, say what to change.
2. **Show the evidence chain.** Tie the recommendation back to the Customer Insight(s) it acts on and the Performance Measurement(s) that motivate it via `derived_from`. A recommendation with no evidence behind it is an opinion — flag it and ask for the insight or measurement.
3. **Name where it lands.** Use `targets[]` to point at the actual Work Product / Strategy objects the change would modify (`MKS-`, `CMS-`, `OFR-`, `CRS-`, `JNY-`, `EXP-`), with a prose `recommended_change` for each. Keep it a pointer plus prose — do not write a field-level patch. Applying the change is a new version of the *target*, not an edit here.
4. **Size it honestly.** Set `priority` and `effort` so a backlog can be triaged. Don't mark everything `high`/`high`; the value of the field is the contrast between items.
5. **Separate lifecycle from decision.** Set `status` for the record's lifecycle and `disposition` for whether it was acted on. New recommendations are usually `status: draft`, `disposition: proposed`.
6. **One change per object.** If a source bundles several distinct changes, split them into separate recommendations — each addressable, prioritizable, and dispositionable on its own. A shared insight is fine; they just reference the same `CIN-`.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One change per object. Save using the OSMM instance-naming convention: `OPTIMIZATION-RECOMMENDATION_<change-slug>.json` (e.g. `OPTIMIZATION-RECOMMENDATION_wendys-checkout-fee-transparency.json`). The `optimization_recommendation_id` (`OPR-<slug>`) is the id *inside* the object, not the filename.
- Set `derived_from` links to the real `CIN-`/`PFM-` ids if they exist; otherwise use the `*-PLACEHOLDER-*` form and tell the user to resolve them. Do the same `BIZ-`/placeholder handling for `linked_business_context`.
- Set each `targets[].target_id` to the real object id if it exists; otherwise use the placeholder form. When a recommendation is **accepted/implemented**, remind the user that applying it produces a **new version of the target object** — this object does not patch the target.
- Default new records to `status: "draft"` and `disposition: "proposed"` unless the source tells you otherwise.
- Validate it parses and conforms to the schema before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out any recommendation missing an evidence link or a target so they can fill the gap.

## Starter prompts

**From an insight or test readout:**
> Turn this into an OSMM Optimization Recommendation Object for [Brand]. Insight: [CIN id / summary]. Evidence: [PFM id / test readout]. State the change as an action, give the rationale, set priority and effort, name the target object(s) it would change, and set disposition to proposed.

**From an optimization backlog or QBR action items:**
> Structure our optimization backlog as OSMM Optimization Recommendation Objects for [Brand]. For each item, write one recommendation: the change, the rationale, derived-from links to the insight and measurement behind it, priority/effort, expected impact, the target object(s), and disposition. Split bundled items into separate recommendations and flag any without supporting evidence.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical instances live in `examples/learning/` (`OPTIMIZATION-RECOMMENDATION_wendys-checkout-fee-transparency.json`, `OPTIMIZATION-RECOMMENDATION_ibm-watsonx-governance-proof.json`) — they are read independently by the Optimization Plan composer, so they are promoted there; the blocks below illustrate the shape.

### Example 1 — B2C challenger (Wendy's): surface checkout fees

Acts on `CIN-wendys-checkout-fee-friction` and the measurement that quantified the drop-off. It writes forward into the app order Journey and the checkout Experience; disposition is `proposed` (logged, awaiting a decision).

```json
{
  "object_type": "optimization_recommendation",
  "osmm_version": "0.1.0",
  "optimization_recommendation_id": "OPR-wendys-checkout-fee-transparency",
  "version": "1.0",
  "status": "draft",
  "name": "Add fee transparency to app checkout",
  "recommendation": "Surface all fees — service, delivery, and small-order fees — itemized on the app checkout review screen before the customer commits, and A/B test this transparent flow against the current late-reveal flow.",
  "rationale": "Customers abandon at the final step when previously hidden fees appear at payment, reading the late reveal as a bait-and-switch. Showing the full price earlier sets expectations up front and is expected to recover abandoned orders and reduce post-order complaints, even if some customers drop earlier in the funnel.",
  "derived_from": {
    "linked_customer_insights": ["CIN-wendys-checkout-fee-friction"],
    "linked_performance_measurements": ["PFM-wendys-app-checkout-funnel"]
  },
  "priority": "high",
  "effort": "medium",
  "expected_impact": "Directional: lower final-step abandonment and fewer fee-related complaints; net order volume measured by the A/B test rather than assumed.",
  "disposition": "proposed",
  "targets": [
    {
      "target_id": "JNY-wendys-app-order",
      "recommended_change": "Move the full fee breakdown from the payment step to the checkout review step so the all-in price is visible before commitment."
    },
    {
      "target_id": "EXP-wendys-app-checkout",
      "recommended_change": "Redesign the checkout review screen to itemize service, delivery, and small-order fees, and run it as the variant in an A/B test against the current flow."
    }
  ],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: public reporting and app-store reviews on QSR app delivery/service-fee complaints (2024). Insight and funnel measurement referenced are illustrative OSMM instances, not internal Wendy's data."
}
```

### Example 2 — B2B enterprise (IBM, abbreviated): lead with watsonx governance proof

Acts on `CIN-ibm-watsonx-trust-gap`. Shown abbreviated; the full instance is `examples/learning/OPTIMIZATION-RECOMMENDATION_ibm-watsonx-governance-proof.json`.

```json
{
  "object_type": "optimization_recommendation",
  "osmm_version": "0.1.0",
  "optimization_recommendation_id": "OPR-ibm-watsonx-governance-proof",
  "version": "1.0",
  "status": "draft",
  "name": "Lead watsonx messaging with governance and trust proof",
  "recommendation": "Reorder watsonx creative and nurture to lead with governance, security, and trust proof points — model governance, data privacy, and customer references — ahead of raw capability claims, for enterprise AI buyers comparing watsonx to hyperscaler alternatives.",
  "rationale": "Enterprise buyers shortlist on trust and governance before features; a perceived trust gap, not a capability gap, is what stalls watsonx evaluations. Leading with proof of governance is expected to lift consideration and progress more evaluations to shortlist.",
  "derived_from": {
    "linked_customer_insights": ["CIN-ibm-watsonx-trust-gap"]
  },
  "priority": "high",
  "effort": "medium",
  "expected_impact": "Directional: higher watsonx shortlist/consideration rate among tracked enterprise AI evaluations.",
  "disposition": "proposed",
  "targets": [
    {
      "target_id": "CRS-ibm-watsonx",
      "recommended_change": "Reorder the creative narrative to open on governance, security, and trust proof, with capability claims supporting rather than leading."
    },
    {
      "target_id": "MKS-ibm-2026",
      "recommended_change": "Elevate enterprise-trust and governance positioning as a lead message for the watsonx portfolio in the 2026 strategy."
    }
  ],
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: IBM watsonx positioning on ibm.com and public commentary on enterprise AI governance/trust (2024). Referenced insight is an illustrative OSMM instance."
}
```
