# Suggestions

## Remaining: dashboard integration

- Connect the booking search form to the school dashboard or its approved API. The form now submits the search term in a CSRF-protected POST body, but the Django view does not search for a booking yet.
- Confirm with the dashboard owner how the kiosk is allowed to access booking data (API, export, or another approved integration), which fields can be searched, and what authentication and network access are required. Keep credentials out of source control.
- Decide whether the error page means “no booking matched this search” or “the booking database contains no records,” then show it only for that condition. Keep dashboard/API outages separate; until integration is added, search submissions show a clear “lookup not connected” response instead of claiming no booking was found.
- Replace the sample attendee, reference, ticket, talk, and status values on the review page with the selected booking's actual data.
- Make Confirm Check-In perform a server-side, CSRF-protected update and show the final confirmation only after that update succeeds. The current page flow is visual and does not record a check-in.
- Implement the booking lookup and confirmation tests with representative results, no-match cases, empty-data cases, and dashboard/API failures.

## Remaining: kiosk deployment

- Verify touch targets, responsive layout, and keyboard operation on the actual kiosk display and browser.
- Configure the real staff-help contact method once convention staff provide it; the current error page directs users to nearby staff rather than presenting a non-working button.
