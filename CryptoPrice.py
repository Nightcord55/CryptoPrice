import requests
from colorama import init, Fore, Style
from pyfiglet import Figlet
import time
import sys


# Инициализация colorama
init(autoreset=True)

# Создаем ASCII-арт логотипа с шрифтом slant
f = Figlet(font='slant')
logo_text = f.renderText('CryptoPrice')

# Выводим логотип голубым цветом
print(f"{Fore.CYAN}{logo_text}")


import sys
import time
from colorama import Fore

def loading_animation(duration=5):
    spinner = ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
    end_time = time.time() + duration
    idx = 0
    max_length = len("Загрузочка " + max(spinner, key=len))
    while time.time() < end_time:
        message = f"{Fore.CYAN}// Загрузка цен криптовалюты {spinner[idx % len(spinner)]}"
        # Записываем сообщение
        sys.stdout.write("\r" + message)
        # Очищаем остаток строки, если новая строка короче предыдущей
        sys.stdout.write(" " * (max_length - len(message)))
        sys.stdout.flush()
        time.sleep(0.2)
        idx += 1
    # Очистка строки после завершения
    sys.stdout.write("\r" + " " * max_length + "\r")
    sys.stdout.flush()

loading_animation(5)



# Цвета для оформления
DARK_PINK = Fore.MAGENTA  # Темно-розовый цвет
HEADER_COLOR = Fore.YELLOW  # Цвет заголовков
PRICE_COLOR = Fore.WHITE  # Цвет цен


def get_crypto_price(ids):
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {
        'ids': ','.join(ids),
        'vs_currencies': 'usd'
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"{DARK_PINK}Ошибка при получении данных о крипте: {e}{Style.RESET_ALL}")
        return None


def get_usd_to_rub():
    url = 'https://www.cbr-xml-daily.ru/daily_json.js'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        rate = data['Valute']['USD']['Value']
        return rate
    except requests.RequestException as e:
        print(f"{DARK_PINK}Ошибка при получении курса рубля: {e}{Style.RESET_ALL}")
        return None


def main():
    crypto_ids = {
        'BTC': 'bitcoin',
        'ETHEREUM': 'ethereum'
    }

    # Выводим заголовок без рамки и эмодзи
    print(f"{Fore.CYAN}// Текущие цены криптовалют")

    data = get_crypto_price(list(crypto_ids.values()))
    usd_to_rub_rate = get_usd_to_rub()

    if data and usd_to_rub_rate:
        for symbol, id in crypto_ids.items():
            price_usd = data.get(id, {}).get('usd', None)
            if price_usd is not None:
                price_rub = price_usd * usd_to_rub_rate
                # В одной строке выводим цену в USD и RUB с префиксом //
                print(f"{Fore.CYAN}// {symbol}: {PRICE_COLOR}${price_usd:.2f} // RUB: {price_rub:.2f}")
            else:
                print(f"{Fore.CYAN}// {symbol}: {Fore.RED}Данные недоступны")
    else:
        print(f"{Fore.RED}// Не удалось получить все необходимые данные.")

    pass

print("\033[90mМеня можно поддержать и купить мне кофейка, и потом клянусь сделаю динамическое обновление <3\033[0m")

if __name__ == "__main__":
    main()