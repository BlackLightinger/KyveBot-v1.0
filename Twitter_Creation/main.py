import traceback
from twitter_creation import twc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import telebot
from telebot import types
from auth_data import telebot_token, bot_pass
from pyvirtualdisplay import Display


bot = telebot.TeleBot(telebot_token)
bot_auth = False
running = False
flag_pass = False
flag_first_auth = False
stop_flag = True
driver = None


def check(running):
    return running


def main():
    global running
    global stop_flag
    while check(running):
        #display = Display(visible=0, size=(800, 600))
        #display.start()

        options = Options()
        options.add_extension('proxy.zip')
        #options.add_argument('--no-sandbox')
        global driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        twc(driver)

        driver.quit()
        #display.stop()

    stop_flag = True


@bot.message_handler(commands=['start'])
def start(message):
    global bot_auth, running, flag_pass, flag_first_auth, stop_flag
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    but1 = types.KeyboardButton('Авторизоваться')

    markup.add(but1)

    bot.send_message(message.chat.id, '<b>Привет, авторизуйся для работы с ботом</b>',
                     parse_mode='html', reply_markup=markup)

    bot_auth = False
    running = False
    flag_pass = False
    flag_first_auth = False
    stop_flag = True


@bot.message_handler(content_types=['text'])
def authorise(message):
    global flag_pass, running, stop_flag, bot_auth, flag_first_auth
    if message.text == 'Авторизоваться' and not flag_first_auth:
        bot.send_message(message.chat.id, '<b>Привет, введи пароль для работы с ботом:</b>',
                         parse_mode='html')
        flag_first_auth = True

    elif message.text != bot_pass and not flag_pass and flag_first_auth:
        bot.send_message(message.chat.id, '<b>Неверный пароль!</b>',
                         parse_mode='html')

    elif message.text == bot_pass and not flag_pass:
        bot_auth = True
        flag_pass = True

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        but2 = types.KeyboardButton('Запустить')
        but3 = types.KeyboardButton('Остановить')
        but4 = types.KeyboardButton('Отключить')
        but5 = types.KeyboardButton('Выслать твиттер аккаунты')

        markup.add(but2, but3, but4, but5)

        bot.send_message(message.chat.id, '<b>Авторизация прошла успешно, можно запускать бота!</b>',
                         parse_mode='html', reply_markup=markup)

    elif message.text == 'Запустить' and flag_pass and stop_flag:
        running = True
        stop_flag = False
        bot.send_message(message.chat.id, '<b>Бот запущен!</b>',
                         parse_mode='html')
        try:
            main()
        except:
            bot.send_message(message.chat.id, traceback.format_exc())
            bot.send_message(message.chat.id, '<b>Бот был остановлен, из-за ошибки!</b>',
                             parse_mode='html')
            global driver
            stop_flag = True
            driver.quit()
            print(traceback.format_exc())

    elif message.text == 'Запустить' and flag_pass and not stop_flag:
        bot.send_message(message.chat.id, '<b>Бот уже работает!</b>',
                         parse_mode='html')

    elif message.text == 'Остановить' and flag_pass and running:
        running = False
        bot.send_message(message.chat.id, '<b>Бот будет остановлен после завершения цикла!</b>',
                         parse_mode='html')

    elif message.text == 'Остановить' and flag_pass and not running:
        bot.send_message(message.chat.id, '<b>Бот не запущен</b>',
                         parse_mode='html')

    elif message.text == 'Выслать твиттер аккаунты' and flag_pass:
        doc = open('page_source.html', 'rb')
        bot.send_document(message.chat.id, doc)

    elif message.text == 'Отключить' and flag_pass and stop_flag:
        bot.send_message(message.chat.id, '<b>Бот отключен</b>',
                         parse_mode='html')
        bot.stop_polling()

    elif message.text == 'Отключить' and flag_pass and not stop_flag:
        bot.send_message(message.chat.id, '<b>Остановите бота нажав на кнопку <em>Остановить</em> '
                                          'или дождитесь его остановки</b>',
                         parse_mode='html')

    else:
        bot.send_message(message.chat.id, '<b>Я не понимаю, о чём ты? Пропиши команду <em>/start</em></b>',
                         parse_mode='html')


bot.polling()
