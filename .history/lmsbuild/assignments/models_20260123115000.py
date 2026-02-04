from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    )

    title = models.CharField(max_length=200)
    course = models.ForeignKey("courses.Course", on_delete=models.CASCADE)
    total_marks = models.IntegerField()
    pass_marks = models.IntegerField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(models.Model):
    assignment = models.ForeignKey(
        Assignment, related_name="questions", on_delete=models.CASCADE
    )
    text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_option = models.CharField(max_length=1)
    marks = models.IntegerField(default=1)

    def __str__(self):
        return self.text[:50]


class Submission(models.Model):
    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    student = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField(default=0)
    attempt_number = models.IntegerField(default=1)
    status = models.CharField(max_length=20, default="started")
    started_at = models.DateTimeField(null=True)
    submitted_at = models.DateTimeField(null=True)

    def __str__(self):
        return f"{self.student} - {self.assignment}"


class Answer(models.Model):
    submission = models.ForeignKey(
        Submission, related_name="answers", on_delete=models.CASCADE
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.CharField(max_length=1)
    is_correct = models.BooleanField(default=False)
