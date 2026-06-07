---
name: osmm-audience-builder
description: >-
  Convert any segmentation or audience source into a structured OSMM Audience Object (canonical JSON).
  Inputs include segmentation studies, audience/segment definitions, CRM or CDP segment exports,
  lifecycle and value-tier frameworks, firmographic target lists, or a strategist's targeting notes.
  Use this skill whenever the user wants to define a targetable segment — "build an audience object,"
  "define this segment," "structure our audience/segment," "turn this segmentation into our format,"
  "objectify this target group," or hands over a segment definition and asks what to do with it. The
  Audience Object is OSMM's addressable segment: who is in, who is out, and what makes them a group.
object: Audience Object
object_type: audience
category: Context Object
phase: 2
wave: 1
osmm_version: 0.1.0
status: draft
---

# OSMM Audience Builder

Build a valid **OSMM Audience Object** from any source that defines a targetable group of customers.

An Audience Object is durable, reusable Context — the structured, **addressable segment**: the membership rules that say who is in and who is out, the lens the segment is drawn on, and its lifecycle and value position. Work Products (Targeting Strategy, Campaign Strategy) and Configurations reference it to decide *who* a campaign is for. Where a Persona answers "who is this person and what drives them," an Audience answers "who exactly are we targeting, and how is that group defined."

This is the lean v0.1 builder. It captures what a marketing workflow needs to *select* a group and nothing more. Raw segmentation math (index/composition tables, model coefficients, exact counts) is deliberately out of scope — distill it into operational membership criteria instead of transcribing the numbers.

## "Segment" is the Audience Object

A **Segment** is not a separate OSMM object — it is exactly what the Audience Object represents. OSMM uses "Audience" as the name for the addressable segment, and the taxonomy is explicit: sub-process **2.2 "Define Audience Segments"** (segment definitions + inclusion criteria), **2.3** (inclusion/exclusion logic), and **2.6** (lifecycle & value segmentation) all write to the Audience Object. When someone says "segment," build an Audience Object; the `segmentation_basis` field records *which kind* of segment it is.

> The one place the industry sometimes splits them — a *Segment* as pure membership logic vs. an *Audience* as an activated, channel-synced instantiation — is an **activation/delivery** concern (Phase 6), not Context. Capture the lightweight version in `activation_notes`; a separate object would only be warranted if/when OSMM needs to model one segment synced as many platform audiences, or one audience composed via set-algebra of several segments.

## Persona vs. Audience — one describes, one selects

This is the central boundary in the Context layer (it mirrors the rule stated in the persona builder):

- **Persona** *describes* — an individual, qualitative portrait (motivations, needs, behaviors). Its demographics are a descriptive snapshot.
- **Audience** *selects* — a group, defined operationally so it can be queried and targeted. Its attributes are **membership criteria**, not description.

