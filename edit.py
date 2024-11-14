from markdownify import markdownify as md

def convert_to_md(html_tag):
    """
    Utility Function to Convert HTML to Markdown, with specific handling for tables
    that includes row and column numbers, and a line separator after each row.
    """
    # Check if the tag is a table
    if html_tag.name == "table":
        rows = html_tag.find_all("tr")
        markdown_table = []

        # Extract headers from the first row if it contains <th> tags
        headers = [f"{th.get_text(strip=True)}" for th in rows[0].find_all("th")]
        
        # Add row and column labels to headers
        if headers:
            headers_with_index = ["Row\\Col"] + [f"Col {i+1}: {header}" for i, header in enumerate(headers)]
            markdown_table.append("| " + " | ".join(headers_with_index) + " |")
            markdown_table.append("| " + " | ".join(["---"] * len(headers_with_index)) + " |")

        # Extract each row of the table
        for row_index, row in enumerate(rows[1:], start=1):
            cells = [f"Row {row_index}"]
            cells.extend([f"{td.get_text(strip=True)}" for td in row.find_all(["td", "th"])])
            markdown_table.append("| " + " | ".join(cells) + " |")
            # Add separator line below each row
            markdown_table.append("| " + " | ".join(["---"] * len(cells)) + " |")

        return "\n".join(markdown_table)
    
    # For other tags, use markdownify
    elif html_tag.name in 'h1 h2 h3 h4 h5 h6 li p pre em'.split():
        return str(md(str(html_tag), strip=['img']))

    return ""

# Example usage:
# Assuming `html_tag` is a BeautifulSoup element containing your HTML content.
# This function will convert <table> tags to Markdown tables and other tags using markdownify.
