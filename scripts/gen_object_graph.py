#!/usr/bin/env python3
"""Generate the OSMM object-graph view: `osmm-object-graph.svg` + `GRAPH.md`.

Single source of truth for the object graph. Edit the OBJ / REALIZED / ENVISIONED
/ LOOP tables below as the model evolves, then regenerate:

    python scripts/gen_object_graph.py     # needs graphviz `dot` on PATH for the SVG

Objects are laid out left -> right by **workflow phase** (1 -> 7), matching the
TAXONOMY flow. Category is shown as node color only (a secondary cue), not the
grouping axis. `REALIZED` edges mirror the established reference fields in
RELATIONSHIPS.md (solid); `ENVISIONED` edges are illustrative (dashed).
"""
from __future__ import annotations
import subprocess, textwrap, shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# object_type -> (label, category, built, phase)
OBJ = {
 'business_context':('Business Context','Context',True,1),
 'brand_context':('Brand Context','Context',True,1),
 'product_context':('Product Context','Context',True,1),
 'marketing_strategy':('Marketing Strategy','Work Product',True,1),
 'measurement_framework':('Measurement Framework','Work Product',True,1),
 'persona':('Persona','Context',True,2),
 'audience':('Audience','Context',True,2),
 'offer':('Offer','Work Product',True,3),
 'experiment_strategy':('Experiment Strategy','Work Product',False,3),
 'campaign_strategy':('Campaign Strategy','Work Product',True,4),
 'journey':('Journey','Work Product',True,4),
 'creative_strategy':('Creative Strategy','Work Product',True,5),
 'content_strategy':('Content Strategy','Work Product',True,5),
 'experience':('Experience','Work Product',True,6),
 'experience_component':('Experience Component','Work Product',True,6),
 'performance_measurement':('Performance Measurement','Measurement',False,7),
 'customer_insight':('Customer Insight','Learning',False,7),
 'optimization_recommendation':('Optimization Recommendation','Learning',False,7),
}

PHASE_LABEL = {
 1: '1 · Define Strategy',
 2: '2 · Define Audience',
 3: '3 · Define Offer',
 4: '4 · Campaign & Journey',
 5: '5 · Content & Creative',
 6: '6 · Build & Deliver',
 7: '7 · Measure, Learn & Optimize',
}

CAT_FILL = {'Context':'#d4f2ec','Work Product':'#dbe7fb','Configuration':'#ece1f9',
            'Measurement':'#fde8c8','Learning':'#d8f0d6'}
CAT_BORDER = {'Context':'#0f1b35','Work Product':'#2c5fb3','Configuration':'#6b4ca3',
              'Measurement':'#b87811','Learning':'#2e7d32'}
CAT_ORDER = ['Context','Work Product','Configuration','Measurement','Learning']

# Realized reference edges — mirror RELATIONSHIPS.md established table. (a, b, bidirectional)
REALIZED = [
 ('business_context','brand_context',True),
 ('product_context','business_context',False),
 ('product_context','brand_context',False),
 ('persona','audience',True),
 ('audience','business_context',False),
 ('marketing_strategy','business_context',False),
 ('marketing_strategy','brand_context',False),
 ('marketing_strategy','audience',False),
 ('marketing_strategy','measurement_framework',True),
 ('measurement_framework','business_context',False),
 # Offer (B11)
 ('offer','product_context',False),
 ('offer','audience',False),
 ('offer','business_context',False),
 # Campaign Strategy (B13)
 ('campaign_strategy','marketing_strategy',False),
 ('campaign_strategy','journey',False),
 ('campaign_strategy','audience',False),
 ('campaign_strategy','offer',False),
 ('campaign_strategy','business_context',False),
 ('campaign_strategy','measurement_framework',False),
 # Journey (B14)
 ('journey','campaign_strategy',False),
 ('journey','audience',False),
 ('journey','persona',False),
 ('journey','business_context',False),
 # Creative Strategy (B17) — absorbs former Experience Design
 ('creative_strategy','brand_context',False),
 ('creative_strategy','product_context',False),
 ('creative_strategy','business_context',False),
 # Content Strategy (B18)
 ('content_strategy','creative_strategy',False),
 ('content_strategy','journey',False),
 ('content_strategy','business_context',False),
 # Experience (B-new) — Phase 6 deliverable, absorbs Spec / Delivery / Personalization / Validation
 ('experience','experience_component',False),
 ('experience','campaign_strategy',False),
 ('experience','journey',False),
 ('experience','audience',False),
 ('experience','offer',False),
 ('experience','creative_strategy',False),
 ('experience','business_context',False),
 # Experience Component — reusable building blocks
 ('experience_component','brand_context',False),
 ('experience_component','product_context',False),
 ('experience_component','persona',False),
]
# Envisioned edges — illustrative, not yet defined in a builder.
ENVISIONED = [
 ('experiment_strategy','offer'),('experiment_strategy','campaign_strategy'),('experiment_strategy','creative_strategy'),
 ('performance_measurement','campaign_strategy'),('performance_measurement','experience'),('performance_measurement','measurement_framework'),
 ('customer_insight','performance_measurement'),
 ('optimization_recommendation','performance_measurement'),
]
# The compounding loop (Learning -> durable Context / Strategy).
LOOP = [('customer_insight','persona'),('optimization_recommendation','marketing_strategy')]

