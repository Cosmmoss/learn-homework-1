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
import logging
import ephem
import settings
import locale
from datetime import datetime
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
logging.basicConfig(format='%(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO,
                    filename='bot.log')
locale.setlocale(locale.LC_TIME, 'ru_RU')  # что бы генерировать кирилические дни недели

planets = {"Mercury": ephem.Mercury, 
            "Venus": ephem.Venus, 
            "Mars" : ephem.Mars, 
            "Saturn": ephem.Saturn, 
            "Uranus": ephem.Uranus, 
            "Neptune": ephem.Neptune,
            "Pluto": ephem.Pluto,
            "Moon": ephem.Moon,
            "Sun": ephem.Sun,
            "Jupiter": ephem.Jupiter
            }

def greet_user(update, context):  # update - это то, что поступило от пользователя Telegram. Context - это спец. штука с помощью которой мы можем изнутри функции отдавать команды боту
    print('Вызван /start')
    update.message.reply_text('Здравствуй пользователь!')

def planet_const(update, context):  # вызов команды /planet
    print('Вызван /planet')
    update.message.reply_text("Введите название объекта Солнечной системы -\
 Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Moon, Sun")
    
def get_constelletion(planet_name):  # функция обрабатывает сообщение пользователя с названием планеты
    current_date = datetime.now().strftime('%d.%m.%Y %H:%M')  # переменная для корректной работы с ephem
    current_planet = planets[planet_name](current_date)  # переменная планеты с обработкой
    current_date = datetime.now().strftime('%A %d.%m.%Y %H:%M')  # переменная с отображением дня недели на кириллице
    return ephem.constellation(current_planet), current_date  # функция возвращает созвездие и дату

def talk_to_me(update, context):  # функция принимает и распределяет все сообщения от пользователя
    user_text = update.message.text
    print(user_text)  
    if user_text.lower().capitalize() in planets:  # если текст сообщения от пользователя есть в словаре с планетами
        planet_name = user_text  # передаём в переменную текст сообщения
        const, current_date = get_constelletion(planet_name)  # получаем переменные из функции get_constelletion(planet_name)
        update.message.reply_text(f"Сегодня: {current_date}")  # вывод пользователю даты
        update.message.reply_text(f"Планета {planet_name} в созвездии: {const[1]}")  # вывод пользователю созвездия
        print(const, current_date, sep='\n')  # вывод в консоль созвездия, даты
    else:
        update.message.reply_text(f"Хотите узнать про созвездия, нажмите: {'/planet'}")
    
def main():
    mybot = Updater(settings.API_KEY, use_context = True)
    
    dp = mybot.dispatcher  # в переменную dp кладём это, чтобы в дальнейшем не набирать длинное название
    dp.add_handler(CommandHandler("start", greet_user))
    dp.add_handler(CommandHandler("planet", planet_const))
    dp.add_handler(MessageHandler(Filters.text, talk_to_me))
    
    logging.info("Bot started")
    mybot.start_polling()
    mybot.idle()

if __name__ == "__main__":
    main()
