# OSMM™ Object Graph

A graph-database view of the OSMM object model — all **26 objects**
(12 with shipped builders, 14 in the backlog) across the 5 categories,
and the reference edges between them.

> **This file is generated** by [`scripts/gen_object_graph.py`](scripts/gen_object_graph.py).
> Edit the object/edge tables in that script and regenerate — do not hand-edit below.

## How to read it

- **Node fill** = category: Context, Work Product, Configuration, Measurement, Learning.
- **Solid node** = builder shipped (12); **dashed node** = backlog (14).
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
flowchart LR
  subgraph context["Context"]
    business_context["Business Context"]
    brand_context["Brand Context"]
    product_context["Product Context"]
    persona["Persona"]
    audience["Audience"]
    keyword["Keyword"]
  end
  subgraph workproduct["Work Product"]
    marketing_strategy["Marketing Strategy"]
    measurement_framework["Measurement Framework"]
    keyword_strategy["Keyword Strategy"]
    offer["Offer"]
    experiment_strategy["Experiment Strategy"]
    campaign_strategy["Campaign Strategy"]
    journey["Journey"]
    messaging_framework["Messaging Framework"]
    creative_strategy["Creative Strategy"]
    content_strategy["Content Strategy"]
    experience_design["Experience Design"]
    experience_specification["Experience Specification"]
    experience_component["Experience Component"]
    experience_delivery["Experience Delivery"]
    experience_validation["Experience Validation"]
    campaign_deployment["Campaign Deployment"]
  end
  subgraph configuration["Configuration"]
    personalization_configuration["Personalization Configuration"]
  end
  subgraph measurement["Measurement"]
    performance_measurement["Performance Measurement"]
  end
  subgraph learning["Learning"]
    customer_insight["Customer Insight"]
    optimization_recommendation["Optimization Recommendation"]
  end
  business_context <--> brand_context
  product_context --> business_context
  product_context --> brand_context
  persona <--> audience
  audience --> business_context
  keyword --> persona
  keyword --> business_context
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
  journey --> campaign_strategy
  journey --> audience
  journey --> persona
  journey --> business_context
  messaging_framework --> persona
  messaging_framework --> product_context
  messaging_framework --> brand_context
  keyword_strategy -.-> keyword
  keyword_strategy -.-> audience
  experiment_strategy -.-> offer
  experiment_strategy -.-> campaign_strategy
  experiment_strategy -.-> creative_strategy
  creative_strategy -.-> messaging_framework
  creative_strategy -.-> brand_context
  content_strategy -.-> creative_strategy
  content_strategy -.-> keyword
  experience_design -.-> creative_strategy
  experience_specification -.-> experience_design
  experience_specification -.-> campaign_strategy
  experience_component -.-> experience_specification
  personalization_configuration -.-> campaign_strategy
  personalization_configuration -.-> audience
  experience_delivery -.-> experience_component
  experience_delivery -.-> journey
  experience_validation -.-> experience_delivery
  campaign_deployment -.-> experience_delivery
  performance_measurement -.-> campaign_strategy
  performance_measurement -.-> experience_delivery
  performance_measurement -.-> measurement_framework
  customer_insight -.-> performance_measurement
  optimization_recommendation -.-> performance_measurement
  customer_insight -.-> persona
  optimization_recommendation -.-> marketing_strategy
  classDef context fill:#d4f2ec,stroke:#0f1b35,color:#0f1b35;
  classDef workproduct fill:#dbe7fb,stroke:#2c5fb3,color:#0f1b35;
  classDef configuration fill:#ece1f9,stroke:#6b4ca3,color:#0f1b35;
  classDef measurement fill:#fde8c8,stroke:#b87811,color:#0f1b35;
  classDef learning fill:#d8f0d6,stroke:#2e7d32,color:#0f1b35;
  classDef backlog stroke-dasharray:6 4;
  class business_context,brand_context,product_context,persona,audience,keyword context;
  class marketing_strategy,measurement_framework,keyword_strategy,offer,experiment_strategy,campaign_strategy,journey,messaging_framework,creative_strategy,content_strategy,experience_design,experience_specification,experience_component,experience_delivery,experience_validation,campaign_deployment workproduct;
  class personalization_configuration configuration;
  class performance_measurement measurement;
  class customer_insight,optimization_recommendation learning;
  class keyword_strategy,experiment_strategy,creative_strategy,content_strategy,experience_design,experience_specification,experience_component,experience_delivery,experience_validation,campaign_deployment,personalization_configuration,performance_measurement,customer_insight,optimization_recommendation backlog;
  linkStyle 0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27 stroke:#222222,stroke-width:2px;
  linkStyle 28,29,30,31,32,33,34,35,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50,51 stroke:#9aa3af,stroke-width:1px;
  linkStyle 52,53 stroke:#1aa179,stroke-width:2px;
```
