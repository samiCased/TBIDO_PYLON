# Generated by Django 4.2.11 on 2025-04-19 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_session_banner'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advisory',
            name='calendar_plot_img',
        ),
        migrations.RemoveField(
            model_name='advisory',
            name='gantt_plot_img',
        ),
    ]
