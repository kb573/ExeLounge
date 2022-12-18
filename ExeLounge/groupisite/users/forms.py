import datetime

from captcha.fields import ReCaptchaField
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from material import Layout, Row

from .models import Module, Course, UserProfile


def validate_exeter_email(email: str) -> None:
    """
    Checks that this is a valid UoE email address.
    """

    if "@exeter.ac.uk" not in email:
        raise ValidationError("Email address must contain @exeter.ac.uk.")


def validate_over_18(dob: datetime.date) -> None:
    """
    Checks that the user is over 18.
    """

    today = datetime.date.today()
    if today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day)) < 18:
        raise ValidationError("You must be over 18 to use this app.")


def validate_not_future_admission_date(date: datetime.date) -> None:
    """
    Checks that the date is not in the future
    """

    today = datetime.date.today()
    if date > today:
        raise ValidationError("The admission date cannot be in the future.")


class DateInput(forms.DateInput):
    """
    Custom date input to display the date widget.
    """

    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)


class CaptchaForm(forms.Form):
    """A form for the Captcha."""

    captcha = ReCaptchaField()


class StudentRegistrationForm(UserCreationForm):
    """
    Declares a form to register a new user.
    """

    # Ask for user details
    email = forms.EmailField(label="Email address",
                             validators=[validate_exeter_email])
    username = None
    first_name = forms.CharField(label="First name(s)", max_length=100)
    last_name = forms.CharField(label="Last name(s)", max_length=100)

    date_of_birth = forms.DateField(label="Date of birth",
                                    validators=[validate_over_18],
                                    widget=DateInput)
    admission_date = forms.DateField(label="Date of admission",
                                     validators=[validate_not_future_admission_date],
                                     widget=DateInput)

    layout = Layout("email",
                    Row("first_name", "last_name"),
                    Row("date_of_birth", "admission_date"),
                    Row("password1", "password2"))

    def clean_email(self) -> str:
        """
        Verifies that the user's email is not already registered to the system.
        """
        if User.objects.filter(email=self.cleaned_data["email"]).exists():
            raise forms.ValidationError("The email address %(email)s is already registered",
                                        params={"email": self.cleaned_data["email"]})
        return self.cleaned_data["email"]

    class Meta:
        """
        Contains metadata relating to the StudentRegistrationForm
        """
        model = User
        fields = ["email", "first_name", "last_name", "date_of_birth",
                  "admission_date", "password1", "password2"]


def validate_credits(modules: list) -> None:
    """Validate that they are taking 120 credits."""

    module_credits = 0

    for module in modules:
        module_credits += Module.objects.get(module_code=module).module_credit_value

    if module_credits != 120:
        raise ValidationError("You must take 120 credits of modules (not %(credits)d).",
                              params={"credits": module_credits})


class StudentStudyForm(forms.Form):
    """
    Form for selecting course & modules.
    """

    @staticmethod
    def module_choices() -> list:
        """Get the possible modules."""

        module_options = Module.objects.all().values_list("module_title", "module_code").order_by("module_code")
        module_choices = []
        for module in module_options:
            module_choices.append((module[1], module[1] + " " + module[0]))
        return module_choices

    @staticmethod
    def course_choices() -> list:
        """Get the possible courses."""

        course_options = Course.objects.all().values_list("course_title").order_by("course_title")
        course_choices = []
        for course in course_options:
            course_choices.append((course[0], course[0]))
        return course_choices

    # Course selector
    course = forms.ChoiceField(choices=course_choices.__get__(forms.Form),
                               error_messages={"required": "You must pick a course.",
                                               "invalid_choice": "%(value)s is not a valid course."})

    # Module selector
    modules = forms.MultipleChoiceField(choices=module_choices.__get__(forms.Form), validators=[validate_credits],
                                        error_messages={"required": "You must pick some modules.",
                                                        "invalid_choice": "%(value)s is not a valid module."},
                                        help_text="Your module credits must add up to 120")


class LoginForm(forms.Form):
    """
    Represents the login form.
    """

    # Fields
    email = forms.EmailField(label="Email address", validators=[validate_exeter_email])
    password = forms.CharField(label="Password", widget=forms.PasswordInput)

    # The Material Design layout
    layout = Layout("email", "password")


class SettingsForm(forms.Form):
    """
    Represents the settings form.
    """

    # Fields
    profile_pic = forms.ImageField(label="Profile picture",
                                   help_text="Your profile picture is only visible on the leaderboard if you choose to display your full name.",
                                   required=False)

    leaderboard_privacy = forms.ChoiceField(choices=UserProfile.LEADERBOARD_PRIVACY_CHOICES,
                                            label="Leaderboard privacy",
                                            help_text="Your full name will always be visible to you on the leadboard.",
                                            error_messages={"required": "You must privacy option.",
                                                            "invalid_choice": "%(value)s is not a valid privacy option."})
