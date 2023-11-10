from django.db import models

# Create your models here.
class person(models.Model):
    Name = models.CharField(max_length=50)
    Age = models.IntegerField()
    Contact = models.CharField(max_length=13)

class ExcelData(models.Model):
    file = models.FileField(upload_to='uploads/')

class ExcelIndividual(models.Model):
    name = models.CharField(max_length=100)
    excel_file = models.FileField(upload_to='excel_files/')