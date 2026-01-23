from dataclasses import dataclass
from Scripts.Domain.Data.Languages import Languages


@dataclass
class UserData:
    active_ai = 0
    tokens = 0
    count_ai = 1
    language = Languages.eng
    ai_data = ()