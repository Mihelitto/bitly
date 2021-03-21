from os import getenv
import pprint
import json
import requests
import dotenv

dotenv.load_dotenv()
TOKEN = getenv("TOKEN")

url = f"https://api-ssl.bitly.com/v4/user"
headers = {"Authorization": f"Bearer {TOKEN}",}

response = requests.get(url, headers=headers)

user_info = json.loads(response.text)

print(response.headers)
pprint.pprint(user_info)