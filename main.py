from os import getenv
import requests
import dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    url_bitlinks = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": f"Bearer {token}", }
    data = {"long_url": url}

    response = requests.post(url_bitlinks, headers=headers, json=data)
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


def get_bitlink(token, bitlink):
    url_bitlinks = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {"Authorization": f"Bearer {token}", }
    response = requests.get(url_bitlinks, headers=headers)
    return response.ok


def main():
    dotenv.load_dotenv()
    token = getenv("BITLY_ACCESS_TOKEN")
    url = input("Введите ссылку: ").strip()
    parser = urlparse(url)
    if parser.netloc == "bit.ly":
        url = parser.netloc + parser.path

    try:
        bitlink_exist = get_bitlink(token, url)
        if bitlink_exist:
            total_clicks = count_clicks(token, url)
            print(f"По ссылке {url} перешли {total_clicks} раз(а).")
        else:
            bitlink = shorten_link(token, url)
            print(f"Теперь для доступа к {url} Вы можете воспользоваться следующей ссылкой:\n{bitlink}")
    except requests.exceptions.ConnectionError:
        print("Сайт не отвечает.")
        return
    except requests.exceptions.HTTPError:
        print("Ошибка! Вы ввели неверную ссылку.")
        return


if __name__ == "__main__":
    main()
