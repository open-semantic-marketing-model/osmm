---
name: osmm-journey-builder
description: >-
  Convert any customer-journey source into a structured OSMM Journey Object (canonical JSON). Inputs include customer journey maps, lifecycle journey plans, journey/flow diagrams, triggering & sequencing logic, cadence rules, stage definitions, or the operational flow built in a marketing-automation platform. Use this skill whenever the user wants to capture the orchestrated path a customer travels — "build a journey object," "map our customer journey," "design a lifecycle journey," "structure our journey," "define the customer path and stages," "capture our triggering and sequencing logic," "configure the journey flow," or hands over a journey map or flow. The Journey Object spans end to end — the goal, the stages, the triggers, the sequencing/cadence, AND the operational delivery logic. A required scope facet separates the durable, persona-anchored lifecycle backbone from a campaign-scoped flow. It is NOT the Campaign Strategy.
object: Journey Object
object_type: journey
category: Work Product
phase: 4
wave: 3
osmm_version: 0.1.0
status: draft
---

# OSMM Journey Builder

Build a valid **OSMM Journey Object** from any source describing the path a customer travels.

A Journey Object is the **orchestrated customer path, strategy through delivery** — the journey
goal, the stages a customer moves through, the triggers that advance them from one stage to the
next, the sequencing/cadence that paces it, and the operational **delivery logic** that implements
it. It is a **Work Product**: a typed record of *how a customer is meant to move and how that
movement is operationalized*, distinct from the campaign that may drive them.

> **One object, strategy + configuration.** OSMM models the journey as a single object rather than
> a separate "journey strategy" and "journey configuration." The designed path (stages, triggers,
> cadence) and its operational build (flow shape, wait steps, audience syncs, message bindings) are
> two views of the same thing; splitting them produced a thin pair, so they are merged here. The
> strategic shape is the required core; the operational specifics live in the optional
> `delivery_logic` field. This object resolves sub-processes **4.2, 4.5, 4.8** (journey strategy /
> goals / path; triggering & sequencing; confirmed direction) **and 6.3** (configure journey &
> delivery logic).

> **The (persona × stage) cell — where questions and messages live.** Each stage carries
> `persona_tracks` — one per persona the journey serves — capturing that decision-maker's
> `buyer_goal`, `milestones`, `key_activities`, the `key_questions` in their mind, and the
> `key_messages` that respond. This is the home for two things OSMM no longer models as separate
> objects: **directional keywords** (the `key_questions` — just enough to point downstream teams,
> not an SEO database) and the **persona/journey layer of messaging**. Messaging cascades in three
> layers — **brand** (Brand Context `brand_promise` / `messaging_pillars`) → **product/solution**
> (Product Context `product_messaging` value pillars) → **persona × journey** (these
> `key_messages`) — and a *messaging-framework* artifact is composed by drawing from all three and
> resolving at this cell.

