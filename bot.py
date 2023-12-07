import requests
import sys

TOKEN = "TELEGRAM_TOKEN"
chat_id = "CHAT_TOKEN"

message = f"{sys.argv[1]}: {sys.argv[2]}"
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
requests.get(url).json()
