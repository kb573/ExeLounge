from django.contrib import admin

from .models import ForumSection, ForumThread, DepartmentForumThread, \
    ModuleForumThread, ForumPost, ForumReply, \
    PostVote, ReplyVote


@admin.register(ForumSection)
class ForumSectionAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "url_slug")


@admin.register(ForumThread)
class ForumThreadAdmin(admin.ModelAdmin):
    list_display = ("name", "section", "url_slug")


@admin.register(DepartmentForumThread)
class DepartmentForumThreadAdmin(admin.ModelAdmin):
    list_display = ("name", "department", "section", "url_slug")


@admin.register(ModuleForumThread)
class ModuleForumThreadAdmin(admin.ModelAdmin):
    list_display = ("name", "module", "section", "url_slug")


@admin.register(ForumPost)
class ForumPostAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "thread", "author", "is_anonymous",
                    "url_slug")
    list_filter = ("author", "is_anonymous")
    date_hierarchy = "date"


@admin.register(ForumReply)
class ForumReplyAdmin(admin.ModelAdmin):
    list_display = ("date", "post", "author", "is_anonymous")
    list_filter = ("author", "is_anonymous")
    date_hierarchy = "date"


@admin.register(PostVote)
class PostVoteAdmin(admin.ModelAdmin):
    list_display = ("date", "post", "user", "direction")
    list_filter = ("user", "direction")
    date_hierarchy = "date"


@admin.register(ReplyVote)
class ReplyVoteAdmin(admin.ModelAdmin):
    list_display = ("date", "reply", "user", "direction")
    list_filter = ("user", "direction")
    date_hierarchy = "date"
