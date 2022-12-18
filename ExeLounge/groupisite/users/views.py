from typing import Union

from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpRequest
from django.shortcuts import render, redirect
from groupisite.views import get_profile_pic

from .forms import StudentRegistrationForm, LoginForm, StudentStudyForm, \
    SettingsForm, CaptchaForm
from .models import CustomLogin, UserProfile, Module, Course


def user_register(request: HttpRequest) -> Union[HttpResponseRedirect,
                                                 HttpResponse]:
    """
    Render and process the user registration form.
    """

    # If they are logged in
    if request.user.is_anonymous is False:
        return redirect("/")

    # If this is a POST request we need to process the form data
    if request.method == "POST":

        # Create the form instances and populate them with data from the request
        register_form = StudentRegistrationForm(request.POST)
        study_form = StudentStudyForm(request.POST)
        captcha_form = CaptchaForm(request.POST)

        # Validate the form
        if len(register_form.errors) > 0 or \
                len(study_form.errors) > 0 or \
                len(captcha_form.errors) > 0:
            return render(request, "register.html",
                          {"register_form": register_form,
                           "study_form": study_form,
                           "captcha_form": captcha_form})

        # Create the user
        user = User.objects.create_user(username=register_form.cleaned_data.get("email"),
                                        email=register_form.cleaned_data.get("email"),
                                        password=register_form.cleaned_data.get("password1"))
        user.first_name = register_form.cleaned_data.get("first_name")
        user.last_name = register_form.cleaned_data.get("last_name")
        user.save()

        # Get the student profile
        try:
            profile = UserProfile.objects.get(user=user)
        except UserProfile.DoesNotExist:
            profile = UserProfile.objects.create(user=user)

        # Add data to the profile
        profile.date_of_birth = register_form.cleaned_data.get("date_of_birth")
        profile.admission_date = register_form.cleaned_data.get("admission_date")
        profile.course_title = Course.objects.get(course_title=study_form.cleaned_data.get("course"))
        for module in study_form.cleaned_data.get("modules"):
            profile.modules.add(Module.objects.get(module_code=module))
        profile.save()

        # Log the user in
        login(request, user)

        return redirect("/")

    # If a GET (or any other method) we'll create a blank form
    else:
        register_form = StudentRegistrationForm()
        study_form = StudentStudyForm()
        captcha_form = CaptchaForm()

    return render(request, "register.html",
                  {"register_form": register_form,
                   "study_form": study_form,
                   "captcha_form": captcha_form})


def user_login(request: HttpRequest) -> Union[HttpResponseRedirect,
                                              HttpResponse]:
    """Render and process the user login form."""

    # If they are logged in already
    if request.user.is_anonymous is False:
        return redirect("/")

    # If they submitted the form
    if request.method == "POST":

        login_form = LoginForm(request.POST)
        captcha_form = CaptchaForm(request.POST)

        # Validate the form
        if len(login_form.errors) > 0 or \
                len(captcha_form.errors) > 0:
            return render(request, "login.html",
                          {"login_form": login_form,
                           "captcha_form": captcha_form})

        # Try and authenticate the user
        email = request.POST["email"]
        password = request.POST["password"]
        user = CustomLogin.authenticate(request, email=email, password=password)

        # If successful then log them in and go to the homepage.
        if user is not None:
            login(request, user)
            return redirect("/")

        # Otherwise return an error message
        login_form.add_error("email", "Invalid email address/password!")
        login_form.add_error("password", "Invalid email address/password!")
        return render(request, "login.html",
                      {"login_form": login_form,
                       "captcha_form": captcha_form})

    # If they're not submitting the form
    else:
        login_form = LoginForm()
        captcha_form = CaptchaForm()

    return render(request, "login.html",
                  {"login_form": login_form,
                   "captcha_form": captcha_form})


def user_logout(request: HttpRequest) -> HttpResponseRedirect:
    """Logs the user out and returns them to the homepage."""

    logout(request)
    return redirect("/login/")


def settings(request: HttpRequest) -> Union[HttpResponseRedirect,
                                            HttpResponse]:
    """
    Render and process the settings page.
    """

    # If they're not logged in then send them to login
    if request.user.is_anonymous:
        return redirect("/login/")

    profile = UserProfile.objects.get(user=request.user)

    # If this is a POST request we need to process the form data
    if request.method == "POST":

        # Create the form instances and populate them with data from the request
        study_form = StudentStudyForm(request.POST, request.FILES)
        settings_form = SettingsForm(request.POST)

        # Validate the form
        if len(study_form.errors) > 0 or \
                len(settings_form.errors) > 0:
            return render(request, "settings.html",
                          {"profile_pic": get_profile_pic(request.user),
                           "study_form": study_form,
                           "settings_form": settings_form})

        # Update the user profile data
        profile.course_title = Course.objects.get(course_title=study_form.cleaned_data.get("course"))
        profile.modules.clear()
        for module in study_form.cleaned_data.get("modules"):
            profile.modules.add(Module.objects.get(module_code=module))
        profile.leaderboard_privacy = settings_form.cleaned_data.get("leaderboard_privacy")

        # Update the profile picture
        if "profile_pic-clear" in request.POST.keys() and request.POST["profile_pic-clear"] == "on":
            profile.profile_pic = "profile_pictures/default.png"
        elif "profile_pic" in request.FILES:
            profile.profile_pic = request.FILES["profile_pic"]

        profile.save()
        return redirect("/")

    # If a GET (or any other method)
    else:

        # Prepare the initial data
        study_initial = {"course": profile.course_title,
                         "modules": profile.modules.all().values_list("module_code", flat=True)}
        settings_initial = {"profile_pic": profile.profile_pic,
                            "leaderboard_privacy": profile.leaderboard_privacy}

        # Create the forms
        study_form = StudentStudyForm(initial=study_initial)
        settings_form = SettingsForm(initial=settings_initial)

    return render(request, "settings.html",
                  {"profile_pic": get_profile_pic(request.user),
                   "study_form": study_form,
                   "settings_form": settings_form})


def change_password(request: HttpRequest) -> Union[HttpResponseRedirect,
                                                   HttpResponse]:
    """
    Render and process the change password page.
    """

    # If they're not logged in then send them to login
    if request.user.is_anonymous:
        return redirect("/login/")

    # If this is a POST request we need to process the form data
    if request.method == "POST":

        # Generate the filled form
        password_form = PasswordChangeForm(user=request.user, data=request.POST)

        # If it's valid then save it and keep them logged in
        if password_form.is_valid():
            password_form.save()
            update_session_auth_hash(request, password_form.user)
            return redirect("/")

        # Otherwise explain the error
        else:
            return render(request, "change-password.html",
                          {"profile_pic": get_profile_pic(request.user),
                           "password_form": password_form})

    # If a GET (or any other method)
    else:
        password_form = PasswordChangeForm(user=request.user)

    return render(request, "change-password.html",
                  {"profile_pic": get_profile_pic(request.user),
                   "password_form": password_form})


def change_password_redirect(request: HttpRequest) -> HttpResponseRedirect:
    return redirect("/settings/change-password/")
