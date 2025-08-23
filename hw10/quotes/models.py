from django.db import models

# Create your models here.
class Author(models.Model):
    fullname=models.CharField(max_length=50)
    born_date=models.CharField(max_length=50)
    born_location=models.CharField(max_length=150)
    description=models.TextField()
    created=models.DateTimeField(auto_now_add=True)

class Tag(models.Model):
    name=models.CharField(max_length=30, null=False, unique=True)

class Quote(models.Model):
    tags=models.ManyToManyField(Tag)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, null=True, default=None)
    quote=models.TextField(null=False)
    created=models.DateTimeField(auto_now_add=True)