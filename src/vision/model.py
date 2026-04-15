"""Vision Model Wrapper"""

import torch
from torch import nn
from torchvision import models
from typing import Tuple, Optional
import logging

logger = logging.getLogger(__name__)

class VisionModel:
    """Wrapper for vision models (EfficientNet-V2, ViT-B16)."""
    
    def __init__(
        self, 
        model_name: str = "efficientnet_v2_s",
        num_classes: int = 38,
        pretrained: bool = True,
        device: Optional[str] = None
    ):
        """Initialize vision model."""
        self.device = device or ("cuda" if torch.cuda.is_available() else "cpu")
        self.model_name = model_name
        self.num_classes = num_classes
        
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
            'num_classes': self.num_classes
        }, path)
        logger.info(f"Model saved to {path}")
