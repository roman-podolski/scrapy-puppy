import re
from app.logs.api_logger import logger
from pydantic import BaseModel

from app.conf.configuration import config
import requests


class MediumConfig(BaseModel):
    host: str
    key: str


def get_article_file(art_id: str) -> str:
    medium_conf = MediumConfig(**config['medium'])

    url = f"https://medium2.p.rapidapi.com/article/{art_id}/markdown"

    headers = {
        "X-RapidAPI-Key": medium_conf.key,
        "X-RapidAPI-Host": medium_conf.host
    }

    response = requests.get(url, headers=headers)
    data = response.json()['markdown']

    chars_to_remove = ["{", "}", "'", "/n"]
    for char in chars_to_remove:
        data = data.replace(char, "")

    pattern = r"/article/([\w-]+)/"

    match = re.search(pattern, url)
    file_name = f"/Users/romanpodolski/Documents/GitHub/scrapy-puppy/app/medium/articles/{match.group(1)}.md"

    try:
        with open(file_name, "x") as f:
            f.write(data)
        logger.info(f"File {file_name} was created")
        return file_name
    except Exception as e:
        logger.error(f"There is problem with writing file {file_name}."
                     f"Error: {e}")

get_article_file('419a8b5e5e2')