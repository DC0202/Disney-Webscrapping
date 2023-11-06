import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.justwatch.com/us/search?q="

def fetch_movie_data(movie_name):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.63 Safari/537.36"
    }
    
    response = requests.get(BASE_URL + movie_name, headers=headers)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage for {movie_name} from JustWatch.")
        return None, None
    
    soup = BeautifulSoup(response.content, 'html.parser')
    disney_link = soup.find('div', class_='buybox-row__offers').find('a')['href']

    driver = webdriver.Chrome()
    driver.get(disney_link)

    try:
        #It will fetch you the Age Certfication for that particular movie.
        element = WebDriverWait(driver, 60).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sc-ccbnFN.jZELRG img"))
        )
        # If you want to fetch the complete HTML Parser, just when we hit the below CSS.selector just print the complete HTML data and load it in html parser.
        # Once data is loaded, fetch particular data by extracting particular data you want.
        rating_img_element = driver.find_element(By.CSS_SELECTOR, ".sc-ccbnFN.jZELRG img")
        rating_img_link = rating_img_element.get_attribute("src")
    except:
        print(f"Failed to load the desired content for {movie_name} from Disney+.")
        driver.quit()
        return None, None

    driver.quit()
    return movie_name, rating_img_link

# Add Movie List name and it will fetch you the Age Certfication for that particular movie.
movie_names = []


# CSV file setup
with open('movie_data1.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Movie Name", "Rating Image Link"])  # Writing headers

    for movie in movie_names:
        movie_name, rating_img_link = fetch_movie_data(movie)
        if movie_name and rating_img_link:
            writer.writerow([movie_name, rating_img_link])
