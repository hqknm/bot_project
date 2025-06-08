from aiogram.fsm.state import State, StatesGroup

class ChartStates(StatesGroup):
    waiting_for_crypto = State()