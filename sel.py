from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from markdownify import markdownify as md
import time

# Set up Selenium WebDriver
service = Service("path/to/chromedriver")  # Replace with your ChromeDriver path
driver = webdriver.Chrome(service=service)

# URL to scrape
url = "https://example.com"  # Replace with the target URL
driver.get(url)
time.sleep(3)  # Wait for the page to fully load

# Get the body content of the page
body_html = driver.find_element(By.TAG_NAME, "body").get_attribute("innerHTML")

# Parse the HTML content with BeautifulSoup
soup = BeautifulSoup(body_html, "html.parser")

# Initialize Markdown output
markdown_content = ""

# Iterate through all tags in the body and convert each to Markdown
for tag in soup.find_all(True):  # True finds all tags
    tag_name = tag.name
    tag_content = str(tag)
    tag_markdown = md(tag_content)
    
    # Append the tag's Markdown content with a header indicating the tag
    markdown_content += f"\n### <{tag_name}>\n\n{tag_markdown}\n"

# Print or save the Markdown content
print(markdown_content)

# Optionally save to a Markdown file
with open("output.md", "w", encoding="utf-8") as file:
    file.write(markdown_content)

# Close the WebDriver
driver.quit()