Same subject, different jobs. A demographic fact lives in the Persona as colour ("a busy parent in their 30s") and in the Audience as a **rule** ("age 30–45 AND has children in household"). A Persona *brings an Audience to life*; link them with `linked_personas` (and the Persona's `linked_audiences`).

**Not here:** *prioritizing* audiences against each other is the **Targeting Strategy Object** (2.1, 2.8), a Work Product. The Audience Object defines a segment; it does not rank it.

## The output schema

Emit a single JSON object with this exact shape. Field order should match.

```jsonc
{
  "object_type": "audience",            // const — always "audience"
  "osmm_version": "0.1.0",             // schema version this conforms to
  "audience_id": "AUD-<slug>",          // stable, human-readable id (see ID rules)
  "version": "1.0",                     // instance version; bump on revision
  "status": "draft",                    // draft | proposed | stable | deprecated

  "name": "",                           // the audience/segment name
  "linked_business_context": "",        // id of the Business Context this audience belongs to (BIZ-<slug>; placeholder ok)

  "description": "",                    // 2-3 sentences: who this segment is and why it matters to marketing
  "segmentation_basis": "",             // controlled enum — the primary lens the segment is drawn on (see vocabulary)
  "lifecycle_stage": "",                // OPTIONAL controlled enum — lifecycle position, if the segment is lifecycle-bound

  "inclusion_criteria": [],             // the rules/attributes that DEFINE membership — operational, queryable ("who's in")
  "exclusion_criteria": [],             // OPTIONAL — who is explicitly out ("who's not")

  "defining_signals": [],               // OPTIONAL — the behaviors/attributes that most distinguish this segment
  "size_estimate": "",                  // OPTIONAL — marketing-relevant scale (qualitative or rough band), never a precise count
  "value_characterization": "",         // OPTIONAL — the segment's value/worth (e.g. high-LTV, price-sensitive, low-frequency)

  "linked_personas": [],                // ids of Persona Objects that humanize this audience (placeholder ok)
  "activation_notes": "",               // OPTIONAL — where/how this segment is addressable (channels, platforms)
  "source": ""                          // one line: what source(s) this was built from and approximate date
}
```

### Field types and requirements

| Field | Type | Required | Notes |
|---|---|---|---|
| `object_type` | string (const `"audience"`) | yes | Never changes. |
| `osmm_version` | string | yes | Use `0.1.0` until told otherwise. |
| `audience_id` | string | yes | See ID rules below. |
| `version` | string | yes | Start at `"1.0"`. |
| `status` | enum | yes | Default `"draft"`. |
| `name` | string | yes | The segment's name. Make it self-describing ("Lapsed value buyers"), not a code. |
| `linked_business_context` | string | no | `BIZ-<slug>` of the owning business. Use `BIZ-PLACEHOLDER-<slug>` if not built yet. Strongly recommended. |
| `description` | string | yes | 2-3 sentences. Who the segment is and why it matters — plain language. |
| `segmentation_basis` | enum | yes | Controlled vocabulary — see below. The *primary* lens. If the segment blends lenses, pick the dominant one and note the blend in `description`/`inclusion_criteria`. |
| `lifecycle_stage` | enum | no | Controlled vocabulary — see below. Include only if the segment is defined by lifecycle position (e.g. "lapsed buyers"). |
| `inclusion_criteria` | string[] | yes | The membership rules — **operational and queryable**, not prose. "Purchased in last 90 days," "company size 500+ employees," "opened ≥3 emails in 30d." 2-8 items. |
| `exclusion_criteria` | string[] | no | Who is explicitly out. Include only where exclusion does real work (e.g. "exclude current subscribers"). |
| `defining_signals` | string[] | no | The handful of attributes/behaviors that most distinguish this segment from adjacent ones. |
| `size_estimate` | string | no | Rough, marketing-relevant scale — a band or qualitative note, never a precise count. Omit if unknown. |
| `value_characterization` | string | no | The segment's economic value/worth (LTV tier, price sensitivity, frequency). The "value segmentation" of 2.6. |
| `linked_personas` | string[] | no | Persona ids that humanize this audience. Use `PER-PLACEHOLDER-<slug>` if none exists yet. |
| `activation_notes` | string | no | Lightweight note on where/how the segment is addressable (channels/platforms). Not a full delivery spec. |
| `source` | string | no | One line. Provenance and approximate date. |

## Segmentation basis vocabulary

`segmentation_basis` is a controlled, governed enum — a stored snake_case token mapping to a human-readable label. Pick the single closest *primary* lens.

| Stored value | Label |
|---|---|
| `demographic` | Demographic |
| `geographic` | Geographic |
| `psychographic` | Psychographic |
| `behavioral` | Behavioral |
| `firmographic` | Firmographic (B2B) |
| `technographic` | Technographic (B2B) |
| `needs_based` | Needs-based |
| `value_based` | Value-based |
| `lifecycle` | Lifecycle stage |
| `intent` | Intent / in-market |
| `lookalike` | Lookalike / modeled |

## Lifecycle stage vocabulary

`lifecycle_stage` is an OPTIONAL controlled, governed enum. Omit it unless the segment is genuinely defined by lifecycle position.

| Stored value | Label |
|---|---|
| `prospect` | Prospect (not yet engaged) |
| `lead` | Lead (engaged, not bought) |
| `new_customer` | New customer |
| `active` | Active customer |
| `lapsed` | Lapsed / at-risk |
| `loyal` | Loyal / repeat |
| `advocate` | Advocate |
| `churned` | Churned |

## ID rules

`audience_id` = `AUD-` + a lowercase, hyphen-delimited slug. Lead with the business slug when the audience belongs to a specific business, then the segment descriptor.

- Wendy's value seekers → `AUD-wendys-value-seekers`
- IBM enterprise IT buyers → `AUD-ibm-enterprise-it`

## Extraction principles

1. **Criteria must be operational, not descriptive.** The test: could someone build this segment from the criteria? "Cares about value" is description (Persona); "redeemed ≥2 value-menu offers in 90 days" is a criterion (Audience). Translate attitudes into the observable signals that stand in for them.
2. **Pick the basis that actually defines the segment.** A "lapsed high-value buyer" is primarily `lifecycle` or `value_based`, not `demographic` — choose the lens that does the defining work; note secondary lenses in `description`.
3. **Keep description and criteria distinct.** `description` is plain "who and why"; `inclusion_criteria` is the rule set. Don't restate one as the other.
4. **Don't prioritize here.** If the source ranks segments, that ranking belongs to a Targeting Strategy Object. Capture *this* segment's definition only.
5. **Value and lifecycle are signal-bearing, not mandatory.** Fill `value_characterization`/`lifecycle_stage` when the source supports them; omit rather than guess.
6. **Link the human.** If a Persona for this segment exists (or is planned), set `linked_personas` (placeholder ok) — the describe/select pair is most useful connected.
7. **One segment per object.** A segmentation study with five segments yields five Audience Objects, each linked to the same Business Context.
8. **Numbers become bands.** Never transcribe exact model outputs or counts; `size_estimate` is a band or qualitative note.

## Output rules

- Emit valid JSON (no comments in the actual output).
- One object per segment. Save using the OSMM instance-naming convention: `AUDIENCE_<entity-slug>.json` (e.g. `AUDIENCE_wendys-value-seekers.json`) — uppercase object name, underscore join, lowercase entity slug. See `CONVENTION.md` → "Instance file naming". The `audience_id` (`AUD-<slug>`) remains the id *inside* the object; it is not the filename.
- Validate it parses before returning it.
- Resolve `linked_business_context` and `linked_personas` to real ids where those objects exist; otherwise use placeholders and tell the user what to resolve later.
- Briefly tell the user what you turned from description into operational criteria, and flag any criteria that are inferred rather than stated.

## Starter prompts

**From a segmentation study:**
> Build OSMM Audience Objects for [Brand] from this segmentation study. Create one Audience Object per segment, translating each segment's profile into operational inclusion criteria, the primary `segmentation_basis`, and value/lifecycle where given. Link each to `BIZ-<brand>` and to its Persona if one exists.

**From a targeting brief / CRM definition:**
> Build an OSMM Audience Object for the "[segment name]" segment. Sources: [CRM/CDP definition, targeting brief]. Capture the inclusion/exclusion rules exactly, the lifecycle stage and value tier, and note how it's activated.

---

## Worked examples

Real, public brands (per `CONVENTION.md` → "Where worked examples live"). Full canonical instances live in `examples/context/`.

### Example 1 — B2C value-based segment (Wendy's)

Built from public knowledge of Wendy's value-driven customer base. Brings the `PER-wendys-deal-savvy-craver` persona to life as a targetable group.

```json
{
  "object_type": "audience",
  "osmm_version": "0.1.0",
  "audience_id": "AUD-wendys-value-seekers",
  "version": "1.0",
  "status": "draft",
  "name": "Value Seekers",
  "linked_business_context": "BIZ-wendys",
  "description": "Price-sensitive, high-frequency fast-food customers who choose where to eat largely on value and current deals. They are the core audience for Wendy's value menu and app-driven offers, and skew younger and mobile-first.",
  "segmentation_basis": "value_based",
  "lifecycle_stage": "active",
  "inclusion_criteria": [
    "Visits QSR brands 2+ times per week",
    "Redeems value-menu items or app offers (e.g. Biggie Bag, 4 for $4) on a majority of visits",
    "Engages with the brand's app and/or social channels",
    "Skews age 18–34"
  ],
  "exclusion_criteria": [
    "Premium/full-service diners who rarely use value menus",
    "Lapsed customers with no visit in 6+ months (separate win-back segment)"
  ],
  "defining_signals": ["Deal redemption rate", "App usage and offer engagement", "Late-night and high-frequency visit patterns"],
  "size_estimate": "Large — the core volume segment for the value daypart",
  "value_characterization": "Moderate per-ticket value but high frequency; lifetime value driven by visit cadence and offer-led repeat",
  "linked_personas": ["PER-wendys-deal-savvy-craver"],
  "activation_notes": "Addressable via the Wendy's app/loyalty, paid social, and short-form video; offer-led creative performs best.",
  "source": "Built from public information: Wendy's marketing and QSR category knowledge (2024). Criteria are illustrative operational definitions, not internal CRM rules."
}
```

### Example 2 — B2B firmographic segment (IBM, abbreviated)

Contrasts a B2B firmographic segment with Example 1's B2C value segment. Full instance: `examples/context/AUDIENCE_ibm-enterprise-it.json`.

```json
{
  "object_type": "audience",
  "osmm_version": "0.1.0",
  "audience_id": "AUD-ibm-enterprise-it",
  "version": "1.0",
  "status": "draft",
  "name": "Enterprise IT Decision Makers",
  "linked_business_context": "BIZ-ibm",
  "description": "Senior technology decision-makers at large enterprises and regulated organizations evaluating hybrid cloud and enterprise AI platforms. The core audience for watsonx and Red Hat consideration.",
  "segmentation_basis": "firmographic",
  "inclusion_criteria": [
    "Organization size 1,000+ employees (or regulated mid-market)",
    "Role in IT/technology leadership (CIO, CTO, VP Infrastructure, platform leads)",
    "Operates a hybrid or multi-cloud environment",
    "Active modernization or AI initiative in the current cycle"
  ],
  "exclusion_criteria": ["SMB with no enterprise IT function", "Net-new startups without hybrid infrastructure needs"],
  "value_characterization": "Very high deal value and long lifetime; multi-year platform and consulting relationships",
  "linked_personas": ["PER-PLACEHOLDER-ibm-enterprise-buyer"],
  "source": "Built from public information: IBM positioning and enterprise-technology category knowledge (2024). Criteria illustrative, not internal targeting rules."
}
```
