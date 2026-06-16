---
name: osmm-journey-strategy-builder
description: >-
  Convert any customer-journey source into a structured OSMM Journey Strategy Object (canonical
  JSON). Inputs include customer journey maps, lifecycle journey plans, journey/flow diagrams,
  triggering & sequencing logic, cadence rules, stage definitions, or a marketer's notes on the
  path a customer should travel. Use this skill whenever the user wants to capture the orchestrated
  path a customer travels — "build a journey strategy object," "map our customer journey," "design
  a lifecycle journey," "structure our journey strategy," "define the customer path and stages,"
  "capture our triggering and sequencing logic," or hands over a journey map and asks what to do
  with it. This is the orchestrated path a customer travels — the journey goal, the stages, the
  triggers that advance them, and the sequencing/cadence. It may serve one campaign or run
  always-on as a lifecycle journey. It is NOT the Campaign Strategy (scope/channel/offer mapping)
  and NOT the Journey Configuration (the Phase 6 operational implementation).
object: Journey Strategy Object
object_type: journey_strategy
category: Work Product
phase: 4
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Journey Strategy Builder

Build a valid **OSMM Journey Strategy Object** from any source describing the path a customer
should travel.

A Journey Strategy Object is the **orchestrated customer path** — the journey goal, the stages a
customer moves through, the triggers that advance them from one stage to the next, and the
sequencing/cadence logic that paces the whole thing. It is a Phase 4 **Work Product**: a typed
record of *how a customer is meant to move*, distinct from the campaign that may drive them and
from the operational system that later runs the journey. Downstream messaging, experience, and the
Phase 6 Journey Configuration all reference this path, so making it explicit means every later
decision is anchored to the same stages and triggers instead of re-deriving them.

A journey can serve a **single campaign** *or* run **always-on as a lifecycle journey** independent
of any one campaign (a welcome/onboarding flow, a winback program, a loyalty nurture). Because of
this, its link to a Campaign Strategy is **optional** — set `linked_campaign_strategy` only when
the journey is tied to a specific campaign; omit it for an always-on journey.

This is the lean v0.1 builder. It captures the strategic shape of the journey — the path, the
triggers, the pacing — and nothing more. The operational implementation (the platform flow nodes,
wait steps, audience-sync mechanics, message bindings) is deliberately out of scope; it belongs to
the **Journey Configuration Object** (Phase 6).

The Journey Strategy resolves workflow sub-processes **4.2, 4.5, and 4.8** (`TAXONOMY.md`): the
journey strategy / goals / customer path (4.2), the triggering & sequencing logic and cadence
(4.5), and the confirmed journey direction (4.8).

## Boundaries — what this object is and is NOT

The Journey Strategy sits between a Phase 4 sibling and its Phase 6 implementation. Keeping the
lines clean is the whole point of giving the journey its own object:

| Object | Answers | Phase | Example |
|--------|---------|------:|---------|
| **Campaign Strategy** | What's the *campaign* — its scope, channels, offer, and timing window? | 4 | "Watsonx Launch — Q2 enterprise demand-gen across paid, events, and web, mapped to the trial offer" |
| **Journey Strategy** (this) | What's the *orchestrated path* a customer travels — the goal, stages, triggers, and sequencing/cadence? | 4 | "Awareness → Consideration → Trial → Deal, advanced by content download, demo request, and trial start" |
| **Journey Configuration** | How is the journey *operationally built* in the platform — flow nodes, wait steps, audience syncs, message bindings? | 6 | "The marketing-automation flow that implements the journey: entry audience, delays, branch conditions, sends" |

Rules of thumb:

- **Campaign Strategy is the *what/where/offer*; Journey Strategy is the *path/triggers/pacing*.**
  Channel-and-offer mapping for a campaign lives in Campaign Strategy. A journey may *reference* a
  campaign (`linked_campaign_strategy`) but does not restate its scope or offer mapping.
- **A journey can stand alone.** An always-on lifecycle journey serves no single campaign — leave
  `linked_campaign_strategy` unset and classify it with `journey_type: lifecycle` (or the closest
  motion). The link is optional precisely so standalone journeys are first-class.
