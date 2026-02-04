from django.contrib import admin
from .models import Assignment, Question, Submission, Answer

@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'course',
        'created_by',
        'status',
        'total_marks',
        'pass_marks',
        'created_at',
    )
    list_filter = ('status', 'course')
    search_fields = ('title',)
    actions = ['approve_assignments', 'reject_assignments']

    def approve_assignments(self, request, queryset):
        queryset.update(status='approved')

    def reject_assignments(self, request, queryset):
        queryset.update(status='rejected')

    approve_assignments.short_description = "Approve selected assignments"
    reject_assignments.short_description = "Reject selected assignments"

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('assignment', 'question_text', 'correct_option', 'marks')
    list_filter = ('assignment',)
    search_fields = ('question_text',)

@admin.register(Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = (
        'submission',
        'question',
        'selected_option',
        'is_correct',
    )
    list_filter = ('is_correct',)
