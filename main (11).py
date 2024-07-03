import pandas as pd
import telebot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton
import os
import requests

bot = telebot.TeleBot('6905965448:AAGJuRakgoRAP_Fm7r4m2DmZSlP5aE9r0-o',parse_mode="Markdown")
admin_ids = [897929245]


@bot.message_handler(commands=['start', 'help'])
def handle_start(message):
    
    photo_url = 'https://sun9-75.userapi.com/impg/t4sq3nroP1WW0YIQgTjh6mgFUNUbxpZrAZtL8g/PPkH9eY1_Qo.jpg?size=2560x1895&quality=95&sign=25d5a8baa86df5d52abdd6c593afdeb4&type=album'
    response = requests.get(photo_url)
    if response.status_code == 200:
        bot.send_photo(message.chat.id, response.content)
        bot.reply_to(message, "Привет!🤖 Я ЦМЛ-БОТ! Напиши свою ФИО в таком порядке: Лапин Владислав Дмитриевич")
    else:
        bot.reply_to(message, "Произошла ошибка при загрузке фотографии.")

@bot.message_handler()
def handle_text(message: Message):
    msg: Message = bot.send_message(message.chat.id, "Выполняю поиск...")
    name = message.text.strip()

    for file in os.listdir():
        if file.endswith(".xlsx"):
            file_name = file
            break

    df = pd.read_excel(file_name)
    row = df.loc[df['Имя'] == name]

    bot.delete_message(msg.chat.id, msg.message_id)
    if not row.empty:
        photo_url = row['URL фото'].values[0] if 'URL фото' in row.columns else None
        text = f"""
*Имя волонтёра:* {name}

💥 Номер участника: {int(row['№ участника'].values[0])}
📈 Количество дней в проекте: {int(row['Количество дней в проекте'].values[0])}
🧾 Количество выполненных заданий: {int(row['Активности (заданий) всего'].values[0])}
📊 Oбщий коэффициент умножения: {int(row['Общий коэффициент умножения'].values[0])}

⌚ Часы в штабе и в штате: {int(row['Часы в штабе и штате'].values[0])}
⏱ Часы за выполненные задания: {int(row['Часы за выполненные задания'].values[0])}

💯 Баллы на призы: {int(row['Текущее количество баллов'].values[0])}
🧧 ЦМЛ всего на призы: {int(row['Текущее количество ЦМЛ'].values[0])}

🎁 Освоено ЦМЛ на призы: {int(row['Всего освоенно ЦМЛ'].values[0])}

👤 Баллы от рефералов: {int(row['Баллы от рефералов'].values[0])}
👥 Количество рефералов: {int(row['Общее количество рефералов'].values[0])}
"""
        if photo_url:
            photo_response = requests.get(photo_url)
            bot.send_photo(message.chat.id, photo_response.content, caption=text, parse_mode='Markdown')
        else:
            bot.send_message(message.chat.id, text, parse_mode='Markdown')
    else:
        bot.send_message(message.chat.id, f"Данный запрос '{name}' не найден в системе, попробуйте ввести по-другому.")


@bot.message_handler(func=lambda message: message.from_user.id in admin_ids, content_types=["document"])
def handle_document(message: Message):
    file_info = bot.get_file(message.document.file_id)
    file_path = file_info.file_path
    downloaded_file = bot.download_file(file_path)

  
    for file in os.listdir():
        if file.endswith(".xlsx"):
            os.remove(file)
            break

 
    with open(message.document.file_name, 'wb') as new_table:
        new_table.write(downloaded_file)

    bot.send_message(message.chat.id, "Таблица успешно загружена!")

bot.polling()