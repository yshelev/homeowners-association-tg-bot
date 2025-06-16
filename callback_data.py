from aiogram.filters.callback_data import CallbackData

class ProblemTypeCallbackData(CallbackData, prefix="problem_type"):
	title: str