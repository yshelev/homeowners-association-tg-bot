from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callback_data import ProblemTypeCallbackData


class InlineKeyboardFabric:
	@classmethod
	def get_problem_type_keyboard(cls):
		return InlineKeyboardMarkup(
			inline_keyboard=[
				[
					InlineKeyboardButton(
						text="Вызов мастера",
						callback_data=ProblemTypeCallbackData(title="master_call").pack()
					),
					InlineKeyboardButton(
						text="Сообщить о проблеме",
						callback_data=ProblemTypeCallbackData(title="create_report").pack()
					),
					InlineKeyboardButton(
						text="Показания счетчиков",
						callback_data=ProblemTypeCallbackData(title="meter_readings").pack()
					),
					InlineKeyboardButton(
						text="Заказать справки",
						callback_data=ProblemTypeCallbackData(title="order_certificates").pack()
					),
					InlineKeyboardButton(
						text="Контакты ТСЖ",
						callback_data=ProblemTypeCallbackData(title="contacts").pack()
					)
				]
			]
		)