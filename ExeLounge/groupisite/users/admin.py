from django.contrib import admin

# from django.contrib.auth.models import User
from .models import Module, Course, Department, College, UserProfile


@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
    list_display = ["college_name"]
    ordering = ["college_name"]


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("department_name", "college_name")
    list_filter = ["college_name"]
    ordering = ["department_name"]


@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ("__str__", "module_credit_value", "module_year",
                    "module_convenor", "module_FCH_available", "department")
    list_filter = ("module_credit_value", "module_FCH_available", "module_year", "department")
    list_editable = ["module_FCH_available"]
    ordering = ["module_code"]


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ("course_title", "level", "campus", "department_name")
    list_filter = ("level", "campus", "department_name")
    ordering = ["department_name"]


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "date_of_birth", "admission_date", "course_title",
                    "leaderboard_privacy", "forum_score")
    list_filter = ("course_title", "leaderboard_privacy")
    list_editable = ["leaderboard_privacy"]
