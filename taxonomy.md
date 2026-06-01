# OSMM Workflow Taxonomy

**Open Semantic Marketing Model — workflow classification**  
Status: Draft v0.1 · generated from the OSMM object model

This taxonomy is the classification layer that drives the standard: it maps the seven workflow **phases** to their **L2 sub-processes**, the **key decisions** each makes, and the canonical **OSMM object** each resolves to. Objects are the machine-readable source of truth; the *human-readable artifact* column is the rendered view a person reads (a brief, a summary, a deck) — the same object-vs-rendering split that runs through the rest of OSMM.

> **How to read a row:** an L2 sub-process makes one or more *key decisions*, and the result is written to (creates or updates) the named *output object*. The *artifact* is how that object is presented to people.

## The seven phases

```mermaid
flowchart LR
  P1["1 · Define Strategy"] --> P2["2 · Define Audience"] --> P3["3 · Define Offer"] --> P4["4 · Define Campaign &amp; Journey"]
  P4 --> P5["5 · Define Content &amp; Creative"] --> P6["6 · Build &amp; Deliver Experiences"] --> P7["7 · Measure, Learn &amp; Optimize"]
  P7 -. "updates durable context (7.7)" .-> P1
```

## Phase 1. Define Strategy

**Theme** — What are we trying to achieve and why?  
**Primary goal** — Strategic direction  
**Key questions** — What business problem are we solving? What priorities matter?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 1.1 Define Business Context | Industry classification, GTM model, competitive set, regulatory assumptions | Business Context Object | Business Context Summary |
| 1.2 Define Brand Context | Brand personality, tone principles, messaging guardrails | Brand Context Object | Brand Playbook, Voice Guide |
| 1.3 Define Business & Marketing Objectives | Business objectives, marketing objectives, success criteria | Marketing Strategy Object | Strategic Brief, Objective Framework |
| 1.4 Define Market & Competitive Strategy | Competitive positioning, differentiation strategy | Marketing Strategy Object | Competitive Strategy Summary |
| 1.5 Define Customer & Growth Priorities | Priority audiences, growth bets | Marketing Strategy Object | Growth Prioritization Framework |
| 1.6 Define Positioning & Value Proposition | Value proposition, positioning strategy | Marketing Strategy Object | Positioning Framework, Messaging Foundation |
| 1.7 Define Measurement Framework | KPI framework, success metrics | Measurement Framework Object | KPI Framework, Measurement Plan |
| 1.8 Confirm Strategic Direction | Final strategic direction | Marketing Strategy Object | Strategy Presentation, Executive Brief |

## Phase 2. Define Audience

**Theme** — Who matters most, what drives them, and how do they search?  
**Primary goal** — Customer understanding  
**Key questions** — Who should we target? Why? What behaviors matter? What do they search and ask?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 2.1 Define Audience Strategy | Priority audiences, strategic segments | Targeting Strategy Object | Audience Strategy Summary |
| 2.2 Define Audience Segments | Segment definitions, inclusion criteria | Audience Object | Audience Definitions |
| 2.3 Define Audience Qualification Rules | Inclusion / exclusion logic | Audience Object | Audience Rules Summary |
| 2.4 Define Customer Needs & Behaviors | Priority behaviors, customer needs | Persona Object | Persona Profiles |
| 2.5 Define Personas | Persona definitions | Persona Object | Persona Profiles |
| 2.6 Define Lifecycle & Value Framework | Lifecycle framework, value segmentation | Audience Object | Lifecycle Framework |
| 2.7 Define Keyword & Topic Strategy | Priority keywords and topics, intent distribution, AEO targets, SEO targets, topic-to-journey mapping | Keyword Object, Keyword Strategy Object | Keyword & Topic Strategy |
| 2.8 Define Audience Prioritization | Target audience prioritization | Targeting Strategy Object | Prioritization Matrix |
| 2.9 Confirm Audience Definition | Final audience strategy | Targeting Strategy Object | Audience Summary |

## Phase 3. Define Offer

**Theme** — What motivates action?  
**Primary goal** — Offer-market fit  
**Key questions** — What value exchange matters? Why will people act?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 3.1 Define Desired Behavior Change | Behavior-change objective | Offer Strategy Object | Behavior Change Summary |
| 3.2 Define Offer Strategy | Offer strategy, incentive philosophy | Offer Strategy Object | Offer Strategy Summary |
| 3.3 Define Offer Architecture | Offer structure | Offer Object | Offer Framework |
| 3.4 Define Incentive & Economics | Incentive structure, profitability thresholds | Offer Object | Incentive Framework |
| 3.5 Define Offer Positioning | Positioning approach | Offer Object | Offer Positioning Summary |
| 3.6 Define Eligibility & Rules | Eligibility logic | Offer Object | Offer Rules Summary |
| 3.7 Define Testing Strategy | Test priorities | Offer Test Strategy Object | Experiment Design |
| 3.8 Confirm Offer Definition | Final offer approval | Offer Object | Offer Summary |

