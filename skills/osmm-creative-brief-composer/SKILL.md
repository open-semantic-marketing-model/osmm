---
name: osmm-creative-brief-composer
description: >-
  Compose a first-draft Creative Brief from a set of OSMM objects. Use this skill
  whenever the user wants to "generate a creative brief," "write a creative brief,"
  "build a brief for this campaign," "turn our strategy into a brief," brief an
  agency or creative team, or produce the human-readable creative direction that
  Phase 5 (Define Content & Creative) resolves to. The brief is an ARTIFACT — a
  rendered view of the underlying objects, not an OSMM object — and is meant as an
  accelerator/starting point a client tailors. Trigger when the user asks for a
  creative brief, a creative direction doc, or an agency brief, or hands over OSMM
  objects and asks to brief creative against them. If the required objects do not
  yet exist, this skill says what is missing and which builder produces each,
  rather than inventing the inputs.
skill_class: artifact-composer
artifact: Creative Brief
consumes:
  required: [business_context, brand_context, persona]
  optional: [marketing_strategy, creative_strategy, content_strategy, product_context, journey, audience, offer, campaign_strategy, measurement_framework]
phase: 5
osmm_version: 0.1.0
status: draft
---

# OSMM Creative Brief Composer

Compose a **Creative Brief** — the human-readable creative direction a person or
agency reads — from the OSMM objects that already hold the decisions.

A Creative Brief is an **artifact, not an object** (see `CONVENTION.md` →
"Resolved: Creative Brief is an artifact"). This skill is an
**artifact-composer**, not an object builder: it reads several objects and emits
a brief. It defines no schema and produces no `object_type`. The brief is a
**non-normative accelerator** — a strong first draft grounded in the structured
data, which a client then tailors to their house format.

The value is twofold: it turns the work already captured in OSMM objects into the
deliverable teams actually use, **and** it enforces the standard by requiring the
core context objects as inputs and pulling the strategy objects through — the
more of the model a client has built, the sharper the brief, so the brief pulls
object adoption through rather than gating on it.

## What it consumes

The brief is composed *from objects*, never from scratch. Inputs fall into three
tiers, resolved by `object_type`:

**Tier 1 — Required.** The brief should not be composed without these three; they
anchor who/what/how and are enough to produce a useful first draft on their own:

| Object | What it supplies to the brief |
|--------|-------------------------------|
| `business_context` | Background; market position; differentiators; what the business needs marketing to do. |
| `brand_context` | Tone, voice, personality, and messaging guardrails (the "how it must sound" + mandatories). |
| `persona` | The target — who we're talking to, their triggers, motivations, pain points, decision criteria. |

**Tier 2 — Strategy (optional, but they sharpen the spine).** When present, each
supplies its section directly. When **absent**, the composer synthesizes a
*provisional* version of that section from Tier 1 and flags it — it does not drop
the section, because a brief without an objective or a proposition isn't a brief:

| Object | Supplies | If absent |
|--------|----------|-----------|
| `marketing_strategy` | The business/marketing objective the creative must serve. | Infer a provisional objective from `business_context` marketing objectives; flag it. |
| `creative_strategy` | Creative themes, emotional strategy, channel creative requirements. | Synthesize a provisional creative angle from persona + brand; flag it. |
| the message cascade (`brand_context` `brand_promise`/`messaging_pillars` → `product_context` `product_messaging` → `journey` `persona_tracks.key_messages`) | The single-minded proposition + support, resolved at the persona/stage. | Draft a provisional proposition from persona motivations + product value pillars; flag it. |

**Tier 3 — Add-ons (optional).** Include when present; **omit the section
entirely when absent** — never fabricate an offer, metrics, or a campaign that
wasn't decided:

| Object | What it adds |
|--------|--------------|
| `audience` | Sharper targeting context behind the persona. |
| `offer` | The value exchange / what we're asking the audience to act on. |
| `campaign_strategy` | Campaign objective, channels, timing, audience-to-offer mapping. |
| `measurement_framework` | Success metrics the creative is accountable to. |
| `journey` | The persona/stage `key_questions` (directional keywords) and `key_messages` the creative should serve. |
| `content_strategy` | The content plan the creative produces against. |

### Handling missing objects (how the pull-through works)

Before composing, check which objects are available, then apply the tier rule:

- **Tier 1 missing** — do not invent it. Report exactly what's missing and name
  the builder that produces it, then offer to proceed with a clearly-flagged gap
  or to build the object first:

  > Missing required input: **Brand Context** (`brand_context`). Build it with
  > `osmm-brand-context-builder`, or I can draft the brief with the *Tone &
  > Personality* section flagged `[GAP: no Brand Context]`.

