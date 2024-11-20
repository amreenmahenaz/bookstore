import os
import json
from atlassian import Confluence
from markdownify import markdownify as md

# Fetch credentials securely from environment variables
username = os.getenv("CONFLUENCE_USERNAME")
password = os.getenv("CONFLUENCE_PASSWORD")
base_url = "https://confluence.corp.etradegrp.com"

# Initialize the Confluence API client
confluence = Confluence(
    url=base_url,
    username=username,
    password=password
)

# Function to fetch all pages and save as Markdown files
def fetch_all_pages_as_markdown(space_key, output_dir="o/p"):
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Fetch all pages in the space
    pages = confluence.get_all_pages_from_space(
        space=space_key,
        start=0,
        limit=100,
        status=None,
        expand="body.storage",
        content_type="page"
    )
    
    for page in pages:
        page_id = page['id']
        title = page['title']
        html_content = page['body']['storage']['value']
        
        # Convert HTML to Markdown (preserving tables)
        markdown_content = md(html_content, heading_style="ATX")
        
        # Generate a sanitized filename based on the title
        sanitized_title = "".join(c for c in title if c.isalnum() or c in (" ", "_", "-")).replace(" ", "_")
        markdown_filename = os.path.join(output_dir, f"{sanitized_title}.md")
        
        # Save the Markdown content to a file
        with open(markdown_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
            print(f"Saved page '{title}' as Markdown to {markdown_filename}")

# Example usage
if __name__ == "__main__":
    space_key = "YOUR_SPACE_KEY"  # Replace with your Confluence space key
    fetch_all_pages_as_markdown(space_key)
