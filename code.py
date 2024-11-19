from markdownify import markdownify as md
import json
import re
import os


def get_page_content_and_save_as_markdown(space, title):
    # Get the page ID based on the space and title
    page_id = confluence.get_page_id(space, title)
    if page_id:
        # Fetch the page content using the page ID
        page_content = confluence.get_page_by_id(
            page_id,
            expand="body.storage,metadata.labels"  # Expand parameters for detailed content
        )
        
        # Extract HTML content
        html_content = page_content['body']['storage']['value']
        
        # Convert HTML to Markdown
        markdown_content = md(html_content, heading_style="ATX")
        
        # Generate a sanitized filename based on the title
        sanitized_title = re.sub(r'[^\w\s-]', '', title).replace(' ', '_')
        markdown_filename = f"{sanitized_title}_content.md"
        
        # Save the Markdown content to a file
        with open(markdown_filename, "w", encoding="utf-8") as f:
            f.write(markdown_content)
        
        print(f"Markdown file saved to: {markdown_filename}")
        return markdown_filename
    else:
        print(f"Page '{title}' not found in space '{space}'")
        return None


# Example usage
space = "YOUR_SPACE_KEY"
title = "YOUR_PAGE_TITLE"
markdown_file = get_page_content_and_save_as_markdown(space, title)

if markdown_file:
    print(f"Markdown file created: {markdown_file}")
