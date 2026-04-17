"""Vision Model Wrapper

How to connect a trained model
-------------------------------
1. Train an EfficientNet-V2-S or ViT-B16 classifier on the PlantVillage
    dataset (38 classes). Save the checkpoint with VisionModel.save().
2. Place the .pt file at the path set by VISION_MODEL_PATH (default: ./models/vision/plant_disease.pt).
3. At startup the API calls VisionModel.load(path) which reads the state_dict
    from the checkpoint and rebuilds the same architecture used during training.
4. Call model.preprocess_image(image_bytes) -> tensor, then model.predict(tensor)
    to get logits and per-class probabilities.
5. Use DISEASE_CLASSES[top_class_index] to convert the argmax prediction to a
    human-readable disease name that is then passed to the LLM engine.
"""

import io
import torch
from torch import nn
from torchvision import models, transforms
from PIL import Image
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# PlantVillage 38-class label map
# ---------------------------------------------------------------------------
DISEASE_CLASSES = [
     "Apple___Apple_scab", "Apple___Black_rot", "Apple___Cedar_apple_rust", "Apple___healthy",
     "Blueberry___healthy", "Cherry_(including_sour)___Powdery_mildew", "Cherry_(including_sour)___healthy",
     "Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot", "Corn_(maize)___Common_rust_",
     "Corn_(maize)___Northern_Leaf_Blight", "Corn_(maize)___healthy",
     "Grape___Black_rot", "Grape___Esca_(Black_Measles)", "Grape___Leaf_blight_(Isariopsis_Leaf_Spot)", "Grape___healthy",
     "Orange___Haunglongbing_(Citrus_greening)", "Peach___Bacterial_spot", "Peach___healthy",
     "Pepper,_bell___Bacterial_spot", "Pepper,_bell___healthy",
     "Potato___Early_blight", "Potato___Late_blight", "Potato___healthy",
     "Raspberry___healthy", "Soybean___healthy", "Squash___Powdery_mildew",
     "Strawberry___Leaf_scorch", "Strawberry___healthy",
     "Tomato___Bacterial_spot", "Tomato___Early_blight", "Tomato___Late_blight",
     "Tomato___Leaf_Mold", "Tomato___Septoria_leaf_spot",
     "Tomato___Spider_mites Two-spotted_spider_mite", "Tomato___Target_Spot",
     "Tomato___Tomato_Yellow_Leaf_Curl_Virus", "Tomato___Tomato_mosaic_virus", "Tomato___healthy",
]

# Standard ImageNet normalisation used by all torchvision pretrained models
_INFERENCE_TRANSFORM = transforms.Compose([
     transforms.Resize((224, 224)),
     transforms.ToTensor(),
     transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])


class VisionModel:
    """Wrapper for vision models (EfficientNet-V2, ViT-B16)."""
    
    def __init__(
        self, 
        model_name: str = "efficientnet_v2_s",
        num_classes: int = 38,
        pretrained: bool = True,
        device: Optional[str] = None,
        class_names: Optional[list[str]] = None,
    ):
        """Initialize vision model."""
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.num_classes = num_classes
        self.class_names = class_names or DISEASE_CLASSES[:num_classes]
        
        self.model = self._load_model(model_name, num_classes, pretrained)
        self.model.to(self.device)
        self.model.eval()
        
        logger.info(f"Loaded {model_name} on {self.device}")
    
    def _load_model(
        self, 
        model_name: str, 
        num_classes: int, 
        pretrained: bool
    ) -> nn.Module:
        """Load and configure model."""
        if model_name.startswith("efficientnet"):
            weights = models.EfficientNet_V2_S_Weights.DEFAULT if pretrained else None
            model = models.efficientnet_v2_s(weights=weights)
        elif model_name == "vit_b16":
            weights = models.ViT_B_16_Weights.DEFAULT if pretrained else None
            model = models.vit_b_16(weights=weights)
        else:
            raise ValueError(f"Unknown model: {model_name}")
        
        # Replace classifier
        num_features = model.classifier[1].in_features if hasattr(model, 'classifier') else model.heads.head.in_features
        if hasattr(model, 'classifier'):
            model.classifier[1] = nn.Linear(num_features, num_classes)
        else:
            model.heads.head = nn.Linear(num_features, num_classes)
        
        return model
    
    def predict(self, image_tensor: torch.Tensor) -> Tuple[torch.Tensor, torch.Tensor]:
        """Get predictions for images."""
        with torch.no_grad():
            image_tensor = image_tensor.to(self.device)
            logits = self.model(image_tensor)
            probabilities = torch.softmax(logits, dim=1)
        
        return logits, probabilities
    
    def save(self, path: str) -> None:
        """Save model checkpoint."""
        torch.save({
            'model_state': self.model.state_dict(),
            'model_name': self.model_name,
            'num_classes': self.num_classes,
            'class_names': self.class_names,
        }, path)
        logger.info(f"Model saved to {path}")

    @classmethod
    def load(cls, path: str) -> "VisionModel":
        """Load a previously saved checkpoint back into a VisionModel instance.

        The checkpoint must have been created with VisionModel.save() so that
        the model_name and num_classes keys are present.  The method rebuilds
        the exact same architecture, loads the state_dict, and sets eval mode.

        Usage::

            model = VisionModel.load("./models/vision/plant_disease.pt")
            tensor = model.preprocess_image(open("leaf.jpg", "rb").read())
            logits, probs = model.predict(tensor)
            predicted_class = DISEASE_CLASSES[probs.argmax().item()]
        """
        checkpoint = torch.load(path, map_location="cpu", weights_only=True)
        instance = cls(
            model_name=checkpoint["model_name"],
            num_classes=checkpoint["num_classes"],
            pretrained=False,
            class_names=checkpoint.get("class_names"),
        )
        instance.model.load_state_dict(checkpoint["model_state"])
        instance.model.eval()
        logger.info(f"Model checkpoint loaded from {path}")
        return instance

    def preprocess_image(self, image_bytes: bytes) -> torch.Tensor:
        """Convert raw image bytes to a normalised batch tensor ready for inference.

        The image is resized to 224x224, converted to RGB, normalised with
        ImageNet statistics, and given a batch dimension of 1.
        """
        image = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        tensor = _INFERENCE_TRANSFORM(image)
        return tensor.unsqueeze(0)  # shape: (1, C, H, W)

    def predict_class(self, image_bytes: bytes) -> Tuple[str, float]:
        """End-to-end helper: bytes -> (disease_name, confidence).

        Returns the top-1 predicted disease label and its probability.
        This is the method called by the API endpoint.
        """
        tensor = self.preprocess_image(image_bytes)
        _, probs = self.predict(tensor)
        top_idx = probs.argmax(dim=1).item()
        confidence = probs[0, top_idx].item()
        labels = self.class_names or DISEASE_CLASSES
        disease_name = labels[top_idx] if top_idx < len(labels) else "unknown"
        return disease_name, confidence
