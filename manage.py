from flask import Flask, jsonify

app = Flask(__name__)

# import class for scrape
from scraper import Crawler, url

# route
@app.route("/")
def index():
    scrape = Crawler(url=url)
    data_dict: dict = {
        "message": scrape.crawling(),
    }
    return  jsonify(data_dict)

if __name__ == "__main__":
    app.run(debug=True)