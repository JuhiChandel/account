from django.db import models


# Create your models here.


class Register(models.Model):
    user = models.CharField(max_length=100)
    email = models.EmailField()
    password = models.CharField(max_length=10)
    confirm_password = models.CharField(max_length=10)

    def __str__(self):
        return '%s - %s' % (self.user, self.email)


class User_ver(models.Model):
    user = models.ForeignKey(Register, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4, null=True, blank=True)
    is_verified = models.BooleanField(default=False)