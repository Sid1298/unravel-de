import os
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timezone

SKIFT_URL = "https://skift.com/news/page/"
TIMESTAMP_FILE = "last_scraped.json"


def load_last_scraped_time():
    if os.path.exists(TIMESTAMP_FILE):
        with open(TIMESTAMP_FILE, "r") as f:
            data = json.load(f)
            return datetime.fromisoformat(data["last_scraped"])
    return datetime.min.replace(tzinfo=timezone.utc)


def save_last_scraped_time(latest_time):
    with open(TIMESTAMP_FILE, "w") as f:
        json.dump({"last_scraped": latest_time.isoformat()}, f)


def fetch_page(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.text


def parse_articles(html):
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


def main():
    last_scraped_time = load_last_scraped_time()
    articles = []
    for page_number in range(1, 11):
        html = fetch_page(SKIFT_URL+f'{page_number}')
        articles.extend(parse_articles(html))
    new_articles = [
        a for a in articles if a["publish_timestamp"] > last_scraped_time]
    if not new_articles:
        print("No new articles found.")
        return
    new_articles.sort(key=lambda x: x["publish_timestamp"])
    for article in new_articles:
        print(
            f"[{article['publish_timestamp']}] {article['title']} -> {article['article_link']}")
    latest_time = new_articles[-1]["publish_timestamp"]
    save_last_scraped_time(latest_time)


if __name__ == "__main__":
    main()
