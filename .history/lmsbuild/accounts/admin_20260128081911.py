from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, TeacherProfile, Batch, Student, StaffProfile, Content, Course, Post



# ================= CUSTOM USER =================

class CustomUserAdmin(UserAdmin):

    list_display = ("username","role","email","is_active")
    list_filter = ("role","is_active")

    fieldsets = UserAdmin.fieldsets + (
        ("Extra Info", {"fields": ("role","mobile","profile_pic")}),
    )

admin.site.register(User, CustomUserAdmin)


# ================= TRAINER =================

class TeacherProfileAdmin(admin.ModelAdmin):

    list_display = ("user","emp_id","subject","is_active")
    search_fields = ("user__username","emp_id","subject")


admin.site.register(TeacherProfile, TeacherProfileAdmin)


# ================= BATCH =================

class BatchAdmin(admin.ModelAdmin):

    list_display = ("name","trainer","created_at","is_active")
    list_filter = ("trainer","is_active")
    search_fields = ("name",)


admin.site.register(Batch, BatchAdmin)


# ================= STUDENT =================

class StudentAdmin(admin.ModelAdmin):

    list_display = ("user","roll_no","trainer","batch","is_active")
    list_filter = ("trainer","batch","is_active")
    search_fields = ("user__username","roll_no")

    def save_model(self, request, obj, form, change):
        # Auto batch assign from trainer
        if obj.trainer and not obj.batch:   
            obj.batch = obj.trainer.batches.first()
        super().save_model(request, obj, form, change)


admin.site.register(Student, StudentAdmin)


# ================= STAFF =================

class StaffProfileAdmin(admin.ModelAdmin):

    list_display = ("user","emp_id","department","position")
    search_fields = ("user__username","emp_id")


admin.site.register(StaffProfile, StaffProfileAdmin)



from .models import Course, Content


class CourseAdmin(admin.ModelAdmin):
    list_display = ("title","trainer","created_at")
    list_filter = ("trainer",)


class ContentAdmin(admin.ModelAdmin):
    list_display = ("title","course","created_at")
    list_filter = ("course",)


admin.site.register(Course, CourseAdmin)
admin.site.register(Content, ContentAdmin)




class PostAdmin(admin.ModelAdmin):
    list_display = ("title","trainer","created_at")
    list_filter = ("trainer",)
    search_fields = ("title",)


admin.site.register(Post, PostAdmin)
