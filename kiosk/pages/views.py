from django.shortcuts import render
from django.views.decorators.cache import never_cache


def welcome(request):
    return render(request, "pages/welcome.html")


def booking(request):
    return render(request, "pages/booking.html")


@never_cache
def checkin(request):
    context = {}
    if request.method == "POST":
        query = request.POST.get("query", "").strip()
        if not query:
            context["search_error"] = "Enter a booking reference, surname, or email address."
            return render(request, "pages/checkin.html", context, status=400)
        if len(query) > 254:
            context["search_error"] = "Search details must be 254 characters or fewer."
            return render(request, "pages/checkin.html", context, status=400)

        context["lookup_unavailable"] = True
        return render(request, "pages/checkin.html", context, status=503)

    return render(request, "pages/checkin.html", context)


@never_cache
def success(request):
    return render(request, "pages/success.html")


@never_cache
def confirmation(request):
    return render(request, "pages/confirmation.html")


@never_cache
def error(request):
    return render(request, "pages/error.html")
