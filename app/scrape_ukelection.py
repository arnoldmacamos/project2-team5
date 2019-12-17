from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Visit UK Election 2019 results in www.bbc.com 
    url = "https://www.bbc.com/news/politics/constituencies"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    #Get all links all constituencies election results page
    constituencies = soup.select(".az-table__row")

    for constituent in constituencies:        
        const_href =  constituent.select_one("a")["href"]
        constituent_name = constituent.select_one("a").text
        nation = constituent.select_one("td").text
        print(f"link to {const_href}")

        browser.visit(f"https://www.bbc.com{const_href}")
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        party_hold =  soup.select_one(".ge2019-constituency-result-headline__text").text    # which party won the constituencies
        voters_count = soup.select_one(".ge2019-constituency-result-turnout__value").text   # total voters 
        con_votes_share = soup.select_one(".ge2019-vote-share__party-title:contains('CON')").parent.parent.select_one(".ge2019-vote-share__value").text                 # conservative votes share
        
        print(f"{constituent_name} {nation} {party_hold} {voters_count} {con_votes_share}")
        

    # Close the browser after scraping
    browser.quit()

    # Return results
    return const_result_hrefs
