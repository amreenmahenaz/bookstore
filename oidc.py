from atlassian import Confluence

# Initialize the Confluence API client
confluence = Confluence(
    url='https://your-confluence-instance.atlassian.net',
    username='your_username',
    password='your_api_token'
)

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

# Example usage
space_key = 'YOUR_SPACE_KEY'  # Replace with your Confluence space key
page_title = 'YOUR_PAGE_TITLE'  # Replace with the title of the page
page_id = get_page_id_by_title(space_key, page_title)

if page_id:
    print(f"The Page ID for '{page_title}' is: {page_id}")
