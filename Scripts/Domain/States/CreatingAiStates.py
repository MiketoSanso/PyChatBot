from aiogram.fsm.state import State, StatesGroup

class CreatingAiStates(StatesGroup):
    number_bot = State()
    name_bot = State()
    prompt = State()
    language = State()
