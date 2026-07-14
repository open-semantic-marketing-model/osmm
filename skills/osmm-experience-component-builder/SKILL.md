---
name: osmm-experience-component-builder
description: >-
  Convert any reusable building block of an experience into a structured OSMM Experience Component Object (canonical JSON). Inputs include a headline, subheadline, hero, CTA / button copy, a copy block or copy deck, an offer card, a trust block, a content block, a landing-page wireframe, an image treatment, an email subject line, or a preheader — with any copy variations for testing. Use this skill whenever the user wants to capture a reusable component referenced (by id) and assembled into many Experience objects: "build an experience component object," "objectify this headline/hero/CTA," "structure this copy deck," "capture these copy variations," "make this a reusable building block," "turn this wireframe into our format," or "create a trust block / offer card we can reuse." This is a definition referenced, not copied, across experiences. Trigger on reusable component, building block, headline, hero, CTA, copy deck, copy variations, offer card, trust block, wireframe, subject line, preheader.
object: Experience Component Object
object_type: experience_component
category: Work Product
phase: 6
wave: 4
osmm_version: 0.1.0
status: draft
---

# OSMM Experience Component Builder

Build a valid **OSMM Experience Component Object** from any source describing a reusable building
block of an experience — a headline, hero, CTA, copy block, offer card, trust block, content block,
wireframe, image treatment, subject line, or preheader.

An Experience Component is a **reusable atom of experiences**: a single building block, defined once,
that is referenced (by id) and assembled into many **Experience** objects. The value of giving it
its own object is **reuse by reference, not by copy** — the same approved Baconator CTA or watsonx
trust block can appear across dozens of experiences, and when it changes it changes everywhere it is
referenced rather than being re-typed and drifting. Wireframes, designs, and copy decks (sub-process
6.2) are exactly this layer.

It is a **definition, not a rendered asset.** For a headline, CTA, or copy block the component *is*
the text; for a wireframe or image treatment it is a *description / spec* of the block. The rendered
artifact (the deployed email, the live landing page) is downstream — it is assembled from these
components, it is not one.

This is the lean v0.1 builder. It captures one reusable block and the few things needed to reuse it
well — its copy or spec, its signal-bearing variants, where to use it, and the voice/product/persona
it serves. It does not describe the assembled experience, the content plan, or the brand voice
itself — it *references* those.

## Boundaries — what this object is and is NOT

The Experience Component is the smallest, most reusable unit in Phase 6. Keeping the lines clean is
the whole point of giving the building block its own object:

