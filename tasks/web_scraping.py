import requests
from bs4 import BeautifulSoup
import re
import validators
import time
import csv
import argparse
import json
import logging

logging.basicConfig(filename='web_scraping.log', level=logging.ERROR,
                    format='%(asctime)s - %(levelname)s - %(message)s')

def validate_url(url):
    if not validators.url(url):
        return False, "Invalid URL format."
    try:
        response = requests.head(url, timeout=5)
        response.raise_for_status()
        return True, None
    except requests.exceptions.RequestException as e:
        return False, f"URL unreachable: {e}"

def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}" 
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}" 
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def extract_gold_rate(soup):
    try:
        # Update these selectors based on the actual HTML structure
        gold_24k_element = soup.find("span", {"class": "gold24k-class"})  # Example - REPLACE!
        gold_22k_element = soup.find("span", {"class": "gold22k-class"})  # Example - REPLACE!
        date_element = soup.find("div", {"class": "date-class"})  # Example - REPLACE!

        gold_24k = gold_24k_element.text.strip() if gold_24k_element else "N/A"
        gold_22k = gold_22k_element.text.strip() if gold_22k_element else "N/A"
        date = date_element.text.strip() if date_element else "N/A"

        return {"date": date, "24K": gold_24k, "22K": gold_22k}, None

    except AttributeError as e:
        return None, f"Error extracting data. Element not found: {e}"
    except Exception as e:
        return None, f"An unexpected error occurred during extraction: {e}"
def display_data(data, output_format="text"):
    if output_format == "json":
        print(json.dumps(data, indent=4))
    else:
        print("Gold Rates:")
        for key, value in data.items():
            print(f"{key}: {value}")

def scrape_website(url):
    valid, message = validate_url(url)
    if not valid:
        print(f"Error: {message}")
        return None

    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.google.com'  # Optional, but sometimes helpful
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        gold_data, error_message = extract_gold_rate(soup)

        if gold_data:
            time.sleep(2)  # Be polite
            return gold_data
        else:
            logging.error(f"Could not extract gold rate data from {url}. {error_message if error_message else 'Check website structure.'}")
            return None

    except requests.exceptions.RequestException as e:
        logging.error(f"Error fetching URL {url}: {e}")
        return None
    except Exception as e:
        logging.error(f"An unexpected error occurred while scraping {url}: {e}")
        return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scrape gold rates from a website.")
    parser.add_argument("url", help="The URL of the website to scrape.")
    parser.add_argument("-o", "--output", choices=["text", "json"], default="text",
                        help="Output format (text or json).")

    args = parser.parse_args()

    url = args.url
    output_format = args.output

    gold_data = scrape_website(url)

    if gold_data:
        display_data(gold_data, output_format)
    else:
        print("Scraping failed. Check the logs for more details.")