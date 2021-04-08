from os import getenv
import requests
import dotenv
from urllib.parse import urlparse


def shorten_link(token, url):
    bitlink_creating_url = "https://api-ssl.bitly.com/v4/bitlinks"
    headers = {"Authorization": f"Bearer {token}", }
    bitlink_payload = {"long_url": url}

    response = requests.post(bitlink_creating_url, headers=headers, json=bitlink_payload)
    response.raise_for_status()

    bitlink_properties = response.json()
    return bitlink_properties["link"]


def count_clicks(token, bitlink):
    total_clicks_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    headers = {"Authorization": f"Bearer {token}", }
    params = {"unit": "day", "units": "-1"}

    response = requests.get(total_clicks_url, headers=headers, params=params)
    response.raise_for_status()

    bitlink_total_clicks_info = response.json()
    return bitlink_total_clicks_info["total_clicks"]


def check_bitlink(token, bitlink):
    bitlink_info_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}"
    headers = {"Authorization": f"Bearer {token}", }
    response = requests.get(bitlink_info_url, headers=headers)
    return response.ok


def main():
    dotenv.load_dotenv()
    token = getenv("BITLY_ACCESS_TOKEN")
    url = input("Введите ссылку: ").strip()
    parser = urlparse(url)
    short_url = f"{parser.netloc}{parser.path}"

    try:
        bitlink_exist = check_bitlink(token, short_url)
        if bitlink_exist:
            total_clicks = count_clicks(token, short_url)
            print(f"По ссылке {short_url} перешли {total_clicks} раз(а).")
        else:
            bitlink = shorten_link(token, url)
            print(f"Теперь для доступа к {url} Вы можете воспользоваться следующей ссылкой:\n{bitlink}")
    except requests.exceptions.ConnectionError:
        print("Сайт не отвечает.")
    except requests.exceptions.HTTPError:
        print("Ошибка! Вы ввели неверную ссылку.")


if __name__ == "__main__":
    main()
