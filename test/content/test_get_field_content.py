import unittest

from app.lib.content import get_field_content


class TestGetFieldContent(unittest.TestCase):

    def setUp(self):
        # Test content with a structure matching content.yaml
        self.test_content = {
            "forms": {
                "fields": {
                    "first_name": {
                        "label": "First name",
                        "messages": {
                            "required": "The service person's first name is required"
                        },
                    },
                    "last_name": {
                        "label": "Last name",
                        "messages": {
                            "required": "The service person's last name is required"
                        },
                    },
                    "requester_country": {
                        "label": "Country",
                        "prompt_to_select": "Select a country",
                        "countries": ["United Kingdom", "United States", "Canada"],
                    },
                }
            }
        }

    def test_get_full_field_content(self):
        """Test retrieving the entire content for a field"""
        expected = {
            "label": "First name",
            "messages": {"required": "The service person's first name is required"},
        }
        result = get_field_content(self.test_content, "first_name")
        self.assertEqual(result, expected)

    def test_get_specific_content_key(self):
        """Test retrieving a specific content key from a field"""
        result = get_field_content(self.test_content, "last_name", "label")
        self.assertEqual(result, "Last name")

    def test_get_nested_content_key(self):
        """Test retrieving a nested content key from a field"""
        result = get_field_content(self.test_content, "first_name", "messages")[
            "required"
        ]
        self.assertEqual(result, "The service person's first name is required")

    def test_missing_content_key(self):
        """Test requesting a content key that doesn't exist"""
        result = get_field_content(self.test_content, "first_name", "placeholder")
        self.assertIsNone(result)

    def test_missing_field(self):
        """Test requesting a field that doesn't exist"""
        result = get_field_content(self.test_content, "non_existent_field")
        self.assertEqual(result, "'non_existent_field' not found in content.")

    def test_complex_field_content(self):
        """Test retrieving content from a field with complex data (list)"""
        result = get_field_content(self.test_content, "requester_country", "countries")
        self.assertEqual(result, ["United Kingdom", "United States", "Canada"])


if __name__ == "__main__":
    unittest.main()
