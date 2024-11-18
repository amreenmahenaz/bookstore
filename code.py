from atlassian import Confluence
from bs4 import BeautifulSoup
import json

# Initialize the Confluence API client
confluence = Confluence(
    url='https://your-confluence-instance.atlassian.net',
    username='your_username',
    password='your_api_token'
)

# Function to fetch and parse page content, then save it to JSON
def fetch_and_save_confluence_content(space_key):
    pages = confluence.get_all_pages_from_space(space=space_key, start=0, limit=50, status=None, expand='body.storage')
    
    all_page_data = []
    
    for page in pages:
        page_data = {}
        page_data['page_id'] = page['id']
        page_data['title'] = page['title']
        
        # Get HTML content of the page
        html_content = page['body']['storage']['value']
        
        # Parse HTML content using BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')
        
        # Extract all tags and their attributes
        tags_data = []
        for tag in soup.find_all(True):
            tags_data.append({
                'tag': tag.name,
                'attributes': tag.attrs,
                'text': tag.get_text(strip=True)
            })
        
        # Add parsed data to the page data
        page_data['tags'] = tags_data
        all_page_data.append(page_data)
    
    # Save all data to a JSON file
    output_file = "confluence_page_data.json"
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(all_page_data, f, ensure_ascii=False, indent=4)

    print(f"Data saved successfully to {output_file}")

# Define the Confluence space key and save content
space_key = 'YOUR_SPACE_KEY'
fetch_and_save_confluence_content(space_key)
