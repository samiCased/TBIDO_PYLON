# Generated by Django 4.2.11 on 2025-04-18 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_eventschedule_lineup_member10_age_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartnerLogo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='tbido_partner_logos/')),
            ],
        ),
    ]
