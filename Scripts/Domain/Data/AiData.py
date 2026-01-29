from dataclasses import dataclass
from typing import Tuple

from Scripts.Domain.Data.Languages import Languages


@dataclass
class AiData:
    name: str = ""
    prompt: str = ""
    messages: Tuple = ()
    last_index_message = 0
    language: Languages = Languages.eng

    @classmethod
    def from_dict(cls, data: dict):
        name = data.get("name", "")
        prompt = data.get("prompt", "")
        messages = data.get("messages", ())
        language = Languages(data.get("language", 0))

        return cls(name=name,
                   prompt=prompt,
                   messages=messages,
                   language=language)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt,
            "messages": self.messages,
            "language": self.language.value,
        }
