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

    def test_army_officer_routing_and_date_of_birth_back_link(self):
        self.app.config["WTF_CSRF_ENABLED"] = False
        prefix = self.app.config["SERVICE_URL_PREFIX"]
        officer_path = f"{prefix}/were-they-a-commissioned-officer/"
        date_of_birth_path = f"{prefix}/what-was-their-date-of-birth/"

        for enabled, destination in (
            (
                False,
                f"{prefix}/we-are-unlikely-to-hold-army-officer-records/",
            ),
            (
                True,
                f"{prefix}/we-may-hold-this-record/",
            ),
        ):
            with self.subTest(feature_13_enabled=enabled):
                self.app.config["ENABLE_FEATURE_13"] = enabled
                self.client.get(f"{prefix}/")
                response = self.client.post(
                    officer_path,
                    data={
                        "service_branch": "BRITISH_ARMY",
                        "were_they_a_commissioned_officer": "yes",
                    },
                )
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.location, destination)

                response = self.client.get(destination)
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'href="{officer_path}"', response.text)

                response = self.client.post(destination)
                self.assertEqual(response.status_code, 302)
                self.assertEqual(response.location, date_of_birth_path)

                response = self.client.get(date_of_birth_path)
                self.assertEqual(response.status_code, 200)
                self.assertIn(f'href="{destination}"', response.text)
