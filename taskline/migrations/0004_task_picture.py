# Generated by Django 3.2.3 on 2021-07-23 13:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('taskline', '0003_task_memo'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='picture',
            field=models.FileField(blank=True, upload_to='student/'),
        ),
    ]