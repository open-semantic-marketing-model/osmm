# OSMM™ Examples

A library of **validated OSMM object instances** — the canonical, machine-readable
`.json` files that other tools read directly: the `osmm-creative-brief-composer`
(which consumes `business_context` + `persona` instances), a future `-validator`,
and third-party importers.

These are the *promoted* form of an example. Builders also carry one or two
**inline** worked examples in their `SKILL.md` for teaching the output shape at
the point of use; an instance is promoted to a file here when a second tool needs
to read it independently of the builder. See
[`CONVENTION.md`](../CONVENTION.md) → "Where worked examples live."

## Rules

- **Real and publicly sourced only.** Every instance is built from public
  material — public-company filings, the brand's own public site, published
  research. The repo is openly licensed, so nothing confidential can live here.
- **Client work never enters the repo** — it is real but confidential, a
  different category from "not yet promoted." Client and internal instances stay
  outside the repo permanently.
- **Filenames follow the instance-naming convention** —
  `<OBJECT-NAME>_<entity-slug>.json` (see `CONVENTION.md` → "Instance file
  naming").
- **Organized by object category**, mirroring `skills/` (`context/`,
  `work-product/`, `configuration/`, `measurement/`, `learning/`).

## Reference brands

The corpus is anchored on two public companies so instances interlink into
coherent sets and exercise both `business_type` paths of the composer:

- **IBM** — enterprise B2B (`enterprise_software`), built from public filings.
- **Wendy's** — consumer QSR (`b2c`), built from public information.

## Current contents

| File | Object | Entity | Notes |
|------|--------|--------|-------|
| `context/BUSINESS-CONTEXT_ibm.json` | Business Context | IBM | Real, public-filing-grounded. |
| `context/BUSINESS-CONTEXT_wendys.json` | Business Context | Wendy's | Real, public-information-grounded. |
| `context/BRAND-CONTEXT_ibm.json` | Brand Context | IBM | Voice/guardrails from public brand expression; guardrails inferred. |
| `context/BRAND-CONTEXT_wendys.json` | Brand Context | Wendy's | Voice/guardrails from public brand expression; guardrails inferred. |
| `context/AUDIENCE_ibm-enterprise-it.json` | Audience | IBM | B2B firmographic segment; illustrative operational criteria. |
| `context/AUDIENCE_wendys-value-seekers.json` | Audience | Wendy's | B2C value-based segment; linked to the Wendy's persona (Persona ↔ Audience). |
| `context/PERSONA_wendys-deal-savvy-craver.json` | Persona | Wendy's | Illustrative persona synthesized from public market knowledge. `linked_audiences` resolved to `AUD-wendys-value-seekers` (v1.1). |

> The Wendy's set (Business Context + Brand Context + Persona) and the IBM set
> (Business Context + Brand Context) now cover the **required inputs** of
> `osmm-creative-brief-composer`, so it can be exercised end-to-end on Wendy's.

As more builders ship and more public-sourced instances are validated, this
library grows by category.

---

*Example instances reference third-party companies (e.g., IBM, Wendy's) nominatively, built only from public material, for illustration. Their names and marks belong to their respective owners; inclusion implies no affiliation or endorsement. Examples are licensed CC BY 4.0 (see [`../LICENSING.md`](../LICENSING.md)).*
