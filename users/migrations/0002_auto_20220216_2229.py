# Generated by Django 3.2.12 on 2022-02-16 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='userdetails',
            name='user_detail_user_na_df87f9_idx',
        ),
        migrations.RenameField(
            model_name='userdetails',
            old_name='user_name',
            new_name='username',
        ),
        migrations.AddIndex(
            model_name='userdetails',
            index=models.Index(fields=['username'], name='user_detail_usernam_ce5008_idx'),
        ),
    ]
