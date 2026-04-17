"""Helpers for bootstrapping a local checkpoint from a Hugging Face model repo."""

from __future__ import annotations

import json
from pathlib import Path

import torch
from huggingface_hub import snapshot_download

from src.vision.model import VisionModel


DEFAULT_HF_MODEL_ID = "BrandonFors/effnetv2_s_plant_disease"


def _normalise_state_dict_keys(state_dict: dict) -> dict:
    return {
        key.removeprefix("model."): value
        for key, value in state_dict.items()
    }


def _extract_class_names(config_path: Path) -> list[str]:
    config = json.loads(config_path.read_text(encoding="utf-8"))
    id2label = config.get("id2label", {})
    if not id2label:
        raise ValueError("No id2label mapping found in Hugging Face config.json")
    return [id2label[str(index)] for index in sorted(map(int, id2label.keys()))]


def convert_huggingface_model_to_local_checkpoint(
    model_id: str = DEFAULT_HF_MODEL_ID,
    output_path: str = "./models/vision/plant_disease.pt",
) -> str:
    """Download a pretrained HF model and save it in the local VisionModel format."""
    repo_dir = Path(
        snapshot_download(
            repo_id=model_id,
            allow_patterns=["config.json", "pytorch_model.bin"],
        )
    )
    config_path = repo_dir / "config.json"
    weights_path = repo_dir / "pytorch_model.bin"

    if not config_path.is_file() or not weights_path.is_file():
        raise FileNotFoundError(f"Expected config.json and pytorch_model.bin in {repo_dir}")

    class_names = _extract_class_names(config_path)
    raw_state_dict = torch.load(weights_path, map_location="cpu", weights_only=True)
    state_dict = _normalise_state_dict_keys(raw_state_dict)

    model = VisionModel(
        model_name="efficientnet_v2_s",
        num_classes=len(class_names),
        pretrained=False,
        class_names=class_names,
    )
    model.model.load_state_dict(state_dict, strict=True)

    output = Path(output_path)
    output.parent.mkdir(parents=True, exist_ok=True)
    model.save(str(output))
    return str(output)
