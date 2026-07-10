# Security Policy

OSMM is a **specification** — canonical JSON Schemas, documentation, and builder
skills — plus a small amount of Python tooling (`scripts/validate.py`,
`scripts/gen_object_graph.py`) used only in development and CI. There is no
deployed service or runtime, so the realistic security surface is narrow: issues
in the validation/generation scripts, a malformed schema that could mislead a
downstream consumer, or a supply-chain concern in the CI workflow.

## Supported versions

The standard is at **draft** and evolves on `main`. Security fixes are applied to
`main`; there are no separately-maintained release branches yet.

## Reporting a vulnerability

Please **do not open a public issue** for a security concern.

Report privately using **GitHub's private vulnerability reporting** — go to the
repository's **Security** tab → **Report a vulnerability**. This keeps the report
confidential within GitHub and routes it directly to the maintainers. (If the
Security tab is not visible, the maintainers have not yet enabled private
reporting — open a minimal public issue asking them to enable it, without
disclosing the vulnerability details.)

When you report, please include:

- a description of the issue and the file(s) involved,
- steps to reproduce, and
- the potential impact as you see it.

You can expect an acknowledgement within a few business days. Once a fix is
prepared we will coordinate disclosure with you and credit you in the release
notes unless you prefer to remain anonymous.

## Scope notes

- **Example data** under `examples/` is drawn from public sources about real
  brands (e.g. IBM, Wendy's) for illustration only; it contains no secrets or
  private data. If you believe an example inadvertently includes sensitive or
  non-public information, report it through the private channel above.
- **Trademark or licensing** questions are not security issues — see
  [`TRADEMARK.md`](TRADEMARK.md) and [`LICENSING.md`](LICENSING.md).
