# Getting Started with OSMM

**A practical guide for marketers. No engineering required.**

If you can write a creative brief, you can use OSMM. This guide takes you from
nothing installed to a working set of marketing objects your AI tools can
actually reason over.

---

## What OSMM is, in plain terms

Your marketing knowledge already exists. It's just trapped.

Your positioning is in a slide deck. Your personas are in a PDF from an agency
two years ago. Your campaign brief is a Word doc in someone's inbox. Your
audience definitions live in a spreadsheet — and a slightly different version of
them lives in the ad platform. Every time you brief an agency, onboard a new
hire, or ask an AI assistant for help, you re-explain all of it from scratch.

**OSMM turns each of those documents into a structured object** — a small,
standard file that both people and AI can read the same way, every time. A
persona stops being 14 slides and becomes a Persona Object. A campaign brief
becomes a Campaign Strategy Object. They link to each other, so an AI can follow
the thread from a campaign to its audience to its offer to the creative without
you re-pasting context.

You don't write these files by hand. **You hand Claude the deck, and a builder
skill writes the object for you.**

## Why bother

Three things change once your context is structured:

**You stop re-explaining yourself.** Build your Business Context and Persona
objects once. Every future brief, campaign, and AI conversation starts from them
instead of from a blank page.

**AI output gets sharply better.** An assistant working from a Persona Object
knows your customer's triggers, objections, and language. One working from
"here's a 40-slide deck, good luck" does not.

**Your work becomes portable.** Objects aren't locked in a vendor's platform.
They're plain files you own, in an open standard.

---

## Install (2 minutes)

In Claude, run these two commands:

```
/plugin marketplace add open-semantic-marketing-model/osmm
/plugin install osmm@osmm
```

That's it. You now have 18 builder skills. To get updates later, run
`/plugin marketplace update osmm` then `/plugin update osmm`. Full details in
[`PLUGIN.md`](PLUGIN.md).

---

## Your first object, in five minutes

Start with **Business Context** — it's the foundation everything else references,
and you already have what you need.

1. Grab something that describes your company: an About page, a pitch deck, an
   investor update, a company one-pager. Anything real.
2. Hand it to Claude and say:

    > *"Build an OSMM business context object from this."*

3. Claude picks the right builder, asks you a few clarifying questions where the
   source is thin, and writes a `BUSINESS-CONTEXT_<yourcompany>.json` file.
4. Read it. Fix anything that's wrong — it's your context, and the object is only
   as good as the source.

You just made your first OSMM object. Now do a **Persona** the same way, from
whatever persona research you have.

You never need to write JSON. You review it.

---

## The one rule that makes this work

**Build context before you build work product.**

Context objects (Business, Brand, Product, Persona, Audience) are the durable
layer — they're true for a year, not a sprint. Everything else *references* them.
If you skip straight to a Campaign Strategy without a Persona, the campaign has
nothing to point at, and you've just made a fancier version of the brief you
already had.

Five Context objects is a realistic, high-value first project. Most teams stop
there for a while, and that's fine — it's where most of the leverage is.

---

## What to build, in what order

OSMM follows the shape of the work you already do. Seven phases:

| Phase | The question you're answering | What you build |
|-------|-------------------------------|----------------|
| **1. Define Strategy** | Who are we, what do we sell, what are we trying to achieve? | Business Context, Brand Context, Product Context, Marketing Strategy, Measurement Framework |
| **2. Define Audience** | Who are we talking to? | Persona, Audience |
| **3. Define Offer** | What's the reason to act now? | Offer |
| **4. Define Campaign & Journey** | How does this reach them, and in what order? | Campaign Strategy, Journey |
| **5. Define Content & Creative** | What do we say, and how do we say it? | Creative Strategy, Content Strategy *(and the Creative Brief artifact)* |
| **6. Build & Deliver** | What actually ships? | Experience, Experience Component |
| **7. Measure, Learn & Optimize** | What happened, why, and what do we change? | Performance Measurement, Customer Insight, Optimization Recommendation |

**Persona vs. Audience** trips everyone up, so learn it once: a **Persona**
*describes* a human archetype (their motivations, objections, language). An
**Audience** *selects* a targetable segment (the criteria that put someone in or
out of the group). Personas explain. Audiences target. They are not the same
object and should never be merged.

---

## Where it pays off

Once your Context objects exist, the pieces compose. Ask Claude:

> *"Write a creative brief for our spring promotion."*

The Creative Brief composer pulls your Business Context, Brand Context, Persona,
and Offer, and drafts a brief grounded in all of them — instead of asking you to
paste four documents. It's a first draft you tailor, not a finished deliverable,
but it starts from your actual context rather than a blank page.

That's the whole thesis: **structure once, compose forever.**

---

## Worked example: Wendy's

The repo ships a complete, public-sourced example set you can read before
building your own. Look at [`examples/`](examples/):

- `BUSINESS-CONTEXT_wendys.json` — who the company is
- `BRAND-CONTEXT_wendys.json` — how it sounds and what it won't say
- `PERSONA_wendys-deal-savvy-craver.json` — a customer archetype
- `AUDIENCE_wendys-value-seekers.json` — the targetable segment that persona sits in
- `MARKETING-STRATEGY_wendys-2026.json` — objectives and positioning
- `MEASUREMENT-FRAMEWORK_wendys-2026.json` — how success gets measured

Notice how the Audience links back to the Persona by ID. That link is what lets
an AI walk the graph. There's a parallel B2B set built on IBM.

---

## Practical notes

**Files are named for you.** Objects save as
`<OBJECT-NAME>_<entity-slug>.json` — e.g. `PERSONA_wendys-deal-savvy-craver.json`.
Keep them together in a folder; that folder is your marketing context library.

**Don't hand-edit the JSON if you can avoid it.** Ask Claude to revise the object.
It knows the schema; a stray comma will break the file.

**Objects are only as good as their sources.** Feed it a real persona study and
you get a real Persona. Feed it vibes and you get structured vibes. Garbage in,
neatly-formatted garbage out.

**Client or confidential material stays out of the public repo.** Build objects
for client work in your own workspace. The `examples/` in this repo are all built
from public sources on purpose.

**It's a draft standard (v0.1).** Objects will evolve. Schemas change under
semver with real deprecation, never silent breaks — the policy is in
[`GOVERNANCE.md`](GOVERNANCE.md).

---

## Common questions

**Do I need to build all 18 objects?** No. Most teams should build five Context
objects and stop. Add work-product objects when you have a real campaign that
needs them.

**Do I need to know JSON?** No. You need to be able to read a structured document
and tell whether it's right about your business.

**Can I use this with my existing tools?** OSMM doesn't replace your MarTech
stack. It's the decision layer that sits above it — the structured brief your
tools and agents read from.

**What if an object doesn't fit my business?** Say so. Propose a change — OSMM is
maintainer-led but open. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

---

## Next steps

1. **Install the plugin** (two commands above).
2. **Build your Business Context** from your own material.
3. **Build a Persona** from your best persona research.
4. **Ask for a creative brief** and watch it pull from both.
5. Read [`TAXONOMY.md`](TAXONOMY.md) when you want the full map of phases and
   objects, and [`RELATIONSHIPS.md`](RELATIONSHIPS.md) when you want to see how
   objects reference each other.

Start with one object. The rest follows.
