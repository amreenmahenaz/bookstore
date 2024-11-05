for link in soup.find_all("a", href=True):
    link_text = link.get_text(strip=True)
    link_url = urljoin(url, link["href"])  # Convert relative URLs to absolute URLs
    all_links.append((link_text, link_url))
