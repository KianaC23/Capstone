import os
import pdb
import requests
import csv
from bs4 import BeautifulSoup

#list of sites to scrape
GENRE_SITE_LIST = [
        "https://www.blackclassicmovies.com/movies-database/action/",
        "https://www.blackclassicmovies.com/movies-database/blaxploitation/",
        "https://www.blackclassicmovies.com/movies-database/comedy-movies/",
        "https://www.blackclassicmovies.com/movies-database/drama-movies-a-l/",
        "https://www.blackclassicmovies.com/movies-database/drama-movies-m-z/",
        "https://www.blackclassicmovies.com/movies-database/family-movies/",
        "https://www.blackclassicmovies.com/movies-database/romance-movies/",
        ]

def persist_html():
    # TODO: Write actual html to a file instead of recrawling web
    pass
    
# write results to new csv file
def persist_results(url, results):
    name = url.split("/")[-2]
    path_to_script = os.path.dirname(os.path.abspath(__file__))
    filename = os.path.join(path_to_script, f"{name}.csv")
    print(f"Writing results to {filename}")
    with open(filename, 'w') as f:
        write = csv.writer(f)
        fields = ["Title", "Year", "Stars", "Director"]
        write.writerow(fields)
        write.writerows(results)
        

def crawl_site():
    for site in GENRE_SITE_LIST:
        results = crawl_movie_genre(site)
        persist_results(site, results)

def crawl_movie_genre(base_url):
    # Crawl the initial genre page
    result_list = []
    results, has_next = parse_page(base_url)
    if results:
        result_list.extend(results)

    index = 2 # we start iterating on the second page
    while has_next and index < 100: # quick backup exit condition
        url = f"{base_url}/page/{index}"
        results, has_next = parse_page(url) # parse page and see if there is another
        if results:
            result_list.extend(results)
        index = index + 1

    return result_list
#parse webpage
def parse_page(url):
    print(f"Parsing url {url}")
    #use this header so site doesn't think you're a bot
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:55.0) Gecko/20100101 Firefox/55.0',
    }
    results = []
    has_next = False
    r = requests.get(url, headers=headers)
    if r.status_code == 200:
        print(f"Successfully called URL")
        html_text = r.text
        soup = BeautifulSoup(html_text, 'html.parser')
        #find the data you want in the html
        mydivs = soup.find_all("div", {"class": "film-data-box"})
        print(f"Found {len(mydivs)} results")
        for div in mydivs:
            title = div.find_all("h3")[0].text.strip()
            year, stars, director = [res.text for res in div.find_all("td")[1::2]]
            print(f"Appending {title, year, stars, director} to results list")
            results.append((title, year, stars, director))

        has_next = len(soup.find_all("a", {"class": "next page-numbers"})) >= 1
    print(results)
    return (results, has_next)

crawl_site()
