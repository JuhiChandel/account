from django.contrib import admin
from register.models import Register, User_ver, Student
# Register your models here.


class RegisterAdmin(admin.ModelAdmin):
   list_display = ['user', 'email', 'password', 'confirm_password']
   search_fields = ['user', 'email', 'password', 'confirm_password']


class UserAdmin(admin.ModelAdmin):
    list_display = ['user',  'otp', 'is_verified']
    search_fields = ['user', 'otp', 'is_verified']


class StudentAdmin(admin.ModelAdmin):
   list_display = ['enroll', 'name', 'class1', 'stream', 'father', 'dob', 'add']
   search_fields = ['enroll', 'name', 'class1', 'stream', 'father', 'dob', 'add']

admin.site.register(Register, RegisterAdmin)
admin.site.register(User_ver, UserAdmin)
admin.site.register(Student, StudentAdmin)