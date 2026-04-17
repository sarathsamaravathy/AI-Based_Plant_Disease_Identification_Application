"""Download and convert a pretrained Hugging Face plant disease model.

Usage:
    python scripts/download_pretrained_model.py
    python scripts/download_pretrained_model.py --model-id BrandonFors/effnetv2_s_plant_disease --output models/vision/plant_disease.pt
"""

from __future__ import annotations

import argparse

from src.vision.hf_loader import DEFAULT_HF_MODEL_ID, convert_huggingface_model_to_local_checkpoint


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Download a pretrained Hugging Face plant disease model")
    parser.add_argument("--model-id", default=DEFAULT_HF_MODEL_ID)
    parser.add_argument("--output", default="models/vision/plant_disease.pt")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    path = convert_huggingface_model_to_local_checkpoint(args.model_id, args.output)
    print(f"Saved local checkpoint to: {path}")
