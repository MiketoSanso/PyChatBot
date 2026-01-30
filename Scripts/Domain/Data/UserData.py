from dataclasses import dataclass
from Scripts.Domain.Data.AiData import AiData
from Scripts.Domain.Data.Languages import Languages


@dataclass
class UserData:
    active_ai: int = 1
    tokens: int = 10000
    count_ai: int = 1
    language: Languages = Languages.eng
    ai_data: AiData = AiData()

    @classmethod
    def from_dict(cls, data: dict):
        active_ai_value = data.get("active_ai", 0)
        tokens_value = data.get("tokens", 0)
        count_ai_value = data.get("count_ai", 1)
        language_value = Languages(data.get("language", 0))
        ai_data_value = data.get("ai_data", AiData())

        return cls(active_ai=active_ai_value,
                   tokens = tokens_value,
                   count_ai = count_ai_value,
                   language=language_value,
                   ai_data=ai_data_value)

    def to_dict(self) -> dict:
        return {
            "active_ai": self.active_ai,
            "tokens": self.tokens,
            "count_ai": self.count_ai,
            "language": self.language.value,
            "ai_data": self.ai_data.to_dict()
        }