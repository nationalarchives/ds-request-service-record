import unittest

from app import create_app


class SitemapBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "https://localhost"

    def test_sitemap(self):
        rv = self.client.get(f"{self.app.config.get('SERVICE_URL_PREFIX')}/sitemap.xml")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            f"<loc>{self.domain}{self.app.config.get('SERVICE_URL_PREFIX')}/</loc>",
            rv.text,
        )
