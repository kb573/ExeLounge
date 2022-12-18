import datetime

from django.test import TestCase

from .forms import StudentRegistrationForm, LoginForm


class StudentRegistrationTests(TestCase):

    def test_exeter_email(self) -> None:
        """Tests that the email address is from the UoE."""

        form = StudentRegistrationForm(data={"email": "derek@gmail.com"})
        self.assertEqual(form.errors["email"],
                         ["Email address must contain the University of Exeter domain name."])

    def test_over_18(self) -> None:
        """Tests that the user is over 18 based on DoB."""

        form = StudentRegistrationForm(data={"date_of_birth": datetime.date(2006, 1, 1)})
        self.assertEqual(form.errors["date_of_birth"],
                         ["You must be over 18 to use this app."])


class LoginTests(TestCase):

    def test_exeter_email(self) -> None:
        """Tests that the email address is from the UoE."""

        form = LoginForm(data={"email": "derek@gmail.com", "password": "samplepassword"})
        self.assertEqual(form.errors["email"],
                         ["Email address must contain the University of Exeter domain name."])
