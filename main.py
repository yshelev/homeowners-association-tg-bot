import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import settings
from config import WEBHOOK_URL
from presentation.final_state_machines import ReportForm, OrderForm, UserFSM
from presentation.keyboards.constants import (
    CONTACTS,
    ORDER_CERTIFICATES,
    CREATE_REPORT,
    MASTER_CALL,
    METER_READINGS,
    ALL_CONTACTS, BACK
)
from presentation.keyboards.reply import ReplyKeyboardFabric

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await bot.set_webhook(
        url=WEBHOOK_URL,
        drop_pending_updates=True
    )
    logging.info("Бот запущен!")

    yield  # Здесь FastAPI работает в обычном режиме

    # Shutdown логика
    await bot.delete_webhook()
    await bot.session.close()
    logging.info("Бот остановлен. Вебхук удалён.")
app = FastAPI(lifespan=lifespan)


@dp.message(Command("start"))
async def start(message: Message, state: FSMContext):
    await state.set_state(UserFSM.start)
    kb = ReplyKeyboardFabric.get_problem_type_keyboard()
    await message.answer(f"Здравствуйте, {message.from_user.first_name}, вас приветствует диспетчер ТСЖ."
                         f"\nВыберите действия ниже.", reply_markup=kb)

@dp.message(F.text == CONTACTS, UserFSM.start)
async def contacts(message: Message, state: FSMContext):
    await state.set_state(UserFSM.informed)
    bkb = ReplyKeyboardFabric.back_keyboard()
    await message.answer(f"contacts, user {await state.get_state()}", reply_markup=bkb)

@dp.message(F.text == CREATE_REPORT, UserFSM.start)
async def create_report(message: Message, state: FSMContext):
    await state.set_state(ReportForm.text)
    await state.set_state(UserFSM.prepare)
    bkb = ReplyKeyboardFabric.back_keyboard()
    await message.answer("Опишите проблему.", reply_markup=bkb)

@dp.message(F.text == ORDER_CERTIFICATES)
async def order_certificates(message: Message, state: FSMContext):
    await state.set_state(OrderForm.text)
    await state.set_state(UserFSM.prepare)
    bkb = ReplyKeyboardFabric.back_keyboard()
    await message.answer("Опишите, какая заявка вам нужна.", reply_markup=bkb)

@dp.message(F.text == MASTER_CALL)
async def master_call(message: Message, state: FSMContext):
    await state.set_state(UserFSM.prepare)
    kb = ReplyKeyboardFabric.contacts_keyboard()
    await message.answer("Выберите мастера", reply_markup=kb)

@dp.message(F.text.in_(ALL_CONTACTS))
async def get_contact(message: Message, state: FSMContext):
    await message.answer(ALL_CONTACTS.get(message.text))

@dp.message(F.text == METER_READINGS)
async def meter_readings(message: Message, state: FSMContext):
    await state.set_state(UserFSM.prepare)
    bkb = ReplyKeyboardFabric.back_keyboard()
    await message.answer("Отправьте фотографии с показаниями ваших счетчиков.", reply_markup=bkb)

@dp.message(ReportForm.text, UserFSM.prepare)
async def handle_report_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    await message.answer("Заявка принята в работу, спасибо💘")

@dp.message(OrderForm.text, UserFSM.prepare)
async def handle_report_text(message: Message, state: FSMContext):
    await state.update_data(text=message.text)
    data = await state.get_data()
    await state.clear()
    await state.set_state(UserFSM.informed)
    await message.answer("Заявка принята в работу, спасибо💘")

@dp.message(F.text == BACK)
async def handle_back_button(message: Message, state: FSMContext):
    await state.set_state(UserFSM.start)
    kb = ReplyKeyboardFabric.get_problem_type_keyboard()
    await message.answer(f"\nВыберите действия ниже.", reply_markup=kb)

@app.post(WEBHOOK_URL)
async def bot_webhook(request: Request):
    update = types.Update(**await request.json())
    await dp.feed_update(bot, update)
    return JSONResponse({"status": "ok"})

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0")