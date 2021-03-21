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


def main():
    dotenv.load_dotenv()
    TOKEN = getenv("TOKEN")
    url = input("Введите ссылку для сокращения: ").strip()

    try:
        bitlink = shorten_link(TOKEN, url)
    except requests.exceptions.ConnectionError:
        print("Сайт не отвечает.")
        return
    except requests.exceptions.HTTPError:
        print("Ошибка! Вы ввели неверную ссылку.")
        return


    print(f"Теперь для доступа к {url} Вы можете воспользоваться следующей ссылкой:")
    print(bitlink)


url_user = f"https://api-ssl.bitly.com/v4/user"

if __name__ == "__main__":
    main()