| Object | Answers | Example (IBM) | Example (Wendy's) |
|--------|---------|---------------|-------------------|
| **Experience Component** (this) | What is one *reusable building block* — the copy or spec of a headline, hero, CTA, offer card, trust block, wireframe? | The watsonx "trust block" (governance + IP-indemnification reassurance) | The "Order the Baconator in the app" CTA |
| **Experience** | What is the *assembled deliverable* — the email, landing page, or ad that *references* a set of components? | The watsonx trial landing page that places the trust block | The Baconator app-order landing page that places the CTA |
| **Content Strategy** | What is the *content plan* — themes, formats, cadence, the editorial plan that says what content to make? | The watsonx demand-gen content plan | The Wendy's value-platform content plan |
| **Brand Context** | What is the *voice and guardrails* the component must follow? | IBM brand voice / tone / guardrails | Wendy's brand voice / tone / guardrails |

Rules of thumb:

- **A component is referenced, not copied.** If a block is meant to live in exactly one deliverable
  and never be reused, it may just be content of that Experience. Give it its own Experience
  Component when its value is reuse-by-reference across many experiences.
- **A component is a definition, not a rendered asset.** Capture the copy or the spec, not a
  screenshot or a deployed URL. The rendered, channel-specific thing is the Experience / Experience
  Delivery layer.
- **The component is not the plan.** *Which* content to produce, in *what* themes, formats, and
  cadence is Content Strategy. The component is one concrete block the plan calls for.
- **The component follows the brand voice; it is not the brand voice.** Tone, lexicon, and
  guardrails live in Brand Context. The component *references* it via `linked_brand_context` and
  carries only block-specific `guidelines` (e.g. "always keep the bacon count concrete").

## The output schema

> **Canonical schema:** [`schemas/experience_component.schema.json`](../../schemas/experience_component.schema.json)
> is the single source of truth for this object's shape, and example instances are
> validated against it in CI. The field list and table below are an *illustrative*
> guide for building — if they ever disagree with the schema file, the schema wins.

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "experience_component",   // const — always "experience_component"
  "osmm_version": "0.1.0",                 // schema version this conforms to
  "experience_component_id": "EXC-<slug>", // stable, human-readable id (see ID rules)
  "version": "1.0",                        // instance version; bump on revision
  "status": "draft",                       // draft | proposed | stable | deprecated

  "name": "",                              // human-readable name used to recognize/reference it ("Baconator app CTA")
  "component_type": "",                    // controlled enum — see vocabulary table
  "content": "",                           // the block itself: the copy (headline/CTA/text) OR a description (wireframe/image treatment)

  "variants": [                            // OPTIONAL — signal-bearing alternates, e.g. headline options for testing
    { "variant": "", "content": "" }       // each { variant label, alternate content }
  ],
  "usage_notes": "",                       // OPTIONAL — where/how to use it (placement, context, fit)
  "guidelines": [],                        // OPTIONAL — do's / constraints that govern correct use

  "linked_brand_context": "",              // OPTIONAL — BRC-id of the brand voice/guardrails it follows (placeholder ok)
  "linked_product": "",                    // OPTIONAL — PRD-id of the product it relates to (placeholder ok)
  "linked_personas": [],                   // OPTIONAL — PER-ids it's written for (placeholder ok)
  "source": ""                             // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"experience_component"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `experience_component_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | Human-readable name used to recognize and reference the component. |
| `component_type` | enum | yes | Controlled vocabulary — see below. Pick the single closest. |
| `content` | string | yes | The block itself. For copy components, the *text*; for a wireframe/image treatment, a *description / spec*. |
| `variants` | object[] | no | Signal-bearing alternates, each `{ "variant": "", "content": "" }` — e.g. three headline options for a test. Omit if there's only one version. |
| `usage_notes` | string | no | Where/how to use it: placement, context, the experiences it fits. |
| `guidelines` | string[] | no | Do's and constraints specific to *this* block (not the brand at large). |
| `linked_brand_context` | string | no | `BRC-` id of the Brand Context whose voice/guardrails it follows. `BRC-PLACEHOLDER-<slug>` ok; omit if none. |
| `linked_product` | string | no | `PRD-` id of the Product Context it relates to. `PRD-PLACEHOLDER-<slug>` ok. |
| `linked_personas` | string[] | no | `PER-` ids it's written for. `PER-PLACEHOLDER-<slug>` ok. |
| `source` | string | no | One line. Document-level provenance and approximate date. |

## Component type vocabulary

`component_type` is a controlled, governed enum — a stored snake_case token mapped to a
human-readable label. Extended deliberately by maintainers, never invented per-project.

| Stored value | Label | Use when |
|---|---|---|
| `headline` | Headline | A primary headline / hed — the lead line of a block, page, or ad. |
| `subheadline` | Subheadline | A supporting line beneath a headline (dek/subhead). |
| `hero` | Hero | A hero unit — the lead visual+copy block at the top of a page or email. |
| `cta` | Call to action | A button or link's action copy ("Order in the app", "Start a free trial"). |
| `copy_block` | Copy block | A reusable body-copy block / paragraph (a copy-deck entry). |
| `offer_card` | Offer card | A packaged card presenting an offer (the framing block, referencing an Offer). |
| `trust_block` | Trust block | A reassurance block — guarantees, certifications, indemnification, social proof. |
| `content_block` | Content block | A generic modular content block not covered by a more specific type. |
| `wireframe` | Wireframe | A layout/structure spec for a page or section (described, not rendered). |
| `image_treatment` | Image treatment | An art-direction / image-treatment spec (described, not the asset itself). |
| `subject_line` | Subject line | An email subject line. |
| `preheader` | Preheader | An email preheader / preview text. |
| `other` | Other | A reusable block that doesn't fit the above. Note the nuance in `usage_notes`. |

Pick the single closest value. If a block legitimately blends types, choose the dominant framing and
note the nuance in `usage_notes`.

## ID rules

`experience_component_id` = `EXC-` + a lowercase, hyphen-delimited slug. Prefer a slug that
namespaces the component under its business so ids stay unique across a portfolio, and that names the
block:

- IBM watsonx trust block → `EXC-ibm-watsonx-trust-block`
- Wendy's Baconator CTA → `EXC-wendys-baconator-cta`
- ACME hero headline → `EXC-acme-spring-hero-headline`

Keep it stable: once assigned, Experience objects reference it. On revision bump `version`, never the
id — that is what makes reuse-by-reference safe.

## Extraction principles

1. **Capture one reusable atom.** One object = one building block. If the source is a whole page or
   copy deck, split it into the distinct reusable blocks (a headline, a CTA, a trust block) rather
   than packing them into one component.
2. **Definition, not rendered asset.** Capture the copy or the spec. For copy components, put the
   actual text in `content`; for a wireframe or image treatment, put a clear *description* of the
   block in `content`. Don't paste screenshots or deployed URLs — those belong to the Experience /
   Delivery layer.
3. **Keep variants signal-bearing.** Use `variants` for *meaningfully different* alternates that
   exist to be chosen between or tested (value-led vs. urgency-led headline). Don't pad with trivial
   rewordings; one real variant beats five near-duplicates. Omit `variants` entirely if there's a
   single version.
4. **`guidelines` are block-specific, not the brand.** Capture constraints that govern *this* block's
   correct reuse ("never drop the app-order ask", "keep the bacon count concrete"). The brand voice,
   tone, and lexicon live in Brand Context — reference it via `linked_brand_context`, don't restate
   it.
5. **Don't smuggle in the experience.** Channel, layout assembly, and which components combine into a
   deliverable are the Experience / Experience Delivery layer. The component is the block; it does
   not decide the page it lands on.
6. **Reference, don't copy.** Point at the Brand Context, Product, and personas via the `linked_*`
   fields rather than restating their content. An offer card references its Offer's value exchange;
   it doesn't re-derive the offer.
7. **Name it for reuse.** `name` and the id should make the block recognizable at a glance so an
   Experience author can find and reference it.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per component. Save using the OSMM instance-naming convention:
  `EXPERIENCE-COMPONENT_<entity-slug>.json` (e.g. `EXPERIENCE-COMPONENT_wendys-baconator-cta.json`)
  — uppercase object name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance
  file naming". The `experience_component_id` (`EXC-<slug>`) remains the id *inside* the object; it
  is not the filename.
- Validate it parses before returning it.
- Briefly tell the user what you inferred vs. extracted, and flag anything thin (especially
  `variants` and `guidelines`) so they can fill gaps.
- If you find Experience-level material (channel assembly, full page layouts, deployed creative),
  note it and point the user to the Experience / Experience Delivery objects rather than packing it
  into this one.

## Starter prompts

**B2B reusable block (headline / trust block / CTA):**
> Build an OSMM Experience Component Object for [Company]'s [block name] used in [context]. Capture
> the copy (or, for a wireframe/image treatment, the spec) in `content`, any tested variants, and the
> guidelines that govern its reuse. Link it to `BRC-[company-slug]` for voice and `PRD-[offering-slug]`.

**B2C reusable block (CTA / hero / copy deck):**
> Build an OSMM Experience Component Object for [Brand]'s [block name]. Put the actual copy in
> `content`, add the headline/CTA variations as `variants`, and note where it's used. Link it to
> `BRC-[brand-slug]`, the product it sells (`PRD-[product-slug]`), and the personas it's written for.

---

## Worked examples

### Example 1 — B2C reusable CTA (Wendy's Baconator)

Input: wendys.com / Wendy's app order flow and public Baconator promotion; CTA copy variations
written for app-order testing.

```json
{
  "object_type": "experience_component",
  "osmm_version": "0.1.0",
  "experience_component_id": "EXC-wendys-baconator-cta",
  "version": "1.0",
  "status": "draft",
  "name": "Baconator app-order CTA",
  "component_type": "cta",
  "content": "Order the Baconator in the app",
  "variants": [
    { "variant": "urgency-led", "content": "Get your Baconator now — order in the app" },
    { "variant": "value-led", "content": "Order the Baconator in the app for app-only deals" }
  ],
  "usage_notes": "Primary action for Baconator promotions across email, landing pages, and paid social. Always points to the Wendy's app order flow; pair with a Baconator hero or offer card.",
  "guidelines": [
    "Always keep the app-order ask explicit — drive to the app, not generic 'order now'",
    "Keep it to a single imperative line; no more than ~7 words",
    "Use 'Baconator' by name; don't soften to 'burger'"
  ],
  "linked_brand_context": "BRC-wendys",
  "linked_product": "PRD-wendys-baconator",
  "source": "wendys.com and Wendy's app order flow; CTA variations for app-order testing (2024)"
}
```

### Example 2 — B2B reusable trust block (IBM watsonx)

Input: ibm.com/watsonx governance and Granite IP-indemnification messaging; reusable reassurance
block for trial and demand-gen experiences.

```json
{
  "object_type": "experience_component",
  "osmm_version": "0.1.0",
  "experience_component_id": "EXC-ibm-watsonx-trust-block",
  "version": "1.0",
  "status": "draft",
  "name": "watsonx enterprise-trust block",
  "component_type": "trust_block",
  "content": "Built for regulated scale: watsonx.governance monitors models for drift, bias, and compliance with audit-ready documentation, and IBM Granite models ship with contractual IP indemnification — so you can deploy generative AI on your governed data without taking on the legal and compliance risk that stalls enterprise adoption.",
  "variants": [
    { "variant": "compact", "content": "Governed, auditable, and IP-indemnified: watsonx.governance and indemnified Granite models let you scale enterprise AI without the compliance and legal risk." }
  ],
  "usage_notes": "Reassurance block for watsonx trial and demand-gen experiences — place below the hero or alongside the trial CTA where enterprise buyers weigh risk. Reusable across landing pages, emails, and gated-content experiences.",
  "guidelines": [
    "Lead with governance and IP indemnification — the two enterprise risk-removers",
    "Keep claims grounded in published watsonx.governance and Granite indemnification messaging; no unsubstantiated guarantees",
    "Pair with a trial or demo CTA, not as a standalone block"
  ],
  "linked_brand_context": "BRC-ibm",
  "linked_product": "PRD-ibm-watsonx",
  "source": "ibm.com/watsonx governance and Granite IP-indemnification messaging (2024)"
}
```
