---
name: osmm-experience-builder
description: >-
  Convert any deliverable-experience source into a structured OSMM Experience Object (canonical
  JSON). An experience is a single deliverable: a winback email, a landing page or landing-page
  variant, an ad or ad set, a paid-social unit, a homepage hero, a triggered SMS or push, an in-app
  message, or a gated content asset. Use this skill whenever the user wants to capture the
  *definition/decision* of one deliverable experience as a reusable object — "build an experience
  object," "spec this email/landing page/ad," "objectify this winback email," "structure this hero,"
  "define this experience's variants," "capture the personalization rules for this email," "record
  the QA/approval status," or "track this experience's deployment / go-live." It models the
  experience's spec/intent, the components it's assembled from, its variants and personalization,
  its QA/approval status, and its deployment. It captures the *decision*, NOT the rendered
  HTML/image — that lives in the ESP/CMS/DAM/ad platform and is *referenced* via
  `delivery_reference`. Trigger on experiences, emails, landing pages, web pages, ads, display,
  paid social, push, SMS, in-app messages, homepage heroes, content assets, experience specs,
  variants, A/B variations, personalization rules, QA/validation, approval, and deployment/go-live.
object: Experience Object
object_type: experience
category: Work Product
phase: 6
wave: 4
osmm_version: 0.1.0
status: draft
---

# OSMM Experience Builder

Build a valid **OSMM Experience Object** from any source describing a single deliverable experience —
a winback email, a landing page variant, an ad set, a homepage hero, a triggered SMS.

An Experience Object is **one deliverable experience's definition and decision** — what the
experience is, who it's for, what it's assembled from, its variants and personalization, its
QA/approval status, and its deployment. It is a **Work Product**: the typed record of *the decision*
behind a deliverable, distinct from the rendered asset itself.

> **OSMM models the decision, not the rendered asset.** The actual HTML, image, or ad creative lives
> in the production tool — the ESP, CMS, DAM, or ad platform — and is *referenced* here via
> `delivery_reference`, never stored. This object captures everything a human or agent needs to
> reason about the experience (what it is, who it's for, what it's made of, its variants,
> personalization, readiness, and go-live) without becoming a copy of the rendered output. The asset
> renders once, in the tool that owns rendering; the *decision* about it is the OSMM object.

> **One object, five absorbed concepts.** The v0.9 right-sizing folds five former Phase-6 objects
> into this single Experience Object, because they were thin views of one deliverable rather than
> separate things:
> - **Experience Specification** (6.1) → the optional `specification` block (scope, dependencies,
>   requirements, success criteria).
> - **Experience Delivery** (6.5) → this object *is* the delivered experience; channel/A-B
>   variations live in `variants`.
> - **Personalization Configuration** (6.4) → the optional `personalization_rules` array
>   (condition → treatment, optionally by audience).
> - **Experience Validation** (6.6) → the optional `validation` block — QA/compliance/approval as a
>   *status*, not a separate object.
> - **Campaign Deployment, per-experience go-live** (6.7) → the optional `deployment` block — the
>   experience's own activation status and window.
>
> It is **assembled from** Experience Component objects (6.2), which stay separate (they are reusable
> building blocks) and are referenced by id via `linked_components`.

This is the lean v0.1 builder. It captures the marketing-relevant *decision* about a deliverable and
nothing more. It does **not** restate the rendered asset, and it does **not** inline its components —
it *references* both.

## Boundaries — what this object is and is NOT

The Experience sits between the reusable parts it's built from, the creative direction it expresses,
and the path it serves. Keeping the lines clean is the whole point of giving the deliverable its own
object:

