# Generated by Django 4.0.4 on 2022-05-05 09:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('hsite', '0003_rename_header_question_title'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='datetime',
            new_name='pub_date',
        ),
    ]
