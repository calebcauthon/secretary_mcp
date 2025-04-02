import json
import os
import uuid
from dataclasses import dataclass
from typing import Any, Dict, Optional

@dataclass
class TextPointer:
    """A pointer to a text file that contains the full content"""
    pointer_id: str
    file_path: str
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "pointer_id": self.pointer_id,
            "file_path": self.file_path,
            "metadata": self.metadata
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TextPointer':
        return cls(**data)

def create_text_pointer(text: str, metadata: Optional[Dict[str, Any]] = None) -> TextPointer:
    """Create a text pointer by writing text to a file and returning a pointer"""
    pointer_id = str(uuid.uuid4())[:8]  # Short unique ID
    file_path = f"text_cache/{pointer_id}.txt"
    
    # Ensure directory exists
    os.makedirs("text_cache", exist_ok=True)
    
    # Write text to file
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(text)
    
    return TextPointer(
        pointer_id=pointer_id,
        file_path=file_path,
        metadata=metadata
    )

def read_text_from_pointer(pointer: TextPointer) -> str:
    """Read the full text from a pointer"""
    with open(pointer.file_path, "r", encoding="utf-8") as f:
        return f.read()

def delete_text_pointer(pointer: TextPointer) -> None:
    """Delete the text file associated with a pointer"""
    if os.path.exists(pointer.file_path):
        os.remove(pointer.file_path) 