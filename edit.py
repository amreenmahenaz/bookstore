import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# Base URL without the hash fragment
base_url = "https://wm3dr.ms.com/pub/content/wm3dr/basepage/the-training-group/3d-desktop-navigation.html"

# List of hash fragments for each section
hash_fragments = [
    "#cif3searchin3d",
    "#cif23dnavigation",
    # Add more hash fragments here as needed
]

# Iterate over each fragment, request the content, and parse it
for fragment in hash_fragments:
    # Construct the full URL with the hash fragment
    url = base_url + fragment

    # Send a GET request to the base URL (hash fragments are ignored by the server)
    response = requests.get(base_url)
    response.raise_for_status()  # Check for HTTP errors

    # Parse the HTML with BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Find all links in this section
    links = soup.find_all("a", href=True)

    print(f"Links for section {fragment}:")
    for link in links:
        link_text = link.get_text(strip=True)
        link_url = urljoin(base_url, link["href"])  # Convert relative URLs to absolute
        print(f"  - {link_text}: {link_url}")
    print("\n" + "-" * 40 + "\n")
