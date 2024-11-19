from markdownify import markdownify as md

# Function to get page ID by title
def get_page_id_by_title(space_key, page_title):
    # Fetch page information by title
    page = confluence.get_page_by_title(space=space_key, title=page_title)
    if page:
        page_id = page['id']
        print(f"Page Title: {page_title}, Page ID: {page_id}")
        return page_id
    else:
        print(f"Page with title '{page_title}' not found in space '{space_key}'.")
        return None

# Function to get page content and save as Markdown
def get_page_content_and_save_as_markdown(space, title):
    page_id = get_page_id_by_title(space, title)
    if page_id:
        # Fetch page content by ID
        page_content = confluence.get_page_by_id(page_id, expand="body.storage,metadata.labels")
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

# Example Usage
if __name__ == "__main__":
    # Fetch and save a specific Confluence page as a Markdown file
    space_key = "RUNBOOKS"
    page_title = "13c Oracle Grid Control Operational Runbook"

    markdown_file = get_page_content_and_save_as_markdown(space_key, page_title)

    if markdown_file:
        print(f"Markdown file created: {markdown_file}")
