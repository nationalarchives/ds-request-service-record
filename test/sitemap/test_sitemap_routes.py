import unittest

from app import create_app


class SitemapBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test").test_client()
        self.domain = "http://localhost"

    def test_sitemap(self):
        rv = self.app.get("/request-a-military-service-record/sitemap.xml")
        self.assertEqual(rv.status_code, 200)
        self.assertIn(
            f"<loc>{self.domain}/request-a-military-service-record/</loc>", rv.text
        )
