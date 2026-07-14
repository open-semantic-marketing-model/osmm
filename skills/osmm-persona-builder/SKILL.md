---
name: osmm-persona-builder
description: >-
  Convert any persona research asset into a structured OSMM Persona Object (canonical JSON).
  Inputs include consumer or B2B persona decks, segmentation reports, audience profiles, research
  exports (Resonate, Gale, Nielsen, Claritas), brand-awareness studies, or a strategist's raw notes.
  Use this skill whenever the user wants to turn a persona document, slide deck, brief, PDF, or research
  summary into a standardized persona, "build a persona object," "make a persona from this deck,"
  extract persona attributes into JSON, normalize a persona into our format/schema, or objectify a
  persona for downstream AI workflows. Trigger even if the user only says "turn this persona into our
  format," "structure this persona," or hands over a persona asset and asks what to do with it.
object: Persona Object
object_type: persona
category: Context Object
phase: 2
wave: 1
osmm_version: 0.1.0
status: draft
---

# OSMM Persona Builder

Build a valid **OSMM Persona Object** from any source describing a target customer.

A Persona Object is durable, reusable Context — the human-centered understanding of who a customer is, what drives them, and how to reach them. Downstream objects reference it by `persona_id` (a Keyword links the personas that search a term; a Customer Insight proposes updates to it). So the output is a *typed, addressable object* — not a prose summary. A summary is just a smaller PDF; the whole point of OSMM is to escape that.

This is the lean v0.1 builder. It captures the seven canonical psychographic fields and nothing more. Rich quantified data (index/composition stats, media tables, brand affinities, day-in-the-life timelines) is deliberately **out of scope** — fold its *implications* into the seven fields instead of transcribing the numbers.

## The output schema

