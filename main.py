from os import getenv
import pprint
import json
import requests
import dotenv


def shorten_link(token, url):
    url_bitlinks = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": f"Bearer {token}", }
    data = json.dumps({"long_url": url})

    response = requests.post(url_bitlinks, headers=headers, data=data)
    response.raise_for_status()

    info = response.json()
    return info["link"]


def count_clicks(token, bitlink):
    url_clicks = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {"Authorization": f"Bearer {token}", }
    params = {"unit": "day", "units": "-1"}

    response = requests.get(url_clicks, headers=headers, params=params)
    response.raise_for_status()

    info = response.json()
    return info["total_clicks"]


def main():
    dotenv.load_dotenv()
    TOKEN = getenv("TOKEN")
    # url = input("Введите ссылку для сокращения: ").strip()
    url = input("Введите ссылку, чтобы узнать количество кликов по ней: ").strip()

    try:
        # bitlink = shorten_link(TOKEN, url)
        total_clicks = count_clicks(TOKEN, url)
    except requests.exceptions.ConnectionError:
        print("Сайт не отвечает.")
        return
    except requests.exceptions.HTTPError:
        print("Ошибка! Вы ввели неверную ссылку.")
        return

    print(f"По ссылке {url} перешли {total_clicks} раз(а).")
    # print(f"Теперь для доступа к {url} Вы можете воспользоваться следующей ссылкой:")
    # print(bitlink)


url_user = f"https://api-ssl.bitly.com/v4/user"

if __name__ == "__main__":
    main()