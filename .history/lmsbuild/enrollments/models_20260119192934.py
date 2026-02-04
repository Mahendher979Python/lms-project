from django.db import models

class Enrollment(models.Model):
    student = models.ForeignKey(
        "accounts.StudentProfile",
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE
    )
    joined_at = models.DateTimeField(auto_now_add=True)


class LessonProgress(models.Model):
    enrollment = models.ForeignKey(
        Enrollment,
        on_delete=models.CASCADE
    )
    lesson = models.ForeignKey(
        "courses.Lesson",
        on_delete=models.CASCADE
    )
    completed = models.BooleanField(default=False)
