---
name: osmm-brand-context-builder
description: >-
  Convert any brand source into a structured OSMM Brand Context Object (canonical JSON).
  Inputs include brand guidelines, voice-and-tone guides, brand strategy decks, messaging
  frameworks, style guides, brand books, positioning documents, or the brand's own published
  copy and social presence. Use this skill whenever the user wants to capture how a brand
  sounds, feels, and what it must (and must not) say — "build a brand context object,"
  "objectify our brand," "structure our brand guidelines," "capture our brand voice and tone,"
  "turn our brand book into our format," or hands over brand guidelines and asks what to do
  with them. This is the durable brand layer that creative and messaging work references.
object: Brand Context Object
object_type: brand_context
category: Context Object
phase: 1
wave: 1
osmm_version: 0.1.0
status: draft
---

# OSMM Brand Context Builder

Build a valid **OSMM Brand Context Object** from any source describing how a brand sounds, feels, and expresses itself.

A Brand Context Object is durable, foundational Context — the structured understanding of a brand's personality, voice, tone, core messages, and the guardrails that govern what it can and cannot say. It is **layer 1 of the message cascade** (brand → product → persona/journey): every downstream creative and content Work Product — Creative Strategy, Content Strategy — the Journey's `persona_tracks.key_messages`, and every rendered artifact (a creative brief, a campaign) references this brand foundation. Making it explicit and structured means agents and humans produce on-brand work against the same baseline instead of re-deriving the brand's voice each time.

This is the lean v0.1 builder. It captures the brand facts a marketing workflow needs to stay on-voice and compliant, and nothing more. A full visual identity system (logo files, color tokens, type scales) is deliberately out of scope — capture only the marketing-relevant *implications* of visual identity in `visual_identity_notes`. When the brand has a formal design system or design language (e.g. a design-token source, a design-language site, or a component library), point to it in `design_system_reference` — OSMM references that upstream system rather than re-encoding it.

**Key difference from Business Context:** the Business Context Object answers *what the business is, sells, and competes on*; the Brand Context Object answers *how the brand sounds and what it must say*. Business Context carries a thin optional `brand_tone_notes` as a placeholder — the Brand Context Object is its full, authoritative replacement. A Brand Context belongs to a business and points back at it via `linked_business_context`.

**Durable vs. applied messaging.** Brand Context is the **durable** brand layer of the message cascade — voice, guardrails, and the brand promise / `messaging_pillars` (high-read, rarely changes). The *applied*, persona/stage-specific messaging lives in the **Journey** (`persona_tracks.key_messages`) and draws from this brand layer plus Product Context `product_messaging`. Durable brand message lives here; campaign-specific message lives in the journey and references this.

## The output schema

