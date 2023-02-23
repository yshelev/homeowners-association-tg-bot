from email.mime.text import MIMEText
from typing import Type

import telebot
from telebot import types
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

TOKEN = "5941022226:AAHWQRMfKB21R__JoxFxhIe910WXCR9_RH4"
bot = telebot.TeleBot(TOKEN)
evidence_or_problem_or_reference = -1  # показания - 0, проблема - 1, справка - 2


@bot.message_handler(commands=['start'])
def start(message=Type[str]) -> None:
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.KeyboardButton("Вызов мастера")
    btn2 = types.KeyboardButton("Сообщить о проблеме")
    btn3 = types.KeyboardButton("Показания счетчиков")
    btn4 = types.KeyboardButton("Заказать справки")
    btn5 = types.KeyboardButton("Контакты ТСЖ")
    markup.add(btn1, btn2, btn3, btn4, btn5)
    bot.send_message(message.chat.id,
                     text="Здравствуйте, вас приветствует диспетчер ТСЖ \"ку ку\". \n Выберите действия ниже.".format(
                         message.from_user), reply_markup=markup)


@bot.message_handler(content_types=['text'])
def func(message=Type[str]) -> None:
    global evidence_or_problem_or_reference
    if message.text == "Сообщить о проблеме":
        bot.send_message(message.chat.id, text=f"Опишите проблему.")
        evidence_or_problem_or_reference = 1
    elif message.text == "Показания счетчиков":
        bot.send_message(message.chat.id, text='Отправьте фотографию с показаниями счетчиков')
        evidence_or_problem_or_reference = 0
    elif message.text == "Заказать справки":
        evidence_or_problem_or_reference = 2
        bot.send_message(message.chat.id, text="Опишите, какая заявка вам нужна.")
    elif message.text == "Контакты ТСЖ":
        bot.send_message(message.chat.id, text='contact1, contact2, contact3, contact4, etc.')
    elif message.text == "Вызов мастера":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Электрик")
        btn2 = types.KeyboardButton("Слесарь")
        btn3 = types.KeyboardButton("Диспетчер ТСЖ")
        btn4 = types.KeyboardButton("Лифтер")
        btn5 = types.KeyboardButton("Домофон")
        back = types.KeyboardButton("Назад")
        markup.add(btn1, btn2, btn3, btn4, btn5, back)
        bot.send_message(message.chat.id, text="Выберите мастера", reply_markup=markup)
    elif message.text == "Назад":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Вызов мастера")
        btn2 = types.KeyboardButton("Сообщить о проблеме")
        btn3 = types.KeyboardButton("Показания счетчиков")
        btn4 = types.KeyboardButton("Заказать справки")
        btn5 = types.KeyboardButton("Контакты ТСЖ")
        markup.add(btn1, btn2, btn3, btn4, btn5)
        bot.send_message(message.chat.id, text="Выберите действие.", reply_markup=markup)
    elif message.text == 'Электрик':
        bot.send_message(message.chat.id, text='contact_electric')
    elif message.text == 'Слесарь':
        bot.send_message(message.chat.id, text='contact_slesar')
    elif message.text == 'Диспетчер ТСЖ':
        bot.send_message(message.chat.id, text='contact_dispetcher')
    elif message.text == 'Лифтер':
        bot.send_message(message.chat.id, text='contact_lifter')
    elif message.text == 'Домофон':
        bot.send_message(message.chat.id, text='contact_domofon')
    else:
        if evidence_or_problem_or_reference != -1:
            if evidence_or_problem_or_reference == 1:
                title = "ПРОБЛЕМА"
                text = message.text
                attach_to_gmail(title, text, False, message)
                evidence_or_problem_or_reference = -1
            else:
                title = 'СПРАВКА'
                text = message.text
                attach_to_gmail(title, text, False, message)
                evidence_or_problem_or_reference = -1
        else:
            bot.send_message(message.chat.id, text="Попробуйте снова.")


@bot.message_handler(content_types=['photo'])
def photo(message=Type[str]) -> None:
    text = message.caption
    if evidence_or_problem_or_reference == 0:
        title = 'ПОКАЗАНИЯ СЧЕТЧИКОВ'
    elif evidence_or_problem_or_reference == 1:
        title = "ПРОБЛЕМА"
    elif evidence_or_problem_or_reference == 2:
        title = "СПРАВКА"
    else:
        title = "idkwhatisit"

    fileID = message.photo[-1].file_id
    file_info = bot.get_file(fileID)
    downloaded_file = bot.download_file(file_info.
                                        file_path)
    with open("image.jpg", 'wb') as new_file:
        new_file.write(downloaded_file)
    attach_to_gmail(title, text, True, message)


def attach_to_gmail(title=Type[str], text=Type[str], need_photo=Type[bool], message=Type[str]) -> None:
    msg = MIMEMultipart()

    password = "xjawajhqgjkbejmk"
    msg['From'] = "alinabadak@gmail.com"
    msg['To'] = "777777777777t@mail.ru"
    msg['Subject'] = title
    if need_photo:
        part = MIMEApplication(open('image.jpg', 'rb').read())
        part.add_header('Content-Disposition', 'attachment', filename='image.jpg')
        msg.attach(part)

    msg.attach(MIMEText(text))

    server = smtplib.SMTP('smtp.gmail.com', 587)

    server.starttls()

    server.login(msg['From'], password)

    server.sendmail(msg['From'], msg['To'], msg.as_string())
    # print(msg["From"], msg['To'], msg.as_string())
    server.quit()
    bot.send_message(message.chat.id, text="Ваше сообщение доставлено. Спасибо за обращение к боту!")


bot.polling(none_stop=True)
