import os

import requests
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import threading
import schedule
import time
import logging
import dotenv


dotenv.load_dotenv()

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('crypto_prices.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Конфигурация
CONFIG = {
    "API_KEY": os.getenv('API_KEY'),  # Замените на реальный ключ
    "SPREADSHEET_ID": os.getenv('SPREADSHEET_ID'),
    "TOKENS": ["ARB", "STRK", "ZK", "W", "WLD", "NOT", "XCH", "TON", "USTC", "ZRO", "OP", "ETH", "APT", "NEAR"],
    "CREDENTIALS_FILE": os.getenv('CREDENTIALS_FILE'),
    "UPDATE_TIME": "08:00",
}


def setup_google_sheets():
    """Инициализация подключения к Google Sheets"""
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        creds = ServiceAccountCredentials.from_json_keyfile_name(
            CONFIG["CREDENTIALS_FILE"], scope)
        client = gspread.authorize(creds)
        return client.open_by_key(CONFIG["SPREADSHEET_ID"]).sheet1
    except Exception as e:
        logger.error(f"Ошибка подключения к Google Sheets: {e}")
        return None


def get_crypto_prices():
    """Получение текущих цен криптовалют"""
    try:
        url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
        headers = {
            "Accepts": "application/json",
            "X-CMC_PRO_API_KEY": CONFIG["API_KEY"]
        }
        params = {
            "symbol": ",".join(CONFIG["TOKENS"]),
            "convert": "USD"
        }

        logger.info("Запрос данных от CoinMarketCap API...")
        response = requests.get(url, headers=headers, params=params, timeout=10)

        if response.status_code != 200:
            error_msg = f"API Error: {response.status_code} - {response.text}"
            logger.error(error_msg)
            return None

        data = response.json()

        # Проверка на ошибки в ответе API
        if 'data' not in data:
            logger.error(f"Неожиданный формат ответа: {data}")
            return None

        prices = {}
        for symbol in CONFIG["TOKENS"]:
            try:
                price = data["data"][symbol]["quote"]["USD"]["price"]
                prices[symbol] = round(price, 4)
                logger.debug(f"{symbol}: ${price:.4f}")
            except KeyError:
                logger.warning(f"Токен {symbol} не найден в ответе API")
                prices[symbol] = "N/A"

        return prices

    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка соединения: {e}")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)

    return None


def update_spreadsheet():
    """Основная функция обновления таблицы"""
    sheet = setup_google_sheets()
    if not sheet:
        return False

    prices = get_crypto_prices()
    if not prices:
        return False

    try:
        today = datetime.now().strftime("%Y-%m-%d %H:%M")
        row_data = [today] + [prices.get(symbol, "N/A") for symbol in CONFIG["TOKENS"]]

        sheet.append_row(row_data)
        logger.info(f"Данные успешно добавлены: {row_data}")
        return True
    except Exception as e:
        logger.error(f"Ошибка записи в таблицу: {e}")
        return False


def manual_update():
    """Обработчик ручного обновления"""
    if update_spreadsheet():
        messagebox.showinfo("Успех", "Данные успешно обновлены!")
    else:
        messagebox.showerror("Ошибка", "Не удалось обновить данные. Проверьте логи.")


def auto_update_job():
    """Фоновая задача для автоматического обновления"""
    while True:
        schedule.run_pending()
        time.sleep(60)


def create_gui():
    """Создание графического интерфейса"""
    root = tk.Tk()
    root.title("Crypto Prices Updater")
    root.geometry("350x180")

    # Стилизация
    root.configure(bg="#f0f0f0")
    font = ("Arial", 10)

    # Виджеты
    frame = tk.Frame(root, bg="#f0f0f0")
    frame.pack(pady=20)

    label = tk.Label(
        frame,
        text="Обновление цен криптовалют",
        bg="#f0f0f0",
        font=("Arial", 12, "bold")
    )
    label.pack(pady=10)

    button = tk.Button(
        frame,
        text="Обновить сейчас",
        command=manual_update,
        bg="#4CAF50",
        fg="white",
        font=font,
        padx=20,
        pady=8,
        relief=tk.FLAT
    )
    button.pack(pady=15)

    status_label = tk.Label(
        root,
        text=f"Автообновление каждый день в {CONFIG['UPDATE_TIME']}",
        bg="#f0f0f0",
        font=font
    )
    status_label.pack(side=tk.BOTTOM, pady=10)

    return root


def main():
    """Основная функция"""
    # Настройка автоматического обновления
    schedule.every().day.at(CONFIG["UPDATE_TIME"]).do(update_spreadsheet)

    # Запуск фонового потока
    threading.Thread(target=auto_update_job, daemon=True).start()

    # Запуск GUI
    root = create_gui()
    root.mainloop()


if __name__ == "__main__":
    logger.info("Запуск приложения...")
    main()