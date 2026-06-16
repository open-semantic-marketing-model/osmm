#!/usr/bin/env python3
"""Generate the OSMM object-graph view: `osmm-object-graph.svg` + `GRAPH.md`.

Single source of truth for the object graph. Edit the OBJ / REALIZED / ENVISIONED
/ LOOP tables below as the model evolves, then regenerate:

    python scripts/gen_object_graph.py     # needs graphviz `dot` on PATH for the SVG

`REALIZED` edges should mirror the established reference fields in RELATIONSHIPS.md
(solid). `ENVISIONED` edges are illustrative (dashed) until a builder defines them.
"""
from __future__ import annotations
import subprocess, textwrap, shutil
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# object_type -> (label, category, built)
OBJ = {
 'business_context':('Business Context','Context',True),
 'brand_context':('Brand Context','Context',True),
 'product_context':('Product Context','Context',True),
 'persona':('Persona','Context',True),
 'audience':('Audience','Context',True),
 'keyword':('Keyword','Context',True),
 'marketing_strategy':('Marketing Strategy','Work Product',True),
 'measurement_framework':('Measurement Framework','Work Product',True),
 'keyword_strategy':('Keyword Strategy','Work Product',False),
 'offer':('Offer','Work Product',True),
 'experiment_strategy':('Experiment Strategy','Work Product',False),
 'campaign_strategy':('Campaign Strategy','Work Product',True),
 'journey':('Journey','Work Product',True),
 'messaging_framework':('Messaging Framework','Work Product',True),
 'creative_strategy':('Creative Strategy','Work Product',True),
 'content_strategy':('Content Strategy','Work Product',True),
 'experience_specification':('Experience Specification','Work Product',False),
 'experience_component':('Experience Component','Work Product',False),
 'experience_delivery':('Experience Delivery','Work Product',False),
 'experience_validation':('Experience Validation','Work Product',False),
 'campaign_deployment':('Campaign Deployment','Work Product',False),
 'personalization_configuration':('Personalization Configuration','Configuration',False),
 'performance_measurement':('Performance Measurement','Measurement',False),
 'customer_insight':('Customer Insight','Learning',False),
 'optimization_recommendation':('Optimization Recommendation','Learning',False),
}

CAT_FILL = {'Context':'#d4f2ec','Work Product':'#dbe7fb','Configuration':'#ece1f9',
            'Measurement':'#fde8c8','Learning':'#d8f0d6'}
CAT_BORDER = {'Context':'#0f1b35','Work Product':'#2c5fb3','Configuration':'#6b4ca3',
              'Measurement':'#b87811','Learning':'#2e7d32'}
CAT_ORDER = ['Context','Work Product','Configuration','Measurement','Learning']
CAT_SLUG = {'Context':'context','Work Product':'workproduct','Configuration':'configuration',
            'Measurement':'measurement','Learning':'learning'}

# Realized reference edges — mirror RELATIONSHIPS.md established table. (a, b, bidirectional)
REALIZED = [
 ('business_context','brand_context',True),
 ('product_context','business_context',False),
 ('product_context','brand_context',False),
 ('persona','audience',True),
 ('audience','business_context',False),
 ('keyword','persona',False),
 ('keyword','business_context',False),
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
 # Journey Strategy (B14)
 ('journey','campaign_strategy',False),
 ('journey','audience',False),
 ('journey','persona',False),
 ('journey','business_context',False),
 # Messaging Framework (B16)
 ('messaging_framework','persona',False),
 ('messaging_framework','product_context',False),
 ('messaging_framework','brand_context',False),
 # Creative Strategy (B17) — absorbs former Experience Design
 ('creative_strategy','messaging_framework',False),
 ('creative_strategy','brand_context',False),
 ('creative_strategy','product_context',False),
 ('creative_strategy','business_context',False),
 # Content Strategy (B18)
 ('content_strategy','messaging_framework',False),
 ('content_strategy','creative_strategy',False),
 ('content_strategy','keyword',False),
 ('content_strategy','journey',False),
 ('content_strategy','business_context',False),
]
# Envisioned edges — illustrative, not yet defined in a builder.
ENVISIONED = [
 ('keyword_strategy','keyword'),('keyword_strategy','audience'),
 ('experiment_strategy','offer'),('experiment_strategy','campaign_strategy'),('experiment_strategy','creative_strategy'),
 ('experience_specification','creative_strategy'),('experience_specification','campaign_strategy'),
 ('experience_component','experience_specification'),
 ('personalization_configuration','campaign_strategy'),('personalization_configuration','audience'),
 ('experience_delivery','experience_component'),('experience_delivery','journey'),
 ('experience_validation','experience_delivery'),
 ('campaign_deployment','experience_delivery'),
 ('performance_measurement','campaign_strategy'),('performance_measurement','experience_delivery'),('performance_measurement','measurement_framework'),
 ('customer_insight','performance_measurement'),
 ('optimization_recommendation','performance_measurement'),
]
# The compounding loop (Learning -> durable Context / Strategy).
LOOP = [('customer_insight','persona'),('optimization_recommendation','marketing_strategy')]

