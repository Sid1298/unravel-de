# unravel-de
This is a repository for the interview process in Unravel Tech. 
This code is intended to fetch latest news articles from [Skift](https://skift.com/news/) and [PhocusWire](https://www.phocuswire.com/Latest-News) to aggregate the fetched articles into one database using SQLite. 
___
# Steps to run
1. Install all required packages from requirements.txt using
```sh
pip install -r requirements.txt
```
2. You can use python to run the main.py file directly in your terminal.
```sh
python main.py
```
3. `article_source.db` will be created on completion of the run.
___
## Heads up
- Phocuswire uses bot protection due to which news articles could not be fetched by directly using requests library in Python. As a work around, implementation was tried with selenium to mock browser behaviour but still data could not be fetched from Phocuswire. 
