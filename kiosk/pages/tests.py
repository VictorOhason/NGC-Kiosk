from django.test import TestCase


class PageViewTests(TestCase):
    def test_page_urls_render_their_templates(self):
        pages = {
            "welcome": "/",
            "booking": "/booking/",
            "checkin": "/checkin/",
            "success": "/success/",
            "error": "/error/",
        }

        for page, path in pages.items():
            with self.subTest(page=page):
                response = self.client.get(path)

                self.assertEqual(response.status_code, 200)
                self.assertTemplateUsed(response, f"pages/{page}.html")
                if page == "welcome":
                    self.assertContains(response, 'href="/static/pages/style.css"')
