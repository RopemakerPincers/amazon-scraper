import requests
from bs4 import BeautifulSoup
import csv
import time
import random

def scrape_amazon_discounts(search_query, pages=1):
    """
    Scrapes Amazon search results for a given query and extracts discounted products.
    """
    base_url = "https://www.amazon.com/s"
    
    # Crucial: Amazon blocks requests without proper headers
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36',
        'Accept-Language': 'en-US, en;q=0.5',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Connection': 'keep-alive'
    }

    results = []

    for page in range(1, pages + 1):
        print(f"Scraping page {page} for query: '{search_query}'...")
        
        params = {
            'k': search_query,
            'page': page
        }
        
        response = requests.get(base_url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"Failed to retrieve page {page}. Status code: {response.status_code}")
            print("Amazon might be blocking the request (CAPTCHA/503).")
            break
            
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Amazon search result items are typically housed within these specific div structures
        items = soup.find_all('div', {'data-component-type': 's-search-result'})
        
        for item in items:
            # 1. Extract Title
            title_element = item.find('h2', class_='a-size-mini')
            title = title_element.text.strip() if title_element else "N/A"
            
            # 2. Extract Link
            link_element = item.find('a', class_='a-link-normal')
            link = "https://www.amazon.com" + link_element['href'] if link_element and 'href' in link_element.attrs else "N/A"
            
            # 3. Extract Current Price
            price_element = item.find('span', class_='a-price')
            current_price = price_element.find('span', class_='a-offscreen').text.strip() if price_element else None
            
            # 4. Extract Original Price (usually crossed out)
            original_price_element = item.find('span', class_='a-text-price')
            original_price = original_price_element.find('span', class_='a-offscreen').text.strip() if original_price_element else None
            
            # Filter logic: We only want items that have both a current price and an original price (indicating a discount)
            if current_price and original_price and current_price != original_price:
                results.append({
                    'Title': title,
                    'Current_Price': current_price,
                    'Original_Price': original_price,
                    'Link': link
                })
        
        # Polite scraping: sleep between page requests to avoid immediate bans
        sleep_time = random.uniform(2.5, 5.5)
        print(f"Sleeping for {sleep_time:.2f} seconds...")
        time.sleep(sleep_time)

    return results

def save_to_csv(data, filename='amazon_discounts.csv'):
    """Saves the scraped data to a CSV file."""
    if not data:
        print("No discounted data to save.")
        return
        
    keys = data[0].keys()
    with open(filename, 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(data)
    print(f"Successfully saved {len(data)} discounted items to {filename}")

if __name__ == "__main__":
    # Example usage: Searching for laptops and scraping the first 2 pages
    search_term = "gaming laptop"
    scraped_data = scrape_amazon_discounts(search_query=search_term, pages=2)
    
    if scraped_data:
        save_to_csv(scraped_data, filename='discounted_laptops.csv')
