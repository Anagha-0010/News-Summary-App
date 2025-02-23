from fastapi import FastAPI, HTTPException
import requests
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
news_api_key= os.getenv("news_api_key") 

app = FastAPI()

class NewsQuery(BaseModel):
    query: str

def fetch_news(query: str):
    url = f"https://newsapi.org/v2/everything?q={query}&apiKey={news_api_key}"
    response = requests.get(url)
    data = response.json()

    if "articles" not in data or not data["articles"]:
        return []  # No articles found

    articles = []
    for article in data["articles"]:
        content = article.get("content")
        if content and "[+" not in content:  # Filtering out incomplete content
            articles.append(content)

    print(f"Fetched {len(articles)} valid articles.")  # Debugging log
    return articles

from transformers import pipeline
summarizer = pipeline("summarization")

def summarize_article(article_text):
    return summarizer(article_text, max_length=150, min_length=30, do_sample=False)[0]["summary_text"]


@app.post("/summarize/")
async def summarize_news(request: NewsQuery):
    try:
        articles = fetch_news(request.query)
        if not articles:
            return {"message": "No valid articles found"}

        summaries = [summarize_article(article) for article in articles[:3]]
        return {"summaries": summaries}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
