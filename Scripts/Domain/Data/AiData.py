from dataclasses import dataclass

from Scripts.Domain.Data.Languages import Languages


@dataclass
class AiData:
    name = ""
    prompt = ""
    messages = ()
    language = Languages.eng
