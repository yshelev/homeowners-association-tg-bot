from aiogram.fsm.state import State, StatesGroup


class ReportForm(StatesGroup):
	text = State()

class OrderForm(StatesGroup):
	text = State()

class MasterCallForm(StatesGroup):
	start = State()
	master = State()

class UserFSM(StatesGroup):
	start = State()
	prepare = State()
	informed = State()

