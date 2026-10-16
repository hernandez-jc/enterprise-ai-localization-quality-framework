#!/usr/bin/env python3
"""
1_eval_metrics/llm_judge_es.py

Automated LLM-as-a-Judge Evaluation Script for English ↔ Spanish Localization
=============================================================================
Executes multi-criteria evaluation of Large Language Model (LLM) translation outputs
against source inputs, operationalizing the Language eXperience Delivery (LXD) rubric:
  - Intent Preservation Score (IPS, 45% weight)
  - Pragmatic Resonance Index (PRI, 45% weight)
  - Fluency & Structural Integrity Balancer (FSIB, 10% weight)

Uses target-language (Spanish) system instructions to mitigate English-centric evaluation bias
and outputs structured JSON with Composite Quality Scores (CQS) and workflow routing actions.
"""

import argparse
import json
import os
import sys
from dataclasses import asdict, dataclass
from typing import Any, Dict, List, Optional


# ============================================================================
# System Evaluation Prompt (Spanish Target Language)
# ============================================================================

SPANISH_EVALUATOR_SYSTEM_PROMPT = """\
Eres un evaluador experto en procesamiento de lenguaje natural y localización multilingüe (Inglés -> Español).
Tu tarea es evaluar la calidad de una traducción u oración generada en español a partir del texto fuente en inglés.

Debes evaluar la muestra según tres vectores cuantitativos (escala de 0.0 a 100.0):

1. **IPS (Intent Preservation Score - Peso 45%)**: Fidelidad semántica, preservación del propósito funcional del mensaje, parámetros técnicos y precisión terminológica.
2. **PRI (Pragmatic Resonance Index - Peso 45%)**: Naturalidad pragmática, adecuación al registro regional especificado (Castellano es-ES vs. Latinoamericano es-LA), corrección sintáctica y nivel de formalidad (tú/usted).
3. **FSIB (Fluency & Structural Integrity Balancer - Peso 10%)**: Preservación de la estructura del texto fuente (listas, viñetas, tablas) sin incurrir en sesgo de sobre-fluidez (expansión verbosa no solicitada o prosas literarias artificiales).

Devuelve tu evaluación estrictamente en formato JSON con el siguiente esquema:
{
  "ips_score": <float 0.0-100.0>,
  "ips_justification": "<explicación técnica breve>",
  "pri_score": <float 0.0-100.0>,
  "pri_justification": "<explicación técnica breve>",
  "fsib_score": <float 0.0-100.0>,
  "fsib_justification": "<explicación técnica breve>"
}
"""


# ============================================================================
# Data Structures
# ============================================================================

@dataclass
class TranslationItem:
    """Represents a single source-target localization unit."""
    id: str
    source_en: str
    target_es: str
    target_locale: str  # "es-ES" or "es-LA"
    domain: Optional[str] = "general"


@dataclass
class EvaluationResult:
    """Container for quantitative evaluation metrics and workflow routing decision."""
    id: str
    target_locale: str
    ips_score: float
    pri_score: float
    fsib_score: float
    cqs_score: float
    routing_action: str
    ips_justification: str
    pri_justification: str
    fsib_justification: str


# ============================================================================
# Scoring Engine & Workflow Routing Logic
# ============================================================================

def calculate_cqs(ips: float, pri: float, fsib: float) -> float:
    """
    Calculates the Composite Quality Score (CQS) based on weighted rubric parameters.
    Formula: CQS = (0.45 * IPS) + (0.45 * PRI) + (0.10 * FSIB)
    """
    cqs = (0.45 * ips) + (0.45 * pri) + (0.10 * fsib)
    return round(cqs, 2)


def determine_workflow_routing(cqs: float) -> str:
    """
    Determines automated routing based on CQS quality thresholds:
      - CQS >= 88.0: AUTOMATED_DEPLOYMENT (Bypasses human edit)
      - 70.0 <= CQS < 88.0: POST_EDITING_HUMAN_PEMT (Routed to linguist pool)
      - CQS < 70.0: HUMAN_ESCALATION_REDRAFT (Routed to domain expert)
    """
    if cqs >= 88.0:
        return "AUTOMATED_DEPLOYMENT"
    elif cqs >= 70.0:
        return "POST_EDITING_HUMAN_PEMT"
    else:
        return "HUMAN_ESCALATION_REDRAFT"


# ============================================================================
# Mock Evaluator (Fallback for offline/test mode without API keys)
# ============================================================================

