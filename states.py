from aiogram.fsm.state import StatesGroup, State

class Anketa(StatesGroup):
    name = State()
    occupation = State()
    education = State()
    about = State()
    photo = State()

class edit_ank(StatesGroup):
    name = State()
    occupation = State()
    education = State()
    about = State()
    photo = State()
        