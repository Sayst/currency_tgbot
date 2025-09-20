# 💱 Currency Bot

Currency Bot — это Telegram-бот для конвертации валют в режиме реального времени.  
Он использует библиотеку [`forex-python`](https://pypi.org/project/forex-python/) для получения актуальных курсов валют.  

## 🚀 Возможности
- Конвертация валют по формату: <сумма> <исходная_валюта> <целевая_валюта>

Пример:
100 USD EUR
500 RUB USD
1000 EUR RUB



- 📊 Просмотр актуальных курсов (пример: USD → EUR, EUR → USD)  
- 📋 Список поддерживаемых валют  
- 🆘 Справка по командам  

## 📋 Доступные команды
- `/start` — начать работу с ботом  
- `/help` — справка по использованию  
- `/currencies` — список поддерживаемых валют  
- `/rate` — курс валют (пример USD ↔ EUR)  

## 🔧 Установка и запуск
1. Клонировать репозиторий:
 ```bash
 git clone <https://github.com/Sayst/currency_tgbot.git>
 cd currency-bot

2. Установить зависимости:
pip install -r requirements.txt

3. В файле config.py указать:
token = "ВАШ_TELEGRAM_BOT_TOKEN"
api_key = "ВАШ_API_KEY_ЕСЛИ_НУЖЕН"

4. Запустить бота:
python bot.py


Пользователь: 100 USD EUR
Бот: 💱 Результат конвертации
100.00 USD = 92.50 EUR
📅 Курс на 20.09.2025 15:30
