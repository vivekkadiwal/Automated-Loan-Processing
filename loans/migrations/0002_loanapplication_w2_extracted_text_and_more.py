# Generated by Django 5.0.1 on 2024-11-13 05:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('loans', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='loanapplication',
            name='w2_extracted_text',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='loanapplication',
            name='w2_image',
            field=models.ImageField(blank=True, null=True, upload_to='w2_forms/'),
        ),
    ]