## Phase 4. Define Campaign & Journey

**Theme** — How will we activate behavior change?  
**Primary goal** — Activation plan  
**Key questions** — What sequence, channels, and triggers?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 4.1 Define Campaign Objective & Scope | Campaign objective, success criteria, scope | Campaign Strategy Object | Campaign Charter |
| 4.2 Define Journey Strategy | Journey goals, customer path | Journey Strategy Object | Journey Map |
| 4.3 Define Audience-to-Offer Mapping | Audience-offer mapping | Campaign Strategy Object | Audience Strategy Matrix |
| 4.4 Define Channel & Touchpoint Strategy | Channel prioritization | Campaign Strategy Object | Channel Plan |
| 4.5 Define Triggering & Sequencing Logic | Trigger logic, cadence | Journey Strategy Object | Journey Flow Diagram |
| 4.6 Define Personalization Strategy | Personalization rules | Campaign Strategy Object | Personalization Framework |
| 4.7 Define Measurement & Test Strategy | Test priorities, KPI logic | Campaign Measurement Object | Measurement Plan |
| 4.8 Confirm Campaign & Journey Definition | Final campaign direction | Campaign Strategy Object + Journey Strategy Object | Campaign Brief |

## Phase 5. Define Content & Creative

**Theme** — What story will we tell and how?  
**Primary goal** — Creative clarity  
**Key questions** — What message, story, and tone?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 5.1 Define Messaging Strategy | Message hierarchy, value framing | Messaging Framework Object | Messaging Framework |
| 5.2 Define Creative Strategy | Creative themes, emotional strategy | Creative Strategy Object | Creative Direction Summary |
| 5.3 Define Content Strategy | Content priorities, content sequencing | Content Strategy Object | Content Plan |
| 5.4 Define Message Hierarchy & Variations | Message prioritization | Messaging Framework Object | Messaging Architecture |
| 5.5 Define Creative System & Experience Concepts | Experience concepts | Experience Design Object | Experience Concepts |
| 5.6 Define Channel-Specific Creative Requirements | Channel creative rules | Creative Strategy Object | Channel Creative Matrix |
| 5.7 Define Content & Creative Testing Strategy | Test priorities | Creative Test Strategy Object | Creative Experiment Plan |
| 5.8 Confirm Content & Creative Direction | Final creative direction | Creative Strategy Object + Messaging Framework Object | Creative Brief |

## Phase 6. Build & Deliver Experiences

**Theme** — Bring the experience to life  
**Primary goal** — Coordinated delivery  
**Key questions** — How do we operationalize and deliver experiences effectively?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 6.1 Define Experience Specifications | Experience scope, dependencies | Experience Specification Object | Experience Blueprint |
| 6.2 Build Experience Components | Component selection | Experience Component Object | Wireframes, Designs, Copy Decks (headline / hero / CTA / offer card / trust block / content block / landing page wireframe / image treatment / copy variations) |
| 6.3 Configure Journey & Delivery Logic | Trigger rules, sequencing | Journey Configuration Object | Journey Flow Diagram |
| 6.4 Configure Personalization Rules | Personalization logic | Personalization Configuration Object | Personalization Matrix |
| 6.5 Build Channel-Specific Experiences | Channel adaptations | Experience Delivery Object | Winback Email #1, Landing Page Variant B, Paid Social Ad Set, Triggered SMS, Homepage Hero Experience |
| 6.6 Quality Assurance & Compliance Validation | Release readiness | Experience Validation Object | QA Checklist |
| 6.7 Deploy & Activate Experiences | Deployment timing | Campaign Deployment Object | Launch Plan |
| 6.8 Monitor Delivery & In-Flight Optimization | Operational optimizations | Experience Performance Object | Performance Dashboard |

## Phase 7. Measure, Learn & Optimize

**Theme** — What worked and what should change?  
**Primary goal** — Continuous improvement  
**Key questions** — What performed? Why? What should improve?

