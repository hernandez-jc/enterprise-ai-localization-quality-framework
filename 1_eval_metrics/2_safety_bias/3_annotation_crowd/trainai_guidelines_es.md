# Crowd Annotation & Post-Editing Guidelines for English ↔ Spanish (`trainai_guidelines_es.md`)

Standard Operating Procedures (SOP) and dataset annotation specifications for post-editors and crowd annotators performing **Post-Editing Machine Translation (PEMT)** and **Reinforcement Learning from Human Feedback (RLHF)** preference ranking in **English ↔ Spanish (en-es)** generative workflows.

---

## 🎯 Task Objectives & Scope

As an AI Data Annotator or Post-Editor, your objective is to evaluate, rank, and refine Large Language Model (LLM) target outputs to generate high-quality supervised fine-tuning (SFT) and preference alignment datasets.

Your work directly trains reward models to eliminate **semantic divergence**, **pragmatic drift**, and **unbalanced token disambiguation** in localized Spanish deployments.

---

## 📐 Task Type 1: Post-Editing Machine Translation (PEMT)

When post-editing machine-generated Spanish text against an English source unit, apply the **Minimal Edit Principle**: modify the target text only when necessary to correct objective errors.

### 1. Classification & Edit Thresholds

| Severity Tier | Definition | Action Required |
| :--- | :--- | :--- |
| **Critical Error** | Severe semantic inversion, factual hallucination, or safety failure. | **Full Redraft**: Rewrite target payload from scratch. |
| **Major Error** | Terminology mismatch, incorrect regional variant (e.g., *es-ES* term in *es-LA*), or grammatical error. | **Targeted Edit**: Fix specific token or clause. |
| **Minor Error** | Slightly stiff phrasing, sub-optimal word order, or minor punctuation flaw. | **Light Edit**: Adjust syntax only if fluency is noticeably impaired. |
| **Stylistic Preference** | Text is accurate and natural, but you prefer an alternative phrasing. | **NO EDIT**: Retain model output to avoid overfitting. |

### 2. Mandatory Quality Standards

1. **Semantic Fidelity (IPS)**: Do not omit or add information. Ensure numbers, technical parameters, product attributes, and proper nouns match the English source unit exactly.
2. **Regional Concordance**: Adhere strictly to the assigned target locale:
   - **`es-ES` (European Castellano)**: Use Peninsular vocabulary (*ordenador*, *coche*, *móvil*) and informal 2nd-person plural (*tú* / *vosotros*) when applicable.
   - **`es-LA` (Latin America)**: Use Latin American vocabulary (*computadora*, *carro*, *celular*) and formal/neutral 2nd-person plural (*ustedes*).
3. **Structural Alignment**: Preserve structural formatting (bullet points, markdown tags, variables, HTML elements) without converting structured lists into prose.

---

## ⚖️ Task Type 2: RLHF Preference Ranking (Pairwise Comparison)

When presented with an English Source Prompt and two candidate Spanish outputs (**Response A** vs. **Response B**), rank the candidate pair using the following rubric.

### Ranking Decision Tree

```text
Step 1: Check for Hallucinations / Semantic Inversions
  ├── Response contains hallucination or factual error? -> Instantly Reject (Lowest Rank)
  └── Both responses semantically accurate? -> Proceed to Step 2

Step 2: Check Regional Variant & Register Alignment
  ├── Response uses wrong regional terminology (e.g., es-ES term in es-LA target)? -> Downrank
  └── Both responses match assigned target locale? -> Proceed to Step 3

Step 3: Check Pragmatic Naturalness & Verbosity
  ├── Response displays over-fluency bias (unnecessary verbose prose)? -> Downrank
  └── Response is concise, natural, and structurally aligned? -> Rank Higher

#Categorical Ranking Scale
Much Better (A >>> B): Response A is fully accurate and pragmatically natural, while Response B contains a major semantic error or severe regional leakage.

Slightly Better (A > B): Both responses are accurate, but Response A uses more natural regional phrasing or adheres better to structural constraints.

Negligible / Equal (A = B): Both responses are functionally identical in quality and accuracy.


```


# 🛡️ Annotation Quality Control & Anti-Poisoning Protocols
To ensure dataset integrity and prevent annotation bias from corrupting model training:
Confirmation Bias Avoidance: Base rankings strictly on objective linguistic rules and the provided glossary—not personal stylistic preferences.
Quality Verification Audits: 10% of all completed tasks are randomly sampled for expert validation. Annotators with agreement rates below 85% against the gold standard are flagged for retraining.
Anti-Poisoning Verification: Any deliberate insertion of ungrounded text, spam patterns, or repeated copy-pasting will result in automated task revocation and dataset purging.
⏭️ Next Step in Framework Implementation
Proceed to Module 3's automated routing logic:
👉 3_annotation_crowd/human_handshake_rules.json
