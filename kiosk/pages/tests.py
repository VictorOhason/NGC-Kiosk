from datetime import datetime, timezone

from django.test import Client, TestCase

from .models import Attendee, Booking, BookingTalk, Talk


class PageViewTests(TestCase):
    def test_page_urls_render_their_templates(self):
        pages = {
            "welcome": "/",
            "booking": "/booking/",
            "checkin": "/checkin/",
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
    def test_booking_search_does_not_put_search_data_in_get_response(self):
        private_value = "sensitive@example.com"

        response = self.client.get("/checkin/", {"query": private_value})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, private_value)
        self.assertIn("no-store", response.headers["Cache-Control"])


class BookingDatabaseTests(TestCase):
    def setUp(self):
        self.attendee = Attendee.objects.create(
            first_name="Casey",
            last_name="Nguyen",
            email="casey@example.com",
        )
        self.booking = Booking.objects.create(
            attendee=self.attendee,
            booking_reference="NGC-2026-001",
            ticket_type="VIP Convention Pass",
        )
        self.talk = Talk.objects.create(
            title="Indie Game Dev",
            starts_at=datetime(2026, 11, 16, 10, 0, tzinfo=timezone.utc),
            ends_at=datetime(2026, 11, 16, 11, 0, tzinfo=timezone.utc),
            location="Main Stage",
        )

    def test_booking_and_attendee_are_persisted_and_searchable(self):
        booking = Booking.objects.get(booking_reference="NGC-2026-001")

        self.assertEqual(booking.attendee, self.attendee)
        self.assertEqual(booking.attendee.email, "casey@example.com")
        self.assertEqual(
            Attendee.objects.filter(last_name__iexact="nguyen").count(),
            1,
        )

    def test_booking_talk_tracks_reservation_and_check_in_status(self):
        reservation = BookingTalk.objects.create(
            booking=self.booking,
            talk=self.talk,
        )

        self.assertEqual(self.booking.talk_reservations.get(), reservation)
        self.assertEqual(reservation.status, BookingTalk.Status.BOOKED)
        self.assertEqual(reservation.talk.location, "Main Stage")

    def test_booking_search_renders_database_details_without_echoing_query(self):
        BookingTalk.objects.create(booking=self.booking, talk=self.talk)

        response = self.client.post(
            "/checkin/",
            {"query": self.booking.booking_reference},
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "pages/success.html")
        self.assertContains(response, "Casey Nguyen")
        self.assertContains(response, "NGC-2026-001")
        self.assertContains(response, "VIP Convention Pass")
        self.assertContains(response, "Indie Game Dev")
        self.assertContains(response, "Main Stage")
        self.assertContains(response, "Confirm Check-In")
        self.assertNotContains(response, "casey@example.com")
        self.assertIn("no-store", response.headers["Cache-Control"])

    def test_surname_search_allows_selecting_a_matching_booking(self):
        second_attendee = Attendee.objects.create(
            first_name="Jordan",
            last_name="Nguyen",
            email="jordan@example.com",
        )
        second_booking = Booking.objects.create(
            attendee=second_attendee,
            booking_reference="NGC-2026-002",
            ticket_type="Standard Pass",
        )

        response = self.client.post("/checkin/", {"query": "Nguyen"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Select Your Booking")
        self.assertContains(response, self.booking.booking_reference)
        self.assertContains(response, second_booking.booking_reference)

        selected = self.client.post(
            "/success/",
            {"booking_id": second_booking.pk},
        )

        self.assertEqual(selected.status_code, 200)
        self.assertContains(selected, "Jordan Nguyen")
        self.assertContains(selected, "NGC-2026-002")

    def test_unmatched_booking_renders_not_found_without_echoing_query(self):
        private_value = "private-search@example.com"

        response = self.client.post("/checkin/", {"query": private_value})

        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "pages/error.html")
        self.assertNotContains(response, private_value, status_code=404)

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
            {"query": self.booking.booking_reference},
        )
        accepted = client.post(
            "/checkin/",
            {"query": self.booking.booking_reference},
            HTTP_X_CSRFTOKEN=csrf_token,
        )

        self.assertEqual(rejected.status_code, 403)
        self.assertEqual(accepted.status_code, 200)

    def test_personal_pages_are_not_cached(self):
        for path in ("/checkin/", "/error/"):
            with self.subTest(path=path):
                response = self.client.get(path)

                self.assertIn("no-store", response.headers["Cache-Control"])

    def test_confirmation_records_check_in_and_prevents_duplicates(self):
        response = self.client.post(
            "/confirmation/",
            {"booking_id": self.booking.pk},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response["Location"], "/confirmation/")
        self.booking.refresh_from_db()
        self.assertIsNotNone(self.booking.checked_in_at)

        confirmation = self.client.get("/confirmation/")
        self.assertEqual(confirmation.status_code, 200)
        self.assertContains(confirmation, "Check-In")
        self.assertContains(confirmation, "has been recorded")
        self.assertIn("no-store", confirmation.headers["Cache-Control"])

        duplicate = self.client.post(
            "/confirmation/",
            {"booking_id": self.booking.pk},
        )
        self.assertEqual(duplicate.status_code, 409)
        self.assertContains(duplicate, "already been checked in", status_code=409)

    def test_confirmation_cannot_be_opened_without_a_successful_check_in(self):
        response = self.client.get("/confirmation/")

        self.assertRedirects(response, "/checkin/")

    def test_already_checked_in_booking_is_not_offered_for_check_in(self):
        self.booking.checked_in_at = datetime(2026, 11, 16, 9, 0, tzinfo=timezone.utc)
        self.booking.save(update_fields=["checked_in_at"])

        response = self.client.post(
            "/checkin/",
            {"query": self.booking.booking_reference},
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "already been checked in")
        self.assertNotContains(response, "Confirm Check-In")
