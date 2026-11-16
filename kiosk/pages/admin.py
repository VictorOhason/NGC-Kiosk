from django.contrib import admin

from .models import Attendee, Booking, BookingTalk, Talk


class BookingTalkInline(admin.TabularInline):
    model = BookingTalk
    extra = 0


@admin.register(Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    list_display = ("attendee_id", "first_name", "last_name", "email")
    search_fields = ("first_name", "last_name", "email")


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        "booking_reference",
        "attendee",
        "ticket_type",
        "status",
        "checked_in_at",
    )
    list_filter = ("status", "ticket_type")
    search_fields = (
        "booking_reference",
        "attendee__first_name",
        "attendee__last_name",
        "attendee__email",
    )
    inlines = (BookingTalkInline,)


@admin.register(Talk)
class TalkAdmin(admin.ModelAdmin):
    list_display = ("title", "starts_at", "ends_at", "location")
    list_filter = ("location",)
    search_fields = ("title", "location")
