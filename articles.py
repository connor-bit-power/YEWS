from fastapi import FastAPI
import requests
from bs4 import BeautifulSoup

app = FastAPI()

def get_article_titles(url):
    response = requests.get(url)
    titles_data = []

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        article_containers = soup.select('div.whole-body')
        
        for container in article_containers:
            article_title_tag = container.find('div', class_='bulletin-text')
            article_title = article_title_tag.get_text(strip=True) if article_title_tag else "No title found"
            titles_data.append(article_title)
    else:
        print(f"Failed to retrieve content: {response.status_code}")
    
    return titles_data

@app.get("/get-article-titles/")
async def read_item(url: str):
    titles = get_article_titles(url)
    return {"titles": titles}
