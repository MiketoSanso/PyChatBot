from collections import deque
from dataclasses import dataclass, field

from Scripts.Domain.Data.Languages import Languages


@dataclass
class AiData:
    name: str = ""
    prompt: str = ""
    messages: deque = field(default_factory=deque)
    language: Languages = Languages.eng

    @classmethod
    def from_dict(cls, data: dict):
        name = data.get("name", "")
        prompt = data.get("prompt", "")

        messages_data = data.get("messages", [])
        messages = deque(messages_data)

        language = Languages(data.get("language", 0))


        return cls(name=name,
                   prompt=prompt,
                   messages=messages,
                   language=language)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "prompt": self.prompt,
            "messages": list(self.messages),
            "language": self.language.value
        }
