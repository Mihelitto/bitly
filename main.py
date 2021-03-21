from os import getenv
import pprint
import json
import requests
import dotenv

dotenv.load_dotenv()
TOKEN = getenv("TOKEN")

url = f"https://api-ssl.bitly.com/v4/user"
url_bitlink = "https://api-ssl.bitly.com/v4/bitlinks"
headers = {"Authorization": f"Bearer {TOKEN}",}
data = json.dumps({"long_url": "https://github.com/Mihelitto"})

response = requests.post(url_bitlink, headers=headers, data=data)
response.raise_for_status()

info = json.loads(response.text)

print(response.headers)
pprint.pprint(response.json())
pprint.pprint(info)
print(info["link"])