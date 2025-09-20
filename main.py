from config import token
import telebot
import logging
from forex_python.converter import CurrencyRates
from datetime import datetime

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(token)
c = CurrencyRates()

# Популярные валюты с эмодзи
CURRENCIES = {
    'USD': '🇺🇸 Доллар США',
    'EUR': '🇪🇺 Евро', 
    'RUB': '🇷🇺 Российский рубль',
    'GBP': '🇬🇧 Британский фунт',
    'JPY': '🇯🇵 Японская иена',
    'CNY': '🇨🇳 Китайский юань',
    'CAD': '🇨🇦 Канадский доллар',
    'AUD': '🇦🇺 Австралийский доллар',
    'CHF': '🇨🇭 Швейцарский франк',
    'SEK': '🇸🇪 Шведская крона',
    'NOK': '🇳🇴 Норвежская крона',
    'DKK': '🇩🇰 Датская крона',
    'PLN': '🇵🇱 Польский злотый',
    'CZK': '🇨🇿 Чешская крона',
    'HUF': '🇭🇺 Венгерский форинт',
    'TRY': '🇹🇷 Турецкая лира',
    'BRL': '🇧🇷 Бразильский реал',
    'INR': '🇮🇳 Индийская рупия',
    'KRW': '🇰🇷 Южнокорейская вона',
    'SGD': '🇸🇬 Сингапурский доллар'
}

def get_currency_list():
    """Получить список валют для отображения"""
    currency_text = "💱 <b>Доступные валюты:</b>\n\n"
    for code, name in CURRENCIES.items():
        currency_text += f"<code>{code}</code> - {name}\n"
    return currency_text

def format_currency(amount, currency):
    """Форматировать сумму валюты"""
    if currency in ('JPY', 'KRW'):
        return f"{amount:,.0f}"
    return f"{amount:,.2f}"

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = """
🏦 <b>Добро пожаловать в Currency Bot!</b>

Я помогу вам конвертировать валюты по актуальному курсу.

<b>Как использовать:</b>
• Введите сумму и валюты в формате: <code>100 USD EUR</code>
• Или используйте команды ниже

<b>Доступные команды:</b>
/currencies - список валют
/rate - курс валют
/help - помощь

<b>Примеры:</b>
<code>100 USD EUR</code>
<code>500 RUB USD</code>
<code>1000 EUR RUB</code>
"""
    bot.send_message(message.chat.id, welcome_text, parse_mode='HTML')

@bot.message_handler(commands=['help'])
def help_command(message):
    help_text = """
📖 <b>Справка по использованию</b>

<b>Формат ввода:</b>
<code>сумма исходная_валюта целевая_валюта</code>

<b>Примеры:</b>
• <code>100 USD EUR</code> - конвертировать 100 долларов в евро
• <code>500 RUB USD</code> - конвертировать 500 рублей в доллары
• <code>1000 EUR RUB</code> - конвертировать 1000 евро в рубли

<b>Команды:</b>
/start - начать работу
/currencies - список валют
/rate - курс валют
/help - эта справка

<b>Поддерживаемые валюты:</b>
USD, EUR, RUB, GBP, JPY, CNY, CAD, AUD, CHF и другие
"""
    bot.send_message(message.chat.id, help_text, parse_mode='HTML')

@bot.message_handler(commands=['currencies'])
def currencies_command(message):
    bot.send_message(message.chat.id, get_currency_list(), parse_mode='HTML')

@bot.message_handler(commands=['rate'])
def rate_command(message):
    try:
        # Получаем курс USD к EUR как пример
        rate = c.get_rate('USD', 'EUR')
        rate_text = f"""
📊 <b>Актуальный курс валют</b>

🇺🇸 USD → 🇪🇺 EUR: <code>{rate:.4f}</code>
🇪🇺 EUR → 🇺🇸 USD: <code>{1/rate:.4f}</code>

<i>Курсы обновляются ежедневно</i>
"""
        bot.send_message(message.chat.id, rate_text, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Ошибка при получении курса: {e}")
        bot.send_message(message.chat.id, "❌ Ошибка при получении курса валют")

@bot.message_handler(func=lambda message: True)
def convert_currency(message):
    try:
        text = message.text.strip()
        parts = text.split()
        
        if len(parts) != 3:
            error_text = """
❌ <b>Неверный формат!</b>

Используйте формат: <code>сумма исходная_валюта целевая_валюта</code>

<b>Примеры:</b>
<code>100 USD EUR</code>
<code>500 RUB USD</code>
<code>1000 EUR RUB</code>

Используйте /currencies для просмотра доступных валют
"""
            bot.reply_to(message, error_text, parse_mode='HTML')
            return

        amount = float(parts[0])
        from_currency = parts[1].upper()
        to_currency = parts[2].upper()

        # Проверяем, что валюты поддерживаются
        unsupported = [cur for cur in (from_currency, to_currency) if cur not in CURRENCIES]
        if unsupported:
            error_text = f"""
❌ <b>Неподдерживаемая валюта!</b>

Валюта <code>{', '.join(unsupported)}</code> не поддерживается.

Используйте /currencies для просмотра доступных валют
"""
            bot.reply_to(message, error_text, parse_mode='HTML')
            return

        if amount <= 0:
            bot.reply_to(message, "❌ Сумма должна быть больше нуля!")
            return

        # Выполняем конвертацию
        converted_amount = c.convert(from_currency, to_currency, amount)
        
        # Форматируем результат
        formatted_amount = format_currency(amount, from_currency)
        formatted_converted = format_currency(converted_amount, to_currency)
        
        result_text = f"""
💱 <b>Результат конвертации</b>

{formatted_amount} {from_currency} = <b>{formatted_converted} {to_currency}</b>

📅 <i>Курс на {datetime.now().strftime('%d.%m.%Y %H:%M')}</i>
"""
        bot.reply_to(message, result_text, parse_mode='HTML')
        
    except ValueError:
        error_text = """
❌ <b>Ошибка ввода!</b>

Сумма должна быть числом.

<b>Правильный формат:</b>
<code>100 USD EUR</code>
<code>500.50 RUB USD</code>
"""
        bot.reply_to(message, error_text, parse_mode='HTML')
    except Exception as e:
        logger.error(f"Ошибка при конвертации: {e}")
        error_text = """
❌ <b>Ошибка конвертации!</b>

Возможные причины:
• Проблемы с интернет-соединением
• Временная недоступность сервиса
• Неверные коды валют

Попробуйте еще раз или используйте /help для справки
"""
        bot.reply_to(message, error_text, parse_mode='HTML')

if __name__ == "__main__":
    try:
        logger.info("Запуск бота конвертации валют...")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
