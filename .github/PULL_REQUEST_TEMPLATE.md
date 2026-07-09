<!--
Thanks for contributing to OSMM! Keep PRs focused — one object, one fix, or one
example where practical (see CONTRIBUTING.md). Delete sections that don't apply.
-->

## What this changes

<!-- A clear description of what changes and why. Link any related issue (e.g. "Closes #12"). -->

## Type of change

- [ ] New builder skill for an object already in the registry
- [ ] New object proposal (opened an issue first — see CONTRIBUTING.md)
- [ ] New / updated example instance
- [ ] Docs or convention change
- [ ] Fix (schema, script, or docs)

## Which tenet(s) does it serve?

<!-- e.g. "lean over over-engineered", "grounded in real assets" — see GOVERNANCE.md#design-tenets -->

## Checklist

- [ ] Follows the naming/frontmatter conventions in [`CONVENTION.md`](../CONVENTION.md)
      (slug = folder = frontmatter `name`; `object_type` uses underscores, slug uses hyphens).
- [ ] If it touches `schemas/` or `examples/`, I ran `python scripts/validate.py`
      locally and it passes (CI runs it too).
- [ ] Any new object enters at `status: draft`, and ships its canonical strict
      schema at `schemas/<object_type>.schema.json`.
- [ ] Examples are **real and public-sourced** (no client/confidential data).
- [ ] Skill `description` frontmatter is ≤ 1024 characters.
- [ ] I updated the tracker in the **same PR** ([`roadmap/BACKLOG.md`](../roadmap/BACKLOG.md):
      moved the card, bumped counts + "Last updated") when this ships OSMM work.
- [ ] Each commit is signed off per the [DCO](../DCO) (`Signed-off-by:` — `git commit -s`).

<!--
By submitting this pull request, I certify the contribution under the Developer
Certificate of Origin (DCO) — see the DCO file and CONTRIBUTING.md.
-->
