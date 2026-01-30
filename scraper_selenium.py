from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.edge.options import Options
import csv
import json
import time

def scrape_usnews_with_selenium():
    """
    Load existing schools from CSV and visit each to get school website links.
    """
    from selenium.webdriver.edge.options import Options as EdgeOptions
    
    # Load existing schools from CSV
    print("Loading schools from colleges_selenium.csv...")
    schools = []
    try:
        with open('colleges_selenium.csv', 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                schools.append({
                    'rank': int(row['rank']),
                    'name': row['name'],
                    'usnews_link': row['usnews_link'],
                    'school_website': row.get('school_website', None)
                })
        print(f"Loaded {len(schools)} schools from CSV")
    except FileNotFoundError:
        print("Error: colleges_selenium.csv not found!")
        return []
    
    # Setup Edge options
    edge_options = EdgeOptions()
    # edge_options.add_argument('--headless')  # Disable headless to see what's happening
    edge_options.add_argument('--no-sandbox')
    edge_options.add_argument('--disable-dev-shm-usage')
    edge_options.add_argument('--disable-blink-features=AutomationControlled')
    edge_options.add_argument('--log-level=3')  # Suppress console errors
    edge_options.add_argument('--disable-logging')
    edge_options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
    edge_options.add_experimental_option('useAutomationExtension', False)
    
    print(f"Launching Edge browser...")
    
    try:
        driver = webdriver.Edge(options=edge_options)
        
        print(f"\nTotal schools loaded: {len(schools)}")
        
        # Skip saving initial data since it's already in CSV
        # Go directly to visiting each school to get website links
        
        # Now visit each school's page to get the actual school website
        print(f"\n{'='*60}")
        print("Now visiting each school to get website links...")
        print(f"{'='*60}\n")
        
        for idx, school in enumerate(schools, 1):
            try:
                # Check if driver session is still valid
                try:
                    driver.current_url
                except:
                    # Session died, recreate driver
                    print("Browser session died, restarting browser...")
                    try:
                        driver.quit()
                    except:
                        pass
                    
                    options = EdgeOptions()
                    options.add_argument('--headless')
                    options.add_argument('--disable-gpu')
                    options.add_argument('--no-sandbox')
                    options.add_argument('--disable-dev-shm-usage')
                    driver = webdriver.Edge(options=options)
                
                print(f"Visiting {idx}/{len(schools)}: {school['name']}")
                
                try:
                    driver.get(school['usnews_link'])
                except Exception as e:
                    print(f"  → Error loading page")
                    school['school_website'] = 'Error'
                    continue
                
                # Wait for page to load
                time.sleep(3)
                
                # Scroll down to trigger lazy loading of the link element
                try:
                    driver.execute_script("window.scrollTo(0, 600);")
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, 1200);")
                    time.sleep(2)
                except:
                    pass
                
                # Look for element with data-tracking-id="edu_profile_link"
                try:
                    script = """
                    let element = document.querySelector('[data-tracking-id="edu_profile_link"]');
                    if (element) {
                        return element.href || element.getAttribute('href');
                    }
                    return null;
                    """
                    
                    website = driver.execute_script(script)
                    
                    if website:
                        school['school_website'] = website
                        print(f"  → Found: {website}")
                    else:
                        school['school_website'] = 'Not found'
                        print(f"  → Not found")
                        
                except Exception as inner_e:
                    school['school_website'] = 'Not found'
                    print(f"  → Not found")
                    print(f"  → Could not find school website link")
            except Exception as e:
                school['school_website'] = 'Error'
                print(f"  → Error: {str(e)}")
                # Try to continue with next school instead of stopping
                time.sleep(2)
        
        try:
            driver.quit()
        except:
            pass
        
        # Save the updated data with school websites
        print(f"\n{'='*60}")
        print("Saving updated data with school websites...")
        print(f"{'='*60}\n")
        
        return schools
        
    except Exception as e:
        print(f"Error: {e}")
        try:
            driver.quit()
        except:
            pass
        return []


def save_to_csv(schools, filename='colleges_selenium.csv'):
    """Save the scraped data to a CSV file."""
    if not schools:
        print("No data to save.")
        return
    
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['rank', 'name', 'usnews_link', 'school_website']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for school in schools:
            writer.writerow(school)
    
    print(f"Data saved to {filename}")


def save_to_json(schools, filename='colleges_selenium.json'):
    """Save the scraped data to a JSON file."""
    if not schools:
        print("No data to save.")
        return
    
    with open(filename, 'w', encoding='utf-8') as jsonfile:
        json.dump(schools, jsonfile, indent=2, ensure_ascii=False)
    
    print(f"Data saved to {filename}")


def main():
    schools = scrape_usnews_with_selenium()
    
    if schools:
        print(f"\n{'='*60}")
        print(f"Successfully scraped {len(schools)} schools!")
        print(f"{'='*60}\n")
        print("First 5 schools:")
        for school in schools[:5]:
            print(f"  #{school['rank']}: {school['name']}")
            print(f"    US News: {school['usnews_link']}")
            print(f"    School Website: {school['school_website']}")
        
        # Save to both CSV and JSON
        save_to_csv(schools)
        save_to_json(schools)
    else:
        print("No schools found. Please check if Microsoft Edge is installed.")


if __name__ == "__main__":
    main()
