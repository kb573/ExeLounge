from typing import Union

from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponsePermanentRedirect, HttpResponseRedirect, \
    HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from users.models import UserProfile


def favicon(request: HttpRequest) -> HttpResponsePermanentRedirect:
    return redirect("/static/favicon.ico", permanent=True)


def get_profile_pic(user: User) -> dict:
    """
    Get the profile pic and name.
    """

    return {"name": user.get_full_name(),
            "url": UserProfile.objects.get(user=user).profile_pic.url}


def home(request: HttpRequest) -> Union[HttpResponseRedirect, HttpResponse]:
    """Load the homepage."""

    # If they're not logged in then send them to login
    if request.user.is_anonymous:
        return redirect("/login/")

    # Start to prepare the response
    context = {"profile_pic": get_profile_pic(request.user),
               "first_name": request.user.first_name,
               "name": request.user.get_full_name(),
               "course": UserProfile.objects.get(user=request.user).course_title}

    # Select profiles that are happy to be on the leaderboard or are the current user
    user_profiles = UserProfile.objects.filter(~Q(leaderboard_privacy="HIDE") |
                                               Q(user=request.user)).order_by("-forum_score")

    # Generate the leaderboard (up to 15 long)
    forum_leaderboard = []
    i = 0
    while len(forum_leaderboard) < 15:

        # If we've run out of users then stop
        if i >= user_profiles.count():
            break

        profile = user_profiles[i]

        # Don't increment their place if they have the same score as the last user
        if i == 0 or profile.forum_score != forum_leaderboard[i - 1]["score"]:
            place = i + 1
        else:
            place = forum_leaderboard[i - 1]["place"]

        # If they want their full name or this is the current user
        if profile.leaderboard_privacy == "FULL_NAME" or profile.user == request.user:
            forum_leaderboard.append({"place": place,
                                      "photo": profile.profile_pic.url,
                                      "name": profile.user.get_full_name(),
                                      "score": profile.forum_score})

        # If they only want their first name
        elif profile.leaderboard_privacy == "FIRST_NAME":
            forum_leaderboard.append({"place": place,
                                      "photo": UserProfile.objects.get(
                                          user=User.objects.get(
                                              username="deleteduser@exeter.ac.uk")).profile_pic.url,
                                      "name": profile.user.first_name,
                                      "score": profile.forum_score})

        # They must want their initials only
        else:
            try:
                forum_leaderboard.append(
                    {"place": place,
                     "photo": UserProfile.objects.get(
                         user=User.objects.get(
                             username="deleteduser@exeter.ac.uk")).profile_pic.url,
                     "name": "".join([x[0].upper() + ". " for x in profile.user.get_full_name().split(" ")]),
                     "score": profile.forum_score})
            except IndexError:
                forum_leaderboard.append(
                    {"place": place,
                     "photo": UserProfile.objects.get(
                         user=User.objects.get(
                             username="deleteduser@exeter.ac.uk")).profile_pic.url,
                     "name": "",
                     "score": profile.forum_score})

        i += 1

    context["forum_leaderboard"] = forum_leaderboard

    return render(request, "home.html", context)
