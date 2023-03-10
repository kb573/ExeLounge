# Generated by Django 3.1.7 on 2021-02-25 16:59

import datetime

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ForumPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='post title')),
                ('body', models.TextField(blank=True, verbose_name='post body')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date posted')),
                ('url_slug', models.SlugField(unique=True)),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='post anonymously?')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'post',
                'verbose_name_plural': 'replies',
                'ordering': ['-date'],
            },
        ),
        migrations.CreateModel(
            name='ForumReply',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', models.TextField(verbose_name='post body')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date posted')),
                ('is_anonymous', models.BooleanField(default=False, verbose_name='reply anonymously?')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forumpost')),
            ],
            options={
                'verbose_name': 'reply',
                'verbose_name_plural': 'replies',
                'ordering': ['date'],
            },
        ),
        migrations.CreateModel(
            name='ForumSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='section name')),
                ('description', models.TextField(blank=True, verbose_name='section description')),
                ('url_slug', models.SlugField(unique=True)),
            ],
            options={
                'verbose_name': 'forum section',
                'verbose_name_plural': 'forum sections',
            },
        ),
        migrations.CreateModel(
            name='ForumThread',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='thread name')),
                ('description', models.TextField(blank=True, verbose_name='thread description')),
                ('url_slug', models.SlugField(unique=True)),
                ('section', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forumsection')),
            ],
            options={
                'verbose_name': 'forum thread',
                'verbose_name_plural': 'forum threads',
            },
        ),
        migrations.CreateModel(
            name='CollegeForumThread',
            fields=[
                ('forumthread_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='forum.forumthread')),
            ],
            options={
                'verbose_name': 'college forum thread',
                'verbose_name_plural': 'college forum threads',
            },
            bases=('forum.forumthread',),
        ),
        migrations.CreateModel(
            name='DepartmentForumThread',
            fields=[
                ('forumthread_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='forum.forumthread')),
            ],
            options={
                'verbose_name': 'department forum thread',
                'verbose_name_plural': 'department forum threads',
            },
            bases=('forum.forumthread',),
        ),
        migrations.CreateModel(
            name='ModuleForumThread',
            fields=[
                ('forumthread_ptr',
                 models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True,
                                      primary_key=True, serialize=False, to='forum.forumthread')),
            ],
            options={
                'verbose_name': 'module forum thread',
                'verbose_name_plural': 'module forum threads',
            },
            bases=('forum.forumthread',),
        ),
        migrations.CreateModel(
            name='ReplyVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date voted')),
                ('direction', models.BooleanField(verbose_name='Upvote?')),
                ('reply', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forumreply')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PostVote',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=datetime.date.today, verbose_name='date voted')),
                ('direction', models.BooleanField(verbose_name='Upvote?')),
                ('post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forumpost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='forumpost',
            name='thread',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='forum.forumthread'),
        ),
        migrations.AddConstraint(
            model_name='replyvote',
            constraint=models.UniqueConstraint(fields=('reply', 'user'), name='unique_user_reply_voter'),
        ),
        migrations.AddConstraint(
            model_name='postvote',
            constraint=models.UniqueConstraint(fields=('post', 'user'), name='unique_user_post_voter'),
        ),
        migrations.AddField(
            model_name='moduleforumthread',
            name='module',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.module'),
        ),
        migrations.AddField(
            model_name='departmentforumthread',
            name='department',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.department'),
        ),
        migrations.AddField(
            model_name='collegeforumthread',
            name='college',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.college'),
        ),
    ]