> **Canonical schema:** [`schemas/brand_context.schema.json`](../../../schemas/brand_context.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "brand_context",       // const — always "brand_context"
  "osmm_version": "0.1.0",              // schema version this conforms to
  "brand_context_id": "BRC-<slug>",     // stable, human-readable id (see ID rules)
  "version": "1.0",                     // instance version; bump on revision
  "status": "draft",                    // draft | proposed | stable | deprecated

  "name": "",                           // brand name (may differ from legal company name)
  "linked_business_context": "",        // id of the owning Business Context (BIZ-<slug>; placeholder ok)

  "brand_promise": "",                  // one line: the core idea/promise the brand stands for
  "brand_archetype": "",                // OPTIONAL — controlled enum (see vocabulary); omit if not evident
  "brand_personality": [],              // 3-7 personality traits — who the brand is if it were a person

  "voice_principles": [],               // how the brand speaks — durable principles, not mood
  "tone_principles": [],                // how tone flexes by context/emotion (e.g. celebratory vs. support)
  "tagline": "",                        // OPTIONAL — the brand's tagline/slogan, if it has one

  "messaging_pillars": [],              // the core, durable messages the brand consistently communicates
  "vocabulary_preferred": [],           // OPTIONAL — signature words/phrases the brand uses
  "vocabulary_avoid": [],               // OPTIONAL — words/phrases the brand deliberately avoids
  "writing_dos": [],                    // OPTIONAL — concrete voice do's (actionable)
  "writing_donts": [],                  // OPTIONAL — concrete voice don'ts (actionable)

  "messaging_guardrails": [],           // non-negotiable message rules — claims that must/must not be made
  "mandatories": [],                    // OPTIONAL — required brand/legal elements (disclaimers, required phrasing, lockups)
  "compliance_notes": "",               // OPTIONAL — regulated-industry or legal constraints on messaging

  "visual_identity_notes": "",          // OPTIONAL — brief, marketing-relevant note; full visual system is out of scope
  "design_system_reference": "",        // OPTIONAL — pointer to the brand's design system / design language, if one exists (OSMM references, not models, it)

  "source": ""                          // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"brand_context"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `brand_context_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | The brand name. May differ from the legal company name in Business Context. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. Use `BIZ-PLACEHOLDER-<slug>` if it doesn't exist yet. Strongly recommended. |
| `brand_promise` | string | yes | One sentence: the core idea the brand stands for. Distinct from the business `value_proposition` (a competitive claim) — this is the brand's emotional/identity core. |
| `brand_archetype` | enum | no | Controlled vocabulary — see below. Omit if the sources don't clearly support one. |
| `brand_personality` | string[] | yes | 3-7 traits. Adjectives or short phrases — who the brand is as a person. |
| `voice_principles` | string[] | yes | How the brand *always* speaks (durable). Principles, not adjectives: "Speak plainly; cut the jargon." 3-6 items. |
| `tone_principles` | string[] | yes | How tone *flexes* by situation (a celebratory launch vs. a service apology). 2-5 items. |
| `tagline` | string | no | The brand's slogan/tagline if it has one. Omit if none. |
| `messaging_pillars` | string[] | yes | The core, durable messages the brand repeats across campaigns. 2-5 items. Not campaign copy — the enduring themes. |
| `vocabulary_preferred` | string[] | no | Signature words/phrases the brand uses. Omit if thin. |
| `vocabulary_avoid` | string[] | no | Words/phrases the brand deliberately avoids. Omit if thin. |
| `writing_dos` | string[] | no | Concrete, actionable voice do's. Strongly encouraged — this is what makes the object operational for downstream creative. |
| `writing_donts` | string[] | no | Concrete, actionable voice don'ts. |
| `messaging_guardrails` | string[] | yes | The non-negotiable rules: claims that must always be made and claims that must never be made. This is what the creative-brief composer reads as guardrails. |
| `mandatories` | string[] | no | Required brand/legal elements every execution must carry (legal disclaimers, required phrasing, logo lockups). Omit if none. |
| `compliance_notes` | string | no | Regulated-industry or legal constraints on messaging (e.g. financial-services disclosure rules, health claims). |
| `visual_identity_notes` | string | no | Brief note on visual identity *as it affects marketing* (e.g. "photography is always real customers, never stock"). Full design system is out of scope — link it via `design_system_reference`. |
| `design_system_reference` | string | no | Link or pointer to the brand's external **design system / design language** (a design-token source, design-language site, or component library), if one exists — e.g. IBM Design Language / Carbon, BBC GEL. OSMM references this upstream system rather than modeling it; omit if the brand has none. |
| `source` | string | no | One line. Provenance and approximate date. |

## Brand archetype vocabulary

`brand_archetype` is an OPTIONAL controlled, governed enum — a stored snake_case token mapping to a human-readable label. It uses the widely-recognized 12 brand archetypes. Pick the single closest one; omit the field entirely if the sources don't clearly support one (don't force it).

| Stored value | Label |
|---|---|
| `innocent` | Innocent |
| `everyperson` | Everyperson |
| `hero` | Hero |
| `outlaw` | Outlaw / Rebel |
| `explorer` | Explorer |
| `creator` | Creator |
| `ruler` | Ruler |
| `magician` | Magician |
| `lover` | Lover |
| `caregiver` | Caregiver |
| `jester` | Jester |
| `sage` | Sage |

## ID rules

`brand_context_id` = `BRC-` + a lowercase, hyphen-delimited slug — normally the **same slug as the owning Business Context** so the pair is obvious. Keep it stable: once assigned, downstream objects reference it.