- **Strategy, not implementation.** This object captures the *designed* path and triggering logic.
  The platform flow that runs it — node-by-node, with wait timers and message bindings — is the
  **Journey Configuration Object** in Phase 6. Capture the logic here; defer the build there.

## The output schema

> **Canonical schema:** [`schemas/journey_strategy.schema.json`](../../../schemas/journey_strategy.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "journey_strategy",       // const — always "journey_strategy"
  "osmm_version": "0.1.0",                 // schema version this conforms to
  "journey_strategy_id": "JNS-<slug>",     // stable, human-readable id (see ID rules)
  "version": "1.0",                        // instance version; bump on revision
  "status": "draft",                       // draft | proposed | stable | deprecated

  "name": "",                              // the journey's name (e.g. "Wendy's App First-Order to Habitual-Use Journey")
  "journey_goal": "",                      // the outcome the journey drives (4.2)
  "journey_type": "",                      // OPTIONAL — controlled enum (see vocabulary): acquisition | onboarding | nurture | conversion | retention | winback | advocacy | lifecycle

  "stages": [                              // the customer path — ordered stages (4.2)
    {
      "stage": "",                         // stage name
      "objective": "",                     // what this stage is trying to achieve
      "touchpoints": [],                   // OPTIONAL — interactions/messages in this stage
      "entry_criteria": "",                // OPTIONAL — what moves a customer into this stage
      "exit_criteria": ""                  // OPTIONAL — what moves them out
    }
  ],
  "triggers": [                            // the triggering logic (4.5)
    {
      "trigger": "",                       // the event/condition that fires
      "action": "",                        // the response it fires
      "timing": ""                         // OPTIONAL — when, relative to the trigger
    }
  ],
  "sequencing_logic": "",                  // OPTIONAL — how stages/messages are sequenced; overall pacing (4.5)
  "cadence": "",                           // OPTIONAL — frequency/pacing guidance
  "channels": [],                          // OPTIONAL — touchpoint channels across the journey

  "entry_criteria": [],                    // OPTIONAL — who/what enters the journey
  "exit_criteria": [],                     // OPTIONAL — who/what exits

  "linked_campaign_strategy": "",          // OPTIONAL — CMS-<slug> if the journey serves a campaign; omit for always-on
  "linked_audiences": [],                  // OPTIONAL — AUD-<slug> ids this journey serves
  "linked_personas": [],                   // OPTIONAL — PER-<slug> ids this journey is designed around
  "linked_business_context": "",           // OPTIONAL — BIZ-<slug> of the owning Business Context
  "source": ""                             // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"journey_strategy"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `journey_strategy_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | A readable label for the journey, usually entity + journey: "Wendy's App First-Order to Habitual-Use Journey". |
| `journey_goal` | string | yes | The single outcome the journey drives (4.2). An outcome, not an activity — "turn first-time app orderers into habitual users," not "send onboarding emails." |
| `journey_type` | enum | no | Controlled vocabulary — see below. Pick the single closest motion; use `lifecycle` for an always-on journey spanning several. |
| `stages` | object[] | yes | The ordered customer path (4.2). Each `{ stage, objective, touchpoints?, entry_criteria?, exit_criteria? }`. Array order is journey order. 2–6 stages is usually right. `stage` and `objective` required per item. |
| `triggers` | object[] | yes | The triggering logic (4.5). Each `{ trigger, action, timing? }`. `trigger` and `action` required per item. The events that advance a customer and what each fires. |
| `sequencing_logic` | string | no | How stages/messages are sequenced — ordering, branching, overall pacing (4.5). |
| `cadence` | string | no | Frequency/pacing guidance (contact limits, suppression windows). |
| `channels` | string[] | no | The touchpoint channels used across the journey (Email, Push, SMS, Paid social, …). |
| `entry_criteria` | string[] | no | Who/what enters the journey overall (distinct from a stage's entry). |
| `exit_criteria` | string[] | no | Who/what exits — completion, disqualification, opt-out. |
| `linked_campaign_strategy` | string | no | `CMS-<slug>` of the Campaign Strategy this journey serves, **only if tied to one**. Omit for an always-on lifecycle journey. Use `CMS-PLACEHOLDER-<slug>` if expected but unbuilt. |
| `linked_audiences` | string[] | no | `AUD-<slug>` ids the journey serves. References, not restated definitions. `AUD-PLACEHOLDER-<slug>` ok. |
| `linked_personas` | string[] | no | `PER-<slug>` ids the journey is designed around. `PER-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## Journey type vocabulary

`journey_type` is a controlled, governed enum — a stored snake_case-style token (single words here)
mapped to a human-readable label. Pick the single closest; don't invent new values per project.

| Stored value | Label | Use when |
|---|---|---|
| `acquisition` | Acquisition | The journey turns a new prospect into a first customer. |
| `onboarding` | Onboarding | The journey activates a new customer into productive first use. |
| `nurture` | Nurture | The journey develops an unready prospect/customer over time toward readiness. |
| `conversion` | Conversion | The journey drives a specific decision/purchase among ready buyers. |
| `retention` | Retention | The journey sustains an active customer's frequency or value. |
| `winback` | Winback | The journey re-engages a lapsed or churned customer. |
| `advocacy` | Advocacy | The journey turns a loyal customer into a referrer/advocate. |
| `lifecycle` | Lifecycle | An always-on journey spanning several of the motions above (e.g. acquisition → onboarding → retention). |

If a journey spans motions, choose the dominant framing or use `lifecycle`, and let `stages`
carry the detail.

## ID rules

`journey_strategy_id` = `JNS-` + a lowercase, hyphen-delimited slug. Scope it to the **entity plus
the journey**, so multiple journeys for the same brand stay distinct and obvious:

- Wendy's app first-order → habitual-use → `JNS-wendys-app-habit` (pairs with `BIZ-wendys`)
- IBM watsonx enterprise evaluation → `JNS-ibm-watsonx-eval` (pairs with `BIZ-ibm`)

Keep it stable once assigned: downstream objects (the Phase 6 Journey Configuration) reference it.
On revision bump `version`, never the id.

## Extraction principles

1. **A journey may stand alone.** Not every journey serves a campaign. If the source describes an
   always-on lifecycle, welcome, winback, or loyalty flow, leave `linked_campaign_strategy` unset
   and classify it (`journey_type: lifecycle` or the closest motion). The campaign link is optional
   by design.
2. **Goal is an outcome, not an activity.** `journey_goal` is the result the path is meant to
   produce ("convert first-time app orderers into habitual users"), not the mechanics ("send three
   onboarding emails"). Keep stage objectives at the outcome level too.
3. **Stages are the path; triggers are the movement.** `stages` capture *where a customer is*;
   `triggers` capture *what advances them*. A trigger usually maps to a stage transition (the event
   that fires the move and the action it takes). Keep them in the right array.
4. **Reference audiences/personas, don't restate them.** `linked_audiences` and `linked_personas`
   hold ids; the segment criteria and persona detail live in those objects. The journey only says
   *who* it serves.
5. **Strategy, not implementation.** Capture the designed path, triggering logic, and pacing — not
   the platform build. Flow nodes, wait timers, audience-sync mechanics, and message bindings are
   the Phase 6 Journey Configuration. If the source is an implemented flow, distill its *strategy*
   here and note the implementation belongs downstream.
6. **Keep Campaign Strategy out.** Channel/offer/scope mapping for a campaign is the Campaign
   Strategy Object. A journey references a campaign; it does not duplicate its scope or offer.
7. **Keep arrays signal-bearing.** A tight set of real stages and triggers beats a long generic
   list. 2–6 stages and a matched set of triggers is usually right. Resist padding.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per journey. Save using the OSMM instance-naming convention:
  `JOURNEY-STRATEGY_<entity-slug>.json` (e.g. `JOURNEY-STRATEGY_wendys-app-habit.json`) — uppercase
  object name, underscore join, lowercase entity slug; append an instance slug when a brand has more
  than one journey. See `CONVENTION.md` → "Instance file naming". The `journey_strategy_id`
  (`JNS-<slug>`) remains the id *inside* the object; it is not the filename.
- Set `linked_campaign_strategy` to the real `CMS-<slug>` only if the journey serves a campaign;
  use a `CMS-PLACEHOLDER-<slug>` if it's expected but unbuilt, and **omit it entirely** for an
  always-on journey. Do the same for `linked_audiences` (`AUD-`), `linked_personas` (`PER-`), and
  `linked_business_context` (`BIZ-`) — real ids where they exist, placeholders otherwise.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin in the source
  (especially missing triggers or stage objectives) so they can fill gaps.

## Starter prompts

**From a journey map or lifecycle plan:**
> Build an OSMM Journey Strategy Object for [Brand]'s [journey name]. Sources: [journey map / flow
> diagram / lifecycle plan / triggering rules]. Capture the journey goal, the stages and their
> objectives, the triggers that advance customers, and the sequencing/cadence. Link the audiences,
> personas, and Business Context; link the Campaign Strategy only if this journey serves one.

**For an always-on lifecycle journey (no campaign):**
> Build an OSMM Journey Strategy Object for [Brand]'s always-on [onboarding / winback / loyalty]
> journey. It serves no single campaign — set `journey_type` to the right motion (or `lifecycle`)
> and leave the campaign link unset. Capture the goal, stages, triggers, and cadence; flag anything
> that's actually an implementation detail as belonging to the Phase 6 Journey Configuration.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below
illustrate the shape; both validate against `schemas/journey_strategy.schema.json`.

### Example 1 — B2C always-on lifecycle journey (Wendy's app, no campaign)

Built from Wendy's public app, loyalty, and marketing material. An always-on journey, so
`linked_campaign_strategy` is omitted. References the shipped `BIZ-wendys`,
`AUD-wendys-value-seekers`, and `PER-wendys-deal-savvy-craver`.

```json
{
  "object_type": "journey_strategy",
  "osmm_version": "0.1.0",
  "journey_strategy_id": "JNS-wendys-app-habit",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's App First-Order to Habitual-Use Journey",
  "journey_goal": "Turn new Wendy's app users into habitual, app-led repeat customers by driving a first mobile order and building order frequency over time.",
  "journey_type": "lifecycle",
  "stages": [
    {
      "stage": "Acquisition",
      "objective": "Get a value-seeking customer to download the app and create an account.",
      "touchpoints": ["In-store QR/app prompts", "Paid social app-install ads", "Offer-led app landing page"],
      "entry_criteria": "Prospect engages with an app-download prompt or install ad",
      "exit_criteria": "App installed and account created"
    },
    {
      "stage": "Onboarding",
      "objective": "Convert the new account into a first mobile order with a welcome offer.",
      "touchpoints": ["Welcome push", "First-order offer (e.g. free Baconator with first app order)", "Onboarding email"],
      "entry_criteria": "Account created, no orders yet",
      "exit_criteria": "First app order placed"
    },
    {
      "stage": "Retention",
      "objective": "Build order frequency and Wendy's Rewards engagement into a habit.",
      "touchpoints": ["Personalized offers", "Rewards-balance nudges", "Daypart-relevant push (breakfast, late-night)"],
      "entry_criteria": "At least one app order placed",
      "exit_criteria": "Sustained repeat ordering, or lapse into winback"
    }
  ],
  "triggers": [
    { "trigger": "App download and account creation", "action": "Send welcome push and surface the first-order offer", "timing": "Immediately" },
    { "trigger": "First app order placed", "action": "Advance to Retention; enroll/encourage Wendy's Rewards and send a follow-up offer", "timing": "Within 24h of order" },
    { "trigger": "14 days without an app order", "action": "Fire a lapse-recovery offer to pull the customer back to a repeat order", "timing": "Day 14 after last order" }
  ],
  "sequencing_logic": "Acquisition → Onboarding → Retention, gated by the first order; lapse routes a Retention customer into a recovery offer rather than dropping them.",
  "cadence": "No more than 2-3 messages per week; suppress promotional push for 48h after any order; respect daypart relevance.",
  "channels": ["Push", "Email", "Paid social", "In-store"],
  "entry_criteria": ["New Wendy's app installs among value-seeking, mobile-first customers"],
  "exit_criteria": ["Customer uninstalls or opts out", "Sustained habitual ordering (graduates to BAU loyalty)"],
  "linked_audiences": ["AUD-wendys-value-seekers"],
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: wendys.com, the Wendy's app and Wendy's Rewards public pages, and public reporting on the brand's digital marketing (2024). Triggers and cadence are illustrative, not internal configuration."
}
```

### Example 2 — B2B campaign-served evaluation journey (IBM watsonx)

Built from IBM's public watsonx marketing and trial flow. This journey serves a launch campaign, so
`linked_campaign_strategy` points to a placeholder Campaign Strategy until that object is built.
References the shipped `BIZ-ibm`.

```json
{
  "object_type": "journey_strategy",
  "osmm_version": "0.1.0",
  "journey_strategy_id": "JNS-ibm-watsonx-eval",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Enterprise Evaluation Journey",
  "journey_goal": "Move enterprise AI buyers from first awareness of watsonx through hands-on evaluation to a qualified sales opportunity.",
  "journey_type": "acquisition",
  "stages": [
    {
      "stage": "Awareness",
      "objective": "Reach enterprise AI decision-makers and establish watsonx as a governed, hybrid-cloud AI platform.",
      "touchpoints": ["Thought-leadership content", "Paid search and social", "Analyst and event presence"],
      "entry_criteria": "Buyer engages watsonx awareness content",
      "exit_criteria": "Buyer downloads gated content or returns for deeper material"
    },
    {
      "stage": "Consideration",
      "objective": "Deepen interest with proof and use-case content; capture intent.",
      "touchpoints": ["Gated whitepapers and webinars", "Use-case and ROI content", "Nurture emails"],
      "entry_criteria": "Content download captured",
      "exit_criteria": "Demo requested"
    },
    {
      "stage": "Trial",
      "objective": "Get the buyer hands-on with watsonx to prove value on their use case.",
      "touchpoints": ["Guided trial / sandbox", "Solution-engineering follow-up", "Trial activation emails"],
      "entry_criteria": "Demo completed or trial started",
      "exit_criteria": "Active trial usage indicating intent"
    },
    {
      "stage": "Deal",
      "objective": "Convert qualified evaluation into a sales opportunity and close.",
      "touchpoints": ["Sales/SE engagement", "Tailored proposal", "IBM Consulting deployment conversation"],
      "entry_criteria": "Trial usage and fit signals meet qualification bar",
      "exit_criteria": "Opportunity created and handed to sales"
    }
  ],
  "triggers": [
    { "trigger": "Content download", "action": "Advance to Consideration and start the use-case nurture track", "timing": "Immediately" },
    { "trigger": "Demo request submitted", "action": "Route to sales/SE and provision trial access", "timing": "Within 1 business day" },
    { "trigger": "Trial started", "action": "Begin trial-activation sequence and monitor usage for qualification", "timing": "On trial provisioning" }
  ],
  "sequencing_logic": "Awareness → Consideration → Trial → Deal, with intent gating each transition; low-engagement leads stay in nurture rather than advancing.",
  "cadence": "Nurture touches roughly weekly during Consideration; activation touches more frequent during the active trial window; suppress nurture once sales-engaged.",
  "channels": ["Email", "Paid search", "Paid social", "Web", "Events"],
  "entry_criteria": ["Enterprise AI buyers (CDO/CIO/heads of AI) engaging watsonx awareness content"],
  "exit_criteria": ["Opportunity created (handed to sales)", "Disqualified or unengaged after nurture window"],
  "linked_campaign_strategy": "CMS-PLACEHOLDER-ibm-watsonx-launch",
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx, the watsonx trial and demo flow, and public IBM enterprise marketing (2024). Triggers, cadence, and qualification logic are illustrative, not internal configuration."
}
```
