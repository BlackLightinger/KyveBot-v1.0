import traceback
from twitter_creation import twc
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import telebot
from auth_data import telebot_token, bot_pass
from pyvirtualdisplay import Display


bot = telebot.TeleBot(telebot_token)
bot_auth = False
running = False
stop_flag = True
driver = None


def check(running):
    return running


def main():
    global running
    global stop_flag
    while check(running):
        display = Display(visible=0, size=(800, 600))
        display.start()

        options = Options()
        options.add_argument("start-maximized")
        options.add_extension('proxy.zip')
        options.headless = True
        global driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        twc(driver)

        display.stop()
    driver.quit()
    stop_flag = True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '<b>Привет, введи пароль для работы с ботом:</b>',
                     parse_mode='html')

    @bot.message_handler(content_types=['text'])
    def auth(password):
        if password.text != bot_pass:
            bot.send_message(message.chat.id, '<b>Я не понимаю, о чём ты?</b>',
                             parse_mode='html')
        else:
            global bot_auth
            bot_auth = True
            bot.send_message(message.chat.id, '<b>Авторизация прошла успешно, можно запускать бота!</b>',
                             parse_mode='html')


@bot.message_handler(commands=['run'])
def  run(message):
    global running
    global stop_flag
    if not bot_auth:
        bot.send_message(message.chat.id, '<b>Вы не авторизованы, введите команду <em>/start</em></b>',
                         parse_mode='html')
    elif stop_flag:
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
            driver.quit()
            print(traceback.format_exc())
    else:
        bot.send_message(message.chat.id, '<b>Бот уже работает!</b>',
                         parse_mode='html')

@bot.message_handler(commands=['stop'])
def stop(message):
    global running
    if not bot_auth:
        bot.send_message(message.chat.id, '<b>Вы не авторизованы, введите команду <em>/start</em></b>',
                         parse_mode='html')
    elif running:
        running = False
        bot.send_message(message.chat.id, '<b>Бот будет остановлен после завершения цикла!</b>',
                         parse_mode='html')
    else:
        bot.send_message(message.chat.id, '<b>Бот не запущен</b>',
                         parse_mode='html')


@bot.message_handler(commands=['exit'])
def ex(message):
    if stop_flag:
        bot.send_message(message.chat.id, '<b>Бот отключен</b>',
                         parse_mode='html')
        bot.stop_polling()
    else:
        bot.send_message(message.chat.id, '<b>Остановите бота командой <em>/stop</em> или дождитесь его остановки</b>',
                         parse_mode='html')


bot.polling()
