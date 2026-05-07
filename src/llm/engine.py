"""LLM Reasoning Engine - OpenRouter Integration

This module integrates with OpenRouter API to generate
farmer-friendly disease diagnoses and treatment recommendations using
chain-of-thought prompting.

Why OpenRouter?
-----------
- Access to multiple models via single API
- No local model management required
- High-quality models for agricultural diagnosis
- Switchable: any OpenRouter model can be swapped via OPENROUTER_MODEL
  environment variable without code changes.
"""

import json
from langchain_openrouter import ChatOpenRouter
from typing import Dict, List, Optional
import os
import logging
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)

LANGUAGE_NAMES = {
    "en": "English",
    "hi": "Hindi",
    "ta": "Tamil",
    "te": "Telugu",
    "ka": "Kannada",
    "ml": "Malayalam",
    "mr": "Marathi",
    "gu": "Gujarati",
    "bn": "Bengali",
}

# ---------------------------------------------------------------------------
# Prompt template – chain-of-thought reasoning for agricultural diagnosis
# ---------------------------------------------------------------------------
DIAGNOSIS_PROMPT = """You are an expert agronomist helping smallholder farmers identify and treat plant diseases.

A computer vision classifier analysed a leaf image and produced the following:
  Disease detected : {disease_name}
  Confidence       : {confidence_pct}%
  Plant type       : {plant_type}
  Observed symptoms: {symptoms_list}

IMPORTANT LANGUAGE RULE:
- Write ALL output fields in {target_language_name}.
- Do not mix with English unless the crop/disease scientific name must stay unchanged.

Think step-by-step, then respond ONLY with a single valid JSON object in this exact schema:
{{
  "disease_name_localized": "<disease name written in {target_language_name}>",
  "farmer_explanation": "<2-3 plain sentences a farmer with no technical background can understand>",
  "treatment_steps": ["<step 1>", "<step 2>", "<step 3>", "<step 4>"],
  "preventive_measures": ["<measure 1>", "<measure 2>", "<measure 3>"],
  "urgency": "high" | "medium" | "low"
}}
Do not include any text outside the JSON object."""


class DiagnosisEngine:
    """LLM-based diagnosis engine that calls OpenRouter API.

    The engine builds a structured prompt containing the vision model output,
    sends it to OpenRouter API, and parses the
    JSON response back into structured recommendation fields.
    """

    def __init__(
        self,
        api_key: str = None,
        model: str = None,
        request_timeout_seconds: int = 20,
    ):
        self.api_key = api_key or os.getenv("OPENROUTER_API_KEY")
        self.model = model or os.getenv("DIAGNOSIS_MODEL", "openrouter/owl-alpha")
        self.request_timeout_seconds = request_timeout_seconds
        self.client = ChatOpenRouter(api_key=self.api_key, model=self.model)
        logger.info(f"DiagnosisEngine initialised | OpenRouter model: {self.model}")

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
        """Call OpenRouter and return structured diagnosis data.

        Falls back to a safe static response if OpenRouter is unreachable so
        that the API never returns a 500 error to the farmer.
        """
        target_language_name = LANGUAGE_NAMES.get(language, "English")
        prompt = DIAGNOSIS_PROMPT.format(
            disease_name=disease_name,
            confidence_pct=round(confidence_score * 100, 1),
            plant_type=plant_type or "unknown crop",
            symptoms_list=", ".join(symptoms) if symptoms else "none reported",
            target_language_name=target_language_name,
        )
        try:
            from langchain_core.messages import HumanMessage
            message = HumanMessage(content=prompt)
            response = self.client.invoke([message])
            raw = response.content
            parsed = json.loads(raw)
            logger.info(f"OpenRouter diagnosis generated for: {disease_name}")
            return {
                "disease_name_localized": parsed.get("disease_name_localized", ""),
                "farmer_friendly_explanation": parsed.get("farmer_explanation", ""),
                "treatment_recommendations": parsed.get("treatment_steps", []),
                "preventive_measures": parsed.get("preventive_measures", []),
                "severity_level": parsed.get("urgency", "medium"),
                "llm_generated": True,
            }
        except Exception as e:
            logger.error(f"LLM engine error: {e}")
            return self._fallback(disease_name)

    def is_available(self) -> bool:
        """Return True if OpenRouter API is reachable."""
        # During startup, just check if API key exists to avoid blocking
        # Actual connectivity will be tested during first request
        return bool(self.api_key)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _fallback(self, disease_name: str) -> Dict:
        # Return empty fields — main.py will substitute localised mock data
        # so the user never sees raw English fallback strings.
        return {
            "disease_name_localized": "",
            "farmer_friendly_explanation": "",
            "treatment_recommendations": [],
            "preventive_measures": [],
            "severity_level": "medium",
            "llm_generated": False,
        }
