import requests
from bs4 import BeautifulSoup
import csv
import logging
from datetime import datetime
from database import save_web_scraping_task

def web_scraping_task(keyword, user_details):
    search_url = f"https://www.google.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    
    try:
        response = requests.get(search_url, headers=headers)
        response.raise_for_status()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch search results - Reason: {str(e)}")
        return
    
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    
    for g in soup.find_all('div', class_='tF2Cxc'):
        title = g.find('h3').text if g.find('h3') else 'No Title'
        link = g.find('a')['href'] if g.find('a') else 'No Link'
        snippet = g.find('div', class_='VwiC3b').text if g.find('div', class_='VwiC3b') else 'No Snippet'
        results.append({"title": title, "link": link, "snippet": snippet})
    
    # Save to CSV
    csv_file = f"web_scraping_{datetime.now().strftime('%Y%m%d%H%M%S')}.csv"
    with open(csv_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["title", "link", "snippet"])
        writer.writeheader()
        writer.writerows(results)
    
    # Save data to MongoDB
    save_web_scraping_task(keyword, results, user_details)
    
    print(f"✅ Web scraping completed for keyword: {keyword}. Data saved to MongoDB and CSV: {csv_file}")