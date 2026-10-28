from django.shortcuts import render


def welcome(request):
    return render(request, "pages/welcome.html")


def booking(request):
    return render(request, "pages/booking.html")


def checkin(request):
    return render(request, "pages/checkin.html")


def success(request):
    return render(request, "pages/success.html")


def error(request):
    return render(request, "pages/error.html")
