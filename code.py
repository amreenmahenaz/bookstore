import requests
from bs4 import BeautifulSoup

# URL of the page to scrape
url = "https://example.com"  # Replace with the actual URL of the page

# Fetch the page content
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find and print all links under each category
sections = soup.find_all("div", class_="your-section-class")  # Replace with the actual class or identifier of each section

for section in sections:
    # Find the section title (like Channels, Marketing, etc.)
    section_title = section.find("h2").get_text(strip=True) if section.find("h2") else "No Title"
    print(f"Section: {section_title}")

    # Find all links within this section
    links = section.find_all("a", href=True)
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = link["href"]
        print(f"  - {link_text}: {link_url}")
