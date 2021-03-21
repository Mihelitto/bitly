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
    url = "https://github.com/Mihelitto"

    try:
        print(shorten_link(TOKEN, url))
    except requests.exceptions.ConnectionError:
        print("Сайт не отвечает.")
    except requests.exceptions.HTTPError:
        print("Страница не найдена.")


url_user = f"https://api-ssl.bitly.com/v4/user"

if __name__ == "__main__":
    main()