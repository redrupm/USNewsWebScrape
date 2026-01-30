import csv

def construct_edu_url(school_name):
    """Try to construct the .edu URL from school name"""
    name = school_name.lower()
    
    # Remove common words
    name = name.replace('university of', '').replace('the ', '').replace(' university', '')
    name = name.replace(' college', '').replace('college of', '')
    name = name.replace(',', '').strip()
    
    # Special cases for well-known universities
    special_cases = {
        'princeton': 'princeton.edu',
        'massachusetts institute of technology': 'mit.edu',
        'harvard': 'harvard.edu',
        'stanford': 'stanford.edu',
        'yale': 'yale.edu',
        'chicago': 'uchicago.edu',
        'duke': 'duke.edu',
        'johns hopkins': 'jhu.edu',
        'northwestern': 'northwestern.edu',
        'pennsylvania': 'upenn.edu',
        'california institute of technology': 'caltech.edu',
        'cornell': 'cornell.edu',
        'brown': 'brown.edu',
        'dartmouth': 'dartmouth.edu',
        'columbia': 'columbia.edu',
        'berkeley': 'berkeley.edu',
        'rice': 'rice.edu',
        'los angeles': 'ucla.edu',
        'vanderbilt': 'vanderbilt.edu',
        'notre dame': 'nd.edu',
        'emory': 'emory.edu',
        'carnegie mellon': 'cmu.edu',
        'georgetown': 'georgetown.edu',
        'michigan': 'umich.edu',
        'southern california': 'usc.edu',
        'virginia': 'virginia.edu',
        'north carolina chapel hill': 'unc.edu',
        'wake forest': 'wfu.edu',
        'new york': 'nyu.edu',
        'tufts': 'tufts.edu',
        'florida': 'ufl.edu',
        'rochester': 'rochester.edu',
        'boston': 'bu.edu',
        'william mary': 'wm.edu',
        'brandeis': 'brandeis.edu',
        'case western reserve': 'case.edu',
        'georgia tech': 'gatech.edu',
        'texas austin': 'utexas.edu',
        'wisconsin madison': 'wisc.edu',
        'tulane': 'tulane.edu',
        'boston college': 'bc.edu',
        'illinois urbana': 'illinois.edu',
        'washington seattle': 'washington.edu',
        'san diego': 'ucsd.edu',
        'davis': 'ucdavis.edu',
        'irvine': 'uci.edu',
        'santa barbara': 'ucsb.edu',
    }
    
    for key, url in special_cases.items():
        if key in name:
            return f'https://www.{url}'
    
    # For remaining schools, take first significant word
    words = name.split()
    if words:
        first_word = words[0]
        return f'https://www.{first_word}.edu'
    
    return 'Unknown'

# Load schools
print("Loading schools from colleges_selenium.csv...")
schools = []
with open('colleges_selenium.csv', 'r', encoding='utf-8') as f:
    reader = csv.DictReader(f)
    for row in reader:
        schools.append({
            'rank': int(row['rank']),
            'name': row['name'],
            'usnews_link': row['usnews_link'],
            'school_website': row.get('school_website', '')
        })

print(f"Loaded {len(schools)} schools\n")

# Add websites
print("Adding .edu URLs...")
for school in schools:
    if not school['school_website'] or school['school_website'] == '':
        url = construct_edu_url(school['name'])
        school['school_website'] = url
        print(f"{school['rank']}. {school['name']}")
        print(f"   → {url}")

# Save back to CSV
print("\nSaving to colleges_selenium.csv...")
with open('colleges_selenium.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['rank', 'name', 'usnews_link', 'school_website'])
    writer.writeheader()
    writer.writerows(schools)

print(f"\nDone! Updated {len(schools)} schools with website URLs.")
