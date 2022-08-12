# Generated by Django 4.0.4 on 2022-08-10 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0009_alter_post_author_remove_tag_related_posts_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tag',
            name='related_posts',
        ),
        migrations.AddField(
            model_name='post',
            name='tags',
            field=models.ManyToManyField(blank=True, null=True, to='posts.tag'),
        ),
    ]