- **Tier 2 missing** — synthesize the section provisionally from Tier 1, flag it
  inline, and recommend the builder so the client knows how to firm it up:

  > `[DRAFT: no Journey key_messages / product_messaging — proposition synthesized
  > from Persona + Product Context. Firm up with osmm-journey-builder / osmm-product-context-builder.]`

- **Tier 3 missing** — omit the section silently or note it lightly; never
  fabricate the underlying decision.

Always end with a short **"To sharpen this brief"** list naming the absent Tier 2
/ Tier 3 objects and their builders — this is the pull-through made explicit.

The builder map:

| Object | Builder | Tier |
|--------|---------|------|
| `business_context` | `osmm-business-context-builder` | 1 |
| `brand_context` | `osmm-brand-context-builder` | 1 |
| `persona` | `osmm-persona-builder` | 1 |
| `marketing_strategy` | `osmm-marketing-strategy-builder` | 2 |
| `creative_strategy` | `osmm-creative-strategy-builder` | 2 |
| `product_context` | `osmm-product-context-builder` | 2 |
| `journey` | `osmm-journey-builder` | 2 |

## Template selection (data-driven, not hand-toggled)

The brief's variant is chosen from object data, not a manual switch — read
`business_context.business_type`:

- **B2C** (`b2c`, `dtc`, `ecommerce`, `retail`, `media`, …) — single decision-maker
  framing; lead with emotional resonance and a tight single-minded proposition;
  brand affinity and social proof carry weight; one primary persona.
- **B2B** (`b2b`, `b2b2c`, `saas`, `enterprise_software`, `professional_services`)
  — buying-committee framing; rational value (ROI/TCO), credibility signals, and
  decision criteria carry weight; longer consideration cycle; may brief to
  multiple personas/roles. Surface the persona `role` block and
  `decision_criteria`.

If `business_type` is absent, infer from the persona's `persona_type`
(`consumer*` → B2C; `b2b*` → B2B) and note the assumption.

## The brief structure

A complete brief, each section sourced from the object(s) noted. Keep it tight —
a brief is a focusing instrument, not a data dump. Drop sections whose source
object is absent (after the missing-object handling above).

1. **Background** — the situation, in 2–4 sentences. *From `business_context`
   (description, market position, challenges) + `campaign_strategy` if present.*
2. **Objective** — what this creative must achieve, tied to a business/marketing
   goal. *From `marketing_strategy` + `campaign_strategy`.* Make it singular and
   measurable where metrics exist.
3. **Target audience** — who we're talking to and what moves them. *From
   `persona` (summary, triggers, motivations, pain points; + `role` and
   `decision_criteria` for B2B) and `audience`.*
4. **Key insight** — the one human truth the creative turns on. *Synthesized from
   `persona` motivations/triggers/pain points and `creative_strategy`.* This is
   the section most worth getting sharp; one sentence beats a list.
5. **Single-minded proposition** — the one thing to land. *From the message cascade:
   `brand_context` `brand_promise` → `product_context` `product_messaging` →
   `journey` `persona_tracks.key_messages` for the relevant persona/stage.*
6. **Reasons to believe** — the support that makes the proposition credible.
   *From `product_context` `product_messaging` proof points / value pillars,
   `business_context` differentiators, and `offer`.*
7. **Tone & personality** — how it must sound and feel. *From `brand_context`
   (voice, tone principles).*
8. **Offer** *(optional)* — the value exchange and the action we're asking for.
   *From `offer`.*
9. **Channels & deliverables** — where this runs and what's needed. *From
   `creative_strategy` (channel creative requirements) + `campaign_strategy`.*
10. **Mandatories & guardrails** — brand, legal, and message guardrails that are
    non-negotiable. *From `brand_context` (guardrails) + `business_context`.*
11. **Success metrics** *(optional)* — what we'll judge it by. *From
    `measurement_framework` / `campaign_measurement`.*
12. **Sources** — the OSMM objects (by id) this brief was composed from, so the
    brief is traceable back to the data.

## Composition principles

1. **Compose first; synthesize only Tier 2, and flag it.** Every claim should
   trace to an object. Where a Tier 2 strategy object is absent you may
   synthesize a *provisional* objective / angle / proposition from Tier 1 — but
   mark it `[DRAFT: …]` and name the builder. Never invent a Tier 3 fact (an
   offer, a metric, a campaign) the objects don't support: flag the gap instead
   of filling it.
