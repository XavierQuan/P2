# Generated by Django 5.0.2 on 2024-03-04 04:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PendingMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_limit', models.DateTimeField()),
                ('message', models.TextField()),
                ('title', models.CharField(max_length=255)),
                ('deadline', models.DateTimeField()),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.BooleanField()),
                ('content', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meeting.pendingmeeting')),
            ],
        ),
        migrations.CreateModel(
            name='FinalizedMeeting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('time', models.DateTimeField()),
                ('time_limit', models.DateTimeField()),
                ('participant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('meeting', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='Meeting.pendingmeeting')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meeting.pendingmeeting')),
            ],
        ),
        migrations.CreateModel(
            name='SuggestedTimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.DateTimeField()),
                ('duration', models.DurationField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meeting.suggestedschedule')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TimeSlot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.DateTimeField()),
                ('priority', models.IntegerField()),
                ('meeting', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Meeting.pendingmeeting')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
