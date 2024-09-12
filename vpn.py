import json
from telegram import Update
from telegram.ext import Application, CommandHandler, CallbackContext


# Функция для загрузки ключей из файла
def load_keys(filename='keys.txt'):
    with open(filename, 'r') as file:
        return [line.strip() for line in file.readlines()]


# Функция для сохранения оставшихся ключей в файл
def save_keys(keys, filename='keys.txt'):
    with open(filename, 'w') as file:
        for key in keys:
            file.write(f"{key}\n")


# Функция для загрузки словаря пользователей из файла
def load_user_keys(filename='user_keys.json'):
    try:
        with open(filename, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


# Функция для сохранения словаря пользователей в файл
def save_user_keys(user_keys, filename='user_keys.json'):
    with open(filename, 'w') as file:
        json.dump(user_keys, file)


# Загрузка ключей и словаря пользователей
keys = load_keys()
user_keys = load_user_keys()


# Функция, которая будет вызываться при команде /start
async def start(update: Update, context: CallbackContext) -> None:
    user_first_name = update.message.from_user.first_name
    greeting_text = (
        f"Привет, {user_first_name}!\n"
        "Добро пожаловать в VPN бот.\n\n"
        "Этот бот помогает вам получить доступ к VPN. "
        "Для получения VPN ключа используйте команду /getkey.\n"
        "Если у вас возникнут вопросы, используйте команду /help."
    )
    await update.message.reply_text(greeting_text)


# Функция для выдачи ключа
async def get_key(update: Update, context: CallbackContext) -> None:
    user_id = update.message.from_user.id

    if user_id in user_keys:
        await update.message.reply_text(f"Вы уже получили ключ: {user_keys[user_id]}")
    elif keys:
        key = keys.pop(0)
        user_keys[user_id] = key
        save_keys(keys)
        save_user_keys(user_keys)
        await update.message.reply_text(f"Твой VPN ключ: {key}")
    else:
        await update.message.reply_text('Извините, но все ключи уже выданы.')


# Функция, которая будет вызываться при команде /help
async def help_command(update: Update, context: CallbackContext) -> None:
    help_text = (
        "Инструкция по подключению к Outline VPN:\n\n"
        "1. Скачайте и установите приложение Outline на ваше устройство:\n"
        "   - [Android](https://play.google.com/store/apps/details?id=org.outline.android.client)\n"
        "   - [iOS](https://apps.apple.com/us/app/outline-app/id1356177741)\n"
        "   - [Windows](https://getoutline.org/)\n"
        "   - [macOS](https://getoutline.org/)\n"
        "   - [Linux](https://getoutline.org/)\n\n"
        "2. Запустите приложение и нажмите 'Добавить сервер'.\n\n"
        "3. Вставьте полученный от бота ключ.\n\n"
        "4. Подключитесь к серверу и наслаждайтесь безопасным интернетом!"
    )
    await update.message.reply_text(help_text)


def main() -> None:
    # Вставьте сюда ваш токен, который вы получили от BotFather
    application = Application.builder().token("").build()

    # Обработчики команд
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("getkey", get_key))
    application.add_handler(CommandHandler("help", help_command))

    # Запуск бота
    application.run_polling()


if __name__ == '__main__':
    main()