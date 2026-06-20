# OSMM™ Object Graph

A graph-database view of the OSMM object model — all **18 objects**
(17 with shipped builders, 1 in the backlog), laid out **left → right by
workflow phase (1 → 7)**, matching the [TAXONOMY](TAXONOMY.md) flow, with the reference
edges between them.

> **This file is generated** by [`scripts/gen_object_graph.py`](scripts/gen_object_graph.py).
> Edit the object/edge tables in that script and regenerate — do not hand-edit below.

## How to read it

- **Left → right = workflow phase** (Phase 1 Define Strategy … Phase 7 Measure, Learn &
  Optimize). Each labeled column is one phase.
- **Node color = category** (Context, Work Product, Configuration, Measurement, Learning) —
  a secondary cue, not the grouping axis.
- **Solid node** = builder shipped (17); **dashed node** = backlog (1).
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
flowchart LR
  subgraph p1["1 · Define Strategy"]
    business_context["Business Context"]
    brand_context["Brand Context"]
    product_context["Product Context"]
    marketing_strategy["Marketing Strategy"]
    measurement_framework["Measurement Framework"]
  end
  subgraph p2["2 · Define Audience"]
    persona["Persona"]
    audience["Audience"]
  end
  subgraph p3["3 · Define Offer"]
    offer["Offer"]
    experiment_strategy["Experiment Strategy"]
  end
  subgraph p4["4 · Campaign and Journey"]
    campaign_strategy["Campaign Strategy"]
    journey["Journey"]
  end
  subgraph p5["5 · Content and Creative"]
    creative_strategy["Creative Strategy"]
    content_strategy["Content Strategy"]
  end
  subgraph p6["6 · Build and Deliver"]
    experience["Experience"]
    experience_component["Experience Component"]
  end
  subgraph p7["7 · Measure, Learn and Optimize"]
    performance_measurement["Performance Measurement"]
    customer_insight["Customer Insight"]
    optimization_recommendation["Optimization Recommendation"]
  end
  business_context <--> brand_context
  product_context --> business_context
  product_context --> brand_context
  persona <--> audience
  audience --> business_context
  marketing_strategy --> business_context
  marketing_strategy --> brand_context
  marketing_strategy --> audience
  marketing_strategy <--> measurement_framework
  measurement_framework --> business_context
  offer --> product_context
  offer --> audience
  offer --> business_context
  campaign_strategy --> marketing_strategy
  campaign_strategy --> journey
  campaign_strategy --> audience
  campaign_strategy --> offer
  campaign_strategy --> business_context
  campaign_strategy --> measurement_framework
  journey --> audience
  journey --> persona
  journey --> business_context
  creative_strategy --> brand_context
  creative_strategy --> product_context
  creative_strategy --> business_context
  content_strategy --> creative_strategy
  content_strategy --> journey
  content_strategy --> business_context
  experience --> experience_component
  experience --> campaign_strategy
  experience --> journey
  experience --> audience
  experience --> offer
  experience --> creative_strategy
  experience --> business_context
  experience_component --> brand_context
  experience_component --> product_context
  experience_component --> persona
  performance_measurement --> measurement_framework
  performance_measurement --> marketing_strategy
  performance_measurement --> business_context
  customer_insight --> performance_measurement
  customer_insight --> audience
  customer_insight --> business_context
  optimization_recommendation --> customer_insight
  optimization_recommendation --> performance_measurement
  optimization_recommendation --> business_context
  experiment_strategy -.-> offer
  experiment_strategy -.-> campaign_strategy
  experiment_strategy -.-> creative_strategy
  performance_measurement -.-> campaign_strategy
  performance_measurement -.-> experience
  customer_insight -.-> persona
  optimization_recommendation -.-> marketing_strategy
  classDef context fill:#d4f2ec,stroke:#0f1b35,color:#0f1b35;
  classDef workproduct fill:#dbe7fb,stroke:#2c5fb3,color:#0f1b35;
  classDef configuration fill:#ece1f9,stroke:#6b4ca3,color:#0f1b35;
  classDef measurement fill:#fde8c8,stroke:#b87811,color:#0f1b35;
  classDef learning fill:#d8f0d6,stroke:#2e7d32,color:#0f1b35;
  classDef backlog stroke-dasharray:6 4;
  class business_context,brand_context,product_context,persona,audience context;
  class marketing_strategy,measurement_framework,offer,experiment_strategy,campaign_strategy,journey,creative_strategy,content_strategy,experience,experience_component workproduct;
  class performance_measurement measurement;
  class customer_insight,optimization_recommendation learning;
  class experiment_strategy backlog;
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46 stroke:#222222,stroke-width:2px;
  linkStyle 47,48,49,50,51 stroke:#9aa3af,stroke-width:1px;
  linkStyle 52,53 stroke:#1aa179,stroke-width:2px;
```
