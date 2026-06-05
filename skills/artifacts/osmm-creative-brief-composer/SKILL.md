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
  required: [business_context, brand_context, persona, marketing_strategy, creative_strategy, messaging_framework]
  optional: [audience, offer, campaign_strategy, measurement_framework, keyword]
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
deliverable teams actually use, **and** it enforces the standard by requiring
those objects as inputs — you cannot get the good brief without the structured
context, so the brief pulls object adoption through.

## What it consumes

The brief is composed *from objects*, never from scratch. Resolve these as
inputs (by `object_type`):

**Required** — the brief should not be composed without these:

| Object | What it supplies to the brief |
|--------|-------------------------------|
| `business_context` | Background; market position; differentiators; what the business needs marketing to do. |
| `brand_context` | Tone, voice, personality, and messaging guardrails (the "how it must sound" + mandatories). |
| `persona` | The target — who we're talking to, their triggers, motivations, pain points, decision criteria. |
| `marketing_strategy` | The business/marketing objective the creative must serve. |
| `creative_strategy` | Creative themes, emotional strategy, channel creative requirements — the creative spine. |
| `messaging_framework` | Message hierarchy and the single-minded proposition + supporting messages. |

**Optional** — include when present; they strengthen the brief:

| Object | What it adds |
|--------|--------------|
| `audience` | Sharper targeting context behind the persona. |
| `offer` | The value exchange / what we're asking the audience to act on. |
| `campaign_strategy` | Campaign objective, channels, timing, audience-to-offer mapping. |
| `measurement_framework` / `campaign_measurement` | Success metrics the creative is accountable to. |
| `keyword` | SEO/AEO topics and intent the creative should serve. |

### Handling missing objects (this is where the standard gets enforced)

Before composing, check which required objects are available.

- **If a required object is missing,** do not invent it. Report exactly what's
  missing and name the builder that produces it, then offer to proceed with a
  clearly-flagged gap or to build the object first:

  > Missing required input: **Brand Context** (`brand_context`). Build it with
  > `osmm-brand-context-builder`, or I can draft the brief with the *Tone &
  > Personality* section flagged `[GAP: no Brand Context]`.

- **If an optional object is missing,** omit its section silently or note it
  lightly; never fabricate an offer or metrics that weren't decided.

The builder map for required inputs:

| Object | Builder |
|--------|---------|
| `business_context` | `osmm-business-context-builder` |
| `brand_context` | `osmm-brand-context-builder` |
| `persona` | `osmm-persona-builder` |
| `marketing_strategy` | `osmm-marketing-strategy-builder` |
| `creative_strategy` | `osmm-creative-strategy-builder` |
| `messaging_framework` | `osmm-messaging-framework-builder` |

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
5. **Single-minded proposition** — the one thing to land. *From
   `messaging_framework` (primary message / value framing).*
6. **Reasons to believe** — the support that makes the proposition credible.
   *From `messaging_framework` supporting messages, `business_context`
   differentiators, and `offer`.*
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

1. **Compose, don't author.** Every claim in the brief should trace to an object.
   If you find yourself inventing a fact, the right move is to flag a missing
   object, not to fill the gap.
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
(`persona`), a `marketing_strategy`, a `creative_strategy`, and a
`messaging_framework`. No `offer` object → the Offer section is omitted.

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
plus the campaign's `marketing_strategy`, `creative_strategy`, and
`messaging_framework` objects.

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
