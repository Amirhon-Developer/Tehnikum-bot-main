import re
import requests
import telebot
from decouple import config
from telebot.types import ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove

BOT_TOKEN: str = config("TOKEN_API", cast=str)
GROUP_ID: str = config("GROUP_ID", cast=str)
GROUP_ID_AMO: str = config("GROUP_ID_AMO", cast=str)
BACKEND_TOKEN: str = config("BACKEND_TOKEN", cast=str)

headers: dict = {"Authorization": f"Token {BACKEND_TOKEN}"}

bot = telebot.TeleBot(BOT_TOKEN)  # (запуск бота)

text = {"none": None}
actions = {"none": None}
buttons = {"none": None}
type_person = []

delete_btn = ReplyKeyboardRemove()  # (отключение кнопок)
BASE_URL: str = config("BASE_URL")


@bot.message_handler(commands=['start'])
def start(message):
    first_info = {
        'id': message.chat.id,
        'username': message.chat.username,
        'first_name': message.chat.first_name
    }
    requests.post(f'{BASE_URL}users/', headers=headers, json=first_info)

    from localize.text_ru import buttons01

    kb01 = ReplyKeyboardMarkup(resize_keyboard=True)   # запрос языка
    kb01.add(buttons01['btn1'], buttons01['btn2'])
    bot.send_photo(message.chat.id, open('./media/main-pic.png', 'rb'), 'Тебя приветствует IT-Academy!\n'
                                                                 '\n'
                                                                 "IT-Academyga hush kelibsiz!")

    bot.send_message(message.chat.id, 'Для удобства, давай сперва определимся с языком.\n'
                                      '\n'
                                      "Qulay bo'lishi  uchun avvalo tilni aniqlaylik.", reply_markup=kb01)


@bot.message_handler(content_types=['text'])
def func_service(message):

    if message.text == 'Uzb 🇺🇿':

        from localize.text_uzb import actions01, text01, type_person01, buttons01
        text.update(text01)
        actions.update(actions01)
        buttons.update(buttons01)
        type_person.extend(type_person01)

        user_name = bot.send_message(message.chat.id, text["name"], reply_markup=delete_btn)
        bot.register_next_step_handler(user_name, name)
        language = {
            "language": 1
        }
        requests.patch(f"{BASE_URL}users/{message.chat.id}/", headers=headers, json=language)

    elif message.text == 'Рус 🇷🇺':
        from localize.text_ru import actions01, text01, type_person01, buttons01

        text.update(text01)
        actions.update(actions01)
        buttons.update(buttons01)
        type_person.extend(type_person01)

        user_name = bot.send_message(message.chat.id, text["name"], reply_markup=delete_btn)
        bot.register_next_step_handler(user_name, name)
        language = {
            "language": 2
        }
        requests.patch(f"{BASE_URL}users/{message.chat.id}/", headers=headers, json=language)

    elif message.text in type_person:  # кто ты воин?

        type_info = {
            "type": type_person.index(message.text)
                     }

        requests.patch(f'{BASE_URL}users/{message.chat.id}/', headers=headers, json=type_info)

        bot.send_message(GROUP_ID, send_first_info(message))

        actions_btn = ReplyKeyboardMarkup(resize_keyboard=True)
        actions_btn.add(buttons['btn3'], buttons['btn4'])
        bot.send_message(message.chat.id, text["action"], reply_markup=actions_btn)

    elif message.text == actions["sign_up"]:  # запись на консультацию
        send_date = bot.send_message(message.chat.id, text["call_back"], reply_markup=delete_btn)
        bot.register_next_step_handler(send_date, consultation_user)

    elif message.text == actions["sign_up_webinar"]:  # запись на вебинар

        response_get_webinar = requests.get(f"{BASE_URL}webinars/", headers=headers).json()

        if response_get_webinar:
            if text['id'] == 2:
                webinar_btn = InlineKeyboardMarkup(row_width=1)
                bot.send_message(message.chat.id, text["super"], reply_markup=delete_btn)
                for i in response_get_webinar:
                    btn1 = InlineKeyboardButton(text=i["name_ru"] or '', callback_data=i["id"])
                    webinar_btn.add(btn1)
                bot.send_message(message.chat.id, text["vebinar_date"], reply_markup=webinar_btn)

            else:
                response = requests.get(f"{BASE_URL}webinars/",  headers=headers,).json()
                webinar_btn = InlineKeyboardMarkup(row_width=1)
                bot.send_message(message.chat.id, text["super"], reply_markup=delete_btn)
                for i in response:
                    btn1 = InlineKeyboardButton(text=i["name_uz"] or '', callback_data=i["id"])
                    webinar_btn.add(btn1)
                bot.send_message(message.chat.id, text["vebinar_date"], reply_markup=webinar_btn)

        else:
            send_gate = bot.send_message(message.chat.id, text["sorry"], reply_markup=delete_btn)
            bot.register_next_step_handler(send_gate, consultation_user)


