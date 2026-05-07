"""Leaf Validation Module"""

import base64
import os
from pydantic import BaseModel
from langchain_openrouter import ChatOpenRouter
from langchain.messages import HumanMessage

class LeafValidationResult(BaseModel):
    """Structured output for leaf validation."""
    is_leaf: bool

# Global client instances
_client = None
_structured_client = None

def init_leaf_validator():
    """Initialize leaf validator with OpenRouter settings."""
    global _client, _structured_client
    
    api_key = os.getenv("OPENROUTER_API_KEY")
    model = os.getenv("LEAF_VALIDATION_MODEL", "openai/gpt-4o")
    
    if api_key:
        _client = ChatOpenRouter(api_key=api_key, model=model)
        _structured_client = _client.with_structured_output(LeafValidationResult, method="json_schema")
    else:
        _client = None
        _structured_client = None
    
    return _structured_client is not None

def validate_leaf(image_bytes: bytes) -> bool:
    """Check if image contains a leaf. Returns True if validation passes or fails gracefully."""
    if not _structured_client:
        return True  # Skip validation if no API key
    
    try:
        base64_image = base64.b64encode(image_bytes).decode('utf-8')
        
        message = HumanMessage(
            content=[
                {"type": "text", "text": "Is this image showing a plant leaf? Respond with true if yes, false if no."},
                {
                    "type": "image",
                    "base64": base64_image,
                    "mime_type": "image/jpeg",
                },
            ]
        )
        
        result = _structured_client.invoke([message])
        return result.is_leaf
        
    except Exception:
        return True  # Allow image if validation fails
