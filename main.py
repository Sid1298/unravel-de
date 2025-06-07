import sqlite3
from skift_scrape import load_skift_articles, show_latest_skift

SKIFT_URL = "https://skift.com/news/page/"
DB_PATH = "article_source.db"

connection = sqlite3.connect(DB_PATH)
load_skift_articles(connection=connection, url=SKIFT_URL)
for row in show_latest_skift(connection=connection):
    format = f"""Published: [{row[6]}] | Title: {row[1]}
Link to article: {row[2]}
"""
    print(format)
connection.close()


# Phocuswire extraction could not be implemented because 
# - The website has enabled bot protection so direct request.get() calls did not work.
# - As a work-around, implementation was done with selenium.
# - Even with selenium, the output remained same and no data for news articles could be fetched.