@bot.callback_query_handler(func=lambda call: True)
def call_back(call):
    response_get = requests.get(f'{BASE_URL}users/{call.message.chat.id}/',  headers=headers,).json()
    req = call.data.split('_')
    response_webinar = requests.get(f"{BASE_URL}webinars/{req[0]}/",  headers=headers,).json()
    reminder = {
        "webinar": req[0],
        "user": call.message.chat.id
    }

    if response_get["language"] == 1:
        bot.send_photo(call.message.chat.id, response_webinar["photo"], response_webinar["description_uz"] or "")

    else:
        bot.send_photo(call.message.chat.id, response_webinar["photo"], response_webinar["description_ru"] or "")

    requests.post(f"{BASE_URL}subscriptions/",  headers=headers, json=reminder)
    additional_data_info = {
        "additional_data": response_webinar["description_ru"]
    }
    requests.patch(f'{BASE_URL}users/{call.message.chat.id}/', headers=headers, json=additional_data_info)

    bot.send_message(GROUP_ID_AMO, send_amo_info(call.message, response_webinar))

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(buttons['btn10'])  # кнопка для отправки сообщения другу

    bot.send_message(call.message.chat.id, text["call_friend"], reply_markup=markup)


def name(message):
    name_info = {
        'first_name': message.text
    }
    response = requests.patch(f'{BASE_URL}users/{message.chat.id}/', headers=headers, json=name_info)
    if response.status_code == 400:
        print(response.json())

    phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
    phone_btn.add(buttons['btn9'])
    user_phone = bot.send_message(message.chat.id, text["contact"], reply_markup=phone_btn)
    bot.register_next_step_handler(user_phone, phone_number)


def phone_number(message):
    who_iam = ReplyKeyboardMarkup(resize_keyboard=True)
    who_iam.add(buttons['btn5'], buttons['btn6'], buttons['btn7'], buttons['btn8'])
    if message.content_type == 'contact':
        phone_number_info = {
            'phone_number': int(message.contact.phone_number)
        }

        requests.patch(f'{BASE_URL}users/{message.chat.id}/', headers=headers, json=phone_number_info)
        bot.send_message(message.chat.id, text["who_you"], reply_markup=who_iam)

    else:

        if len(message.text) == 12 and re.match(r'^(998)[\d]{9}$', message.text):
            phone_number_info = {
                'phone_number': int(message.text)
            }
            requests.patch(f'{BASE_URL}users/{message.chat.id}/', headers=headers, json=phone_number_info)
            bot.send_message(message.chat.id, text["who_you"],
                             reply_markup=who_iam)
        else:
            phone_btn = ReplyKeyboardMarkup(resize_keyboard=True)
            phone_btn.add(buttons['btn9'])
            user_phone = bot.send_message(message.chat.id, text["alert"], reply_markup=phone_btn)
            bot.register_next_step_handler(user_phone, phone_number)


def consultation_user(message):

    additional_data_info = {
        "additional_data": message.text
    }

    requests.patch(f'{BASE_URL}users/{message.chat.id}/', headers=headers, json=additional_data_info)

    bot.send_message(GROUP_ID_AMO, send_amo_info(message, None))

    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(buttons['btn10'])  # кнопка для отправки сообщения другу

    bot.send_message(message.chat.id, text["called"])
    bot.send_message(message.chat.id, text["call_friend"], reply_markup=markup)


def send_first_info(message):
    response_get = requests.get(f'{BASE_URL}users/{message.chat.id}/', headers=headers).json()
    user_language = 'Узб' if response_get['language'] == 1 else "Русс"

    user_info = (
        f"Имя: {response_get['first_name']}\n"
        f"Язык: {user_language}\n"
        f"Телефон: {response_get['phone_number']}\n"
        f"Тип лида: {type_person[response_get['type']]}\n"
    )

    return user_info


def send_amo_info(message, webinar=None):
    response_get = requests.get(f'{BASE_URL}users/{message.chat.id}/',  headers=headers).json()
    response_webinar = webinar
    user_language = 'Узб' if response_get['language'] == 1 else "Русс"

    if webinar is None:
        user_info = (
            f"Имя: {response_get['first_name']}\n"
            f"Язык: {user_language}\n"
            f"Телефон: {response_get['phone_number']}\n"
            f"Тип лида: {type_person[response_get['type']]}\n"
            f"Записался на звонок к {response_get['additional_data']}"
        )
        return user_info

    else:
        user_info = (
            f"Имя: {response_get['first_name']}\n"
            f"Язык: {user_language}\n"
            f"Телефон: {response_get['phone_number']}\n"
            f"Тип лида: {type_person[response_get['type']]}\n"
            f"Записался на вебинар {response_webinar['name_ru']} к ({response_webinar['date']}"
        )
        return user_info

bot.infinity_polling()
