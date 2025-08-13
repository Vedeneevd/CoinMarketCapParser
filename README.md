# Crypto Prices Updater

Приложение для автоматического сбора цен криптовалют и записи их в Google Sheets с удобным графическим интерфейсом.

## 📌 Основные возможности

*   📊 Автоматический сбор цен криптовалют с CoinMarketCap API
*   🕒 Ежедневное обновление данных в заданное время
*   📈 Запись данных в Google Sheets
*   🖥️ Простой графический интерфейс для ручного управления
*   📝 Логирование всех операций

## 🛠️ Технологии

*   Python 3.8+
*   CoinMarketCap API
*   Google Sheets API
*   Tkinter для GUI

Пакеты: `requests`, `gspread`, `python-dotenv`, `schedule`

## ⚙️ Установка

Клонируйте репозиторий:

    git clone https://github.com/Vedeneevd/CoinMarketCapParser
    

Перейдите в папку проекта:

    cd ...  
    

Установите зависимости:

    pip install -r requirements.txt  
    

Создайте файл `.env` в корне проекта и заполните его следующими данными:

    API_KEY=your_coinmarketcap_api_key  
    SPREADSHEET_ID=your_google_sheet_id  
    CREDENTIALS_FILE=credentials.json  
    

Получите учетные данные для Google Sheets API: следуйте официальной документации, сохраните файл учетных данных как `credentials.json` в корне проекта.

## 🚀 Использование

Запустите приложение командой:

    CoinMarketParser.py
    

После запуска откроется окно с кнопкой для ручного обновления данных. По умолчанию автоматическое обновление происходит каждый день в 08:00 (можно изменить в коде).

## ⚙️ Конфигурация

Вы можете настроить параметры приложения, изменяя словарь `CONFIG` внутри файла `main.py`:

    CONFIG = {  
        "API_KEY": os.getenv('API_KEY'),  
        "SPREADSHEET_ID": os.getenv('SPREADSHEET_ID'),  
        "TOKENS": ["ARB", "STRK", "ZK", ...],  # список отслеживаемых токенов  
        "CREDENTIALS_FILE": os.getenv('CREDENTIALS_FILE'),  
        "UPDATE_TIME": "08:00",  # время автоматического обновления (24ч формат)  
    }  
    

## 📊 Структура данных в Google Sheets

Приложение создает таблицу со следующей структурой:

| Дата/Время | ARB | STRK | ... | ETH |
| --- | --- | --- | --- | --- |
| 2025-01-01 08:00 | 1.234 | 0.567 | ... | 2500.0 |

## 📜 Логирование

Все операции логируются в файл `crypto_prices.log`:

    2025-01-01 08:00:00,123 - INFO - Данные успешно добавлены: [...] 
    
