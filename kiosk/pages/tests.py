from django.test import Client, TestCase


class PageViewTests(TestCase):
    def test_page_urls_render_their_templates(self):
        pages = {
            "welcome": "/",
            "booking": "/booking/",
            "checkin": "/checkin/",
            "success": "/success/",
            "confirmation": "/confirmation/",
            "error": "/error/",
        }

        for page, path in pages.items():
            with self.subTest(page=page):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"pages/{page}.html")
                if page == "welcome":
                    self.assertContains(response, 'href="/static/pages/style.css"')
                    self.assertContains(
                        response,
                        '<a class="welcome-page__start-link" href="/checkin/">',
                    )
                    self.assertContains(response, "Press any key or touch to begin")
                if page == "checkin":
                    self.assertContains(response, "Find Your Booking")
                    self.assertContains(response, 'name="query"')
                    self.assertContains(response, "Search Booking (Enter)")
                    self.assertContains(response, 'href="/static/pages/style.css"')
                    self.assertContains(response, 'src="/static/pages/checkin.js"')
                    self.assertContains(response, 'method="post"')
                    self.assertContains(response, 'name="csrfmiddlewaretoken"')
                if page == "error":
                    self.assertContains(response, "Booking Not Found")
                    self.assertContains(response, "We couldn't find a registration")
                    self.assertContains(response, 'href="/checkin/"')
                    self.assertContains(response, 'href="/static/pages/style.css"')
                    self.assertContains(response, 'data-kiosk-escape')
                    self.assertContains(response, "Please ask a convention staff member")
                    self.assertNotContains(response, "Call Staff for Help")
                if page == "success":
                    self.assertContains(response, "Welcome,")
                    self.assertContains(response, "Attendee Name")
                    self.assertNotContains(response, "Victor Ohason")
                    self.assertContains(response, "VIP Convention Pass")
                    self.assertContains(response, "Your Booked Talks")
                    self.assertContains(response, "Confirm Check-In")
                    self.assertContains(response, 'href="/static/pages/style.css"')
                    self.assertContains(response, 'href="/confirmation/"')
                    self.assertContains(response, 'data-kiosk-enter')
                    self.assertContains(response, 'data-kiosk-escape')
                    self.assertContains(response, 'src="/static/pages/kiosk.js"')
                if page == "confirmation":
                    self.assertContains(response, "Check-In")
                    self.assertContains(response, "Successful!")
                    self.assertContains(response, "5 seconds")
                    self.assertContains(response, 'href="/"')
                    self.assertContains(response, 'http-equiv="refresh"')

    def test_booking_search_does_not_put_search_data_in_get_response(self):
        private_value = "sensitive@example.com"

        response = self.client.get("/checkin/", {"query": private_value})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, private_value)
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_booking_search_shows_unavailable_until_dashboard_is_connected(self):
        private_value = "sensitive@example.com"

        response = self.client.post("/checkin/", {"query": private_value})

        self.assertEqual(response.status_code, 503)
        self.assertContains(
            response,
            "Booking lookup is not connected yet",
            status_code=503,
        )
        self.assertNotContains(response, private_value, status_code=503)
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_booking_search_requires_a_non_empty_query(self):
        response = self.client.post("/checkin/", {"query": "   "})

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "Enter a booking reference", status_code=400)

    def test_booking_search_rejects_overlong_query(self):
        response = self.client.post("/checkin/", {"query": "x" * 255})

        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "254 characters or fewer", status_code=400)

    def test_booking_search_requires_csrf_protection(self):
        client = Client(enforce_csrf_checks=True)
        client.get("/checkin/")
        csrf_token = client.cookies["csrftoken"].value

        rejected = Client(enforce_csrf_checks=True).post(
            "/checkin/",
            {"query": "NGC-1234"},
        )
        accepted = client.post(
            "/checkin/",
            {"query": "NGC-1234"},
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(rejected.status_code, 403)
        self.assertEqual(accepted.status_code, 503)

    def test_personal_pages_are_not_cached(self):
        for path in ("/checkin/", "/success/", "/confirmation/", "/error/"):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertIn("no-store", response.headers["Cache-Control"])
