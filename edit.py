link_section = soup.find_all("div", class_="complexindexflex")

# Extract all links within the section
links = []
for section in link_section:
    for a_tag in section.find_all("a", href=True):
        link_url = a_tag['href']
        link_text = a_tag.get_text(strip=True)
        # If URL is relative, add base URL
        if not link_url.startswith("http"):
            link_url = "https://wm3dr.ms.com" + link_url
        links.append((link_text, link_url))