> **Canonical schema:** [`schemas/persona.schema.json`](../../schemas/persona.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "persona",          // const — always "persona"
  "osmm_version": "0.1.0",           // schema version this conforms to
  "persona_id": "PER-<slug>",        // stable, human-readable id (see ID rules)
  "version": "1.0",                  // instance version; bump on revision
  "status": "draft",                 // draft | proposed | stable | deprecated
  "name": "",                        // the persona's name/handle
  "persona_type": "",                // controlled enum — see vocabulary below
  "summary": "One or two sentences capturing who this person is and what defines them.",
  "representative_quote": "A short line in the persona's own voice.",

  "demographics": {                  // OPTIONAL — descriptive snapshot, NOT targeting logic (see boundary note)
    "age": "",                       // value or range
    "gender": "",
    "household": "",                 // marital status, children, living situation
    "income": "",
    "education": "",
    "location": "",                  // geography / setting (urban, suburban, region)
    "occupation": ""
  },

  "triggers": [],                    // what prompts them to act NOW (priority initiatives / trigger events)
  "goals": [],                       // what they are trying to achieve
  "motivations": [],                 // the underlying drivers behind those goals
  "pain_points": [],                 // frustrations and obstacles in their way
  "objections": [],                  // reasons they hesitate or resist (optional — see note)
  "behavioral_traits": [],           // characteristic behaviors and habits (short characterizations, NOT a data dump)
  "decision_criteria": [],           // what they weigh when choosing/buying
  "messaging_preferences": [],       // how to communicate with them effectively

  "role": {                          // OPTIONAL — include for B2B personas, omit for B2C
    "title": "",                     // job title
    "responsibilities": [],          // what they own
    "influence_level": ""            // e.g. high | medium | low
  },

  "linked_audiences": [],            // ids of Audience Objects this persona brings to life (placeholder ok)
  "source": "Where this came from: studies, vendors, date."
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"persona"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `persona_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | |
| `persona_type` | enum | yes | Controlled vocabulary — see below. The persona's relationship to the purchase/decision. Machine-facetable; the coarse classifier the optional `role` block then details. |
| `summary` | string | yes | 1-2 sentences. The only "summary" allowed — the structured fields do the real work. |
| `representative_quote` | string | yes | A short line in the persona's voice. Extract a real quote if the source has one; otherwise compose a faithful one from their stated attitudes. Distinct from `summary` — voice, not description. |
| `demographics` | object | no | Optional descriptive snapshot — individual attributes that ground the persona. All keys optional; include what the source provides. NOT targeting logic (see boundary note). Omit for personas where it adds nothing. |
| `triggers` | string[] | yes | What prompts them to act *now* — the events or pressures that move them off the status quo. The "why now" that goals and pains don't capture. |
| `goals` | string[] | yes | |
| `motivations` | string[] | yes | |
| `pain_points` | string[] | yes | |
| `objections` | string[] | no | Often not stated in source material. Include only if grounded; leave `[]` rather than padding. |
| `behavioral_traits` | string[] | yes | A handful of crisp characterizations. |
| `decision_criteria` | string[] | yes | Plain phrases. Do NOT attach weights/percentages in v0.1. |
| `messaging_preferences` | string[] | yes | |
| `role` | object | no | Include for B2B personas. Carries *details* (title, responsibilities, influence level) — the committee role itself lives in `persona_type`. Omit entirely for B2C (don't emit an empty block). |
| `linked_audiences` | string[] | no | If no Audience Object exists yet, use a placeholder id like `AUD-PLACEHOLDER-<slug>`. |
| `source` | string | no | One line. Document-level provenance only. |

## Persona type vocabulary

`persona_type` is a controlled, governed enum — a stored snake_case token (consistent with `object_type`) that maps to a human-readable label. This keeps the field machine-facetable instead of fragmenting into free-text variants. The starter set:

| Stored value | Label |
|---|---|
| `consumer` | Consumer |
| `consumer_household_decision_maker` | Consumer — Head of Household |
| `consumer_influencer` | Consumer — Influencer (e.g. a child/partner who sways the choice) |
| `b2b_decision_maker` | B2B Buyer — Decision Maker |
| `b2b_economic_buyer` | B2B Buyer — Economic Buyer |
| `b2b_champion` | B2B Buyer — Champion |
| `b2b_influencer` | B2B Buyer — Influencer |
| `b2b_end_user` | B2B — End User |
| `b2b_gatekeeper` | B2B — Gatekeeper |

This is a starter vocabulary, not the final word. New types (negative/exclusion personas, internal personas, channel partners) are added deliberately under OSMM governance — not invented per-project — so the facet stays consistent across the standard. Pick the single closest value; if a persona genuinely spans roles, choose the dominant one and note the nuance in `summary`.

## Demographics: descriptive, not operational

Demographics belong on the persona, but as a *descriptive snapshot* — never as targeting logic. The two live in different objects in different forms:

- **Persona `demographics`** — descriptive prose that grounds the human: "~38, married, two young kids, ~$157K household." Read by people and agents to understand who this is.
- **Audience `demographic_criteria`** — qualification rules a system executes: `age 35-44 AND hhi >= 150000 AND has_children`. Used to *select* who to target.

Same subject, different jobs — one describes, one selects, so it isn't true duplication. The rule that keeps it clean: **the persona's snapshot is never the targeting source of truth.** If you need to query or segment, that's the linked Audience object. Keep the snapshot to *individual* descriptive attributes; firmographics (company size, industry, revenue) belong to Audience/Business Context, not here. Translate research into plain descriptive values — don't transcribe index or composition figures.

## ID rules

`persona_id` = `PER-` + a lowercase, hyphen-delimited slug that is stable and human-readable. Derive it from the brand/context plus the persona name so it stays unique across a portfolio.

- `The Busy Parent` for Acme → `PER-acme-busy-parent`
- `Enterprise VP of Marketing Ops` → `PER-vp-marketing-ops`

Keep it stable: once assigned, other objects point at it, so don't change an id on revision — bump `version` instead.

## Extraction principles

1. **Extract before you infer.** Pull what the source actually states. Most persona assets state goals, pains, and decision factors fairly directly.
2. **Infer conservatively, never fabricate.** `objections`, `triggers`, and `messaging_preferences` are often implied rather than stated. Infer these from adjacent evidence, but never invent data points the source gives no basis for. If there's no basis, leave the array empty.
3. **`triggers` is the "why now," not the goal.** A goal is an ongoing aim ("feed the family well"); a trigger is the event or pressure that moved them to act ("had kids," "a budget cycle opened," "a security incident forced a vendor review"). Source decks rarely label these — mine the backstory, the opening quote, and life-stage cues for them.
4. **`representative_quote` is voice, not summary.** If the source has a real quote, use it (lightly trimmed). If not, compose one faithful to the persona's stated attitudes — first person, conversational, the kind of thing they'd actually say.
5. **Classify `persona_type` first.** Decide the single closest value from the vocabulary before filling other fields — it frames everything else. Use B2C/B2B and decision-relationship cues in the source.
6. **Only emit `role` for B2B personas, and don't restate the committee role there.** The committee role now lives in `persona_type`. The `role` block carries the *details*: title, what they own, influence level. Omit the block entirely for consumer personas rather than emitting an empty one.
7. **Fill `demographics` descriptively, not operationally.** Pull the individual attributes the source provides as plain values. Don't transcribe index/composition stats, and don't treat this as targeting logic — that's the Audience object's job.
8. **Fold rich data into implications.** A deck full of Resonate index/composition stats, media-channel tables, brand logos, and a day-in-the-life wheel is signal — but the numbers themselves are out of scope. Translate them into fields.
9. **Keep `behavioral_traits` to characterizations, not a data dump.** 5-10 crisp behaviors, not every statistic. This is the field most likely to balloon — resist it.
10. **One persona per object.** If a source covers several personas/segments, build one object each.
11. **Write fields as clean, self-contained phrases** a strategist or an agent could act on without the original deck.

## Output rules

- Emit valid JSON (no comments in the actual output — the `jsonc` above is illustrative).
- One object per persona. Save using the OSMM instance-naming convention: `PERSONA_<entity-slug>.json`, with an optional instance slug when one entity has multiple personas (e.g. `PERSONA_wendys-deal-savvy-craver.json`) — uppercase object name, underscore join, lowercase entity/instance slug. See `CONVENTION.md` → "Instance file naming". The `persona_id` (`PER-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin in the source so they can fill gaps.

---

## Worked examples

### Example 1 — B2C consumer persona

Input: a consumer persona deck for a household brand, dense with research stats and a day-in-the-life profile.

```json
{
  "object_type": "persona",
  "osmm_version": "0.1.0",
  "persona_id": "PER-acme-busy-parent",
  "version": "1.0",
  "status": "draft",
  "name": "The Busy Parent",
  "persona_type": "consumer_household_decision_maker",
  "summary": "Affluent suburban parent who wants to make smart, quality purchases for the household but is perpetually short on time and resistant to complexity.",
  "representative_quote": "I just need it to work — I don't have time to research five options or wait three weeks for delivery.",
  "demographics": {
    "age": "Mid-30s to mid-40s",
    "household": "Married, one or two children under 12",
    "income": "~$120–160K household",
    "location": "Suburban"
  },
  "triggers": [
    "A household item breaks or wears out and needs immediate replacement",
    "A seasonal or life-stage change (new home, new child) creates a new category need",
    "A peer recommendation or online review breaks through the consideration paralysis"
  ],
  "goals": [
    "Make reliable purchases that don't require rework or returns",
    "Simplify household management without sacrificing quality",
    "Feel confident they got good value, not just a low price"
  ],
  "motivations": [
    "Family wellbeing and home comfort",
    "Efficiency — protecting scarce time",
    "Social proof and feeling like a competent decision-maker"
  ],
  "pain_points": [
    "Too many options with insufficient signal to differentiate them",
    "Returns and replacements are a hidden cost of cheap decisions",
    "Discovery is fragmented across platforms — hard to find trusted sources quickly"
  ],
  "objections": [
    "Skeptical of brands they haven't heard of, even with good reviews",
    "Resistant to subscriptions or commitments before trust is established"
  ],
  "behavioral_traits": [
    "Researches on mobile, often buys on desktop or in-store",
    "Relies heavily on reviews and word-of-mouth; trusts friends/family over advertising",
    "Streaming-first; avoids interruptive ad formats",
    "Highly loyal once trust is earned — low churn if satisfaction holds"
  ],
  "decision_criteria": [
    "Reliability and quality reputation",
    "Ease of purchase and delivery",
    "Price relative to perceived value (not lowest price)"
  ],
  "messaging_preferences": [
    "Lead with outcomes and reliability, not features or specs",
    "Use social proof and testimonials as primary credibility signals",
    "Reach via streaming, social, and word-of-mouth; minimize interruptive formats"
  ],
  "linked_audiences": ["AUD-PLACEHOLDER-acme-busy-parent"],
  "source": "Acme consumer segmentation research, Resonate / Gale (2024)"
}
```

---

### Example 2 — B2B decision maker (high-tech purchase)

Input: a B2B persona profile for a VP of IT or technology infrastructure lead evaluating enterprise software vendors.

```json
{
  "object_type": "persona",
  "osmm_version": "0.1.0",
  "persona_id": "PER-enterprise-vp-it",
  "version": "1.0",
  "status": "draft",
  "name": "The Enterprise Technology Buyer",
  "persona_type": "b2b_decision_maker",
  "summary": "Senior IT or technology leader at a large enterprise who owns infrastructure and platform decisions — highly risk-averse, accountable to the board for security and uptime, and deeply skeptical of vendor claims that haven't been validated by peers or analysts.",
  "representative_quote": "I'm not buying a product — I'm buying a relationship. I need to know you'll still be there in five years and that your team will answer the phone when something breaks.",
  "demographics": {
    "age": "40s to mid-50s",
    "education": "BS/MS in Computer Science, Engineering, or MIS",
    "location": "Major metro or remote; enterprise HQ",
    "occupation": "VP of IT, VP of Infrastructure, CTO (mid-market), Director of Enterprise Architecture"
  },
  "triggers": [
    "An existing vendor contract is up for renewal and the incumbent has underdelivered",
    "A security incident or compliance audit exposes gaps in the current stack",
    "A board or C-suite mandate to modernize, reduce costs, or adopt AI/cloud at scale",
    "An acquisition or merger forces platform consolidation"
  ],
  "goals": [
    "Maintain system reliability, security, and compliance at enterprise scale",
    "Reduce total cost of ownership without sacrificing capability or support quality",
    "Deliver on executive mandates for cloud migration, AI adoption, or infrastructure modernization",
    "Minimize organizational disruption during platform transitions"
  ],
  "motivations": [
    "Career protection — a failed implementation is a career event, not just a project miss",
    "Credibility with the C-suite and board as a strategic technology leader, not just a cost center",
    "Genuine belief in the right technical architecture for the organization's future"
  ],
  "pain_points": [
    "Vendor sales cycles that consume team bandwidth without delivering useful signal",
    "Proof of concepts that look great but don't translate to production performance at scale",
    "Integration complexity and hidden implementation costs that inflate TCO post-contract",
    "Vendors who disappear after the deal closes and before go-live is stable"
  ],
  "objections": [
    "Skeptical of AI and automation claims that haven't been validated at their scale and in their industry",
    "Concerned about vendor lock-in and what exit looks like if the platform underperforms",
    "Wary of vendors whose customer success model is thin relative to the sales motion"
  ],
  "behavioral_traits": [
    "Consults Gartner, Forrester, and G2/peer review sites before engaging vendors directly",
    "Relies on peer networks (CIO forums, industry groups) for trusted signal",
    "Involves security, legal, and finance early — deals rarely move on a single buyer",
    "Long evaluation cycles (6–18 months for major platform decisions); late-stage decisions move quickly once consensus is built"
  ],
  "decision_criteria": [
    "Security posture, compliance certifications, and audit trail capability",
    "Proven scalability in comparable enterprise environments",
    "Total cost of ownership including implementation, integration, and ongoing support",
    "Vendor stability and long-term roadmap credibility",
    "Quality of implementation and post-sale support, not just product capability"
  ],
  "messaging_preferences": [
    "Lead with enterprise credibility signals: customer logos, analyst recognition, compliance certifications",
    "Peer case studies and reference calls carry more weight than vendor-produced content",
    "Technical depth is expected — don't simplify away the architecture conversation",
    "ROI and TCO models must be honest and specific, not generic; inflated claims destroy trust"
  ],
  "role": {
    "title": "VP of IT / VP of Infrastructure / Director of Enterprise Architecture",
    "responsibilities": [
      "Own infrastructure, platform, and security architecture decisions",
      "Manage vendor relationships and contract renewals",
      "Deliver technology roadmap aligned to business strategy",
      "Report to CIO or CTO; present major investment cases to CFO or board"
    ],
    "influence_level": "high"
  },
  "linked_audiences": ["AUD-PLACEHOLDER-enterprise-vp-it"],
  "source": "Composite B2B persona based on enterprise technology buyer research (2024)"
}
```
