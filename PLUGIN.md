# The OSMM Plugin

The OSMM builder skills ship as a **Claude plugin**, distributed from this
repository. Install it once and every OSMM builder becomes available in Claude;
update it with one command as the standard evolves.

---

## Install

Two commands in Claude (Claude Code or Cowork):

```
/plugin marketplace add open-semantic-marketing-model/osmm
/plugin install osmm@osmm
```

The first registers this repository as a plugin marketplace. The second installs
the `osmm` plugin — all 18 builder skills, the canonical JSON Schemas they
validate against, and the worked examples.

## Stay up to date

```
/plugin marketplace update osmm
/plugin update osmm
```

Run these to pull the latest released version of the standard. Clients receive a
new version whenever the maintainers bump the plugin version (see
[Releasing](#releasing-maintainers) below) — not on every commit, so the standard
stays stable underneath them.

## What you get

| Category | Skills |
|----------|--------|
| **Context** (5) | `osmm-business-context-builder`, `osmm-brand-context-builder`, `osmm-product-context-builder`, `osmm-persona-builder`, `osmm-audience-builder` |
| **Work Product** (9) | `osmm-marketing-strategy-builder`, `osmm-measurement-framework-builder`, `osmm-offer-builder`, `osmm-campaign-strategy-builder`, `osmm-journey-builder`, `osmm-creative-strategy-builder`, `osmm-content-strategy-builder`, `osmm-experience-builder`, `osmm-experience-component-builder` |
| **Measurement** (1) | `osmm-performance-measurement-builder` |
| **Learning** (2) | `osmm-customer-insight-builder`, `osmm-optimization-recommendation-builder` |
| **Artifacts** (1) | `osmm-creative-brief-composer` |

Skills are namespaced by the plugin, so they appear as `osmm:osmm-persona-builder`
and so on. In practice you rarely type them — the skill descriptions are
trigger-rich, so saying *"turn this persona deck into an OSMM object"* invokes the
right builder.

New to OSMM? Start with [`GETTING-STARTED.md`](GETTING-STARTED.md).

---

## How it's wired

The **plugin root is the repository root** (`"source": "./"` in
`.claude-plugin/marketplace.json`). This is deliberate and load-bearing:

- Each `SKILL.md` points at its canonical schema with a repo-relative path
  (`../../../schemas/<object_type>.schema.json`).
- Claude copies a plugin into a local cache on install. Files **outside** the
  plugin root are not copied.
- Making the repo root the plugin root means `schemas/` and `examples/` travel
  with the skills, so those references resolve after install.

If the plugin root were `skills/` alone, every schema reference would break.

The manifests:

- **`.claude-plugin/plugin.json`** — the plugin manifest. Declares the version and
  lists the five skill category directories.
- **`.claude-plugin/marketplace.json`** — the marketplace catalog, so this repo can
  be added directly with `/plugin marketplace add`.

Because `plugin.json` lists skill **category directories** (not individual
skills), a new builder dropped into an existing category is picked up
automatically — no manifest edit required.

---

## Releasing (maintainers)

Client installs only update when the **plugin version changes**. Version is pinned
in `.claude-plugin/plugin.json`; a commit alone does not ship an update. That is
intentional — it matches the semver governance in
[`GOVERNANCE.md`](GOVERNANCE.md) and keeps the standard from shifting under
adopters on every docs typo.

**To ship a release:**

1. **Land the change** — a builder needs its `SKILL.md`, its canonical schema in
   `schemas/`, and at least one validated example in `examples/`
   (see [`CONTRIBUTING.md`](CONTRIBUTING.md)).
2. **Run validation** — `python scripts/validate.py`. CI runs it too; it must pass.
3. **Bump the version** in `.claude-plugin/plugin.json`, following semver:
   - **patch** (`0.1.0` → `0.1.1`) — clarifications, fixes, docs, non-breaking skill edits.
   - **minor** (`0.1.0` → `0.2.0`) — new builder, new object, new optional field.
   - **major** (`0.1.0` → `1.0.0`) — a breaking schema change (per the deprecation policy).
4. **Update [`CHANGELOG.md`](CHANGELOG.md)** with what changed.
5. **Merge to `main`.** Clients pick it up on their next
   `/plugin marketplace update osmm` + `/plugin update osmm`.

**Adding a new builder to an existing category:** steps 1–5 only. No manifest edit.

**Adding a new *category*:** also add its path to the `skills` array in
`.claude-plugin/plugin.json`.

> **Do not** set `version` in `marketplace.json` as well. When both are set,
> `plugin.json` silently wins, and a stale entry can mask the version you meant to
> ship. `plugin.json` is the single source of truth for the plugin version.

### Testing a release before you push

From a local clone:

```
/plugin marketplace add ./path/to/osmm
/plugin install osmm@osmm
```

Then confirm a builder triggers and resolves its schema. Remove the local
marketplace before re-adding the GitHub one.