| L2 sub-process | Key decisions | Resolves to object | Human-readable artifact |
|---|---|---|---|
| 7.1 Measure Performance | KPI interpretation | Performance Measurement Object | Performance Dashboard |
| 7.2 Analyze Customer Behavior & Response | Customer insights | Customer Insight Object | Audience Insights Report |
| 7.3 Evaluate Offer Performance | Offer effectiveness | Offer Performance Object | Offer Analysis |
| 7.4 Evaluate Messaging & Creative Effectiveness | Creative learning | Creative Performance Object | Creative Performance Summary |
| 7.5 Evaluate Journey & Channel Performance | Journey optimization opportunities | Journey Performance Object | Journey Analysis |
| 7.6 Generate Optimization Recommendations | Optimization priorities | Optimization Recommendation Object | Optimization Plan |
| 7.7 Update Durable Context & Strategy | Persistent learning decisions | Business Context Object, Brand Context Object, Marketing Strategy Object, Persona Object, Targeting Strategy Object, Keyword Object | Updated Strategy Summary |
| 7.8 Confirm Learning & Next Action | Next-step decision | Marketing Strategy Object | Executive Learning Summary |

## Object resolution index

Every object mapped to the sub-processes that write it and its builder skill (per the naming convention). This is the bridge from taxonomy to the builder skills.

| OSMM object | Written by | Builder skill |
|---|---|---|
| Business Context Object | 1.1, 7.7 | `osmm-business-context-builder` |
| Brand Context Object | 1.2, 7.7 | `osmm-brand-context-builder` |
| Marketing Strategy Object | 1.3, 1.4, 1.5, 1.6, 1.8, 7.7, 7.8 | `osmm-marketing-strategy-builder` |
| Measurement Framework Object | 1.7 | `osmm-measurement-framework-builder` |
| Targeting Strategy Object | 2.1, 2.8, 2.9, 7.7 | `osmm-targeting-strategy-builder` |
| Audience Object | 2.2, 2.3, 2.6 | `osmm-audience-builder` |
| Persona Object | 2.4, 2.5, 7.7 | `osmm-persona-builder` |
| Keyword Object | 2.7, 7.7 | `osmm-keyword-builder` |
| Keyword Strategy Object | 2.7 | `osmm-keyword-strategy-builder` |
| Offer Strategy Object | 3.1, 3.2 | `osmm-offer-strategy-builder` |
| Offer Object | 3.3, 3.4, 3.5, 3.6, 3.8 | `osmm-offer-builder` |
| Offer Test Strategy Object | 3.7 | `osmm-offer-test-strategy-builder` |
| Campaign Strategy Object | 4.1, 4.3, 4.4, 4.6, 4.8 | `osmm-campaign-strategy-builder` |
| Journey Strategy Object | 4.2, 4.5, 4.8 | `osmm-journey-strategy-builder` |
| Campaign Measurement Object | 4.7 | `osmm-campaign-measurement-builder` |
| Messaging Framework Object | 5.1, 5.4, 5.8 | `osmm-messaging-framework-builder` |
| Creative Strategy Object | 5.2, 5.6, 5.8 | `osmm-creative-strategy-builder` |
| Content Strategy Object | 5.3 | `osmm-content-strategy-builder` |
| Experience Design Object | 5.5 | `osmm-experience-design-builder` |
| Creative Test Strategy Object | 5.7 | `osmm-creative-test-strategy-builder` |
| Experience Specification Object | 6.1 | `osmm-experience-specification-builder` |
| Experience Component Object | 6.2 | `osmm-experience-component-builder` |
| Journey Configuration Object | 6.3 | `osmm-journey-configuration-builder` |
| Personalization Configuration Object | 6.4 | `osmm-personalization-configuration-builder` |
| Experience Delivery Object | 6.5 | `osmm-experience-delivery-builder` |
| Experience Validation Object | 6.6 | `osmm-experience-validation-builder` |
| Campaign Deployment Object | 6.7 | `osmm-campaign-deployment-builder` |
| Experience Performance Object | 6.8 | `osmm-experience-performance-builder` |
| Performance Measurement Object | 7.1 | `osmm-performance-measurement-builder` |
| Customer Insight Object | 7.2 | `osmm-customer-insight-builder` |
| Offer Performance Object | 7.3 | `osmm-offer-performance-builder` |
| Creative Performance Object | 7.4 | `osmm-creative-performance-builder` |
| Journey Performance Object | 7.5 | `osmm-journey-performance-builder` |
| Optimization Recommendation Object | 7.6 | `osmm-optimization-recommendation-builder` |
