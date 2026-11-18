from django.contrib.auth import get_user_model
from django.test import Client, SimpleTestCase, TestCase, override_settings
from django.urls import reverse

TEST_STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
}

@override_settings(STORAGES=TEST_STORAGES)
class PublicPageTests(SimpleTestCase):
    def test_homepage_links_to_login(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'href="/login/"')
        self.assertNotContains(response, "portal-notice")
        self.assertContains(response, 'id="icon-arrow-up-right"')
        self.assertContains(response, 'href="#icon-asterisk"')

    def test_login_screen(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "STAFF SIGN IN")
        self.assertContains(response, 'autocomplete="current-password"')
        self.assertContains(response, 'name="csrfmiddlewaretoken"')
        self.assertNotIn("public", response.headers.get("Cache-Control", ""))

    @override_settings(STAFF_LOGIN_ENABLED=False)
    def test_render_without_persistent_database_does_not_accept_credentials(self):
        response = self.client.get(reverse("login"))
        self.assertContains(response, "<fieldset disabled>")
        response = self.client.post(reverse("login"), {"username": "someone", "password": "private"})
        self.assertEqual(response.status_code, 503)
        self.assertNotContains(response, 'value="private"', status_code=503)


@override_settings(STORAGES=TEST_STORAGES)
class StaffAuthenticationTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        users = get_user_model().objects
        cls.password = "test-only-password-not-a-live-account"
        cls.staff = users.create_user("ogs-staff-test", password=cls.password, is_staff=True)
        cls.student = users.create_user("non-staff-test", password=cls.password)
        cls.inactive = users.create_user("inactive-staff-test", password=cls.password, is_staff=True, is_active=False)

    def test_staff_can_sign_in_and_sign_out(self):
        response = self.client.post(reverse("login"), {"username": self.staff.username, "password": self.password})
        self.assertRedirects(response, reverse("portal"))
        self.assertContains(self.client.get(reverse("portal")), self.staff.username)
        self.assertEqual(self.client.get(reverse("logout")).status_code, 405)
        self.assertRedirects(self.client.post(reverse("logout")), reverse("login"))
        self.assertRedirects(self.client.get(reverse("portal")), "/login/?next=/portal/")

    def test_non_staff_inactive_and_incorrect_credentials_are_rejected(self):
        for username, password in [
            (self.student.username, self.password),
            (self.inactive.username, self.password),
            (self.staff.username, "incorrect"),
        ]:
            with self.subTest(username=username):
                response = self.client.post(reverse("login"), {"username": username, "password": password})
                self.assertEqual(response.status_code, 200)
                self.assertTrue(response.context["form"].non_field_errors())
                self.assertNotIn("_auth_user_id", self.client.session)

    def test_login_does_not_redirect_to_an_external_site(self):
        response = self.client.post(reverse("login"), {
            "username": self.staff.username, "password": self.password, "next": "https://untrusted.example/",
        })
        self.assertRedirects(response, reverse("portal"))

    def test_non_staff_cannot_enter_portal_with_existing_session(self):
        self.client.force_login(self.student)
        self.assertEqual(self.client.get(reverse("portal")).status_code, 403)

    def test_login_requires_csrf_token(self):
        response = Client(enforce_csrf_checks=True).post(reverse("login"), {
            "username": self.staff.username, "password": self.password,
        })
        self.assertEqual(response.status_code, 403)
