import requests

from data.config import tgbot

BOT_TOKEN = tgbot.BOT_TOKEN


def get_photo_url_by_file_id(file_id: str) -> str:
    r = requests.get(
        f"https://api.telegram.org/bot{BOT_TOKEN}/getFile", params={"file_id": file_id}
    )
    data = r.json()

    file_path = data["result"]["file_path"]

    return f"https://api.telegram.org/file/bot{BOT_TOKEN}/{file_path}"