BUILT = sum(1 for _,_,b in OBJ.values() if b)
BACKLOG = len(OBJ) - BUILT


def gv_node(o):
    label, cat, built = OBJ[o]
    wl = '\\n'.join(textwrap.wrap(label, 14))
    style = 'rounded,filled' + ('' if built else ',dashed')
    pen = '2.4' if built else '1.1'
    return (f'    {o} [label="{wl}", fillcolor="{CAT_FILL[cat]}", '
            f'color="{CAT_BORDER[cat]}", penwidth={pen}, style="{style}"];')


def build_dot():
    L = ['digraph OSMM {',
         '  graph [rankdir=LR, fontname="Helvetica", bgcolor="white", nodesep=0.5, ranksep=2.0, '
         'pad=0.5, splines=true, overlap=false, concentrate=true, newrank=true];',
         '  node [shape=box, fontname="Helvetica", fontsize=13, margin="0.20,0.12", height=0.45];',
         '  edge [arrowsize=0.8];',
         '  labelloc="t"; fontsize=26; fontname="Helvetica-Bold";',
         '  label="OSMM™ Object Graph — 25 objects across 5 categories\\n'
         f'solid node = builder shipped ({BUILT})   ·   dashed node = backlog ({BACKLOG})   ·   '
         'solid edge = realized reference   ·   dashed edge = envisioned   ·   mint edge = learning loop";']
    for i, cat in enumerate(CAT_ORDER):
        L.append(f'  subgraph cluster_{i} {{')
        L.append(f'    label="{cat}"; style="rounded,filled"; fillcolor="#f7f9fb"; '
                 f'color="{CAT_BORDER[cat]}"; fontname="Helvetica-Bold"; fontsize=18; margin=18; penwidth=2;')
        for o, (_, c, _) in OBJ.items():
            if c == cat:
                L.append(gv_node(o))
        L.append('  }')
    for a, b, both in REALIZED:
        L.append(f'  {a} -> {b} [color="#222222", penwidth=1.7{", dir=both" if both else ""}];')
    for a, b in ENVISIONED:
        L.append(f'  {a} -> {b} [color="#9aa3af", penwidth=1.0, style=dashed];')
    for a, b in LOOP:
        L.append(f'  {a} -> {b} [color="#1aa179", penwidth=1.8, style=dashed, constraint=false];')
    L.append('}')
    return '\n'.join(L)


def build_mermaid():
    L = ['flowchart LR']
    for cat in CAT_ORDER:
        L.append(f'  subgraph {CAT_SLUG[cat]}["{cat}"]')
        for o, (label, c, _) in OBJ.items():
            if c == cat:
                L.append(f'    {o}["{label}"]')
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
    # category fills
    for cat in CAT_ORDER:
        L.append(f'  classDef {CAT_SLUG[cat]} fill:{CAT_FILL[cat]},stroke:{CAT_BORDER[cat]},color:#0f1b35;')
    L.append('  classDef backlog stroke-dasharray:6 4;')
    for cat in CAT_ORDER:
        ids = [o for o, (_, c, _) in OBJ.items() if c == cat]
        L.append(f'  class {",".join(ids)} {CAT_SLUG[cat]};')
    backlog_ids = [o for o, (_, _, b) in OBJ.items() if not b]
    L.append(f'  class {",".join(backlog_ids)} backlog;')
    L.append(f'  linkStyle {",".join(map(str, realized_idx))} stroke:#222222,stroke-width:2px;')
    L.append(f'  linkStyle {",".join(map(str, env_idx))} stroke:#9aa3af,stroke-width:1px;')
    L.append(f'  linkStyle {",".join(map(str, loop_idx))} stroke:#1aa179,stroke-width:2px;')
    return '\n'.join(L)


def build_md(mermaid):
    return f"""# OSMM™ Object Graph

A graph-database view of the OSMM object model — all **{len(OBJ)} objects**
({BUILT} with shipped builders, {BACKLOG} in the backlog) across the 5 categories,
and the reference edges between them.

> **This file is generated** by [`scripts/gen_object_graph.py`](scripts/gen_object_graph.py).
> Edit the object/edge tables in that script and regenerate — do not hand-edit below.

## How to read it

- **Node fill** = category: Context, Work Product, Configuration, Measurement, Learning.
- **Solid node** = builder shipped ({BUILT}); **dashed node** = backlog ({BACKLOG}).
- **Solid edge** = a *realized* reference (a reference field defined in a shipped
  builder; mirrors the established table in [`RELATIONSHIPS.md`](RELATIONSHIPS.md)).
- **Dashed gray edge** = an *envisioned* reference — illustrative, not yet defined in a
  builder; it becomes solid when that builder ships and declares the field.
- **Mint edge** = the **learning loop** (Learning objects propose updates back into
  durable Context / Strategy — sub-process 7.7).

Context sits as the high-read foundation that everything references; Work Products flow
into Configuration → Delivery → Measurement; Learning closes the loop.

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