- Wendy's → `BRC-wendys` (pairs with `BIZ-wendys`)
- IBM → `BRC-ibm` (pairs with `BIZ-ibm`)

## Extraction principles

1. **Distill voice into principles, not adjectives alone.** "Witty" is a personality trait; "Earn the joke — be clever, never random" is a voice principle. Personality says who the brand is; voice principles say how to write as them. Capture both.
2. **Guardrails are the highest-value output.** The point of structured brand context is keeping downstream creative on-brand and compliant. Extract the must-say and must-not-say rules carefully — they are what protect the brand at scale.
3. **Separate durable from campaign-specific.** If a source mixes enduring brand voice with a specific campaign's messaging, keep only the durable part here; the campaign/persona-specific part belongs in the Journey's `persona_tracks.key_messages`.
4. **`brand_promise` ≠ `value_proposition`.** The value proposition (in Business Context) is a competitive claim ("better X at lower cost"). The brand promise is the identity/emotional core ("we make the everyday extraordinary"). Don't duplicate the value proposition here.
5. **Ground personality in evidence.** Derive personality and voice from how the brand *actually* speaks in its real copy/social, not from aspirational adjectives in a deck. When a brand guideline asserts a trait the published copy doesn't support, weight the published copy and note the gap.
6. **Make dos and don'ts concrete.** "Be conversational" is weak; "Use contractions and second person; never open with a feature spec" is operational. Downstream agents act on the concrete version.
7. **Keep arrays signal-bearing.** Resist padding. A tight set of real pillars and guardrails beats a long generic list.
8. **One Brand Context per brand.** A company with distinct sub-brands gets one object per sub-brand, each linked to the same Business Context (or to sub-unit Business Contexts).

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per brand. Save using the OSMM instance-naming convention: `BRAND-CONTEXT_<entity-slug>.json` (e.g. `BRAND-CONTEXT_wendys.json`) — uppercase object name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The `brand_context_id` (`BRC-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Set `linked_business_context` to the real `BIZ-<slug>` if the Business Context exists; otherwise use a `BIZ-PLACEHOLDER-<slug>` and tell the user to resolve it once that object is built.
- Briefly tell the user what you inferred vs. extracted, and call out anything thin in the source (especially missing guardrails) so they can fill gaps.

## Starter prompts

**From brand guidelines:**
> Build an OSMM Brand Context Object for [Brand]. Sources: [brand guidelines / voice-and-tone guide / brand book / messaging framework]. Capture durable voice and tone, the core messaging pillars, and especially the must-say / must-not-say guardrails and any legal mandatories.

**From a public brand's own presence (no internal docs):**
> Build an OSMM Brand Context Object for [Brand] from its public presence — website copy, social channels, advertising, and any published brand values. Infer personality and voice from how it actually speaks; flag that guardrails and mandatories are inferred and should be confirmed against internal guidelines.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical instances live in `examples/context/` (`BRAND-CONTEXT_wendys.json`, `BRAND-CONTEXT_ibm.json`); these illustrate the shape.

### Example 1 — B2C consumer brand with a distinctive voice (Wendy's)

Built from Wendy's public presence — its advertising, its famously sharp social voice, and published brand values.

```json
{
  "object_type": "brand_context",
  "osmm_version": "0.1.0",
  "brand_context_id": "BRC-wendys",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's",
  "linked_business_context": "BIZ-wendys",
  "brand_promise": "Quality food served with a side of personality — we don't take the food lightly, but we don't take ourselves too seriously.",
  "brand_archetype": "jester",
  "brand_personality": ["Witty", "Bold", "Irreverent", "Confident", "Culturally fluent", "Warm underneath the edge"],
  "voice_principles": [
    "Earn the joke — be clever and quick, never random or mean for its own sake",
    "Talk like a sharp friend, not a corporation",
    "Lead with the food's quality; let the attitude ride alongside it, not over it",
    "React in real time and in-culture — the brand is fast and current"
  ],
  "tone_principles": [
    "Playful and savage in social banter and roasts",
    "Confident and appetite-first in product and value advertising",
    "Genuine and helpful (drop the snark) in customer service and sensitive moments"
  ],
  "tagline": "Where's the beef? / Fresh, never frozen",
  "messaging_pillars": [
    "Fresh, never frozen beef — real quality, not fast-food compromise",
    "Quality you can taste at a price that's still a deal",
    "A brand with a personality — fun, current, and in on the joke"
  ],
  "vocabulary_preferred": ["fresh", "never frozen", "real", "beef", "deal"],
  "vocabulary_avoid": ["corporate jargon", "generic fast-food clichés", "mean-spirited insults that punch down"],
  "writing_dos": [
    "Use short, punchy lines with confident rhythm",
    "Be specific about food quality (fresh, never frozen) to back the attitude",
    "Use contractions and a conversational, in-the-moment voice"
  ],
  "writing_donts": [
    "Don't be edgy with nothing behind it — the wit must serve the food or the value",
    "Don't punch down or alienate the customer; roast competitors, not people in need",
    "Don't bury the offer or the product behind the joke"
  ],
  "messaging_guardrails": [
    "Always substantiate the 'fresh, never frozen' beef claim — it is the brand's central proof and must stay accurate",
    "Humor must never come at the expense of the customer or marginalized groups",
    "Value/price claims must reflect actual current offers",
    "Franchisee-funded national advertising must work across markets — avoid jokes that don't travel"
  ],
  "mandatories": ["Logo lockup on all paid executions", "Required legal/price disclaimers on offer advertising (e.g. 'at participating locations')"],
  "compliance_notes": "Price and limited-time-offer claims require standard QSR disclaimers ('at participating locations,' 'for a limited time') and must match current franchise pricing.",
  "visual_identity_notes": "Appetite-forward, real-food photography; bold, confident type. The brand's red and the Wendy's character are recognizable equities.",
  "source": "Built from public information: Wendy's advertising, public social channels, and published brand values (2024). Voice and personality inferred from real published copy; guardrails inferred and should be confirmed against internal brand guidelines."
}
```

### Example 2 — B2B enterprise brand (IBM, abbreviated)

Built from IBM's public brand expression — advertising, website, and brand guidelines. Shown abbreviated to contrast a credibility-led B2B voice with Example 1's consumer voice; the full instance is `examples/context/BRAND-CONTEXT_ibm.json`.

```json
{
  "object_type": "brand_context",
  "osmm_version": "0.1.0",
  "brand_context_id": "BRC-ibm",
  "version": "1.0",
  "status": "draft",
  "name": "IBM",
  "linked_business_context": "BIZ-ibm",
  "brand_promise": "Let's create — IBM partners with the world's organizations to put technology to work on their hardest problems.",
  "brand_archetype": "sage",
  "brand_personality": ["Authoritative", "Pragmatic", "Credible", "Forward-looking", "Understated"],
  "voice_principles": [
    "Lead with the business outcome, not the technology",
    "Be precise and substantiated — credibility over hype",
    "Speak as a peer to senior enterprise decision-makers"
  ],
  "tone_principles": [
    "Confident and visionary in brand and thought-leadership work",
    "Clear and technically rigorous in product and developer content"
  ],
  "messaging_pillars": [
    "Enterprise-grade AI and hybrid cloud built for security, scale, and trust",
    "Open technology (Red Hat) that modernizes without lock-in",
    "Deep expertise that turns technology into business outcomes"
  ],
  "messaging_guardrails": [
    "AI claims must emphasize governance, trust, and enterprise readiness — never overstate autonomy",
    "Avoid hype; substantiate capability claims with evidence",
    "Maintain an enterprise, outcome-first frame — not consumer-tech aspiration"
  ],
  "design_system_reference": "IBM Design Language (https://www.ibm.com/design/language/), implemented as the Carbon Design System (https://carbondesignsystem.com/) — design tokens, IBM Plex type, and component library.",
  "source": "Built from public information: IBM advertising, ibm.com, and public brand expression (2024). Guardrails inferred and should be confirmed against internal brand guidelines."
}
```
