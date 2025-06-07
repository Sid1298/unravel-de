import sqlite3
from typing import List


def get_latest_article_timestamp(connection: sqlite3.Connection, data_source:str):
    cursor = connection.cursor()
    query = f"SELECT MAX(publish_timestamp) FROM {data_source}_articles;"
    cursor.execute(query)
    result = cursor.fetchone()
    return result[0]


def show_latest_articles(connection: sqlite3.Connection, data_source:str, num_rows: int):
    cursor = connection.cursor()
    query = f"SELECT * FROM {data_source}_articles ORDER BY publish_timestamp DESC LIMIT {num_rows};"
    cursor.execute(query)
    result = cursor.fetchall()
    return result


def create_skift_table(connection: sqlite3.Connection):
    cursor = connection.cursor()
    query = """
        CREATE TABLE IF NOT EXISTS skift_articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            article_link TEXT UNIQUE,
            slug TEXT,
            author TEXT,
            author_link TEXT,
            publish_timestamp TEXT,
            niche TEXT
        );
    """
    cursor.execute(query)
    connection.commit()


def insert_skift_articles(connection: sqlite3.Connection, articles: List[dict]):
    insert_counter = 0
    cursor = connection.cursor()

    latest_timestamp = get_latest_article_timestamp(connection, 'skift')

    if latest_timestamp:
        from datetime import datetime
        latest_timestamp = datetime.fromisoformat(latest_timestamp)

    if len(articles)==0:
        return 0

    new_articles = [article for article in articles if (
        not latest_timestamp or article["publish_timestamp"] > latest_timestamp)]

    if not new_articles:
        print("No new articles to be loaded into database.")
        return 0

    for article in new_articles:
        query = """INSERT OR IGNORE INTO skift_articles 
        (title, article_link, slug, author, author_link, publish_timestamp, niche)
        VALUES (?, ?, ?, ?, ?, ?, ?)"""
        data = (
            article["title"],
            article["article_link"],
            article["slug"],
            article["author"],
            article["author_link"],
            article["publish_timestamp"].isoformat(),
            article["niche"]
        )
        try:
            cursor.execute(query, data)
            insert_counter += 1
        except Exception as e:
            print(f"Error in inserting data into table... Exception {e}")

    connection.commit()
    return insert_counter
