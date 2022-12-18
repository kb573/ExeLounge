import datetime
import uuid
from typing import Optional, Any

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class CustomLogin(ModelBackend):
    """Represents a custom login backend."""

    def authenticate(self, email=None, username=None,
                     password=None, **kwargs) -> Optional[User]:
        """Authenticates the user with their email or username and password.

        :param email: the email address
        :param username: the username
        :param password: the password
        :return: either the User object, or None
        """

        # Try and find the user from their email or username
        try:
            if email is not None:
                user = User.objects.get(email=email)
            elif username is not None:
                user = User.objects.get(username=username)
            else:
                return None

        # If they don't exist
        except User.DoesNotExist:
            return None

        # Check that their password is correct
        else:
            if user.check_password(password):
                return user
        return None


class College(models.Model):
    """
    Stores a single College, related to :model:`user.College`.
    """
    college_name = models.CharField(max_length=200)

    class Meta:
        """
        Contains metadata related to College.
        """
        verbose_name_plural = "Colleges"
        ordering = ["college_name"]

    def __str__(self):
        """
        Returns the colleges name when executed.
        """
        return self.college_name


class Department(models.Model):
    """
    Stores a single Department, related to :model:`user.Department`.
    """
    department_name = models.CharField(max_length=200)

    college_name = models.ForeignKey(
        College, default=1, verbose_name="College",
        on_delete=models.CASCADE)

    class Meta:
        """
        Contains metadata related to Department.
        """
        verbose_name_plural = "Departments"
        ordering = ["department_name"]

    def __str__(self):
        """
        Returns the departments name when executed.
        """
        return self.department_name


class Course(models.Model):
    """
    Stores a single Course, related to :model:`user.Course`.
    """
    course_title = models.CharField(max_length=200)
    level = models.CharField(max_length=200)
    campus = models.CharField(max_length=200)

    department_name = models.ForeignKey(
        Department, default=1, verbose_name="Department",
        on_delete=models.CASCADE)

    class Meta:
        """
        Contains metadata related to College.
        """
        verbose_name_plural = "Courses"
        ordering = ["department_name"]

    def __str__(self):
        """
        Returns the courses name when executed.
        """
        return self.course_title


class Module(models.Model):
    """
    Stores a single Module, related to :model:`user.Module`.
    """
    module_title = models.CharField(max_length=200)
    module_code = models.CharField(max_length=200, unique=True)
    module_year = models.IntegerField()
    module_credit_value = models.IntegerField()
    module_convenor = models.CharField(max_length=200)
    module_descriptor_URL = models.CharField(max_length=200)
    module_FCH_available = models.BooleanField(default=True)

    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        """
        Contains metadata related to Module.
        """
        verbose_name_plural = "Modules"
        ordering = ["module_code"]

    def __str__(self):
        """
        Returns the modules name when executed.
        """
        return self.module_code + " " + self.module_title


def upload_to(instance: Any, filename: str) -> str:
    return "profile_pictures/%s.%s" % (uuid.uuid4(), filename.split(".")[-1])


class UserProfile(models.Model):
    """
    Stores a single User Profile, related to :model:`users.Module`.
    """

    # user uses a one-to-one field to relate UserProfile to the default django User model
    user = models.OneToOneField(User, related_name="profile", on_delete=models.CASCADE)
    date_of_birth = models.DateField(verbose_name="date of birth", default=datetime.date.today)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # strictly student attributes
    admission_date = models.DateField(verbose_name="admission date", default=datetime.date.today)
    profile_pic = models.ImageField(upload_to=upload_to, default="profile_pictures/default.png")
    bio = models.CharField(max_length=500, blank=True)

    # Course and modules
    course_title = models.ForeignKey(Course, on_delete=models.DO_NOTHING, blank=True, null=True)
    modules = models.ManyToManyField(Module, blank=True)

    # Leaderboard
    LEADERBOARD_PRIVACY_CHOICES = [
        ("HIDE", "Hide entirely"),
        ("INITIALS", "Show initials only"),
        ("FIRST_NAME", "Show first name only"),
        ("FULL_NAME", "Show full name")
    ]
    leaderboard_privacy = models.CharField(choices=LEADERBOARD_PRIVACY_CHOICES,
                                           default="HIDE", max_length=20)

    forum_score = models.IntegerField(default=0, validators=[MinValueValidator(0)])

    def update_forum_score(self, value: int) -> None:
        """Update the forum score, not letting it drop below 0."""

        if self.forum_score + value < 0:
            self.forum_score = 0
        else:
            self.forum_score += value
        self.save()

    class Meta:
        verbose_name = "user profile"
        verbose_name_plural = "user profiles"

    def __str__(self):
        """
        String function to return a user's username.
        """

        return self.user.username


@receiver(post_save, sender=User)
def create_user_profile(sender, instance: User,
                        created: bool, **kwargs) -> None:
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance: User, **kwargs) -> None:
    try:
        UserProfile.objects.get(user=instance).save()
    except UserProfile.DoesNotExist:
        UserProfile.objects.create(user=instance)
