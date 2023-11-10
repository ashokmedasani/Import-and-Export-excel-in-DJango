# Generated by Django 4.2.3 on 2023-11-10 10:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ipxp', '0002_exceldata'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExcelIndividual',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('excel_file', models.FileField(upload_to='excel_files/')),
            ],
        ),
    ]