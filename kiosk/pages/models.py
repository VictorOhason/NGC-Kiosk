from django.db import models


class Attendee(models.Model):
    attendee_id = models.AutoField(primary_key=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, db_index=True)
    email = models.EmailField(max_length=254, db_index=True)

    class Meta:
        ordering = ["last_name", "first_name", "attendee_id"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Booking(models.Model):
    class Status(models.TextChoices):
        CONFIRMED = "confirmed", "Confirmed"
        CANCELLED = "cancelled", "Cancelled"

    attendee = models.ForeignKey(
        Attendee,
        on_delete=models.PROTECT,
        related_name="bookings",
    )
    booking_reference = models.CharField(max_length=50, unique=True)
    ticket_type = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.CONFIRMED,
    )
    booked_at = models.DateTimeField(auto_now_add=True)
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["booking_reference"]

    def __str__(self):
        return self.booking_reference


class Talk(models.Model):
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    location = models.CharField(max_length=150)

    class Meta:
        ordering = ["starts_at", "title"]

    def __str__(self):
        return self.title


class BookingTalk(models.Model):
    class Status(models.TextChoices):
        BOOKED = "booked", "Booked"
        CHECKED_IN = "checked_in", "Checked In"
        CANCELLED = "cancelled", "Cancelled"

    booking = models.ForeignKey(
        Booking,
        on_delete=models.CASCADE,
        related_name="talk_reservations",
    )
    talk = models.ForeignKey(
        Talk,
        on_delete=models.PROTECT,
        related_name="reservations",
    )
    status = models.CharField(
        max_length=12,
        choices=Status.choices,
        default=Status.BOOKED,
    )
    checked_in_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["talk__starts_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["booking", "talk"],
                name="unique_talk_per_booking",
            ),
        ]

    def __str__(self):
        return f"{self.booking} — {self.talk}"
