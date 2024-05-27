"""
Домашнее задание №1

Использование библиотек: ephem

* Установите модуль ephem
* Добавьте в бота команду /planet, которая будет принимать на вход
  название планеты на английском, например /planet Mars
* В функции-обработчике команды из update.message.text получите
  название планеты (подсказка: используйте .split())
* При помощи условного оператора if и ephem.constellation научите
  бота отвечать, в каком созвездии сегодня находится планета.

"""
import logging, ephem, settings
from datetime import date
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')

def greet_user(update, context):  
    print('Вызван /start')
    print(update.message.reply_text('Здравствуй пользователь!'))

def name_planet(update, context):  
    print('Вызван /planet')
    print(update.message.reply_text('Введите название планеты на английском -\
 Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto'))

def talk_to_me(update, context):
    user_text = update.message.text
    print(user_text)
    
    planets = {"Mercury": ephem.Mercury("2024/05/27"), 
                "Venus": ephem.Venus("2024/05/27"), 
                "Mars" : ephem.Mars("2024/05/27"), 
                "Saturn": ephem.Saturn("2024/05/27"), 
                "Uranus": ephem.Uranus("2024/05/27"), 
                "Neptune": ephem.Neptune("2024/05/27"),
                "Pluto": ephem.Pluto("2024/05/27")
                }
    
    if user_text in planets:  # если сообщение от пользователя название планеты из словаря
        planet_input = user_text.lower().capitalize()
        print(planet_input)
        if planet_input in planets:
            const = ephem.constellation(planets[planet_input])
            update.message.reply_text(f"Планета: {planet_input}")
            update.message.reply_text(f"Сегодня 27.05.2024 в созвездии: {const[1]}")
            print(const)
    else:
        update.message.reply_text(f'Сам ты {user_text}')  # если сообщение от пользователя не содержит планету

def main():
    mybot = Updater(settings.API_KEY, use_context = True)
    
    dp = mybot.dispatcher 
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", name_planet))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
