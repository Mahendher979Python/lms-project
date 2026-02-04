from .models import Enrollment

def is_enrolled(student, course):
    return Enrollment.objects.filter(
        student=student,
        course=course,
        is_active=True
    ).exists()
