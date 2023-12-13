# Generated by Django 4.1.3 on 2023-12-08 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0004_refund_req_appointment_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Add_work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=30)),
                ('titel', models.CharField(max_length=30)),
                ('current_role', models.CharField(max_length=50)),
                ('start_month', models.CharField(max_length=50)),
                ('start_year', models.CharField(max_length=50)),
                ('end_month', models.CharField(max_length=50)),
                ('end_year', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Mentor_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Add_profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IMG', models.ImageField(upload_to='img')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('headline', models.CharField(max_length=50)),
                ('about_you', models.CharField(max_length=50)),
                ('cou', models.CharField(max_length=50)),
                ('sta', models.CharField(max_length=50)),
                ('cit', models.CharField(max_length=50)),
                ('lunguages', models.CharField(max_length=500)),
                ('links1', models.CharField(max_length=1000)),
                ('links2', models.CharField(max_length=1000)),
                ('ex_education', models.CharField(max_length=1000)),
                ('add_work', models.CharField(max_length=1000)),
                ('add_education', models.CharField(max_length=1000)),
                ('topics', models.CharField(max_length=1000)),
                ('price', models.CharField(choices=[(6000, 6000), (5000, 5000), (1000, 1000), (500, 500), (100, 100)], max_length=500)),
                ('durations', models.CharField(choices=[(6000, 6000), (5000, 5000), (1000, 1000), (500, 500), (100, 100)], max_length=1000)),
                ('topics_durations', models.CharField(max_length=1000)),
                ('blocked', models.BooleanField(default=False)),
                ('exp', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='myapp.expertise')),
                ('main', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.main_category')),
                ('sub', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.sub_category')),
            ],
        ),
    ]