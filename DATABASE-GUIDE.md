# Kiosk Database Guide

The kiosk uses the local SQLite database at `kiosk/db.sqlite3`. No external
database account or credentials are required.

## Start the project

Open PowerShell in the `kiosk` folder:

```powershell
cd "C:\Users\ohaso\OneDrive - NCG\NGC-Kiosk\kiosk"
```

Apply database migrations (repeat this after model changes):

```powershell
..\.venv\Scripts\python.exe manage.py migrate
```

Create an admin account once:

```powershell
..\.venv\Scripts\python.exe manage.py createsuperuser
```

Start the development server:

```powershell
..\.venv\Scripts\python.exe manage.py runserver
```

Visit <http://127.0.0.1:8000/admin/> and sign in with the superuser account.
Keep the server running while using the kiosk at <http://127.0.0.1:8000/>.

## Add booking data

Add records in this order:

1. **Attendees** — Enter the attendee's first name, last name, and email.
2. **Talks** — Enter each talk's title, start and end times, and location.
3. **Bookings** — Select the attendee and enter a unique booking reference,
   ticket type, and status. Leave status as **Confirmed** for bookings that
   should be searchable.
4. **Talk reservations** — In the booking form's **Booking talks** section,
   choose the talks included in that booking. Each reservation starts as
   **Booked**. Avoid assigning the same talk to one booking more than once.

## Try the kiosk

On the kiosk's booking search page, search using the exact booking reference,
the attendee's full surname, or their exact email address. Search is not
partial-match. A single match opens the booking review. If a surname matches
multiple attendees, select the correct booking from the list.

Review the attendee, ticket, and talks, then select **Confirm Check-In** to
record the booking's check-in time. A booking that has already been checked in
cannot be checked in again. Cancelled bookings are not returned by search.

## Important notes

- The database is local to this project; bookings are not imported from the
  PHP test database or another dashboard.
- The development server is for local development. Do not expose it directly
  to the public internet for a live event.
- Back up `kiosk\db.sqlite3` before making database or data changes you cannot
  easily recreate.
