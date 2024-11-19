import unittest
from unittest.mock import MagicMock, patch
import os
import json
import re

# Mocking the Confluence object
class MockConfluence:
    def get_page_id(self, space, title):
        if title == "Existing Page":
            return "12345"  # Mock page ID
        return None  # Simulate a non-existing page

    def get_page_by_id(self, page_id, expand):
        if page_id == "12345":
            return {
                "id": "12345",
                "title": "Existing Page",
                "body": {
                    "storage": {
                        "value": "<p>Page content in HTML</p>",
                        "representation": "storage"
                    }
                },
                "metadata": {
                    "labels": [{"name": "important"}]
                }
            }
        return None  # Simulate a missing page ID


# Import the function to test
from your_script_name import get_page_content_and_save  # Replace `your_script_name` with your file name


class TestWebScraper(unittest.TestCase):
    @patch('your_script_name.confluence', new_callable=MockConfluence)
    def test_get_page_content_and_save_success(self, mock_confluence):
        # Test case for a valid page
        space = "TEST_SPACE"
        title = "Existing Page"

        # Call the function
        filename = get_page_content_and_save(space, title)

        # Check that the file is created
        self.assertTrue(os.path.exists(filename), "JSON file was not created.")

        # Read and validate file content
        with open(filename, "r", encoding="utf-8") as f:
            content = json.load(f)
            self.assertEqual(content["id"], "12345")
            self.assertEqual(content["title"], "Existing Page")
            self.assertIn("body", content)
            self.assertIn("metadata", content)

        # Clean up
        os.remove(filename)

    @patch('your_script_name.confluence', new_callable=MockConfluence)
    def test_get_page_content_and_save_not_found(self, mock_confluence):
        # Test case for a non-existent page
        space = "TEST_SPACE"
        title = "Non-Existent Page"

        # Call the function
        filename = get_page_content_and_save(space, title)

        # Verify the result is None and no file is created
        self.assertIsNone(filename, "Function should return None for non-existent pages.")

    @patch('your_script_name.confluence', new_callable=MockConfluence)
    def test_filename_sanitization(self, mock_confluence):
        # Test case for filename sanitization
        space = "TEST_SPACE"
        title = "Page with Invalid/Characters"

        # Call the function
        filename = get_page_content_and_save(space, title)

        # Verify sanitized filename
        expected_filename = re.sub(r'[^\w\s-]', '', title).replace(' ', '_') + "_content.json"
        self.assertTrue(os.path.exists(expected_filename), "Sanitized filename was not created.")

        # Clean up
        os.remove(expected_filename)


if __name__ == "__main__":
    unittest.main()
