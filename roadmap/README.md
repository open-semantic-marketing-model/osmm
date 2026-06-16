# OSMM™ Roadmap & Project Tracker

This folder is the project-management layer for building out OSMM — what's done,
what's in flight, and what's next. It complements (does not replace) the
standard's own docs:

- [`../TAXONOMY.md`](../TAXONOMY.md) — the 7 phases and the 27 objects each resolves to.
- [`../CONVENTION.md`](../CONVENTION.md) — the full builder registry and naming rules.
- [`../RELATIONSHIPS.md`](../RELATIONSHIPS.md) — how objects reference each other.
- [`../GOVERNANCE.md`](../GOVERNANCE.md) — design tenets and the object lifecycle.

## The documents

| Doc | What it is | When to read it |
|-----|------------|-----------------|
| [`BACKLOG.md`](BACKLOG.md) | The **Kanban board** — every work item in **To Do / In Progress / Done**. The single source of truth for status. | "What should I pick up next?" / "What's the status of X?" |
| [`ROADMAP.md`](ROADMAP.md) | The **sequenced plan** — milestones, the build order, dependencies, and the rationale for the sequence. | "Where is this all going?" / "Why this order?" |

## How the work is scoped

Three kinds of deliverable make up the build-out:

1. **Object builders** (`osmm-<object>-builder`) — one per object. **8 of 27 shipped.**
   This is the bulk of the work and the spine of the roadmap.
2. **Artifact composers** (`osmm-<artifact>-composer`) — non-normative
   accelerators that read several objects and render a human artifact. **1 shipped.**
   Each composer is gated on its input objects existing.
3. **Infrastructure** — the example library, validators (and the schema
   promotion they trigger), id-prefix ratification, and vocabulary expansion.

## Keeping this current (working agreement)

> **Update the tracker whenever we ship work on OSMM.** Every time a builder,
> composer, example, or doc lands, move its card in [`BACKLOG.md`](BACKLOG.md)
> (To Do → In Progress → Done), update the counts, and bump the "Last updated"
> line. If the work changes the plan, reflect it in [`ROADMAP.md`](ROADMAP.md)
> too.

This agreement is also recorded in [`../CLAUDE.md`](../CLAUDE.md) so it is loaded
as project context at the start of every session. It is a convention we follow,
not an automated hook — the tracker is only as current as our discipline in
updating it alongside the change (ideally in the same commit/PR).
