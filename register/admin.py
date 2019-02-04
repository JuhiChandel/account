from django.contrib import admin
from register.models import Register, User_ver
# Register your models here.


class RegisterAdmin(admin.ModelAdmin):
   list_display = ['user', 'email', 'password', 'confirm_password']
   search_fields = ['user', 'email', 'password', 'confirm_password']


class UserAdmin(admin.ModelAdmin):
    list_display = ['user',  'otp', 'is_verified']
    search_fields = ['user', 'otp', 'is_verified']


admin.site.register(Register, RegisterAdmin)
admin.site.register(User_ver, UserAdmin)