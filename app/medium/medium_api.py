import re
from app.logs.api_logger import logger
from pydantic import BaseModel
import os
from app.conf.configuration import config
import requests
import markdown2
import pdfkit



class MediumConfig(BaseModel):
    host: str
    key: str

def md_to_pdf(filename: str) -> str:

    mode = "r"

    with open(filename, mode) as file:
        markdown_text = file.read()

    html_text = markdown2.markdown(markdown_text)
    config = pdfkit.configuration(wkhtmltopdf="/path/to/wkhtmltopdf.exe")
    output = filename.replace("articles", "pdf_articles").replace(".md", ".pdf")
    pdfkit.from_string(html_text, output, configuration=config)
    return output

def get_article_file(medium_url: str) -> str:
    medium_conf = MediumConfig(**config['medium'])

    url_parts = medium_url.split('/')

    last_part = url_parts[-1]
    identifier = last_part.split('-')[-1]
    logger.info(f"Identifier: {identifier}")
    url = f"https://medium2.p.rapidapi.com/article/{identifier}/markdown"

    headers = {
        "X-RapidAPI-Key": medium_conf.key,
        "X-RapidAPI-Host": medium_conf.host
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()['markdown']

    chars_to_remove = ["{", "}", "'", "/n"]
    for char in chars_to_remove:
        data = data.replace(char, "")

    pattern = r"/article/([\w-]+)/"

    match = re.search(pattern, url)
    file_name = f"/Users/romanpodolski/Documents/GitHub/scrapy-puppy/app/medium/articles/{match.group(1)}.md"

    # pdf_file_name = md_to_pdf(file_name)

    if os.path.isfile(file_name):
        logger.info(f"File {file_name} already exists")
        return file_name
    try:
        with open(file_name, "x") as f:
            f.write(data)
        logger.info(f"File {file_name} was created")
        return file_name

    except Exception as e:
        logger.error(f"There is problem with writing file {file_name}."
                     f"Error: {e}")

