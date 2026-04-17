"""LLM Reasoning Engine - Ollama Integration

This module integrates with a locally-running Ollama instance to generate
farmer-friendly disease diagnoses and treatment recommendations using
chain-of-thought prompting.

Why Ollama?
-----------
- Runs entirely on-premise: farmer data never leaves the local server.
- No API key or internet connection required after initial model download.
- Supports quantized models (e.g. llama3:8b-q4) that run on CPU-only hardware,
  making deployment viable on low-cost edge devices in rural areas.
- Switchable: any Ollama-compatible model can be swapped via the LLM_MODEL
  environment variable without code changes.
"""

import json
import requests
from typing import Dict, List, Optional
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Prompt template – chain-of-thought reasoning for agricultural diagnosis
# ---------------------------------------------------------------------------
DIAGNOSIS_PROMPT = """You are an expert agronomist helping smallholder farmers identify and treat plant diseases.

A computer vision classifier analysed a leaf image and produced the following:
  Disease detected : {disease_name}
  Confidence       : {confidence_pct}%
  Plant type       : {plant_type}
  Observed symptoms: {symptoms_list}

Think step-by-step, then respond ONLY with a single valid JSON object in this exact schema:
{{
  "farmer_explanation": "<2-3 plain sentences a farmer with no technical background can understand>",
  "treatment_steps": ["<step 1>", "<step 2>", "<step 3>", "<step 4>"],
  "preventive_measures": ["<measure 1>", "<measure 2>", "<measure 3>"],
  "urgency": "high" | "medium" | "low"
}}
Do not include any text outside the JSON object."""


class DiagnosisEngine:
    """LLM-based diagnosis engine that calls a local Ollama server.

    The engine builds a structured prompt containing the vision model output,
    sends it to Ollama via its HTTP /api/generate endpoint, and parses the
    JSON response back into structured recommendation fields.
    """

    def __init__(
        self,
        ollama_url: str = "http://localhost:11434",
        model: str = "llama3",
        request_timeout_seconds: int = 20,
    ):
        base = ollama_url.rstrip("/")
        # Accept either base URL (...:11434) or API URL (...:11434/api)
        self.ollama_url = base[:-4] if base.endswith("/api") else base
        self.model = model
        self.request_timeout_seconds = request_timeout_seconds
        logger.info(f"DiagnosisEngine initialised | Ollama URL: {ollama_url} | model: {model}")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate_diagnosis(
        self,
        disease_name: str,
        confidence_score: float,
        symptoms: List[str],
        plant_type: str,
        language: str = "en",
        context: Optional[Dict] = None,
    ) -> Dict:
        """Call Ollama and return structured diagnosis data.

        Falls back to a safe static response if Ollama is unreachable so
        that the API never returns a 500 error to the farmer.
        """
        prompt = DIAGNOSIS_PROMPT.format(
            disease_name=disease_name,
            confidence_pct=round(confidence_score * 100, 1),
            plant_type=plant_type or "unknown crop",
            symptoms_list=", ".join(symptoms) if symptoms else "none reported",
        )
        try:
            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json={"model": self.model, "prompt": prompt, "stream": False, "format": "json"},
                timeout=self.request_timeout_seconds,
            )
            response.raise_for_status()
            raw = response.json().get("response", "{}")
            parsed = json.loads(raw)
            logger.info(f"Ollama diagnosis generated for: {disease_name}")
            return {
                "farmer_friendly_explanation": parsed.get("farmer_explanation", ""),
                "treatment_recommendations": parsed.get("treatment_steps", []),
                "preventive_measures": parsed.get("preventive_measures", []),
                "severity_level": parsed.get("urgency", "medium"),
                "llm_generated": True,
            }
        except requests.exceptions.ConnectionError:
            logger.warning("Ollama not reachable – using static fallback response.")
            return self._fallback(disease_name)
        except Exception as e:
            logger.error(f"LLM engine error: {e}")
            return self._fallback(disease_name)

    def is_available(self) -> bool:
        """Return True if the Ollama service is reachable."""
        try:
            r = requests.get(f"{self.ollama_url}/api/tags", timeout=3)
            return r.status_code == 200
        except Exception:
            return False

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fallback(self, disease_name: str) -> Dict:
        return {
            "farmer_friendly_explanation": (
                f"Disease detected: {disease_name}. "
                "Please consult your local agricultural extension officer for treatment advice."
            ),
            "treatment_recommendations": ["Contact your local agricultural extension office for guidance."],
            "preventive_measures": ["Monitor crops regularly and isolate infected plants."],
            "severity_level": "medium",
            "llm_generated": False,
        }
