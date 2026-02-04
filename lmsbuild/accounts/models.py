from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):

    ROLE_CHOICES = (
        ('superadmin','Super Admin'),
        ('admin','Admin'),
        ('trainer','Trainer'),
        ('student','Student'),
        ('staff','Staff'),
    )

    role = models.CharField(max_length=20,choices=ROLE_CHOICES)
    mobile = models.CharField(max_length=15,blank=True,null=True)
    profile_pic = models.ImageField(upload_to="profile_pics/",blank=True,null=True)

    def __str__(self):
        return self.username


# ================= TRAINER =================

class TeacherProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="teacher_profile")

    emp_id = models.CharField(max_length=20,unique=True)
    subject = models.CharField(max_length=100)

    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} - {self.subject}"


# ================= BATCH =================

class Batch(models.Model):

    name = models.CharField(max_length=100)

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="batches"
    )

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.trainer.subject})"





# ================= STUDENT =================
class Student(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE)

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE
    )

    batch = models.ForeignKey(
        Batch,
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    roll_no = models.CharField(max_length=50,unique=True)
    is_active = models.BooleanField(default=True)

    def save(self,*args,**kwargs):
        # AUTO batch from trainer
        if self.trainer and not self.batch:
            self.batch = self.trainer.batches.first()
        super().save(*args,**kwargs)

    def __str__(self):
        return self.user.username


# ================= STAFF =================

class StaffProfile(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name="staff_profile")
    emp_id = models.CharField(max_length=20,unique=True)
    department = models.CharField(max_length=100)
    position = models.CharField(max_length=100)

    def __str__(self):
        return self.user.username

# ================= COURSE =================

class Course(models.Model):

    title = models.CharField(max_length=200)
    trainer = models.ForeignKey(TeacherProfile,on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# ================= CONTENT =================

class Content(models.Model):

    course = models.ForeignKey(Course,on_delete=models.CASCADE,related_name="contents")
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to="course_content/")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


# ================= POSTS =================

class Post(models.Model):

    trainer = models.ForeignKey(
        TeacherProfile,
        on_delete=models.CASCADE,
        related_name="posts"
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)

    image = models.ImageField(upload_to="post_images/",blank=True,null=True)
    pdf = models.FileField(upload_to="post_pdfs/",blank=True,null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title