> **Scope: the durable backbone vs. the campaign slice.** A required `scope` facet classifies the
> journey. A **`lifecycle`** journey is the durable, always-on, persona-anchored backbone — the
> end-to-end view of how a persona experiences the brand (high-read, low-write, referenced by many
> campaigns). A **`campaign`** journey is a scoped activation flow that runs *within* that backbone
> for a specific campaign. **Campaigns are scoped slices within a broader journey**, so the
> canonical reference runs **Campaign Strategy → Journey** (the campaign's `linked_journey`): a
> Journey never points down at a campaign. A `lifecycle` journey must anchor to at least one
> **Persona** and **Audience** — the spine it is built around.

This is the lean v0.1 builder. It captures the strategic shape of the journey *and* the
decision-relevant delivery logic — not a raw platform export. Node-by-node automation dumps,
credentials, and vendor-specific config stay in the platform; distill the *logic* into the fields.

## Boundaries — what this object is and is NOT

| Object | Answers | Example |
|--------|---------|---------|
| **Campaign Strategy** | What's the *campaign* — its scope, channels, offer, and timing window? | "Watsonx Launch — Q2 enterprise demand-gen across paid, events, and web, mapped to the trial offer" |
| **Journey** (this) | What's the *orchestrated path* a customer travels — goal, stages, triggers, sequencing/cadence — and how is it operationally delivered? | "Awareness → Consideration → Trial → Deal, advanced by content download, demo request, and trial start; built as a nurture flow with intent-gated branches" |

Rules of thumb:

- **Campaign Strategy is the *what/where/offer*; Journey is the *path/triggers/pacing/delivery*.**
  Channel-and-offer mapping for a campaign lives in Campaign Strategy. The campaign *references* the
  journey (`Campaign Strategy.linked_journey`); the journey does not point back at the campaign or
  restate its scope or offer mapping.
- **The durable journey is the backbone; campaigns are slices of it.** A `scope: lifecycle` journey
  is the always-on, persona-anchored backbone (`journey_type: lifecycle` or the closest motion); a
  `scope: campaign` journey is a slice that runs within it for one campaign. Either way the journey
  is referenced *by* the campaign, never the reverse.
- **Strategy and configuration in one object.** Capture the designed path *and* its delivery logic
  here. The strategic shape (stages, triggers, cadence) is the required core; operational specifics
  (flow branches, wait steps, audience syncs, message bindings) go in `delivery_logic`. Keep it to
  decision-relevant logic, not a platform dump.

## The output schema

> **Canonical schema:** [`schemas/journey.schema.json`](../../../schemas/journey.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "journey",                // const — always "journey"
  "osmm_version": "0.1.0",                 // schema version this conforms to
  "journey_id": "JNY-<slug>",              // stable, human-readable id (see ID rules)
  "version": "1.0",                        // instance version; bump on revision
  "status": "draft",                       // draft | proposed | stable | deprecated

  "name": "",                              // the journey's name (e.g. "Wendy's App First-Order to Habitual-Use Journey")
  "scope": "",                             // REQUIRED — lifecycle | campaign (the durable backbone vs. a campaign-scoped slice)
  "journey_goal": "",                      // the outcome the journey drives (4.2)
  "journey_type": "",                      // OPTIONAL — controlled enum (see vocabulary): acquisition | onboarding | nurture | conversion | retention | winback | advocacy | lifecycle

  "stages": [                              // the customer path — ordered stages (4.2)
    {
      "stage": "",                         // stage name
      "objective": "",                     // what this stage is trying to achieve
      "touchpoints": [],                   // OPTIONAL — interactions/messages in this stage
      "entry_criteria": "",                // OPTIONAL — what moves a customer into this stage
      "exit_criteria": "",                 // OPTIONAL — what moves them out
      "persona_tracks": [                  // OPTIONAL — the (persona × stage) cell, one per persona the journey serves
        {
          "persona": "PER-<slug>",         // the Persona this track is for
          "buyer_goal": "",                // what this persona is trying to accomplish at this stage
          "milestones": [],                // milestones the buyer hits within the stage
          "key_activities": [],            // what the buyer is doing
          "key_questions": [],             // the questions/considerations in mind — directional "keywords", not an SEO database
          "key_messages": []               // the responses to those questions (draw from brand promise + product value pillars)
        }
      ]
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

  "delivery_logic": [],                    // OPTIONAL — operational delivery/configuration (6.3): flow shape, wait steps, audience syncs, branch conditions, message bindings

  "linked_audiences": [],                  // AUD-<slug> ids this journey serves (REQUIRED for scope: lifecycle — the spine)
  "linked_personas": [],                   // PER-<slug> ids this journey is designed around (REQUIRED for scope: lifecycle — the spine)
  "linked_business_context": "",           // OPTIONAL — BIZ-<slug> of the owning Business Context
  "source": ""                             // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"journey"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `journey_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | A readable label, usually entity + journey: "Wendy's App First-Order to Habitual-Use Journey". |
| `scope` | enum | yes | `lifecycle` (the durable, persona-anchored backbone — high-read, low-write, referenced by many campaigns) or `campaign` (a scoped slice that runs within a lifecycle journey for one campaign). A `lifecycle` journey **must** carry `linked_personas` and `linked_audiences`. |
| `journey_goal` | string | yes | The single outcome the journey drives (4.2). An outcome, not an activity — "turn first-time app orderers into habitual users," not "send onboarding emails." |
| `journey_type` | enum | no | Controlled vocabulary — see below. Pick the single closest motion; use `lifecycle` for an always-on journey spanning several. |
| `stages` | object[] | yes | The ordered customer path (4.2). Each `{ stage, objective, touchpoints?, entry_criteria?, exit_criteria?, persona_tracks? }`. Array order is journey order. 2–6 stages is usually right. `stage` and `objective` required per item. |
| `stages[].persona_tracks` | object[] | no | The **(persona × stage) cell** — one per persona the journey serves. Each `{ persona, buyer_goal?, milestones?, key_activities?, key_questions?, key_messages? }`; only `persona` is required. `key_questions` are the directional "keywords" (the considerations in the decision-maker's mind — *not* an SEO keyword database); `key_messages` are the responses, drawn from the brand promise (Brand Context) and product value pillars (Product Context `product_messaging`). |
| `triggers` | object[] | yes | The triggering logic (4.5). Each `{ trigger, action, timing? }`. `trigger` and `action` required per item. The events that advance a customer and what each fires. |
| `sequencing_logic` | string | no | How stages/messages are sequenced — ordering, branching, overall pacing (4.5). |
| `cadence` | string | no | Frequency/pacing guidance (contact limits, suppression windows). |
| `channels` | string[] | no | The touchpoint channels used across the journey (Email, Push, SMS, Paid social, …). |
| `entry_criteria` | string[] | no | Who/what enters the journey overall (distinct from a stage's entry). |
| `exit_criteria` | string[] | no | Who/what exits — completion, disqualification, opt-out. |
| `delivery_logic` | string[] | no | The operational build (6.3): flow shape, wait steps, branch conditions, audience-sync mechanics, message bindings. Decision-relevant logic, not a platform export. Omit if the journey is captured at the strategic level only. |
| `linked_audiences` | string[] | **conditional** | `AUD-<slug>` ids the journey serves — part of the spine. References, not restated definitions. `AUD-PLACEHOLDER-<slug>` ok. **Required (≥1) when `scope` is `lifecycle`.** |
| `linked_personas` | string[] | **conditional** | `PER-<slug>` ids the journey is designed around — the spine. `PER-PLACEHOLDER-<slug>` ok. **Required (≥1) when `scope` is `lifecycle`.** The journey does **not** reference the Campaign Strategy that uses it — that edge runs Campaign Strategy → Journey. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Provenance and approximate date. |

## Scope: `lifecycle` vs `campaign`

`scope` is a required, governed enum — the primary classifier separating the durable backbone from a campaign slice. Pick exactly one.

| Stored value | Label | Use when |
|---|---|---|
| `lifecycle` | Lifecycle backbone | The durable, always-on, persona-anchored journey — the end-to-end view of how a persona experiences the brand (a welcome/onboarding flow, a loyalty nurture, the full acquisition→retention path). High-read, low-write, referenced by many campaigns. **Must** anchor to ≥1 Persona and ≥1 Audience. |
| `campaign` | Campaign slice | A scoped activation flow that runs *within* a lifecycle journey for a specific campaign. Referenced by that campaign via `Campaign Strategy.linked_journey`. |

Either way the edge runs **Campaign Strategy → Journey**: a journey never points down at a campaign. A `scope: lifecycle` journey will usually also carry `journey_type: lifecycle`, but the two are independent — a `campaign`-scope slice can still be, say, a `winback` motion.

## Journey type vocabulary

`journey_type` is a controlled, governed enum — a stored token mapped to a human-readable label.
Pick the single closest; don't invent new values per project.

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

If a journey spans motions, choose the dominant framing or use `lifecycle`, and let `stages` carry
the detail.

## ID rules

`journey_id` = `JNY-` + a lowercase, hyphen-delimited slug. Scope it to the **entity plus the
journey**, so multiple journeys for the same brand stay distinct and obvious:

- Wendy's app first-order → habitual-use → `JNY-wendys-app-habit` (pairs with `BIZ-wendys`)
- IBM watsonx enterprise evaluation → `JNY-ibm-watsonx-eval` (pairs with `BIZ-ibm`)

Keep it stable once assigned: campaigns and downstream objects reference it. On revision bump
`version`, never the id.

## Extraction principles

1. **Set `scope` first — backbone or slice.** Decide whether the source describes the durable,
   always-on backbone (`scope: lifecycle` — a welcome/onboarding/loyalty/winback program or the full
   acquisition→retention path) or a campaign-scoped flow (`scope: campaign`). A `lifecycle` journey
   must anchor to ≥1 Persona and ≥1 Audience. Never add a campaign reference *to* the journey — the
   campaign references the journey, not the reverse.
2. **Goal is an outcome, not an activity.** `journey_goal` is the result the path is meant to
   produce, not the mechanics. Keep stage objectives at the outcome level too.
3. **Stages are the path; triggers are the movement.** `stages` capture *where a customer is*;
   `triggers` capture *what advances them*. A trigger usually maps to a stage transition. Keep them
   in the right array.
4. **Reference audiences/personas, don't restate them.** `linked_audiences` and `linked_personas`
   hold ids; the segment criteria and persona detail live in those objects.
5. **Strategy and configuration, one object — but stay decision-relevant.** Capture the designed
   path *and* the delivery logic that implements it (`delivery_logic`). Do not transcribe a raw
   platform export: distill the flow shape, branch conditions, wait steps, audience syncs, and
   message bindings into readable logic. If the source is purely strategic, omit `delivery_logic`;
   if it's an implemented flow, capture both the strategy (stages/triggers) and the build.
6. **Keep Campaign Strategy out — and don't point at it.** Channel/offer/scope mapping for a
   campaign is the Campaign Strategy Object, which references the journey via `linked_journey`. The
   journey carries no campaign reference and does not duplicate a campaign's scope or offer.
7. **Keep arrays signal-bearing.** A tight set of real stages and triggers beats a long generic
   list. 2–6 stages and a matched set of triggers is usually right. Resist padding.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per journey. Save using the OSMM instance-naming convention:
  `JOURNEY_<entity-slug>.json` (e.g. `JOURNEY_wendys-app-habit.json`) — uppercase object name,
  underscore join, lowercase entity slug; append an instance slug when a brand has more than one
  journey. See `CONVENTION.md` → "Instance file naming". The `journey_id` (`JNY-<slug>`) remains the
  id *inside* the object; it is not the filename.
- Set `scope` explicitly (`lifecycle` or `campaign`). For a `lifecycle` journey, include at least
  one `linked_personas` (`PER-`) and one `linked_audiences` (`AUD-`) — the schema requires the spine.
  Use real ids where they exist, `…-PLACEHOLDER-<slug>` otherwise. Set `linked_business_context`
  (`BIZ-`) the same way. Do **not** add any campaign reference to the journey — the Campaign Strategy
  links to the journey via its `linked_journey`, not vice versa.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin (especially
  missing triggers or stage objectives) so they can fill gaps.

## Starter prompts

**From a journey map or lifecycle plan:**
> Build an OSMM Journey Object for [Brand]'s [journey name]. Sources: [journey map / flow diagram /
> lifecycle plan / triggering rules]. Set `scope` (`lifecycle` for the durable backbone, `campaign`
> for a campaign slice). Capture the journey goal, the stages and their objectives, the triggers that
> advance customers, the sequencing/cadence, and any operational delivery logic. Anchor it to the
> personas and audiences it's built around (required for a lifecycle journey) and the Business Context.

**For an always-on lifecycle journey (the durable backbone):**
> Build an OSMM Journey Object for [Brand]'s always-on [onboarding / winback / loyalty] journey. Set
> `scope: lifecycle` and `journey_type` to the right motion (or `lifecycle`), and anchor it to the
> persona(s) and audience(s) it serves. Capture the goal, stages, triggers, cadence, and the delivery
> logic. Campaigns will reference this journey — do not add a campaign link here.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below
illustrate the shape; both validate against `schemas/journey.schema.json`.

### Example 1 — B2C lifecycle backbone (Wendy's app)

Built from Wendy's public app, loyalty, and marketing material. The durable, persona-anchored
backbone, so `scope: lifecycle` and it carries the required Persona/Audience spine; no campaign
reference (campaigns reference *it*). Includes `delivery_logic` to show the absorbed configuration
view. References the shipped `BIZ-wendys`, `AUD-wendys-value-seekers`, and `PER-wendys-deal-savvy-craver`.

```json
{
  "object_type": "journey",
  "osmm_version": "0.1.0",
  "journey_id": "JNY-wendys-app-habit",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's App First-Order to Habitual-Use Journey",
  "scope": "lifecycle",
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
      "exit_criteria": "First app order placed",
      "persona_tracks": [
        {
          "persona": "PER-wendys-deal-savvy-craver",
          "buyer_goal": "Get the most food for the money on a first app order without friction",
          "milestones": ["Opened the welcome offer", "Built a first mobile order", "Redeemed the offer"],
          "key_activities": ["Browsing the app menu", "Comparing the deal to the in-store price", "Checking how to redeem"],
          "key_questions": ["is the app deal actually worth it?", "how do I redeem the free Baconator?", "is mobile order faster than the line?"],
          "key_messages": ["Your first app order comes with a free Baconator — more food for less", "Skip the line: order ahead and pick up"]
        }
      ]
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
  "delivery_logic": [
    "Entry: app-install/account-created event syncs the user into the journey audience",
    "Onboarding branch: if no order within 72h of account creation, resend the first-order offer once",
    "Order event exits the user from Onboarding and enrolls them in the Retention track",
    "Lapse branch: a 14-day no-order timer fires the recovery offer; two misses route to a winback journey",
    "Suppression: a 48h post-order hold blocks promotional push across all branches"
  ],
  "linked_audiences": ["AUD-wendys-value-seekers"],
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: wendys.com, the Wendy's app and Wendy's Rewards public pages, and public reporting on the brand's digital marketing (2024). Triggers, cadence, and delivery logic are illustrative, not internal configuration."
}
```

### Example 2 — B2B campaign-scoped evaluation journey (IBM watsonx)

Built from IBM's public watsonx marketing and trial flow. A `scope: campaign` slice that runs for a
launch campaign — the **Campaign Strategy references this journey** via its `linked_journey`, not the
reverse, so the journey carries no campaign field. References the shipped `BIZ-ibm`.

```json
{
  "object_type": "journey",
  "osmm_version": "0.1.0",
  "journey_id": "JNY-ibm-watsonx-eval",
  "version": "1.0",
  "status": "draft",
  "name": "IBM watsonx Enterprise Evaluation Journey",
  "scope": "campaign",
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
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-ai-buyer"],
  "linked_audiences": ["AUD-ibm-enterprise-it"],
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx, the watsonx trial and demo flow, and public IBM enterprise marketing (2024). Triggers, cadence, and qualification logic are illustrative, not internal configuration."
}
```