BUILT = sum(1 for v in OBJ.values() if v[2])
BACKLOG = len(OBJ) - BUILT
PHASES = sorted(PHASE_LABEL)


def phase_nodes(p):
    return [o for o, v in OBJ.items() if v[3] == p]


def gv_node(o):
    label, cat, built, _ = OBJ[o]
    wl = '\\n'.join(textwrap.wrap(label, 14))
    style = 'rounded,filled' + ('' if built else ',dashed')
    pen = '2.4' if built else '1.1'
    return (f'    {o} [label="{wl}", fillcolor="{CAT_FILL[cat]}", '
            f'color="{CAT_BORDER[cat]}", penwidth={pen}, style="{style}"];')


def build_dot():
    L = ['digraph OSMM {',
         '  graph [rankdir=LR, fontname="Helvetica", bgcolor="white", nodesep=0.28, ranksep=2.2, '
         'pad=0.5, splines=true, overlap=false, newrank=true];',
         '  node [shape=box, fontname="Helvetica", fontsize=12.5, margin="0.18,0.10", height=0.42];',
         '  edge [arrowsize=0.75];',
         '  labelloc="t"; fontsize=24; fontname="Helvetica-Bold";',
         '  label="OSMM™ Object Graph — 18 objects, ordered left→right by workflow phase (1→7)\\n'
         f'solid node = builder shipped ({BUILT})   ·   dashed node = backlog ({BACKLOG})   ·   '
         'node color = category   ·   solid edge = realized reference   ·   '
         'dashed edge = envisioned   ·   mint edge = learning loop";']
    # one labeled cluster (column) per phase, in order
    for p in PHASES:
        L.append(f'  subgraph cluster_p{p} {{')
        L.append(f'    label="{PHASE_LABEL[p]}"; labelloc="t"; style="rounded,filled"; '
                 f'fillcolor="#f4f6f9"; color="#aab3c0"; fontname="Helvetica-Bold"; '
                 f'fontsize=15; margin=14; penwidth=1.5;')
        for o in phase_nodes(p):
            L.append(gv_node(o))
        # keep this phase's objects in one vertical column
        L.append(f'    {{ rank=same; {"; ".join(phase_nodes(p))}; }}')
        L.append('  }')
    # force the columns left -> right by phase (invisible anchor chain)
    anchors = [phase_nodes(p)[0] for p in PHASES]
    L.append('  ' + ' -> '.join(anchors) + ' [style=invis, weight=10];')
    # reference edges are decoration only (constraint=false) so they don't distort the columns
    for a, b, both in REALIZED:
        L.append(f'  {a} -> {b} [color="#222222", penwidth=1.6, constraint=false{", dir=both" if both else ""}];')
    for a, b in ENVISIONED:
        L.append(f'  {a} -> {b} [color="#9aa3af", penwidth=1.0, style=dashed, constraint=false];')
    for a, b in LOOP:
        L.append(f'  {a} -> {b} [color="#1aa179", penwidth=1.7, style=dashed, constraint=false];')
    L.append('}')
    return '\n'.join(L)


