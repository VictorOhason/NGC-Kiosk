from django.db import transaction
from django.db.models import Q
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.decorators.cache import never_cache
from django.views.decorators.http import require_POST

from .models import Booking


def welcome(request):
    return render(request, "pages/welcome.html")


def booking(request):
    return render(request, "pages/booking.html")


@never_cache
def checkin(request):
    if request.method == "GET":
        return render(request, "pages/checkin.html")
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    query = request.POST.get("query", "").strip()
    if not query:
        return render(
            request,
            "pages/checkin.html",
            {"search_error": "Enter a booking reference, surname, or email address."},
            status=400,
        )
    if len(query) > 254:
        return render(
            request,
            "pages/checkin.html",
            {"search_error": "Search details must be 254 characters or fewer."},
            status=400,
        )

    bookings = (
        Booking.objects.filter(status=Booking.Status.CONFIRMED)
        .filter(
            Q(booking_reference__iexact=query)
            | Q(attendee__last_name__iexact=query)
            | Q(attendee__email__iexact=query)
        )
        .select_related("attendee")
        .prefetch_related("talk_reservations__talk")
        .order_by("booking_reference")
    )
    matches = list(bookings[:21])
    if not matches:
        return render(request, "pages/error.html", status=404)
    if len(matches) == 1:
        return render(
            request,
            "pages/success.html",
            {
                "booking": matches[0],
                "already_checked_in": matches[0].checked_in_at is not None,
            },
        )

    return render(
        request,
        "pages/checkin.html",
        {
            "bookings": matches[:20],
            "too_many_matches": len(matches) > 20,
        },
    )


@never_cache
@require_POST
def success(request):
    booking_id = request.POST.get("booking_id", "")
    try:
        booking = (
            Booking.objects.filter(status=Booking.Status.CONFIRMED)
            .select_related("attendee")
            .prefetch_related("talk_reservations__talk")
            .get(pk=booking_id)
        )
    except (Booking.DoesNotExist, ValueError):
        return render(request, "pages/error.html", status=404)

    return render(
        request,
        "pages/success.html",
        {
            "booking": booking,
            "already_checked_in": booking.checked_in_at is not None,
        },
    )


@never_cache
def confirmation(request):
    if request.method == "GET":
        booking_id = request.session.pop("checked_in_booking_id", None)
        if not booking_id or not Booking.objects.filter(
            pk=booking_id,
            checked_in_at__isnull=False,
        ).exists():
            return redirect("pages:checkin")
        return render(request, "pages/confirmation.html")
    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    booking_id = request.POST.get("booking_id", "")
    try:
        with transaction.atomic():
            booking = (
                Booking.objects.select_for_update()
                .filter(status=Booking.Status.CONFIRMED)
                .get(pk=booking_id)
            )
            if booking.checked_in_at is not None:
                return render(
                    request,
                    "pages/success.html",
                    {
                        "booking": booking,
                        "already_checked_in": True,
                    },
                    status=409,
                )
            booking.checked_in_at = timezone.now()
            booking.save(update_fields=["checked_in_at"])
    except (Booking.DoesNotExist, ValueError):
        return render(request, "pages/error.html", status=404)

    request.session["checked_in_booking_id"] = booking.pk
    return redirect("pages:confirmation")


@never_cache
def error(request):
    return render(request, "pages/error.html")
