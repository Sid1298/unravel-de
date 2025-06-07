import sqlite3
import database
import requests
from bs4 import BeautifulSoup
from datetime import datetime


def fetch_page(url:str):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_articles(html:str):
    soup = BeautifulSoup(html, "lxml")
    article_elements = soup.find_all("article")
    articles = []
    for article in article_elements:
        try:
            niche_tag = article.select_one(
                "div.c-tease__content.is-layout-flow")
            title_tag = article.select_one("h3.c-tease__title a")
            slug_tag = article.select_one("div.c-tease__excerpt")
            author_tag = article.select_one(
                "div.c-tease__byline.has-tertiary-font-family a")
            time_tag = article.select_one("time.o-pretty-time-relative")
            publish_timestamp = None
            if time_tag and time_tag.has_attr("datetime"):
                try:
                    publish_timestamp = datetime.fromisoformat(
                        time_tag["datetime"])
                except ValueError:
                    print(f"Invalid datetime format: {time_tag['datetime']}")
            data = {
                "niche": niche_tag.get_text(strip=True) if niche_tag else None,
                "title": title_tag.get_text(strip=True) if title_tag else None,
                "article_link": title_tag["href"] if title_tag and title_tag.has_attr("href") else None,
                "slug": slug_tag.get_text(strip=True) if slug_tag else None,
                "author": author_tag.get_text(strip=True) if author_tag else None,
                "author_link": author_tag["href"] if author_tag and author_tag.has_attr("href") else None,
                "publish_timestamp": publish_timestamp
            }
            articles.append(data)
        except Exception as e:
            print(f"Error parsing article: {e}")
            continue
    return articles


def fetch_latest_skift(skift_url: str):
    articles = []
    for page_number in range(1, 11):
        html = fetch_page(skift_url+f'{page_number}')
        articles.extend(parse_articles(html))
    if len(articles) == 0:
        print("No new articles found...")
    return articles


def load_skift_articles(connection: sqlite3.Connection):
    articles = fetch_latest_skift()
    num_loaded_rows = database.insert_skift_articles(connection, articles)
    return num_loaded_rows


def show_latest_skift(connection: sqlite3.Connection):
    return database.show_latest_articles(connection, "skift", 5)
