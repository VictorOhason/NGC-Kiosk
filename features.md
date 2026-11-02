# Kiosk Features

This document describes the kiosk pages and behavior currently implemented in the Django project.

## Pages

### Welcome — `/`

- Introduces the Newcastle Games Convention self-service check-in kiosk.
- The entire purple call-to-action links to the booking search page.
- Includes a logo placeholder and a short assistance message.
- Uses the shared stylesheet and responsive layout.

### Booking — `/booking/`

- Route and template placeholder exist.
- The page is currently empty and has no booking behavior.

### Booking search — `/checkin/`

- Provides a search field for a booking reference, surname, or email address.
- Submits the search using a CSRF-protected `POST` form so the submitted value is not placed in the URL.
- Rejects empty and overlong search values.
- Shows a searching status while the form is submitting.
- The search panel focuses the input when clicked outside its controls.
- **Dashboard lookup is not connected.** A valid submission displays a clear “lookup is not connected yet” message rather than returning mock search results or claiming no booking exists.
- Pressing Escape clears the form and returns focus to the search field.
- Search terms are not echoed into the response, and the page is marked as non-cacheable.

### Booking review — `/success/`

- Shows the review layout for attendee details, ticket type, booked talks, locations, and statuses.
- Uses placeholder attendee and booking data for the design; it is not populated from a real booking.
- “Cancel / Start Over” returns to the booking search page. Escape activates this action.
- “Confirm Check-In” opens the final confirmation page. Enter activates it when no other element has focus.
- This page does **not** save a check-in to a database.
- The talks table has a compact layout for small screens.

### Final confirmation — `/confirmation/`

- Shows a checkmark, successful check-in message, and “Finish Now” link.
- “Finish Now” returns to the welcome page.
- The browser automatically returns to the welcome page after five seconds.
- This page currently represents the visual flow only; it is not proof of a persisted check-in.

### Booking not found — `/error/`

- Shows the booking-not-found message and a retry link back to search.
- Escape activates the retry link.
- Provides guidance to ask a nearby convention staff member; no help call or contact integration is configured.
- The page is not automatically selected by booking search yet.

## Shared behavior and presentation

- Pages use the project’s dark color palette and Plus Jakarta Sans font from `pages/static/pages/style.css`.
- Key kiosk pages use responsive layouts, visible keyboard focus styles, and larger touch targets.
- Search, review, confirmation, and error pages are marked non-cacheable to reduce the chance of personal information persisting in browser caches.
- A back/forward-cache return to review or error redirects to the welcome page.
- Django page tests cover the routes, key UI content, search validation and unavailable state, CSRF protection, and cache headers.

## Not implemented yet

- Connection to the school dashboard or another approved booking-data source.
- Searching for a booking and distinguishing no match, an empty database, and a dashboard outage.
- Displaying the selected attendee’s real details and booked talks.
- Persisting check-in before showing the final confirmation.
- A real staff-help contact method.
