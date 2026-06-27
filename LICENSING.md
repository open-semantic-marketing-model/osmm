# Licensing

OSMM is released under a **dual license**, plus a separate **trademark policy**
for the brand. This file is the authoritative mapping of which terms apply to
which parts of the repository. Where this file and a file header disagree, this
file governs.

Copyright © 2026 **Design of Work Partners LLC**.

## Per-path license map

| Path | Contents | License |
|------|----------|---------|
| `schemas/**` | Canonical JSON Schemas | Apache-2.0 — [`LICENSE`](LICENSE) |
| `scripts/**` | Validation / generation code | Apache-2.0 — [`LICENSE`](LICENSE) |
| `skills/**` | Builder skills (`SKILL.md` + assets) | Apache-2.0 — [`LICENSE`](LICENSE) |
| `examples/**` | Validated example instances | CC BY 4.0 — [`LICENSE-docs`](LICENSE-docs) |
| `*.md` at repo root (`README`, `CONVENTION`, `TAXONOMY`, `RELATIONSHIPS`, `GOVERNANCE`, `CONTRIBUTING`, `GRAPH`, `CHANGELOG`) | Documentation | CC BY 4.0 — [`LICENSE-docs`](LICENSE-docs) |
| `roadmap/**` | Roadmap & backlog docs | CC BY 4.0 — [`LICENSE-docs`](LICENSE-docs) |
| `osmm-object-graph.svg` | Generated documentation diagram | CC BY 4.0 — [`LICENSE-docs`](LICENSE-docs) |
| `brand/*.svg` | Logo / wordmark artwork | **Trademark-protected — [`TRADEMARK.md`](TRADEMARK.md). NOT under CC BY 4.0 or Apache-2.0.** |
| `brand/LOGO.md` | Brand-guideline text (excluding the artwork it describes) | CC BY 4.0 — [`LICENSE-docs`](LICENSE-docs) |

**Why the split.** Apache-2.0 is the right fit for the functional, reusable
parts (schemas, code, and the builder skills that operate on them) because it
carries an explicit patent grant and a clear contribution clause. CC BY 4.0 fits
the prose and the example data — reuse is encouraged, attribution is required.
The logo and name are deliberately kept **out** of both open licenses: they are
trademarks, and open-licensing the artwork would undercut the brand control a
standard depends on. See [`TRADEMARK.md`](TRADEMARK.md).

## Attribution

For CC BY 4.0 material, attribute as:

> "Open Semantic Marketing Model (OSMM), © Design of Work Partners LLC, used
> under CC BY 4.0."

## A note on GitHub's license badge

GitHub detects a single primary license per repository and will display
**Apache-2.0** (from `LICENSE`). That badge does not capture the documentation
(CC BY 4.0) or the trademark terms — this file is the complete picture.

## Third-party material

The wordmark uses **IBM Plex Mono** (IBM Plex © IBM Corp., SIL OFL 1.1). The
font files are not redistributed here — type in the logo SVGs is outlined to
vector paths. Example instances reference third-party companies (e.g., IBM,
Wendy's) nominatively for illustration; their names and marks belong to their
respective owners, and their inclusion implies no affiliation or endorsement.
