# English ↔ Spanish Quality Evaluation Rubric (`lxd_rubric_es.md`)

This document defines the quantitative scoring methodology for evaluating Large Language Model (LLM) translation and generation outputs in **English ↔ Spanish (en-es)** localization workflows. It operationalizes **Language eXperience Delivery (LXD)** by shifting quality assessment from traditional error-density counts (MQM) to multi-dimensional semantic and pragmatic metrics.

---

## 📐 Scoring Framework Overview

The framework evaluates outputs across three core quantitative vectors:

\\[\text{Composite Quality Score (CQS)} = 0.45 \times \text{IPS} + 0.45 \times \text{PRI} + 0.10 \times \text{FSIB}\\]

| Metric | Full Name | Weight | Primary Objective |
| :--- | :--- | :--- | :--- |
| **IPS** | Intent Preservation Score | 45% | Measures semantic fidelity and functional purpose preservation. |
| **PRI** | Pragmatic Resonance Index | 45% | Evaluates regional register, tone, and contextual appropriateness (ES-ES vs. ES-LA). |
| **FSIB** | Fluency & Structural Integrity Balancer | 10% | Penalizes over-fluency bias, structural distortion, and hallucinated expansion. |

---

## 1. Intent Preservation Score (IPS)

**Weight:** 45% | **Scale:** 0 – 100

Evaluates whether the core functional message, domain terminology, and semantic proposition of the source text are accurately rendered in the target output without mechanical word-for-word mapping errors.

### Scoring Criteria

| Score Range | Classification | Technical Description |
| :--- | :--- | :--- |
| **90 – 100** | **Optimal** | Complete semantic fidelity. Core proposition, technical parameters, and functional intent are fully preserved. Terminology alignment is exact. |
| **75 – 89** | **Acceptable** | Minor semantic divergence that does not alter key functional meaning. Slight non-critical terminology variance present. |
| **50 – 74** | **Sub-optimal** | Moderate semantic shift. Key product attributes or contextual nuances are misrendered, requiring human post-editing. |
| **0 – 49** | **Fail** | Critical semantic failure, factual distortion, or ungrounded translation that invalidates the functional purpose. |

---

## 2. Pragmatic Resonance Index (PRI)

**Weight:** 45% | **Scale:** 0 – 100

Evaluates the target text's naturalness, syntactic flow, and register alignment for specific Spanish regional variants (**European Castellano [es-ES]** vs. **Latin American Spanish [es-LA]**).

### Scoring Criteria

| Score Range | Classification | Technical Description |
| :--- | :--- | :--- |
| **90 – 100** | **Optimal** | Native pragmatic resonance. Exact regional register matching (*tú* / *usted* / *vos*), correct localized idiomatic structures, and domain-appropriate style. |
| **75 – 89** | **Acceptable** | Grammatically correct with minor regional register mismatches (e.g., using a neutral term where a region-specific variant is expected). |
| **50 – 74** | **Sub-optimal** | Pragmatically stiff or literal. Displays clear machine-translation artifacts or cross-regional confusion (e.g., mixing *es-ES* and *es-LA* conventions). |
| **0 – 49** | **Fail** | Inappropriate register, severe grammatical/syntactic distortion, or culturally jarring phrasing for the target demographic. |

### Regional Disambiguation Parameters

```yaml
regional_targets:
  es-ES (Castellano):
    formality_default: "Informal/Professional (Tú / Vosotros)"
    lexical_markers: ["ordenador", "fichero", "coche", "móvil"]
    syntactic_preference: "Present perfect for recent past (hemos recibido)"
  es-LA (Latin America):
    formality_default: "Formal/Neutral (Usted / Ustedes)"
    lexical_markers: ["computadora", "archivo", "carro/auto", "celular"]
    syntactic_preference: "Preterite for recent past (recibimos)"
```



## 3. Fluency & Structural Integrity Balancer (FSIB)

## Fluency & Structural Integrity Balancer (FSIB)

**Weight:** 10% | **Scale:** 0–100

Detects and penalizes over-fluency bias—the tendency of generative models to convert concise, structured source input, such as bullet points or attribute tables, into overly verbose, literary prose.

### Penalty & Scoring Matrix

| Observed Phenomenon | Structural Impact | Score Adjustment |
|---|---|---:|
| **Concise & Structurally Aligned** | Target output preserves source length, formatting, and structural density. | **100** (Full Score) |
| **Minor Over-Fluency** | Output adds non-functional conversational filler or unnecessary transitional phrases. | **75** (-25 Penalty) |
| **Significant Verbosity / Expansion** | Output expands bullet points or tabular data into wordy prose, altering length by >30%. | **50** (-50 Penalty) |
| **Structural Breakdown / Hallucination** | Output truncates essential structure or hallucinates ungrounded textual additions. | **0** (Maximum Penalty) |


## 📊 Quality Thresholds & Escalation Matrix

Outputs are automatically categorized based on their final **Composite Quality Score (CQS)**:

\[
\text{CQS} = (0.45 \times \text{IPS}) + (0.45 \times \text{PRI}) + (0.10 \times \text{FSIB})
\]

| CQS Range | Action / Status | Workflow Routing |
|---|---|---|
| **88.0 – 100.0** | **Automated Deployment** | Direct publish; bypasses human post-editing. |
| **70.0 – 87.9** | **Human Post-Editing (PEMT)** | Routed to linguist pool for targeted refinement. |
| **< 70.0** | **Human Redraft / Escalation** | Rejected; routed to senior domain expert for re-translation. |

## ⏭️ Next Step in Framework Implementation

Proceed to Module 1’s automated evaluation script:

👉 `1_eval_metrics/`
