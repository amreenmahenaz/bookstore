from bs4 import BeautifulSoup
import requests

# Fetch the HTML content (Replace with your actual URL or HTML string)
url = "https://www.geeksforgeeks.org/time-complexity-and-space-complexity/#"  # Replace with the target URL
response = requests.get(url)
response.raise_for_status()

# Parse HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")

# Find the table - this selects the first table on the page; adjust if necessary
table = soup.find("table")

# Convert HTML table to Markdown
def table_to_markdown(table):
    rows = table.find_all("tr")
    markdown_table = []

    # Extract headers
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")]
    markdown_table.append("| " + " | ".join(headers) + " |")
    markdown_table.append("| " + " | ".join(["---"] * len(headers)) + " |")

    # Extract rows
    for row in rows[1:]:
        cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
        markdown_table.append("| " + " | ".join(cells) + " |")

    return "\n".join(markdown_table)

# Convert table to markdown format
markdown_content = table_to_markdown(table)

# Save to Markdown file
with open("table_content.md", "w", encoding="utf-8") as f:
    f.write(markdown_content)

print("Markdown table saved successfully:\n")
print(markdown_content)  # Print to verify
