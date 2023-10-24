import requests
from bs4 import BeautifulSoup

def scrape_distinct_urls(url, existing_urls=None):
    try:
        # Send an HTTP GET request to the URL
        response = requests.get(url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content of the page
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find the div elements with class 'detailProductTile__contentRow'
            divs = soup.find_all('div', class_='detailProductTile__contentRow')

            # Initialize a set to store distinct URLs
            distinct_urls = set()

            # Iterate through the div elements and find URLs in their href attributes
            for div in divs:
                a_tags = div.find_all('a')
                for a in a_tags:
                    href = a.get('href')
                    if href:
                        distinct_urls.add(href)

            # Check if there are existing URLs from previous runs
            if existing_urls is not None:
                distinct_urls.update(existing_urls)

            return distinct_urls
        else:
            print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return existing_urls


def output_to_file(existing_urls): 
    output_file = "saatva_product_urls.txt"
    with open(output_file, "w") as file:
        # Iterate through the URLs in the set
        for url in existing_urls:
            # Append a "/" character to each URL
            url_with_slash = "https://www.saatva.com" + url 
            
            # Write the modified URL to the file, followed by a newline
            file.write( url_with_slash  +",")
        for url in urls:
            file.write(url+",")
    print(f"Modified URLs have been saved to {output_file}")

   

urls = ['https://www.saatva.com/mattresses', 'https://www.saatva.com/furniture', 'https://www.saatva.com/bedding', 'https://www.saatva.com/gifts','https://www.saatva.com/sale' ]
existing_urls = set()
for url in urls: 
    existing_urls = scrape_distinct_urls(url, existing_urls)

output_to_file(existing_urls)

