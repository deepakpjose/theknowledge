import requests
from bs4 import BeautifulSoup
import os

# URL of the page to scrape
base_url = "https://www.theguardian.com/football/series/theknowledge?page="
file_name = f"theknowledge_pages/guardian_knowledge.txt"
contents = dict()
last_page = 58

# Create a directory to store the downloaded pages
if not os.path.exists("theknowledge_pages"):
    os.makedirs("theknowledge_pages")

def get_contents_by_class(url, class_name=["dcr-s3ycb2","dcr-13fd1ms"]):
    content_list = []

    # Send a GET request to the webpage
    response = requests.get(url)
    if response.status_code != 200:
        return content_list
    
    # Parse the page with BeautifulSoup
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find all elements with the specified class
    elements = soup.find_all(class_=class_name)
    
    # Collect the text content of each element in a list
    content_list = [element.get_text(strip=True) for element in elements]

    # Find the <time> element with the publication date
    time_element = soup.find('time', {'itemprop': 'datePublished'})

    if time_element and 'datetime' in time_element.attrs:
        publication_date = time_element['datetime']
        print(f'Publication date: {publication_date}')
        content_list.insert(0, time_element.get_text())
        print(content_list[0])
    else:
        print('Publication date not found.')

    return content_list


def download_page(url, page_num, iteration):
    content_list = get_contents_by_class(url)
    contents[page_num + iteration] = content_list
    print(f"Page {page_num} {iteration} saved successfully!")

def write_html_body():
    with open(file_name, 'w', encoding='utf-8') as file:
        for key, value in contents.items():
            file.write(f"{key}: {value}\n")

# Function to download and save the page content
def download_page_list(url, page_num):
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

                download_page(link, page_num * iteration, iteration) 
    else:
        print(f"Failed to retrieve page {page_num}.")

# Function to get the next page link (assuming 'next' pagination is used)
def get_next_page(base_url, page_num):
    next_url = base_url + str(page_num)
    next_page = requests.get(next_url)
    if next_page.status_code == 200 and page_num <= 1:
        print("next_url:", next_url)
        return next_url

    return None

# Start scraping
def scrape_all_pages():
    page_num = 1
    url = base_url + str(page_num)
    while url:
        print(f"Downloading page {page_num}...")
        response = requests.get(url)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            download_page_list(url, page_num)
            page_num += 1
            url = get_next_page(base_url, page_num)
        else:
            print(f"Failed to retrieve page {page_num}.")
            break

# Run the scraping function
scrape_all_pages()
write_html_body()
