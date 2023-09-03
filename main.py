import requests
from bs4 import BeautifulSoup
import json
import pandas as pd

url: str = "https://quotes.toscrape.com"

head: dict = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

def get_quotes(url:str):
    res = requests.get(url, headers=head)
    if res.status_code == 200:
        soup: BeautifulSoup = BeautifulSoup(res.text, "html.parser")

        # proses scrape
        contents = soup.find_all("div", attrs={"class": "quote"})
        quotes_list: list = []

        for content in contents:
            quote = content.find("span", attrs={"class": "text"}).text.strip()
            author = content.find("small", attrs={"class": "author"}).text.strip()

            # url detail, bisa langsung karena tdk terikat dengan tag diatasnya
            author_details = content.find("a")["href"]
            data_dict: dict = {
                "quote": quote,
                "quotes by": author,
                "author detail": url + author_details, # di tambah url, agar bisa jadi link
            }
            quotes_list.append(data_dict)

        # proses pengolahan data
        with open("quotes.json", "w+") as f:
            json.dump(quotes_list, f)
        print("Data generate 50%")
        return quotes_list

def get_detail(detail_url: str):
    res = requests.get(detail_url, headers=head)
    if res.status_code == 200:
        soup = BeautifulSoup(res.text, "html.parser")

        # proses scraping
        author_title = soup.find("h3", attrs={"class": "author-title"}).text.strip()
        born = soup.find("span", attrs={"class": "author-born-date"}).text.strip()
        location = soup.find("span", attrs={"class": "author-born-location"}).text.strip()
        description = soup.find("div", attrs={"class": "author-description"}).text.strip()

        # mapping data
        data_dict: dict = {
            "author": author_title,
            "born": born,
            "born location": location,
            "description": description,
        }

        return data_dict

def generate_format(filename: str, results: list):
    df = pd.DataFrame(results)
    if ".csv" or ".xlsx" not in filename:
        df.to_csv(filename + ".csv", index=False)
        df.to_excel(filename + ".xlsx", index=False)

    print("Data generated complete")

def crawling():
    results: list[dict[str, str]] = []

    quotes: list = get_quotes(url=url)
    for quote in quotes:
        detail = get_detail(detail_url=quote["author detail"])

        # merger 2 dictionary
        final_result: dict = {**quote, **detail}

        results.append(final_result)

    # olah data
    generate_format(results=results, filename="reports")

if __name__ == "__main__":
    crawling()

"""
https://requests.readthedocs.io/en/latest/
https://www.crummy.com/software/BeautifulSoup/bs4/doc/
"""