| Object | Answers | Example (IBM) | Example (Wendy's) |
|--------|---------|---------------|-------------------|
| **Experience Component** | What are the *reusable building blocks* — a headline, hero, CTA, offer card, trust block — that experiences assemble from? | The watsonx hero block, the trial CTA button | The Baconator hero image, the "free with first order" offer card |
| **Experience** (this) | What's *this one deliverable's definition/decision* — its spec, what it's assembled from, its variants, personalization, readiness, and go-live? | "watsonx Trial Landing Page" (A/B variants) | "Baconator App Winback Email" |
| **Creative Strategy** | What's the *creative direction* — the system, concepts, and look-and-feel the experience expresses? | The watsonx creative system & experience concepts | The Wendy's bold-value creative direction |
| **Journey** | What's the *orchestrated path* this experience serves — its stages, triggers, cadence? | The watsonx enterprise evaluation journey | The Wendy's app habit (winback) journey |

Rules of thumb:

- **The Experience is the deliverable's *decision*, not its rendered bytes.** The HTML/image/ad
  creative lives in the ESP/CMS/DAM/ad platform; capture its location in `delivery_reference` and
  model the decision here.
- **Reference components, don't inline them.** A headline, hero, CTA, or offer card is an Experience
  Component (its own object). The Experience lists the components it's assembled from via
  `linked_components` (and the assembled order in `structure`); it does not restate their content.
- **QA and deployment are *statuses*, not objects.** Release readiness lives in `validation.status`
  (draft / in_review / approved / rejected); go-live lives in `deployment.status` (not_scheduled /
  scheduled / live / paused / ended). They are facets of this one deliverable, not separate records.
- **Creative direction lives in Creative Strategy.** The system, concepts, and look-and-feel are
  Creative Strategy (Phase 5); the Experience *expresses* it (link via `linked_creative_strategy`)
  but doesn't restate it.
- **The journey owns the path; the Experience is a deliverable on it.** Stages, triggers, and cadence
  are Journey; the Experience references the journey it serves via `linked_journey`.

## The output schema

> **Canonical schema:** [`schemas/experience.schema.json`](../../../schemas/experience.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "experience",             // const — always "experience"
  "osmm_version": "0.1.0",                 // schema version this conforms to
  "experience_id": "EXP-<slug>",           // stable, human-readable id (see ID rules)
  "version": "1.0",                        // instance version; bump on revision
  "status": "draft",                       // draft | proposed | stable | deprecated

  "name": "",                              // the experience's name ("Baconator App Winback Email")
  "experience_type": "",                   // controlled enum — see vocabulary table
  "channel": "",                           // OPTIONAL — the delivery channel ("Email", "Web", "Paid social")
  "objective": "",                         // what this experience is for (the job it does)

  "specification": {                       // OPTIONAL — the spec/intent (former Experience Specification, 6.1)
    "scope": "",                           // what it does / doesn't cover
    "dependencies": [],                    // assets, data, upstream decisions it depends on
    "requirements": [],                    // functional/content requirements it must meet
    "success_criteria": []                 // what "done/working" looks like
  },

  "linked_components": [],                 // OPTIONAL — EXC-ids it's assembled from (6.2)
  "structure": [],                         // OPTIONAL — assembled layout/sections (headline → hero → body → CTA)

  "variants": [                            // OPTIONAL — channel/A-B variations (former Experience Delivery, 6.5)
    { "variant": "", "description": "" }   // variant label + what differs
  ],
  "personalization_rules": [               // OPTIONAL — condition → treatment (former Personalization Configuration, 6.4)
    { "condition": "", "treatment": "", "audience": "AUD-<slug>" }
  ],

  "validation": {                          // OPTIONAL — QA/approval as a status (former Experience Validation, 6.6)
    "status": "",                          // draft | in_review | approved | rejected
    "qa_notes": "",                        // QA findings / checks
    "compliance_notes": "",                // legal/brand/regulatory notes
    "approved_by": ""                      // who approved it
  },
  "deployment": {                          // OPTIONAL — per-experience go-live (former Campaign Deployment, 6.7)
    "status": "",                          // not_scheduled | scheduled | live | paused | ended
    "window": "",                          // when it goes/went live
    "activation_notes": ""                 // go-live notes
  },

  "delivery_reference": "",                // OPTIONAL — URL/id of the rendered asset in the production tool (referenced, not stored)

  "linked_campaign_strategy": "",          // OPTIONAL — CMS-id of the campaign it serves (placeholder ok)
  "linked_journey": "",                    // OPTIONAL — JNY-id of the journey it serves (placeholder ok)
  "linked_audiences": [],                  // OPTIONAL — AUD-ids it's for (placeholder ok)
  "linked_offer": "",                      // OPTIONAL — OFR-id it activates (placeholder ok)
  "linked_creative_strategy": "",          // OPTIONAL — CRS-id it expresses (placeholder ok)
  "linked_business_context": "",           // OPTIONAL — BIZ-id of the owning Business Context (placeholder ok)
  "source": ""                             // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"experience"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `experience_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | The experience's name ("Baconator App Winback Email"). |
| `experience_type` | enum | yes | Controlled vocabulary — see below. Pick the single closest. |
| `channel` | string | no | The delivery channel, if not already obvious from the type. |
| `objective` | string | yes | What this experience is *for* — the outcome/job it does in the journey or campaign. |
| `specification` | object | no | The spec/intent (former Experience Specification, 6.1). See sub-fields. Omit if thin. |
| `specification.scope` | string | no | What the experience does and does not cover. |
| `specification.dependencies` | string[] | no | Assets, data, or upstream decisions it depends on. |
| `specification.requirements` | string[] | no | Functional/content requirements it must meet. |
| `specification.success_criteria` | string[] | no | What "done/working" looks like for the experience. |
| `linked_components` | string[] | no | `EXC-` ids of the Experience Components it's assembled from (6.2). `EXC-PLACEHOLDER-<slug>` ok. |
| `structure` | string[] | no | The assembled layout/sections in order (headline → hero → body → CTA). |
| `variants` | object[] | no | Channel/A-B variations (former Experience Delivery, 6.5). Each `{ variant, description? }`; `variant` required per item. |
| `personalization_rules` | object[] | no | Condition → treatment rules (former Personalization Configuration, 6.4). Each `{ condition, treatment, audience? }`; `condition` and `treatment` required per item. |
| `validation` | object | no | QA/compliance/approval as a *status* (former Experience Validation, 6.6). See sub-fields. |
| `validation.status` | enum | no | `draft` \| `in_review` \| `approved` \| `rejected`. |
| `validation.qa_notes` | string | no | QA findings, checks run, issues to resolve. |
| `validation.compliance_notes` | string | no | Legal/brand/regulatory compliance notes. |
| `validation.approved_by` | string | no | Who approved the experience for release. |
| `deployment` | object | no | Per-experience go-live (former Campaign Deployment, 6.7). See sub-fields. |
| `deployment.status` | enum | no | `not_scheduled` \| `scheduled` \| `live` \| `paused` \| `ended`. |
| `deployment.window` | string | no | The activation window (when it goes/went live). |
| `deployment.activation_notes` | string | no | Go-live notes — targeting cutovers, ramp, dependencies. |
| `delivery_reference` | string | no | URL/id of the rendered asset in the production tool. The asset is *referenced*, not stored here. |
| `linked_campaign_strategy` | string | no | `CMS-` id of the campaign it serves. `CMS-PLACEHOLDER-<slug>` ok. |
| `linked_journey` | string | no | `JNY-` id of the journey it serves. `JNY-PLACEHOLDER-<slug>` ok. |
| `linked_audiences` | string[] | no | `AUD-` ids it's for. `AUD-PLACEHOLDER-<slug>` ok. |
| `linked_offer` | string | no | `OFR-` id it activates. `OFR-PLACEHOLDER-<slug>` ok. |
| `linked_creative_strategy` | string | no | `CRS-` id it expresses. `CRS-PLACEHOLDER-<slug>` ok. |
| `linked_business_context` | string | no | `BIZ-` id of the owning Business Context. `BIZ-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Document-level provenance and approximate date. |

## Experience type vocabulary

`experience_type` is a controlled, governed enum — a stored snake_case token mapped to a
human-readable label. Extended deliberately by maintainers, never invented per-project.

| Stored value | Label | Use when |
|---|---|---|
| `email` | Email | A deliverable email — newsletter, promo, winback, triggered/lifecycle send. |
| `landing_page` | Landing page | A standalone, conversion-focused page (often campaign- or offer-specific). |
| `web_page` | Web page | A site page that isn't a dedicated landing page (product page, content page). |
| `ad` | Ad | A single advertising unit not better described by a more specific channel below. |
| `display` | Display ad | A banner/display advertising unit or set. |
| `paid_social` | Paid social | A paid social ad or ad set (Meta, LinkedIn, TikTok, etc.). |
| `push` | Push notification | A mobile/web push notification. |
| `sms` | SMS | A text-message experience (often triggered). |
| `in_app` | In-app message | An in-app message, banner, or interstitial. |
| `homepage_hero` | Homepage hero | A homepage/hero placement or featured slot. |
| `content_asset` | Content asset | A gated or ungated content deliverable (whitepaper, guide, tool). |
| `other` | Other | Anything not covered above; note the specifics in `name`/`objective`. |

Pick the single closest value. If a deliverable spans formats, choose the dominant delivery surface
and note the nuance in `objective` or `specification.scope`.

## ID rules

`experience_id` = `EXP-` + a lowercase, hyphen-delimited slug. Prefer a slug that namespaces the
experience under its business so ids stay unique across a portfolio:

- Wendy's Baconator app winback email → `EXP-wendys-baconator-winback-email`
- IBM watsonx trial landing page → `EXP-ibm-watsonx-trial-lp`
- ACME homepage hero (spring) → `EXP-acme-homepage-hero-spring`

Keep it stable: once assigned, journeys, campaigns, and measurement objects reference it. On revision
bump `version`, never the id.

## Extraction principles

1. **Model the decision, not the rendered asset.** Capture what the experience *is* and the decisions
   around it; do not paste in the HTML, image, or ad creative. Record where the rendered asset lives
   in `delivery_reference` and let the production tool own rendering.
2. **Reference components, don't inline them.** A headline, hero, CTA, offer card, or trust block is
   an Experience Component (its own object). List the components the experience is assembled from in
   `linked_components`, and the assembled order in `structure`. Don't restate their content here.
3. **QA and deploy are statuses.** Release readiness is `validation.status`; go-live is
   `deployment.status`. They are facets of this one deliverable — don't reach for a separate object.
4. **Variants vs. personalization are different.** `variants` are channel/A-B *versions* of the whole
   experience (variant A vs B, mobile vs desktop). `personalization_rules` are condition→treatment
   swaps *within* an experience (e.g. show offer X to value-seekers). Keep them in the right array.
5. **Spec is intent, captured only if real.** Use `specification` for the scope, dependencies,
   requirements, and success criteria the brief actually carried. Omit it rather than inventing a
   spec for a deliverable that didn't have one.
6. **Reference, don't restate, the surrounding objects.** `linked_journey`, `linked_campaign_strategy`,
   `linked_audiences`, `linked_offer`, `linked_creative_strategy`, and `linked_business_context` hold
   ids; the path, scope, audience criteria, deal, and creative direction live in those objects.
7. **Keep arrays signal-bearing.** A few real components, variants, or rules beat a padded list.
   Resist restating the obvious or inventing variants that don't exist.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per experience. Save using the OSMM instance-naming convention:
  `EXPERIENCE_<entity-slug>.json` (e.g. `EXPERIENCE_wendys-baconator-winback-email.json`) — uppercase
  object name, underscore join, lowercase entity slug; append an instance slug when an entity has more
  than one experience. See `CONVENTION.md` → "Instance file naming". The `experience_id`
  (`EXP-<slug>`) remains the id *inside* the object; it is not the filename.
- Set `delivery_reference` to where the rendered asset actually lives (ESP/CMS/DAM/ad-platform URL or
  id) when known; omit it rather than inventing one.
- Use real `EXC-`/`AUD-`/`OFR-`/`JNY-`/`CMS-`/`CRS-`/`BIZ-` ids where they exist; use a
  `*-PLACEHOLDER-<slug>` form where the object is expected but unbuilt; omit the field entirely when
  there's no link.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially
  `specification`, `validation`, and `deployment`) so they can fill gaps.
- If you find Experience-Component material (a specific headline, hero, CTA, offer card), note it and
  point the user to the Experience Component Object rather than inlining it — link via
  `linked_components` instead.

## Starter prompts

**B2C deliverable (email / push / SMS):**
> Build an OSMM Experience Object for [Brand]'s [winback email / triggered push / SMS]. Capture what
> it's for, the components it's assembled from, any variants and personalization rules, and its
> QA/approval and deployment status. Don't paste the rendered creative — reference it via
> `delivery_reference`. Link it to `BIZ-[brand-slug]`, the journey it serves, and the audiences it
> targets.

**B2B deliverable (landing page / ad):**
> Build an OSMM Experience Object for [Company]'s [landing page / ad set] for [offering]. Capture the
> objective, the assembled structure, any A/B variants, and the offer it activates. Keep the rendered
> asset out — reference it via `delivery_reference`. Link it to `BIZ-[company-slug]`,
> `OFR-[offer-slug]`, and the creative strategy it expresses.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The blocks below illustrate
the shape; both validate against `schemas/experience.schema.json`.

### Example 1 — B2C deliverable email (Wendy's Baconator app winback)

Built from Wendy's public app, loyalty, and marketing material. A triggered winback email that serves
the always-on app-habit journey; includes `validation` and `deployment` blocks to show the absorbed
QA and go-live views. References the shipped `BIZ-wendys`, `AUD-wendys-value-seekers`, and
`JNY-wendys-app-habit`; components are placeholders until the Experience Component objects are built.

```json
{
  "object_type": "experience",
  "osmm_version": "0.1.0",
  "experience_id": "EXP-wendys-baconator-winback-email",
  "version": "1.0",
  "status": "draft",
  "name": "Baconator App Winback Email",
  "experience_type": "email",
  "channel": "Email",
  "objective": "Re-engage lapsed Wendy's app users with a Baconator-led offer that pulls them back to a repeat mobile order.",
  "specification": {
    "scope": "A single triggered winback email for app users with no order in 14 days; covers subject line, hero, offer, and CTA — not the in-app redemption flow.",
    "dependencies": ["Lapse signal from the app-habit journey (14-day no-order timer)", "Active Baconator winback offer", "Approved Baconator hero imagery in the DAM"],
    "requirements": ["Mobile-first layout", "Single primary CTA to the app", "Offer terms in the footer"],
    "success_criteria": ["Open and click-to-app rates beat the winback baseline", "Drives measurable return orders within the offer window"]
  },
  "linked_components": [
    "EXC-PLACEHOLDER-wendys-baconator-hero",
    "EXC-PLACEHOLDER-wendys-winback-subject-line",
    "EXC-PLACEHOLDER-wendys-app-order-cta"
  ],
  "structure": ["Subject line", "Baconator hero", "Winback offer copy", "Primary CTA (order in app)", "Offer terms footer"],
  "variants": [
    { "variant": "A", "description": "Free Baconator with next app order — appetite-led hero." },
    { "variant": "B", "description": "Discount-led framing — '$3 off your comeback order' with the same hero." }
  ],
  "personalization_rules": [
    { "condition": "Lapsed user previously ordered a Baconator or bacon item", "treatment": "Lead with the Baconator hero and a free-Baconator offer", "audience": "AUD-wendys-value-seekers" },
    { "condition": "Lapsed user with no bacon-item history", "treatment": "Swap the hero for their most-ordered item and keep the discount framing" }
  ],
  "validation": {
    "status": "approved",
    "qa_notes": "Rendering checked across major email clients; all links route to the app deep link; offer code resolves.",
    "compliance_notes": "Offer terms and CAN-SPAM unsubscribe present; promo claims cleared by brand/legal.",
    "approved_by": "Lifecycle marketing lead"
  },
  "deployment": {
    "status": "scheduled",
    "window": "Triggers on the day-14 lapse event during the active winback window",
    "activation_notes": "Suppressed for users who ordered in the last 48h; A/B split 50/50 at send."
  },
  "delivery_reference": "ESP template id wendys-winback-baconator-v1 (rendered HTML lives in the ESP, not in this object)",
  "linked_journey": "JNY-wendys-app-habit",
  "linked_audiences": ["AUD-wendys-value-seekers"],
  "linked_business_context": "BIZ-wendys",
  "source": "Built from public information: wendys.com, the Wendy's app and Wendy's Rewards public pages, and public reporting on the brand's digital marketing (2024). Component ids, variants, QA, and deployment details are illustrative, not internal configuration."
}
```

### Example 2 — B2B deliverable landing page (IBM watsonx trial)

Built from IBM's public watsonx trial flow. A conversion landing page for the watsonx trial offer
with A/B variants. References the shipped `BIZ-ibm`; the offer is a placeholder until that Offer
object is built.

```json
{
  "object_type": "experience",
  "osmm_version": "0.1.0",
  "experience_id": "EXP-ibm-watsonx-trial-lp",
  "version": "1.0",
  "status": "draft",
  "name": "watsonx Trial Landing Page",
  "experience_type": "landing_page",
  "channel": "Web",
  "objective": "Convert enterprise AI evaluators arriving from paid and content channels into started watsonx trials.",
  "specification": {
    "scope": "The standalone trial landing page — hero, value proof, trial form, and trust block; not the post-signup trial provisioning flow.",
    "dependencies": ["Active watsonx trial offer", "Approved watsonx creative system", "Trial signup form / marketing-automation integration"],
    "requirements": ["Above-the-fold trial CTA", "Three proof points with use-case content", "Enterprise trust/compliance block"],
    "success_criteria": ["Trial-start conversion rate beats the prior page", "Form-fill quality holds (qualified evaluators)"]
  },
  "linked_components": [
    "EXC-PLACEHOLDER-ibm-watsonx-hero",
    "EXC-PLACEHOLDER-ibm-watsonx-trial-cta",
    "EXC-PLACEHOLDER-ibm-watsonx-trust-block"
  ],
  "structure": ["watsonx hero + headline", "Value proof points", "Trial signup form", "Enterprise trust/compliance block", "Secondary 'book a demo' CTA"],
  "variants": [
    { "variant": "A", "description": "Self-serve trial-first: primary CTA is 'Start your free trial', demo is secondary." },
    { "variant": "B", "description": "Guided-first: primary CTA is 'Book a demo', trial offered as the secondary path." }
  ],
  "validation": {
    "status": "in_review",
    "qa_notes": "Cross-browser and accessibility pass pending; form submission tested against the staging endpoint.",
    "compliance_notes": "Privacy/consent language under legal review for the form.",
    "approved_by": ""
  },
  "deployment": {
    "status": "not_scheduled",
    "window": "Targeted for the watsonx demand-gen flight",
    "activation_notes": "Go-live gated on legal sign-off and the A/B test being configured in the experimentation tool."
  },
  "delivery_reference": "CMS page id /watsonx/trial (rendered page lives in the CMS, not in this object)",
  "linked_campaign_strategy": "CMS-PLACEHOLDER-ibm-watsonx-launch",
  "linked_journey": "JNY-ibm-watsonx-eval",
  "linked_offer": "OFR-PLACEHOLDER-ibm-watsonx-trial",
  "linked_business_context": "BIZ-ibm",
  "source": "Built from public information: ibm.com/watsonx and the watsonx trial/demo flow (2024). Component ids, variants, QA, and deployment details are illustrative, not internal configuration."
}
```
