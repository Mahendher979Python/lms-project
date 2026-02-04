from django.contrib import admin
from .models import Assignment, Question, Submission, Answer, Certificate


class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'course',
        'created_by',
        'status',
        'total_marks',
        'pass_marks',
        'created_at'
    )

    list_filter = ('status', 'course')
    search_fields = ('title', 'course__title')
    inlines = [QuestionInline]


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = (
        'assignment',
        'student',
        'attempt_number',
        'score',
        'status',
        'submitted_at'
    )

    list_filter = ('status', 'assignment')
    search_fields = ('student__username', 'assignment__title')


@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'submission',
        'question',
        'selected_option',
        'is_correct'
    )


@admin.register(Certificate)
class CertificateAdmin(admin.ModelAdmin):
    list_display = (
        'submission',
        'issued_at'
    )
