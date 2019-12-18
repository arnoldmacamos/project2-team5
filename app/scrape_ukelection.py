from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re


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
    
    #list of constituency election results
    election_results = []     
    
    i=0 #for testing
    for constituent in constituencies: 
        
        #bbc election result by constituency
        bbc_er_href =  constituent.select_one("a")["href"]        
       
        ons_code = bbc_er_href.split("/")[-1]
       
        constituency_name = constituent.select_one("a").text
        
        print(f"link to {bbc_er_href}")

        browser.visit(f"https://www.bbc.com{bbc_er_href}")
        time.sleep(1)
        html = browser.html
        soup = bs(html, "html.parser")
        
        probrexit_voteshare = 0
        
        party_voteshares = soup.select(f".ge2019-vote-share__party-title")
        

        for party_voteshare in party_voteshares:                 
            party_code = party_voteshare.text
            txt_votes_share = re.sub("[^0-9\.]","",party_voteshare.parent.parent.select_one(".ge2019-vote-share__value").text ) # conservative votes share
            votes_share = float(txt_votes_share)/100.0
        
            result = {
                "ons_code": ons_code,
                "constituency_name": constituency_name,
                "party_code":  party_code,            
                "votes_share": votes_share,
                "year": 2019
            }            
            print(result)
        
            election_results.append(result)
            
        i = i + 1
        
        if(i == 5):
            break
            
                
    # Close the browser after scraping
    browser.quit()

    # Return results
    return election_results
