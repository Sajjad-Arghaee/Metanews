# Generated by Django 4.0.4 on 2022-06-12 08:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=250, null=True)),
                ('short_intro', models.CharField(blank=True, max_length=250, null=True)),
                ('full_intro', models.TextField(blank=True, null=True)),
                ('email', models.EmailField(blank=True, max_length=250, null=True)),
                ('profile_image', models.ImageField(blank=True, default='images/profiles/default.png', null=True, upload_to='images/profiles/')),
                ('active_posts', models.IntegerField(blank=True, default=0, null=True)),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