2. **The brief is a focusing tool.** Distill — a single-minded proposition is
   *single-minded*. Resist transcribing whole arrays from the objects; select the
   signal-bearing items.
3. **Keep traceability.** The Sources section lists the consumed object ids; where
   a section leans on a specific object, it's fine to keep the brief readable
   without inline citations, but the brief must be reconstructable from its
   inputs.
4. **It's a starting point, say so.** Open the output by noting this is an
   OSMM-composed first draft to tailor — not a finished, approved brief.
5. **Don't resolve contradictions silently.** If objects conflict (e.g. the
   creative strategy implies a tone the brand guardrails forbid), surface the
   tension in the brief rather than papering over it.
6. **Respect the object/artifact boundary.** This skill never edits or emits
   objects. If composing the brief reveals that an object is wrong or thin, say so
   and point to the relevant builder — don't fix it here.

## Output rules

- Emit a human-readable **Markdown** brief, not JSON (the brief is an artifact).
- Lead with a one-line note that it's an OSMM-composed first draft to tailor, and
  the variant used (B2C/B2B) and why.
- End with the **Sources** list of consumed object ids.
- If any required object was missing, make the gaps visible in the brief
  (`[GAP: …]`) and summarize them at the top so the user knows what to firm up.
- Suggested filename if saved: `CREATIVE-BRIEF_<entity-slug>.md` (artifact naming
  mirrors the object instance pattern; artifacts are not standardized, so this is
  a convenience, not a contract).

---

## Worked example — B2C brief composed from objects

**Inputs available:** `BIZ-acme-wile-e-coyote-corp` (`business_context`,
`business_type: b2c`), `BRC-acme...` (`brand_context`), `PER-acme-busy-parent`
(`persona`), a `marketing_strategy`, a `creative_strategy`, a `product_context`,
and a `journey`. No `offer` object → the Offer section is omitted.

> *OSMM-composed first draft — tailor before use. Variant: **B2C** (Business
> Context `business_type: b2c`; single primary persona).*

### Creative Brief — ACME DTC Spring Push

**Background.** ACME is a mid-market DTC home-and-outdoor brand with strong brand
personality but awareness skewed to an older cohort. It's pushing to grow
e-commerce share and reach 25–44 homeowners, against rising acquisition costs and
a diffuse, broad catalog.

**Objective.** Drive trial among 25–44 homeowners and lift DTC consideration —
not just clicks, but first purchase from a new-to-brand segment.

**Target audience.** The Busy Parent — an affluent suburban parent, perpetually
short on time, resistant to complexity, loyal once trust is earned. Acts when a
household item fails or a peer recommendation breaks through their consideration
paralysis. Trusts reviews and word-of-mouth over advertising.

**Key insight.** They don't want more options — they want one they can trust
without spending the evening researching it.

**Single-minded proposition.** *Ingenious products that just work — so you can
stop researching and get on with your day.*

**Reasons to believe.** Distinctive, high-recognition brand; catalog depth that
makes ACME a one-stop problem-solver; a loyal repeat base that vouches for
reliability.

**Tone & personality.** Clever, optimistic, slightly self-aware — leans into the
ACME mythology without taking itself too seriously. Warm and confident, never
gimmicky.

**Channels & deliverables.** Streaming and social first (the audience is
streaming-first and avoids interruptive formats); review-led and word-of-mouth
amplification. Deliverables per the creative strategy's channel matrix.

**Mandatories & guardrails.** Lead with outcomes and reliability, not specs; use
real social proof; honor brand voice guardrails; no interruptive ad formats.

**Sources.** `BIZ-acme-wile-e-coyote-corp`, `BRC-acme...`, `PER-acme-busy-parent`,
plus the campaign's `marketing_strategy`, `creative_strategy`, `product_context`,
and `journey` objects.

---

### Note on the B2B variant

For a B2B input set (`business_type: b2b`/`saas`/…), the same skill shifts the
frame: the **Objective** ties to pipeline/consideration in a buying committee;
**Target audience** surfaces the persona `role` and `decision_criteria` and may
brief to more than one role (economic buyer, champion, end user); **Key insight**
and **Reasons to believe** lean rational (ROI/TCO, credibility, peer/analyst
proof); and **Single-minded proposition** is framed for a considered, multi-stakeholder
decision rather than a single impulse. The structure is identical — the emphasis
is data-driven off the objects.
