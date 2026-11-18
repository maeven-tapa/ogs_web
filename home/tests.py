from django.test import SimpleTestCase, override_settings
from django.urls import resolve


class HomepageTests(SimpleTestCase):
    def test_homepage_and_unconfigured_portal(self):
        with override_settings(OGS_PORTAL_URL=""):
            response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "home/index.html")
        self.assertContains(response, "Office of Guidance Services")
        self.assertContains(response, "Access Portal")
        self.assertContains(response, 'id="portal-notice"')
        self.assertEqual(resolve("/").url_name, "home")

    @override_settings(OGS_PORTAL_URL="https://portal.example.edu/ogs/")
    def test_portal_links_to_configured_destination(self):
        response = self.client.get("/")
        self.assertContains(response, 'href="https://portal.example.edu/ogs/"')
        self.assertNotContains(response, 'id="portal-notice"')

    @override_settings(OGS_PORTAL_URL="javascript:alert(1)")
    def test_invalid_portal_url_uses_notice(self):
        response = self.client.get("/")
        self.assertContains(response, 'id="portal-notice"')
        self.assertNotContains(response, "javascript:")

    def test_no_additional_application_pages(self):
        self.assertEqual(self.client.get("/portal/").status_code, 404)
