import unittest

from app import create_app


class MainBlueprintTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app("config.Test")
        self.client = self.app.test_client()
        self.domain = "http://localhost"

    def test_healthcheck_live(self):
        rv = self.client.get("/healthcheck/live/")
        self.assertEqual(rv.status_code, 200)
        self.assertIn("ok", rv.text)

    def test_trailing_slash_redirects(self):
        rv = self.client.get("/healthcheck/live")
        self.assertEqual(rv.status_code, 308)
        self.assertEqual(rv.location, f"{self.domain}/healthcheck/live/")

    def test_requires_session_key_redirects(self):
        rv = self.client.get(
            f"{self.app.config.get('SERVICE_URL_PREFIX')}/which-military-branch-did-the-person-serve-in/"
        )
        self.assertEqual(rv.status_code, 302)
        self.assertEqual(rv.location, f"{self.app.config.get('SERVICE_URL_PREFIX')}/")

    def test_requires_session_key_does_not_redirect(self):
        rv = self.client.get(f"{self.app.config.get('SERVICE_URL_PREFIX')}/")
        self.assertEqual(rv.status_code, 200)

    def test_homepage(self):
        rv = self.client.get(f"{self.app.config.get('SERVICE_URL_PREFIX')}/")
        self.assertIn(
            '<h1 class="tna-heading-xl">Request a military service record</h1>', rv.text
        )

    def test_upload_a_proof_of_death_error_page(self):
        with self.client.session_transaction() as session:
            session["entered_through_index_page"] = True
        rv = self.client.get(
            f"{self.app.config.get('SERVICE_URL_PREFIX')}/upload-a-proof-of-death-error/"
        )
        self.assertEqual(rv.status_code, 200)
        self.assertIn("Sorry, there was an error uploading your file", rv.text)
