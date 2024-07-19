import telebot
from dotenv import load_dotenv, find_dotenv
import os
from g4f.client import Client
from generate_img_with_sber import gen_img

from gtts import gTTS

load_dotenv(find_dotenv())
API_TOKEN = os.getenv('TOKEN')
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(commands=['MeM'])
def start_poisk2(message):
    chatID = message.from_user.id
    bot.send_message(chatID, 'Тема для мема')
    bot.register_next_step_handler(message, generate_mem)

def generate_mem(message):
    chatID = message.from_user.id
    try:
        content = gen_img(message.text, '10A44144735334CF20BF7363F09D60F5', '38C8048E16F38F9E61B10CD910B48382')
        bot.send_photo(message.chat.id, content)
        answer = get_info_wolfram(f'сгенерируй шутку на тему {message.text}')
        print(answer)

        # озвучиваем текст
        tts = gTTS(text=answer, lang='ru')
        tts.save("good.mp3")
        bot.send_voice(message.chat.id, open("good.mp3", "rb"))
        bot.send_message(chatID, answer)
    except:
        bot.send_message(message.chat.id, 'Попробуйте ещё раз')
def get_info_wolfram(query):
    client = Client()
    response = client.chat.completions.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": query}])
    return response.choices[0].message.content


bot.infinity_polling()