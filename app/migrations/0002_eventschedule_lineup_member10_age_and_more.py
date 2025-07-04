# Generated by Django 4.2.11 on 2025-04-18 09:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EventSchedule',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event_name', models.CharField(max_length=255)),
                ('event_time_start', models.DateTimeField()),
                ('event_time_end', models.DateTimeField(blank=True, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member10_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member11_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member12_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member3_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member4_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member5_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member6_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member7_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member8_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_age',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_amount_paid',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_employee_number',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_employment',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lineup',
            name='member9_rank',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='logo',
            name='image',
            field=models.ImageField(upload_to='tbido_pylon_logo/'),
        ),
    ]
