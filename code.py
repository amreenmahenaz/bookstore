import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md
from urllib.parse import urlparse
import os

# URL of the page to scrape
url = "https://www.geeksforgeeks.org/time-complexity-and-space-complexity/#"

# Send a GET request to fetch the page content
response = requests.get(url)
response.raise_for_status()  # Check for HTTP errors

# Parse the page content with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Extract the main content section
content_div = soup.find("div", class_="entry-content")

# Function to convert HTML table to Markdown table
def convert_table_to_markdown(table):
    headers = []
    rows = []

    # Extract headers
    header_row = table.find("tr")
    if header_row:
        headers = [th.get_text(strip=True) for th in header_row.find_all("th")]
    
    # Extract rows
    for row in table.find_all("tr")[1:]:  # Skip the header row
        rows.append([td.get_text(strip=True) for td in row.find_all("td")])

    # Build Markdown table
    md_table = "| " + " | ".join(headers) + " |\n"
    md_table += "| " + " | ".join(["---"] * len(headers)) + " |\n"
    for row in rows:
        md_table += "| " + " | ".join(row) + " |\n"
    
    return md_table

# Find and convert tables in the content to Markdown format
for table in content_div.find_all("table"):
    markdown_table = convert_table_to_markdown(table)
    table.replace_with(BeautifulSoup(markdown_table, "html.parser"))

# Convert the entire content to Markdown
markdown_content = md(str(content_div))

# Save to a Markdown file
output_filename = "geeksforgeeks_time_space_complexity.md"
with open(output_filename, "w", encoding="utf-8") as f:
    f.write(markdown_content)

print(f"Content saved to {output_filename}")
