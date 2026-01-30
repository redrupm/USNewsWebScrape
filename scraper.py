import requests
from bs4 import BeautifulSoup
import csv
import json
import time

def scrape_usnews_rankings():
    """
    Scrape US News college rankings to get name, link, and rank for each school.
    """
    url = "https://www.usnews.com/best-colleges/rankings/national-universities"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    print(f"Fetching data from {url}...")
    try:
        response = requests.get(url, headers=headers, timeout=10)
    except requests.exceptions.Timeout:
        print("Error: Request timed out after 10 seconds")
        return []
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []
    
    if response.status_code != 200:
        print(f"Error: Status code {response.status_code}")
        return []
    
    soup = BeautifulSoup(response.content, 'html.parser')
    
    schools = []
    
    print("Parsing HTML...")
    # Try to find the school data - US News often uses specific CSS classes
    # Look for common patterns in college ranking pages
    
    # Method 1: Look for anchor tags with college links
    college_links = soup.find_all('a', href=lambda x: x and '/best-colleges/' in x and '-' in x)
    
    print(f"Found {len(college_links)} potential college links")
    
    for idx, link in enumerate(college_links, 1):
        school_name = link.get_text(strip=True)
        school_link = link.get('href')
        
        # Make sure it's a valid school link (not navigation or other links)
        if school_name and len(school_name) > 3 and not any(x in school_link for x in ['rankings', 'search', 'compare']):
            # Build full URL if needed
            if school_link.startswith('/'):
                school_link = 'https://www.usnews.com' + school_link
            
            schools.append({
                'rank': idx,
                'name': school_name,
                'link': school_link
            })
    
    # Remove duplicates while preserving order
    seen = set()
    unique_schools = []
    for school in schools:
        if school['link'] not in seen:
            seen.add(school['link'])
            unique_schools.append(school)
            print(f"Found #{len(unique_schools)}: {school['name']}")
            
            # Stop at 100 schools
            if len(unique_schools) >= 100:
                break
    
    # Re-number ranks after removing duplicates
    for idx, school in enumerate(unique_schools, 1):
        school['rank'] = idx
    
    return unique_schools


def save_to_csv(schools, filename='colleges.csv'):
    """Save the scraped data to a CSV file."""
    if not schools:
        print("No data to save.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'name', 'link']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for school in schools:
            writer.writerow(school)
    
    print(f"Data saved to {filename}")


def save_to_json(schools, filename='colleges.json'):
    """Save the scraped data to a JSON file."""
    if not schools:
        print("No data to save.")
        return
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(schools, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filename}")


def main():
    schools = scrape_usnews_rankings()
    
    if schools:
        print(f"\nFound {len(schools)} schools")
        print("\nFirst 5 schools:")
        for school in schools[:5]:
            print(f"  #{school['rank']}: {school['name']}")
            print(f"    Link: {school['link']}")
        
        # Save to both CSV and JSON
        save_to_csv(schools)
        save_to_json(schools)
    else:
        print("No schools found. The page structure might have changed or require JavaScript rendering.")
        print("You may need to use Selenium for dynamic content.")


if __name__ == "__main__":
    main()
