<picture>
  <source media="(prefers-color-scheme: dark)" srcset="brand/osmm-primary-horizontal-reversed.svg">
  <img alt="OSMM — Open Semantic Marketing Model" src="brand/osmm-primary-horizontal.svg" width="440">
</picture>

# Open Semantic Marketing Model

**An open interoperability standard for the decision work of marketing.**

OSMM defines canonical, machine-readable objects — and the relationships
between them — for the parts of marketing that have always lived in documents:
brand context, personas, audiences, creative and campaign strategy, journeys,
measurement, and the learning that flows back into all of it. It is not a
platform, a taxonomy, or a vendor framework. It is the shared structure that
lets people, tools, and AI agents operate against a common definition of the
work.

---

## Why this exists

Three decades and billions of dollars into MarTech, the *decision* work of
marketing still runs on slide decks, spreadsheets, and PDFs. Briefs live in
Word, personas in decks, audiences in Excel, journeys in Miro. There is no
shared structure to any of it, so every handoff between teams or tools happens
in meetings and inboxes rather than in systems.

That was an inefficiency tax in a pre-AI world. As organizations move to
automate the decision work itself, it becomes the constraint: LLMs and agents
need structured context to be reliable, and they cannot scale on free-text
briefs and strategy decks. OSMM gives that work a structure to compose against.

A structured object is also far cheaper to reason over than its source
artifact — roughly a 5× reduction in tokens versus the source text it distills,
and far more versus a rendered deck. We frame this honestly as *distillation,
not lossless compression*: the canonical JSON is the interoperability contract,
and richer source assets are referenced, not replaced.

## How it works

Every object is a typed JSON document with stable references to other objects,
so an agent can resolve a campaign to its audience, its offer, its creative,
and its measurement framework without bespoke integration code.

```json
{
  "object_type": "persona",
  "version": "1.0",
  "persona_id": "PER-example",
  "persona_type": "consumer",
  "representative_quote": "I want to know exactly what I'm getting.",
  "triggers": ["...", "..."],
  "demographics": { "...": "..." }
}
```

The model is deliberately **lean over over-engineered** — minimal cores with
optional extensions — and grounded in real assets rather than invented
examples.

## The object model

OSMM currently spans **34 objects** across **7 workflow phases**, grouped into
**5 categories** by their read/write and governance profile:

| Category | Purpose |
|----------|---------|
| **Context** | Durable, reusable business intelligence (Business Context, Brand Context, Audience, Persona, Keyword). High-read, low-write. |
| **Work Product** | The structured outputs of decisions that today live in documents (Marketing Strategy, Creative Strategy, Campaign Strategy, Journey Strategy, …). |
| **Configuration** | Operational logic for orchestration (Journey Configuration, Personalization Configuration). |
| **Measurement** | Performance data structured for analysis. Append-only. |
| **Learning** | Durable insight that updates the Context layer — the loop that makes the model compound rather than reset. |

Each builder is a skill named `osmm-<object-slug>-builder`; the full registry
and naming convention live in [`CONVENTION.md`](CONVENTION.md).

## Repository structure

```
osmm/
├── schemas/        # canonical JSON schemas, by category
├── examples/       # validated example instances grounded in real assets
├── skills/         # builder skills (osmm-<object>-builder), by category
├── brand/          # logo, color tokens, usage — see brand/LOGO.md
├── CONVENTION.md   # object registry + skill naming convention
├── GOVERNANCE.md   # maintainer-led review model
├── CONTRIBUTING.md # how to propose objects and changes
└── README.md
```

## Status

Early and active — **draft v0.1**. The standard is being built iteratively:
ship a concrete, validated artifact, then refine. First validated builder is
`osmm-persona-builder`, tested against a real consumer persona. Schemas evolve
under strict semantic versioning with formal deprecation, never silent breaks.

## Relationship to OSI

OSMM is complementary to the [Open Semantic Interchange](https://open-semantic-interchange.org)
(OSI), not competitive. OSI operates at the BI/metrics layer; OSMM is the
marketing-decision layer that sits above it. Think of OSMM as the
decision-object companion to OSI's metrics objects.

## Governance & contributing

OSMM is **maintainer-led, not consensus-driven** — open standards fragment when
consensus becomes the goal. The community submits pull requests and proposed
objects; a small, opinionated maintainer core of operators reviews and approves
changes. See [`GOVERNANCE.md`](GOVERNANCE.md) and [`CONTRIBUTING.md`](CONTRIBUTING.md).

## License

Schemas and code: **Apache 2.0**. Documentation: **CC BY 4.0**. See
[`LICENSE`](LICENSE) and [`LICENSE-docs`](LICENSE-docs).

## Brand

Logo files, color tokens, and usage rules are in
[`brand/LOGO.md`](brand/LOGO.md). The wordmark is set in IBM Plex Mono (SIL OFL 1.1).
