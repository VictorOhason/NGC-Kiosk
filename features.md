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
- Looks up confirmed bookings in the local Django database using an exact booking reference, surname, or email match.
- Shows a booking review for a single match, or lets the visitor select among multiple matches.
- Shows the booking-not-found page when no confirmed booking matches.
- Pressing Escape clears the form and returns focus to the search field.
- Search terms are not placed in URLs or repopulated into the form; the page is marked as non-cacheable.

### Booking review — `/success/`

- Shows the review layout for attendee details, ticket type, booked talks, locations, and statuses.
- Loads attendee and booking details from the local Django database.
- “Cancel / Start Over” returns to the booking search page. Escape activates this action.
- “Confirm Check-In” submits a CSRF-protected request that records the booking's check-in time before displaying confirmation. Enter activates it when no other element has focus.
- Already checked-in bookings are identified and cannot be checked in a second time.
- The talks table has a compact layout for small screens.

### Final confirmation — `/confirmation/`

- Shows a checkmark, successful check-in message, and “Finish Now” link.
- “Finish Now” returns to the welcome page.
- The browser automatically returns to the welcome page after five seconds.
- It is only available after a successful database check-in.

### Booking not found — `/error/`

- Shows the booking-not-found message and a retry link back to search.
- Escape activates the retry link.
- Provides guidance to ask a nearby convention staff member; no help call or contact integration is configured.
- Booking search sends unmatched confirmed bookings to this page.

## Shared behavior and presentation

- Pages use the project’s dark color palette and Plus Jakarta Sans font from `pages/static/pages/style.css`.
- Key kiosk pages use responsive layouts, visible keyboard focus styles, and larger touch targets.
- Search, review, confirmation, and error pages are marked non-cacheable to reduce the chance of personal information persisting in browser caches.
- A back/forward-cache return to review or error redirects to the welcome page.
- Django tests cover search results, selection, check-in persistence, duplicate check-in prevention, CSRF protection, and cache headers.

## Not implemented yet

- Connection to the school dashboard or another approved booking-data source.
- Importing or synchronizing bookings from an external data source.
- A real staff-help contact method.

## Local Django database

- Django's SQLite database has models for attendees, bookings, talks, and booking-to-talk reservations.
- Bookings store a unique reference, ticket type, booking status, and overall check-in time.
- Talk reservations store their own booking/check-in/cancellation status and check-in time.
- These tables are editable in Django admin and are used by the kiosk search and check-in flow.
- Booking data must be entered in admin or imported before visitors can find their bookings.
