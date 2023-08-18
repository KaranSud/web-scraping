import requests
from bs4 import BeautifulSoup
import json

def scrape_website_details(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Scrape meta title & description
        meta_title = soup.find('title').text if soup.find('title') else ''
        meta_description = soup.find('meta', attrs={'name': 'description'})
        meta_description = meta_description['content'] if meta_description else ''
        
        # Scrape total number of links
        total_links = len(soup.find_all('a'))
        
        # Scrape social media links (Twitter & LinkedIn)
        social_links = {
            'twitter': soup.find('a', href=lambda href: href and 'twitter.com' in href),
            'linkedin': soup.find('a', href=lambda href: href and 'linkedin.com' in href)
        }
        social_links = {platform: link['href'] if link else '' for platform, link in social_links.items()}
        
        # Scrape number of times "technology" word is present
        technology_count = soup.text.lower().count('technology')
        
        return {
            'url': url,
            'meta_title': meta_title,
            'meta_description': meta_description,
            'total_links': total_links,
            'social_links': social_links,
            'technology_count': technology_count
        }
    else:
        print(f"Failed to fetch {url}")
        return None

def main():
    websites = [
        "https://www.alfred.tech/",
        "https://www.alianzacorp.mx/",
        "https://www.align.com/",
        "https://www.alignright.tech/",
        "https://www.goadsi.com/",
        "https://www.myalignedit.com/",
        "https://alima.tech/",
        "https://www.alinatechnology.com/",
        "https://www.aliscs.com/",
        "https://www.alithya.com/en"
    ]
    
    scraped_data = []
    for website in websites:
        data = scrape_website_details(website)
        if data:
            scraped_data.append(data)
    
    with open('scraped_data.txt', 'w') as outfile:
        json.dump(scraped_data, outfile, indent=4)
    
    print("Scraping completed. Data saved to 'scraped_data.json'")

if __name__ == "__main__":
    main()
