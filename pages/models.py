from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    mobile = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    content = models.TextField()

    def __str__(self):
        return self.name