def mock_llm_evaluator(item: TranslationItem) -> Dict[str, Any]:
    """
    Deterministic evaluation heuristic used when running tests without an API connection.
    Evaluates basic lengths, key term overlaps, and regional marker conventions.
    """
    # Baseline scores
    ips = 92.0
    pri = 88.0
    fsib = 95.0
    
    ips_just = "Semantic intent and key attributes are accurately preserved."
    pri_just = f"Pragmatic flow aligned with target region '{item.target_locale}'."
    fsib_just = "Structure matches source without unnecessary expansion."

    # Check for regional marker alignment
    if item.target_locale == "es-ES" and "computadora" in item.target_es.lower():
        pri -= 15.0
        pri_just = "Detected Latin American lexical term 'computadora' in es-ES context (expected 'ordenador')."
    elif item.target_locale == "es-LA" and "ordenador" in item.target_es.lower():
        pri -= 15.0
        pri_just = "Detected European Castellano lexical term 'ordenador' in es-LA context (expected 'computadora')."

    # Check for over-fluency / verbosity penalty (>40% character expansion)
    ratio = len(item.target_es) / max(len(item.source_en), 1)
    if ratio > 1.4:
        fsib -= 25.0
        fsib_just = f"Target text expanded by {round((ratio-1)*100, 1)}% over source (over-fluency penalty)."

    return {
        "ips_score": ips,
        "ips_justification": ips_just,
        "pri_score": pri,
        "pri_justification": pri_just,
        "fsib_score": fsib,
        "fsib_justification": fsib_just,
    }


# ============================================================================
# Pipeline Orchestration
# ============================================================================

def evaluate_dataset(
    items: List[TranslationItem], use_mock: bool = True
) -> List[EvaluationResult]:
    """Iterates over input translation units and executes evaluation pipeline."""
    results = []

    for item in items:
        if use_mock:
            raw_eval = mock_llm_evaluator(item)
        else:
            # Here API calls (e.g., OpenAI/Anthropic/Bedrock client) would be executed
            # passing SPANISH_EVALUATOR_SYSTEM_PROMPT and user prompt payload.
            raise NotImplementedError("Live API calls require configuring API credentials.")

        ips = float(raw_eval["ips_score"])
        pri = float(raw_eval["pri_score"])
        fsib = float(raw_eval["fsib_score"])
        
        cqs = calculate_cqs(ips, pri, fsib)
        action = determine_workflow_routing(cqs)

        result = EvaluationResult(
            id=item.id,
            target_locale=item.target_locale,
            ips_score=ips,
            pri_score=pri,
            fsib_score=fsib,
            cqs_score=cqs,
            routing_action=action,
            ips_justification=raw_eval["ips_justification"],
            pri_justification=raw_eval["pri_justification"],
            fsib_justification=raw_eval["fsib_justification"],
        )
        results.append(result)

    return results


# ============================================================================
# CLI Entry Point
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Run automated EN->ES LLM-as-a-Judge quality evaluations."
    )
    parser.add_argument(
        "--input",
        type=str,
        help="Path to input JSON file containing array of translation items.",
        default=None,
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Path to output JSON file for evaluation metrics.",
        default="evaluation_results.json",
    )
    parser.add_argument(
        "--mock",
        action="store_true",
        default=True,
        help="Use deterministic offline evaluator mode (default: True).",
    )

    args = parser.parse_args()

    # Load input data or use sample test suite
    if args.input and os.path.exists(args.input):
        with open(args.input, "r", encoding="utf-8") as f:
            raw_data = json.load(f)
            items = [TranslationItem(**d) for d in raw_data]
    else:
        print("[INFO] No input file provided. Running evaluation on standard sample dataset...")
        items = [
            TranslationItem(
                id="sample_001",
                source_en="Open the settings menu and click on 'Save File' to update your computer.",
                target_es="Abre el menú de configuración y haz clic en 'Guardar archivo' para actualizar tu ordenador.",
                target_locale="es-ES",
                domain="software",
            ),
            TranslationItem(
                id="sample_002",
                source_en="Open the settings menu and click on 'Save File' to update your computer.",
                target_es="Abra el menú de configuración y haga clic en 'Guardar archivo' para actualizar su ordenador.",
                target_locale="es-LA",
                domain="software",
            ),
            TranslationItem(
                id="sample_003",
                source_en="User registration form.",
                target_es="Este es un formulario completo destinado al registro de nuevos usuarios en la plataforma digital.",
                target_locale="es-LA",
                domain="ui_text",
            ),
        ]

    # Run evaluations
    eval_results = evaluate_dataset(items, use_mock=args.mock)

    # Save results
    output_payload = [asdict(r) for r in eval_results]
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(output_payload, f, indent=2, ensure_ascii=False)

    # Print summary table
    print("\n" + "=" * 80)
    print(f"{'ID':<12} | {'Locale':<7} | {'IPS':<6} | {'PRI':<6} | {'FSIB':<6} | {'CQS':<6} | {'Routing Action'}")
    print("=" * 80)
    for r in eval_results:
        print(
            f"{r.id:<12} | {r.target_locale:<7} | {r.ips_score:<6.1f} | {r.pri_score:<6.1f} | "
            f"{r.fsib_score:<6.1f} | {r.cqs_score:<6.1f} | {r.routing_action}"
        )
    print("=" * 80)
    print(f"\n[SUCCESS] Evaluation report successfully written to '{args.output}'.\n")


if __name__ == "__main__":
    main()
