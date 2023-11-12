from django.db import models

# Create your models here.
class person(models.Model):
    Name = models.CharField(max_length=50)
    Age = models.IntegerField()
    Contact = models.CharField(max_length=13)

class ExcelData(models.Model):
    file = models.FileField(upload_to='uploads/')

class File(models.Model):
    name = models.CharField(max_length=255)
    deleted = models.BooleanField(default=False)

class ExcelIndividual(models.Model):
    user_name = models.CharField(max_length=255)
    excel_file = models.FileField(upload_to='excel_files/')

    def __str__(self):
        return self.user_name
    
class UserData(models.Model):
    username = models.CharField(max_length=255)
    excel_file = models.FileField(upload_to='uploads/')