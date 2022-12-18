from django.conf import settings
from django.shortcuts import render, redirect

# Create your views here.
from groupisite.views import get_profile_pic


def live_chat(request):
    """Produce the live chat."""

    # If they're not logged in then send them to login
    if request.user.is_anonymous:
        return redirect("/login/")

    context = {"debug_mode": settings.DEBUG,
               "room_id": "1",
               "profile_pic": get_profile_pic(request.user)}

    return render(request, "chat.html", context=context)
