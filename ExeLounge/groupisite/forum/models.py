from datetime import date

from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver
from users.models import Department, Module, UserProfile


class ForumSection(models.Model):
    """Represents a collection of threads."""

    name = models.CharField(verbose_name="section name", max_length=100)
    description = models.TextField(verbose_name="section description",
                                   blank=True)
    CATEGORY_CHOICES = [
        ("ACADEMIC", "Academic"),
        ("GUILD", "Students' Guild"),
        ("SOCIAL", "Social"),
        ("WELLBEING", "Wellbeing")
    ]
    category = models.CharField(choices=CATEGORY_CHOICES, max_length=20)

    # Used to determine the URL of this section
    url_slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "forum section"
        verbose_name_plural = "forum sections"

    def __str__(self):
        return self.name


class ForumThread(models.Model):
    """Represents a thread of posts."""

    name = models.CharField(verbose_name="thread name", max_length=100)
    description = models.TextField(verbose_name="thread description",
                                   blank=True)

    # The parent section
    section = models.ForeignKey(ForumSection, on_delete=models.CASCADE)

    # Used to determine the URL of this section
    url_slug = models.SlugField(unique=True)

    class Meta:
        verbose_name = "forum thread"
        verbose_name_plural = "forum threads"

    def __str__(self):
        return self.name


class DepartmentForumThread(ForumThread):
    """Represents a ForumThread that's tied to a department."""

    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "department forum thread"
        verbose_name_plural = "department forum threads"


class ModuleForumThread(ForumThread):
    """Represents a ForumThread that's tied to a module."""

    module = models.ForeignKey(Module, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "module forum thread"
        verbose_name_plural = "module forum threads"


class ForumPost(models.Model):
    """Represents a post in the forum."""

    title = models.CharField(verbose_name="post title", max_length=100)
    body = models.TextField(verbose_name="post body", blank=True)
    date = models.DateTimeField(verbose_name="date & time posted", auto_now_add=True)

    # Used to determine the URL of this section
    url_slug = models.SlugField(unique=True)

    # The parent thread
    thread = models.ForeignKey(ForumThread, on_delete=models.CASCADE)

    # The author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(verbose_name="post anonymously?",
                                       default=False)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"

        # Sort in descending order, newest first
        ordering = ["-date"]

    def __str__(self):
        return self.title + " by " + self.author.username


class ForumReply(models.Model):
    """Represents a reply to a post in a forum."""

    body = models.TextField(verbose_name="reply body")
    date = models.DateTimeField(verbose_name="date & time posted", auto_now_add=True)

    # The post that this reply is attributed to
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)

    # The author
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    is_anonymous = models.BooleanField(verbose_name="reply anonymously?",
                                       default=False)

    class Meta:
        verbose_name = "reply"
        verbose_name_plural = "replies"

        # Sort in ascending order, oldest first
        ordering = ["date"]

    def __str__(self):
        return "Reply by " + self.author.username + " to " + self.post.title


class ForumVote(models.Model):
    """Represents an up or down vote."""

    date = models.DateField(verbose_name="date voted", default=date.today)

    # True for up vote, False for down vote
    direction = models.BooleanField(verbose_name="Upvote?")

    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        abstract = True


class PostVote(ForumVote):
    """Represents an up or down vote to a forum post."""

    # The post that's being up or down voted
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE)

    class Meta:
        # No user can vote more than once on a post
        constraints = [
            models.UniqueConstraint(fields=["post", "user"],
                                    name="unique_user_post_voter")
        ]

    def __str__(self):
        if self.direction is True:
            return "+1 on " + self.post.title + " by " + self.user.username
        else:
            return "-1 on " + self.post.title + " by " + self.user.username


class ReplyVote(ForumVote):
    """Represents an up or down vote to a forum post."""

    # The reply that's being up or down voted
    reply = models.ForeignKey(ForumReply, on_delete=models.CASCADE)

    class Meta:
        # No user can vote more than once on a reply
        constraints = [
            models.UniqueConstraint(fields=["reply", "user"],
                                    name="unique_user_reply_voter")
        ]

    def __str__(self):
        if self.direction is True:
            return "+1 on a reply to " + self.reply.post.title + " by " + self.user.username
        else:
            return "-1 on a reply to " + self.reply.post.title + " by " + self.user.username


def update_forum_score(sender, instance, direction):
    """Update the forum score, either increment or decrement."""

    if direction != -1 and direction != 1:
        raise ValueError("direction can only be -1 or 1!")

    # +5 for a post
    if sender.__name__ == "ForumPost":
        UserProfile.objects.get(user=instance.author).update_forum_score(5 * direction)

    # +3 for a reply
    elif sender.__name__ == "ForumReply":
        UserProfile.objects.get(user=instance.author).update_forum_score(3 * direction)

    # +1 for an up vote, -1 for a down vote on own post
    elif sender.__name__ == "PostVote" and instance.direction is True:
        user = UserProfile.objects.get(user=instance.post.author)
        if instance.direction is True:
            user.update_forum_score(1 * direction)
        else:
            user.update_forum_score(-1 * direction)

    # +1 for an up vote, -1 for a down vote on own reply
    elif sender.__name__ == "ReplyVote" and instance.direction is True:
        user = UserProfile.objects.get(user=instance.reply.author)
        if instance.direction is True:
            user.update_forum_score(1 * direction)
        else:
            user.update_forum_score(-1 * direction)

    else:
        pass


@receiver(post_save, sender=ForumPost)
@receiver(post_save, sender=ForumReply)
@receiver(post_save, sender=PostVote)
@receiver(post_save, sender=ReplyVote)
def increase_forum_score(sender, instance, **kwargs):
    """Increase the forum score when any of the above is created."""

    # Only run on object creation
    if kwargs.get("created", True) is False:
        return

    update_forum_score(sender, instance, 1)


@receiver(pre_delete, sender=ForumPost)
@receiver(pre_delete, sender=ForumReply)
@receiver(pre_delete, sender=PostVote)
@receiver(pre_delete, sender=ReplyVote)
def decrease_forum_score(sender, instance, **kwargs):
    """Decrease the forum score when any of the above is deleted."""

    update_forum_score(sender, instance, -1)