def build_mermaid():
    L = ['flowchart LR']
    for p in PHASES:
        safe = PHASE_LABEL[p].replace('&', 'and')
        L.append(f'  subgraph p{p}["{safe}"]')
        for o in phase_nodes(p):
            L.append(f'    {o}["{OBJ[o][0]}"]')
        L.append('  end')
    idx = 0
    realized_idx, env_idx, loop_idx = [], [], []
    for a, b, both in REALIZED:
        L.append(f'  {a} {"<-->" if both else "-->"} {b}')
        realized_idx.append(idx); idx += 1
    for a, b in ENVISIONED:
        L.append(f'  {a} -.-> {b}')
        env_idx.append(idx); idx += 1
    for a, b in LOOP:
        L.append(f'  {a} -.-> {b}')
        loop_idx.append(idx); idx += 1
    # node color by category (secondary cue)
    for cat in CAT_ORDER:
        slug = cat.replace(' ', '').lower()
        L.append(f'  classDef {slug} fill:{CAT_FILL[cat]},stroke:{CAT_BORDER[cat]},color:#0f1b35;')
    L.append('  classDef backlog stroke-dasharray:6 4;')
    for cat in CAT_ORDER:
        ids = [o for o, v in OBJ.items() if v[1] == cat]
        if ids:
            L.append(f'  class {",".join(ids)} {cat.replace(" ", "").lower()};')
    backlog_ids = [o for o, v in OBJ.items() if not v[2]]
    L.append(f'  class {",".join(backlog_ids)} backlog;')
    L.append(f'  linkStyle {",".join(map(str, realized_idx))} stroke:#222222,stroke-width:2px;')
    L.append(f'  linkStyle {",".join(map(str, env_idx))} stroke:#9aa3af,stroke-width:1px;')
    L.append(f'  linkStyle {",".join(map(str, loop_idx))} stroke:#1aa179,stroke-width:2px;')
    return '\n'.join(L)


def build_md(mermaid):
    return f"""# OSMM™ Object Graph

A graph-database view of the OSMM object model — all **{len(OBJ)} objects**
({BUILT} with shipped builders, {BACKLOG} in the backlog), laid out **left → right by
workflow phase (1 → 7)**, matching the [TAXONOMY](TAXONOMY.md) flow, with the reference
edges between them.

> **This file is generated** by [`scripts/gen_object_graph.py`](scripts/gen_object_graph.py).
> Edit the object/edge tables in that script and regenerate — do not hand-edit below.

## How to read it

- **Left → right = workflow phase** (Phase 1 Define Strategy … Phase 7 Measure, Learn &
  Optimize). Each labeled column is one phase.
- **Node color = category** (Context, Work Product, Configuration, Measurement, Learning) —
  a secondary cue, not the grouping axis.
- **Solid node** = builder shipped ({BUILT}); **dashed node** = backlog ({BACKLOG}).
- **Solid edge** = a *realized* reference (a reference field defined in a shipped builder;
  mirrors the established table in [`RELATIONSHIPS.md`](RELATIONSHIPS.md)).
- **Dashed gray edge** = an *envisioned* reference — illustrative, not yet defined in a
  builder; it becomes solid when that builder ships and declares the field.
- **Mint edge** = the **learning loop** (Phase 7 Learning objects propose updates back into
  the durable Phase 1–2 Context — sub-process 7.7).

Most reference edges point **right → left** (a later-phase Work Product references the
earlier-phase Context it depends on); the mint learning-loop edges close the cycle from
Phase 7 back to Phase 1.

## Full view (SVG)

![OSMM object graph](osmm-object-graph.svg)

## Inline view (Mermaid)

```mermaid
{mermaid}
```
"""


def main():
    dot = build_dot()
    if shutil.which('dot'):
        subprocess.run(['dot', '-Tsvg', '-o', str(REPO / 'osmm-object-graph.svg')],
                       input=dot, text=True, check=True)
        print('rendered osmm-object-graph.svg')
    else:
        print('WARNING: graphviz `dot` not found — SVG not regenerated (committed copy kept).')
    (REPO / 'GRAPH.md').write_text(build_md(build_mermaid()), encoding='utf-8')
    print(f'wrote GRAPH.md  (objects={len(OBJ)} realized={len(REALIZED)} '
          f'envisioned={len(ENVISIONED)} loop={len(LOOP)})')


if __name__ == '__main__':
    main()
