from django import  forms



class Register(models.Model):

    user = models. CharField(max_length=100)
    email = models. CharField(max_length=50)
    password = models. CharField(max_length=10)