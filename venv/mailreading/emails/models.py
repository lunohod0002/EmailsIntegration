from django.db import models


class User(models.Model):
    login = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)

    def __str__(self):
        return self.login


class Email(models.Model):
    theme = models.CharField(max_length=255)
    date_of_dispatch = models.DateField()
    date_of_receive = models.DateField()
    description = models.TextField()
    files = models.CharField(max_length=255,default=None)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.theme


class File(models.Model):
    file = models.BinaryField()
    filename = models.CharField(max_length=255)
    email = models.ForeignKey(Email, on_delete=models.CASCADE, null=True)


class EmailFile(models.Model):
    email_file = models.ForeignKey(File, on_delete=models.CASCADE)
    email = models.ForeignKey(Email, on_delete=models.CASCADE)
