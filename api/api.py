#YEWS API
import os
import json
from fastapi import FastAPI
from pydantic import BaseModel
import requests
from bs4 import BeautifulSoup

app = FastAPI()

class UrlData(BaseModel):
    url: str

@app.post("/titlesPlusText")
async def read_titles_plus_text(url_data: UrlData):
    response = requests.get(url_data.url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        title_divs = soup.select('div[data-w-id] > div.bulletin-text')
        titles = [title_div.get_text(strip=True) for title_div in title_divs]
        return {"titles": titles}
    else:
        return {"error": f"Failed to retrieve content: {response.status_code}"}
