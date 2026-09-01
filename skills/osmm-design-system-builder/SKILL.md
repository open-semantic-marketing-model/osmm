---
name: osmm-design-system-builder
description: >-
  Convert any visual identity or design system source into a structured OSMM Design System Object
  (canonical JSON). Inputs include brand books, visual identity guidelines, design system sites,
  Figma libraries, design token files, logo usage guides, packaging standards, or a designer's notes.
  Use this skill whenever the user wants to capture how a brand LOOKS — logo and identity rules,
  color palette and semantic roles, typography and type scale, imagery and art direction,
  iconography, motion, layout and grid, accessibility standards, rights and licensing, and the
  constraints governing what an AI system may generate with the identity. Triggers include "build a
  design system object," "capture our visual identity," "house this client's design system,"
  "structure our brand guidelines," "objectify our brand book," or handing over a style guide,
  brand book, or token file and asking what to do with it.
  This is the visual counterpart to Brand Context, which owns voice and messaging.
object: Design System Object
object_type: design_system
category: Context Object
phase: 1
wave: 1
osmm_version: 0.1.0
status: draft
---

# OSMM Design System Builder

Build a valid **OSMM Design System Object** from any source describing how a brand *looks*.

A Design System Object is durable, foundational Context — the structured record of a brand's
**visual identity**: its marks and lockups, its color system, its typography, its imagery and art
direction, its icons, motion, layout, accessibility standards, asset rights, and the rules governing
what a generative system may produce with that identity. It resolves workflow sub-process **1.10
Define Design System** and is revised through the Phase 7 learning loop (**7.7**) like any other
durable Context.

It is the **visual counterpart to Brand Context**. Brand Context owns how the brand *sounds*; this
object owns how the brand *looks*. The two pair one-to-one on the same slug (`BRC-ibm` ↔ `DSY-ibm`)
and together form the complete identity. They are separate objects because they have different
owners, different change cadences, and different consumers: a copy generator needs voice principles
and guardrails; a layout or asset generator needs the type scale and the palette. Keeping them apart
means each consumer loads only what it needs.

## Core design rule — carry the semantic layer, reference the raw source

OSMM standardizes the *decisions* in a design system, not its artifacts.

- **Carry** the semantic layer: what each color is *for*, what each type step *does*, what the
  identity rules *forbid*, what a generator *may* produce. A downstream agent can act on this.
- **Reference** the raw layer: the full token tree, the component library, the asset binaries. Point
  at them via `token_sources[]` and `asset_sources[]` with a version, and stop there.
- **Never mirror** hundreds of tokens into the object. The upstream source is the source of truth
  for values; duplicating it guarantees drift.

The one deliberate exception: **embed the core palette and type scale**. Most brands have a brand
book and no token file, and an object with no values at all is not operable. Capture the core
palette and the scale by role; leave the exhaustive ramp upstream.

## Boundaries — what this object is and is NOT

| Object | Owns | This object's relationship |
|--------|------|----------------------------|
| **Brand Context** | The **verbal** identity — voice, tone, personality, messaging pillars, and messaging guardrails. | **Paired peer**, referenced via `linked_brand_context`. Brand Context's `visual_identity_notes` is a one-line summary and `design_system_reference` an external pointer; when a Design System Object exists, **this object is the authoritative home** and those fields stay thin. |
| **Business Context** | The company — what it is, sells, and competes on. | **Upstream**, optional via `linked_business_context`. |
| **Creative Strategy** | The **campaign-scoped** creative direction — the big idea, themes, emotional strategy, and `channel_creative` treatment for a specific piece of work. | **Downstream consumer.** Creative Strategy expresses a campaign *inside* this system. Durable channel specs (safe zones, aspect ratios, minimum sizes) live here in `channel_specs`; the campaign's creative treatment for that channel lives there. |
| **Experience Component** | The reusable built blocks (headline, hero, CTA, offer card). | **Downstream consumer.** Components are built to this system; they don't redefine it. |
| **Experience** | The assembled deliverable and its rendered asset. | **Downstream consumer.** |
| **Design System** (this) | The durable **visual** identity: identity, color, typography, imagery, iconography, motion, layout, accessibility, channel specs, rights, and generation constraints (1.10). | — |

