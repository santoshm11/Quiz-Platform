from django.contrib import admin
from .models import CustomUser, Student, MCQQuestion, UserQuiz, Result
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

# Custom User Admin
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ("uucms_id", "email", "is_staff", "is_superuser")
    search_fields = ("uucms_id", "email")
    ordering = ("uucms_id",)
    
    fieldsets = (
        (None, {"fields": ("uucms_id", "email", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "phone_number")}),
        (_("Permissions"), {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")}),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("uucms_id", "email", "password1", "password2", "is_staff", "is_superuser"),
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# Student Admin
@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('uucms_id', 'name')
    search_fields = ('uucms_id', 'name')

# MCQQuestion Admin
@admin.register(MCQQuestion)
class MCQQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_name', 'category', 'correct_answer', 'duration')
    search_fields = ('question_name', 'category')

# UserQuiz Admin
@admin.register(UserQuiz)
class UserQuizAdmin(admin.ModelAdmin):
    list_display = ('uucms_id', 'question', 'answered_question', 'status', 'submitted_at')
    search_fields = ('uucms_id',)

# Result Admin
@admin.register(Result)
class ResultAdmin(admin.ModelAdmin):
    list_display = ('uucms_id', 'score')
    search_fields = ('uucms_id',)
