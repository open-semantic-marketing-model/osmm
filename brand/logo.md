# OSMM Logo & Brand Guidelines

**Open Semantic Marketing Model** — visual identity v1.0

The OSMM mark is a 2×2 matrix of rounded squares with a plus formed at its
center. The four cells stand for the object model's structure; the central
plus — surfaced by a filled disc sitting behind the cells and showing through
the cross gap — reads as the "+" of an open, additive, interoperable standard.
The cells use one mint at two values arranged on a diagonal (a single material
catching light differently), anchored by a deep navy plus.

---

## Files

| File | Use |
|------|-----|
| `osmm-primary-horizontal.svg` | Primary lockup. README headers, site nav, decks, the default everywhere. |
| `osmm-primary-horizontal-reversed.svg` | Primary lockup for dark backgrounds (plus knocks out to white). |
| `osmm-stacked.svg` | Square / centered contexts — social avatars, profile images, cards. |
| `osmm-acronym.svg` | Compact lockup (mark + OSMM, no descriptor) for tight horizontal space. |
| `osmm-mark.svg` | Mark only. App icons and uses ≥ 32 px. |
| `osmm-favicon.svg` | Mark with higher-contrast cells so the structure survives ≤ 24 px. |
| `osmm-mono.svg` | One-ink lockup (single navy) — stamps, fax, embroidery, single-color print. |
| `osmm-mark-mono.svg` | One-ink mark only. |

All files are vector SVG with the type already converted to outlines, so they
render identically without IBM Plex Mono installed.

---

## Color

| Token | Hex | Role |
|-------|-----|------|
| `--osmm-navy` | `#0f1b35` | Plus, wordmark, dark UI surfaces |
| `--osmm-mint-deep` | `#34c6a4` | Deep cell pair (top-right, bottom-left) |
| `--osmm-mint-light` | `#d4f2ec` | Light cell pair (top-left, bottom-right) |
| `--osmm-mint-mid` | `#79d4c0` | Light cells in the favicon variant only |
| `--osmm-desc-gray` | `#5b6472` | Descriptor text on light backgrounds |
| `--osmm-desc-light` | `#9fb0c9` | Descriptor text on dark backgrounds |

The two mint values are solid colors (not transparency), so the mark reproduces
identically on any background. On dark backgrounds use the reversed file, where
the plus becomes white.

---

## Construction

The mark is built from five shapes on a fixed grid; everything scales
proportionally from the cell size.

- **Cell:** the base unit. Square, corner radius = 5% of the cell.
- **Gap:** 20.8% of the cell (cell : gap ≈ 4.8 : 1).
- **Matrix:** 2 cells + 1 gap on each side.
- **Disc (the plus):** a filled circle centered on the matrix, radius = 41.5%
  of the full matrix width, drawn behind the four cells. It only shows through
  the cross-shaped gap, which is what forms the plus.
- **Checker:** light cells top-left and bottom-right; deep cells top-right and
  bottom-left.

In source units (cell = 120): gap 25, matrix 265, disc radius 110, corner
radius 6.

---

## Typography

The wordmark is **IBM Plex Mono** — *Medium* for "OSMM", *Regular* for the
"Open Semantic Marketing Model" descriptor. The monospace voice is deliberate:
OSMM is a machine-readable schema standard, and the type says so.

IBM Plex is licensed under the **SIL Open Font License 1.1** (free, open-source,
embeddable). When self-hosting, ship the original font files unmodified; the
name "Plex" is reserved under the OFL, so only renamed forks may redistribute
modified versions. For long-form documentation, IBM Plex Sans (body) and IBM
Plex Serif (editorial) extend the same family.

---

## Clear space & minimum size

- **Clear space:** keep free space equal to one cell width on all sides of the
  lockup. Nothing — type, edges, other logos — intrudes into it.
- **Minimum size:** full lockup no smaller than 120 px wide. Mark alone no
  smaller than 32 px; below that use `osmm-favicon.svg` (down to 16 px) or the
  mono mark.

---

## Do / don't

Do recolor only via the reversed and mono files provided. Do keep the cell
checker orientation fixed. Do let the plus stay centered.

Don't rotate or skew the mark. Don't change the cell colors or swap the
diagonal. Don't add effects (shadows, gradients, glows). Don't set the wordmark
in another typeface or re-letter-space it. Don't place the full-color mark on a
busy photo — use the reversed or mono version on a solid field instead.

---

*Logo and documentation released under CC BY 4.0. IBM Plex © IBM Corp., SIL OFL 1.1.*