Rules of thumb:

- **Durable, not campaign.** If it changes when the campaign changes, it belongs in Creative
  Strategy. If it holds across every campaign for years, it belongs here.
- **Rules, not renders.** Capture the rule that governs the asset, never the asset.
- **One system per brand.** A company with distinct sub-brands gets one object per sub-brand, each
  paired with that sub-brand's Brand Context. How the system flexes across them goes in
  `brand_architecture_rules`.

## The output schema

> **Canonical schema:** [`schemas/design_system.schema.json`](../../schemas/design_system.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "design_system",        // const — always "design_system"
  "osmm_version": "0.1.0",               // schema version this conforms to
  "design_system_id": "DSY-<slug>",      // stable, human-readable id (see ID rules)
  "version": "1.0",                      // instance version; bump on revision
  "status": "draft",                     // draft | proposed | stable | deprecated

  "name": "",                            // the system's own name (e.g. "IBM Design Language")
  "linked_brand_context": "",            // BRC-<slug> of the paired Brand Context (placeholder ok)
  "linked_business_context": "",         // OPTIONAL — BIZ-<slug> of the owning Business Context
  "owner": "",                           // OPTIONAL — the team/role that owns and approves changes

  "design_principles": [],               // 3-6 durable visual principles — how the system decides

  "identity": {                          // the mark and its protections
    "primary_mark": "",                  // the primary logo/mark and its canonical form
    "mark_variants": [],                 // OPTIONAL — approved variants and when each is used
    "lockup_rules": "",                  // OPTIONAL — how the mark locks up with names/taglines
    "clear_space": "",                   // OPTIONAL — minimum clear space, in the system's own unit
    "minimum_size": "",                  // OPTIONAL — minimum reproduction size
    "misuse_rules": [],                  // OPTIONAL — explicit don'ts (high value for generation)
    "co_branding_rules": ""              // OPTIONAL — partner/sponsor/endorsement lockups
  },

  "color": {
    "palette": [                         // ≥1 — semantic role first, raw value second
      { "token": "", "name": "", "value": "", "role": "", "usage_notes": "" }
    ],
    "usage_rules": [],                   // OPTIONAL — proportion, pairing, and forbidden combos
    "modes": []                          // OPTIONAL — light / dark / high-contrast behavior
  },

  "typography": {
    "typefaces": [                       // ≥1 — licensing is not optional detail
      { "name": "", "role": "", "foundry": "", "license": "", "fallback_stack": "", "weights": [] }
    ],
    "type_scale": [                      // OPTIONAL — by role, not by pixel guess
      { "token": "", "role": "", "size": "", "weight": "", "line_height": "", "letter_spacing": "" }
    ],
    "usage_rules": []                    // OPTIONAL — pairing, hierarchy, case, and the never-dos
  },

  "imagery": {                           // OPTIONAL — strongly encouraged
    "art_direction": "", "subject_matter": [], "treatment": "", "sourcing": "",
    "representation": "", "dos": [], "donts": []
  },

  "iconography": {                       // OPTIONAL
    "style": "", "source": "", "illustration_style": "", "usage_rules": []
  },

  "motion": {                            // OPTIONAL
    "principles": [], "durations": "", "easing": "", "usage_rules": []
  },

  "layout": {                            // OPTIONAL
    "grid": "", "spacing_scale": "", "breakpoints": [], "composition_principles": []
  },

  "accessibility": {                     // OPTIONAL — strongly encouraged
    "conformance_target": "", "contrast_requirements": "", "minimum_type_size": "", "requirements": []
  },

  "channel_specs": [                     // OPTIONAL — durable format rules, not campaign treatment
    { "channel": "", "specifications": "" }
  ],

  "brand_architecture_rules": [],        // OPTIONAL — how the system flexes for sub-brands/partners
  "localization_rules": [],              // OPTIONAL — scripts, RTL, substitute faces, regional meaning

  "rights_and_licensing": [              // OPTIONAL — the rights that expire and restrict
    { "asset_type": "", "terms": "", "expires": "", "rights_holder": "" }
  ],

  "generation_constraints": {            // OPTIONAL — what a model may produce with this identity
    "generative_imagery_permitted": true,
    "permitted": [], "prohibited": [], "style_descriptors": [],
    "negative_prompts": [], "human_review_required": []
  },

  "token_sources": [                     // OPTIONAL — reference the raw tokens, don't mirror them
    { "type": "", "name": "", "reference": "", "source_version": "" }
  ],
  "asset_sources": [                     // OPTIONAL — where the binaries live; OSMM never holds them
    { "type": "", "name": "", "reference": "", "access_notes": "" }
  ],

  "source": ""                           // one line: what source(s) this was built from and when
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"design_system"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `design_system_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | The system's own name if it has one; otherwise `"<Brand> Design System"`. |
| `linked_brand_context` | string | no | `BRC-<slug>` of the paired Brand Context. Use `BRC-PLACEHOLDER-<slug>` if it doesn't exist yet. Strongly recommended — the pair is the full identity. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning Business Context. |
| `owner` | string | no | The team or role that owns and approves changes. Design systems have a different owner and cadence from the verbal brand; recording it prevents unattributed drift. |
| `design_principles` | string[] | yes | 3-6. Principles, not adjectives: *"Type carries the hierarchy; color never has to"* beats *"clean."* |
| `identity` | object | yes | `primary_mark` required. `misuse_rules` is the highest-value sub-field — see principle 3. |
| `color` | object | yes | `palette` required (≥1). Capture `role`, not just the swatch. |
| `typography` | object | yes | `typefaces` required (≥1). Always try to capture `license` — see principle 5. |
| `imagery` | object | no | Strongly encouraged. The fastest route to off-brand output. |
| `iconography` | object | no | Icons and illustration. |
| `motion` | object | no | Non-optional in practice for social, CTV, and product UI. |
| `layout` | object | no | Grid, spacing, breakpoints, composition. |
| `accessibility` | object | no | Strongly encouraged. A generator violates whatever isn't written down. |
| `channel_specs` | object[] | no | **Durable** format rules only. Campaign treatment is Creative Strategy's `channel_creative`. |
| `brand_architecture_rules` | string[] | no | Sub-brands, endorsed brands, acquisitions, regions, partnerships. |
| `localization_rules` | string[] | no | Script coverage, RTL, substitute faces, regional color meaning. |
| `rights_and_licensing` | object[] | no | The field nobody models and everybody gets burned by. Capture anything time-bound. |
| `generation_constraints` | object | no | The reason this is an object and not a linked PDF. See principle 6. |
| `token_sources` | object[] | no | Pointers to the upstream machine-readable source, with a version. |
| `asset_sources` | object[] | no | DAM, Figma library, Storybook, brand portal. OSMM never holds binaries. |
| `source` | string | no | One line. Provenance and approximate date. |

## ID rules

`design_system_id` = `DSY-` + a lowercase, hyphen-delimited slug — normally the **same slug as the
paired Brand Context**, so the pair is obvious at a glance. Keep it stable once assigned.

- IBM → `DSY-ibm` (pairs with `BRC-ibm` and `BIZ-ibm`)
- Wendy's → `DSY-wendys` (pairs with `BRC-wendys` and `BIZ-wendys`)

A brand with genuinely separate sub-brand systems gets one object each, disambiguated by a second
slug segment (e.g. `DSY-ibm-consulting`).

## Extraction principles

1. **Roles before values.** `#0F62FE` is not usable knowledge; *"the primary interactive color, used
   deliberately and never as a background wash"* is. Always capture what a color or type step is
   **for**. A palette of bare hex codes teaches a downstream agent nothing.
2. **Principles, not adjectives.** "Clean and modern" describes nothing and constrains nothing. Push
   every principle until it makes a decision: *"Neutral ground, deliberate accent."*
3. **The don'ts are worth more than the dos.** Misuse rules, forbidden color pairings, and image
   don'ts are what actually protect a brand at scale, and they are exactly what a generative system
   violates first. Extract them carefully; they are the most operational content in the object.
4. **Mark uncertainty rather than inventing precision.** Where a brand publishes no design system,
   you are reading its expression, not its standards. Capture the roles and rules you can genuinely
   observe and write *"to be confirmed against brand standards"* for exact hex values, typeface
   names, and licensing terms. A confident wrong hex is worse than an honest gap — see the Wendy's
   example below.
5. **Chase the licensing.** An unlicensed typeface is a legal exposure and a production blocker, and
   time-bound photography, music, and talent rights expire while the assets sit in the DAM looking
   usable. Capture terms and expiry whenever the source gives them, and flag the gap when it doesn't.
6. **Write the generation constraints even if the source has none.** Almost no brand book was
   written with generative systems in mind, so this section is usually inferred from the identity
   rules rather than quoted. Infer it anyway, and say you did. The rule *"never regenerate the mark,
   place it from approved artwork"* follows directly from any normal logo standard, and it is the
   single most useful line in the object.
7. **Reference, don't mirror.** When a token file, Figma library, or component package exists, point
   at it with a version and keep the object semantic. Copying the token tree in guarantees drift.
8. **Durable only.** A seasonal campaign palette is not a design system. If it expires, it belongs in
   Creative Strategy.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per brand or sub-brand. Save using the OSMM instance-naming convention:
  `DESIGN-SYSTEM_<entity-slug>.json` (e.g. `DESIGN-SYSTEM_ibm.json`) — uppercase object name,
  underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The
  `design_system_id` (`DSY-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Set `linked_brand_context` to the real `BRC-<slug>` if the Brand Context exists; otherwise use a
  `BRC-PLACEHOLDER-<slug>` and tell the user to resolve it once that object is built.
- Briefly tell the user what you **extracted** vs. **inferred** vs. **flagged for confirmation**, and
  call out anything thin — especially missing licensing terms, accessibility standards, and
  generation constraints, which sources almost never contain.
- **Never copy client-confidential material into the OSMM repository.** Client design systems are
  built as instances in the client's own workspace; only real, public-sourced examples belong in
  `examples/` (see `CONVENTION.md` → "Where instance files live").

## Starter prompts

**From a brand book or visual identity guidelines:**
> Build an OSMM Design System Object for [Brand]. Sources: [brand book / visual identity guidelines /
> logo usage guide / packaging standards]. Capture the identity rules and misuse don'ts, the palette
> with semantic roles, the type system with licensing, art direction, and accessibility standards.
> Infer generation constraints from the identity rules and flag them as inferred.

**From a published design system or token source:**
> Build an OSMM Design System Object for [Brand] from its design system at [URL / Figma library /
> token file]. Carry the semantic layer — roles, rules, and the core palette and scale — and
> reference the token source and component library rather than mirroring the full token tree.

**From public expression only (no internal docs):**
> Build an OSMM Design System Object for [Brand] from its public expression — website, app,
> packaging, advertising, and social. Capture roles, rules, and principles you can genuinely observe;
> mark exact hex values, typeface names, and licensing terms "to be confirmed" rather than guessing.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). The full canonical
instances live in `examples/` (`DESIGN-SYSTEM_ibm.json`, `DESIGN-SYSTEM_wendys.json`); the excerpts
below illustrate the two build paths.

### Example 1 — a brand that publishes its system (IBM)

Built from the public IBM Design Language, the Carbon Design System token reference, and the IBM Plex
repository. Values are quoted because the brand publishes them; the object still references the token
source rather than mirroring it.

```json
{
  "object_type": "design_system",
  "osmm_version": "0.1.0",
  "design_system_id": "DSY-ibm",
  "version": "1.0",
  "status": "draft",
  "name": "IBM Design Language",
  "linked_brand_context": "BRC-ibm",
  "design_principles": [
    "Good design is good business — design is a business discipline at IBM, not decoration",
    "Carry the hierarchy with type and grid; color is a signal, never the structure",
    "Neutral ground, deliberate accent — restraint is the brand's most recognizable trait"
  ],
  "identity": {
    "primary_mark": "The IBM 8-bar logo — the striped 'IBM' wordmark designed by Paul Rand in 1972, still the sole primary mark.",
    "misuse_rules": [
      "Never redraw, restripe, or regenerate the 8-bar mark — it is reproduced from approved artwork only",
      "Never apply effects — shadows, gradients, outlines, bevels, or textures"
    ]
  },
  "color": {
    "palette": [
      { "token": "$blue-60", "name": "IBM Blue 60", "value": "#0F62FE", "role": "primary / interactive",
        "usage_notes": "The brand's anchor blue and the primary interactive color. Used deliberately, not as a background wash." },
      { "token": "$gray-100", "name": "Gray 100", "value": "#161616", "role": "surface (dark) / text" }
    ],
    "usage_rules": ["Color never carries meaning alone — pair it with type, icon, or position"]
  },
  "typography": {
    "typefaces": [
      { "name": "IBM Plex Sans", "role": "display, headline, body, UI",
        "foundry": "Commissioned by IBM (Mike Abbink with Bold Monday)",
        "license": "Open source under the SIL Open Font License 1.1 — removes the seat-licensing constraint most brand systems carry",
        "fallback_stack": "'IBM Plex Sans', 'Helvetica Neue', Arial, sans-serif" }
    ]
  },
  "generation_constraints": {
    "generative_imagery_permitted": true,
    "prohibited": [
      "Generating, redrawing, or approximating the 8-bar mark — it is placed from approved artwork only",
      "Inventing colors outside the published palette, including 'close' variations of IBM Blue"
    ],
    "negative_prompts": ["glowing blue circuit board", "digital brain, neural network cliché"]
  },
  "token_sources": [
    { "type": "Design tokens (published theme tokens)", "name": "Carbon Design System theme and type tokens",
      "reference": "https://carbondesignsystem.com/elements/color/tokens/" }
  ]
}
```

### Example 2 — a brand that publishes nothing (Wendy's)

Built from observable public expression: website, app, packaging, advertising, and social. This is
the more common client situation. Note how roles and rules are captured confidently while exact
values are **flagged rather than guessed** — principle 4 in practice.

```json
{
  "object_type": "design_system",
  "osmm_version": "0.1.0",
  "design_system_id": "DSY-wendys",
  "version": "1.0",
  "status": "draft",
  "name": "Wendy's Design System",
  "linked_brand_context": "BRC-wendys",
  "design_principles": [
    "The food is the hero — every composition earns its way back to the product",
    "Red is the brand and it is loud; everything else stays out of its way",
    "Freshness is shown, not claimed — texture, steam, and real ingredients do the work a claim can't"
  ],
  "color": {
    "palette": [
      { "name": "Wendy's Red", "role": "primary",
        "usage_notes": "The dominant brand color, used at full strength as a background and in the mark. Exact value to be confirmed against brand standards." },
      { "name": "Promotional yellow", "role": "accent (value messaging)",
        "usage_notes": "Reserved for value and limited-time-offer communications. It signals a deal; it is not a general accent." }
    ],
    "usage_rules": ["Promotional yellow appears only in value and LTO contexts — using it elsewhere devalues it"]
  },
  "typography": {
    "typefaces": [
      { "name": "Brand headline face", "role": "display, headline",
        "license": "To be confirmed against brand standards — licensing scope (desktop, web seats, broadcast) must be verified before production use." }
    ]
  },
  "generation_constraints": {
    "generative_imagery_permitted": false,
    "prohibited": [
      "Generating, redrawing, or restyling the Wendy character in any form",
      "Generating food imagery presented as Wendy's product",
      "Generating prices, offer terms, dates, or availability"
    ],
    "human_review_required": ["Any cultural-moment or reactive social post"]
  },
  "source": "Built from Wendy's publicly observable visual expression (accessed 2026). Exact token values, typeface names, and licensing terms are flagged 'to be confirmed' rather than guessed."
}
```
