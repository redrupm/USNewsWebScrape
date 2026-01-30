# USNewsWebScrape

A web scraper to extract college rankings data from US News & World Report.

## Features

- Scrapes college name, rank, and link from US News National Universities rankings
- Two implementations:
  - `scraper.py`: Basic scraper using requests and BeautifulSoup
  - `scraper_selenium.py`: Advanced scraper using Selenium for dynamic content
- Exports data to both CSV and JSON formats

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. For Selenium scraper, you'll need Chrome WebDriver:
```bash
pip install webdriver-manager
```

## Usage

### Basic Scraper (requests + BeautifulSoup)
```bash
python scraper.py
```
C:\Users\redrupm\AppData\Local\Python\bin\python.exe scaper_selenium.py
### Selenium Scraper (for dynamic content)
```bash
python scraper_selenium.py
```

## Output

Both scrapers will create:
- `colleges.csv` / `colleges_selenium.csv`: CSV file with columns: rank, name, link
- `colleges.json` / `colleges_selenium.json`: JSON file with the same data

## Notes

- The basic scraper may not capture all schools if the content is dynamically loaded
- The Selenium scraper handles dynamic content and "Load More" buttons
- US News may have rate limiting or anti-scraping measures, so use responsibly