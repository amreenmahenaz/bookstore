if html_tag.name == "table":
    rows = html_tag.find_all("tr")
    markdown_table = []

    # Extract headers from the first row if it contains <th> tags
    headers = [th.get_text(strip=True) for th in rows[0].find_all("th")] if rows else []

    if headers:
        # Add column headers with separator line
        markdown_table.append("| " + " | ".join(headers) + " |")
        markdown_table.append("|" + "|".join(["---"] * len(headers)) + "|")
        
        # Extract each row of the table
        for row in rows[1:]:  # Skip the header row
            cells = [td.get_text(strip=True) for td in row.find_all(["td", "th"])]
            markdown_table.append("| " + " | ".join(cells) + " |")

    # Join all rows with a newline
    return "\n".join(markdown_table)
