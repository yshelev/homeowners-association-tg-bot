from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from presentation.keyboards.constants import (
	ORDER_CERTIFICATES,
	METER_READINGS,
	CREATE_REPORT,
	MASTER_CALL,
	CONTACTS,
	DISPATCHER_CONTACT,
	ELECTRIC_CONTACT, BACK
)


class ReplyKeyboardFabric:
	@classmethod
	def get_problem_type_keyboard(cls):
		return ReplyKeyboardMarkup(
			keyboard=[
				[
					KeyboardButton(text=MASTER_CALL),
					KeyboardButton(text=CREATE_REPORT),
					KeyboardButton(text=METER_READINGS),
				],
				[
					KeyboardButton(text=ORDER_CERTIFICATES),
					KeyboardButton(text=CONTACTS)
				],
			],
			resize_keyboard=True,
			one_time_keyboard=True
		)

	@classmethod
	def contacts_keyboard(cls):
		return ReplyKeyboardMarkup(
			keyboard=[
				[
					KeyboardButton(text=DISPATCHER_CONTACT),
					KeyboardButton(text=ELECTRIC_CONTACT),
					KeyboardButton(text=BACK)
				]
			],
			resize_keyboard=True,
		)

	@classmethod
	def back_keyboard(cls):
		return ReplyKeyboardMarkup(
			keyboard=[
				[
					KeyboardButton(text=BACK)
				]
			],
			resize_keyboard=True
		)