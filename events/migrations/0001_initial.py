# Generated by Django 4.0.4 on 2022-05-15 13:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contracts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventStatus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=64)),
            ],
            options={
                'verbose_name': 'Event Status',
                'verbose_name_plural': 'Event Status',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('attendees', models.IntegerField()),
                ('event_date', models.DateTimeField()),
                ('notes', models.CharField(blank=True, max_length=256)),
                ('contract', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contracts.contract')),
                ('status', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='events.eventstatus')),
                ('support_contact', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
