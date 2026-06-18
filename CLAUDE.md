# OSMM™ — Project Guide for Claude

The Open Semantic Marketing Model: a standard of 18 typed, addressable marketing
**objects**, each built by an `osmm-<object>-builder` skill, plus non-normative
`osmm-<artifact>-composer` skills that render human artifacts from those objects.

## Orientation (read these first)

- [`TAXONOMY.md`](TAXONOMY.md) — the 7 phases and the 18 objects.
- [`CONVENTION.md`](CONVENTION.md) — naming, frontmatter contract, builder
  registry, composer class, and the schema/example promotion rules.
- [`RELATIONSHIPS.md`](RELATIONSHIPS.md) — how objects reference each other.
- [`GOVERNANCE.md`](GOVERNANCE.md) / [`CONTRIBUTING.md`](CONTRIBUTING.md) — tenets,
  lifecycle, and how changes land.
- [`roadmap/`](roadmap/) — what's built, in progress, and next.

## Working agreements

1. **Keep the tracker current — every time.** Whenever we ship work on OSMM (a
   builder, composer, example, or doc), update [`roadmap/BACKLOG.md`](roadmap/BACKLOG.md):
   move the item's card (To Do → In Progress → Done), update the "Progress at a
   glance" counts, and bump the "Last updated" date. If it changes the plan,
   update [`roadmap/ROADMAP.md`](roadmap/ROADMAP.md) too. Do this **in the same
   commit/PR** as the work, so the tracker never drifts from reality.
2. **One focused change per PR** (one object, fix, or example) — per
   `CONTRIBUTING.md`.
3. **Follow the conventions exactly.** Builders match `CONVENTION.md`
   (slug = folder = frontmatter `name`; schema inline until a second tool needs
   it; `object_type` uses underscores, slugs use hyphens). New objects enter at
   `status: draft`.
4. **Examples must be real and public-sourced.** Client/confidential data never
   enters the repo (see `CONVENTION.md` → "Where instance files live"). Reference
   brands: **IBM** (B2B) and **Wendy's** (B2C).

## Repo map

- `skills/<category>/` — builder skills (`context`, `work-product`,
  `configuration`, `measurement`, `learning`) and `skills/artifacts/` (composers).
- `examples/<category>/` — validated, public-sourced instances.
- `schemas/` — standalone schemas (added only on promotion).
- `roadmap/` — backlog and roadmap.
