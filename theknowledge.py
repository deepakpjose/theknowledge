import requests
from bs4 import BeautifulSoup
import os

# URL of the page to scrape
base_url = "https://www.theguardian.com/football/series/theknowledge"

# Create a directory to store the downloaded pages
if not os.path.exists("theknowledge_pages"):
    os.makedirs("theknowledge_pages")

# Function to download and save the page content
def download_page(url, page_num):
    response = requests.get(url)
    
    if response.status_code == 200:
        # Parse the page content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        #print(soup)

        # Find the article content (change selector as needed)
        divs = soup.find_all('div', {'class': 'dcr-f9aim1'})
        for iteration,div in enumerate(divs): 
            if div:
                print('div')
                print(div)
                a_href = div.find('a')


            if a_href:
                print('a_href')
                print(a_href)
                url = a_href.get('href')
                if url:
                    link = "https://www.theguardian.com" + url
                    print("url")
                    print(link)

            if link:
                content = requests.get(link)
                if content.status_code != 200:
                    print("status_code:", content.status_code)
                    continue

                # Clean the content to text and save it
                article_link = content.get_text(separator="\n", strip=True)
                file_name = f"theknowledge_pages/page_{iteration}.txt"
                with open(file_name, 'w', encoding='utf-8') as file:
                    file.write(article_text)
                print(f"Page {page_num} saved successfully!")
            else:
                print(f"Couldn't find the article content on page {page_num}.")
    else:
        print(f"Failed to retrieve page {page_num}.")

# Function to get the next page link (assuming 'next' pagination is used)
def get_next_page(soup):
    next_button = soup.find('a', {'rel': 'next'})
    if next_button:
        return next_button['href']
    return None

# Start scraping
def scrape_all_pages():
    page_num = 1
    url = base_url
    while url:
        print(f"Downloading page {page_num}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_page(url, page_num)
            url = get_next_page(soup)
            page_num += 1
        else:
            print(f"Failed to retrieve page {page_num}.")
            break

# Run the scraping function
scrape_all_pages()

