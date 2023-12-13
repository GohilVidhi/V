# Generated by Django 4.1.3 on 2023-11-21 12:23

from django.db import migrations, models
import django.db.models.deletion
import myapp.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='admin_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=40, unique=True)),
                ('password', models.CharField(max_length=10)),
                ('otp', models.IntegerField(default=1234)),
            ],
        ),
        migrations.CreateModel(
            name='appointment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.IntegerField(default=myapp.models.generate_random_number, unique=True)),
                ('menter_name', models.CharField(max_length=100)),
                ('mentee_name', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField()),
                ('status', models.CharField(choices=[('upcoming', 'Upcoming'), ('confirmed', 'Confirmed'), ('canceled', 'Canceled')], default='upcoming', max_length=10)),
                ('payment', models.CharField(choices=[('panding', 'panding'), ('refunded', 'refunded')], default='panding', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='ChartData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=100)),
                ('value', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='main_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(blank=True, null=True, upload_to='img')),
            ],
        ),
        migrations.CreateModel(
            name='order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='price',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='session',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='sub_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='img')),
                ('name', models.CharField(max_length=30)),
                ('mcategory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.main_category')),
            ],
        ),
        migrations.CreateModel(
            name='refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.IntegerField(default=1234)),
                ('menter_name', models.CharField(max_length=100)),
                ('mentee_name', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('resone', models.CharField(max_length=200)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.appointment')),
            ],
        ),
        migrations.CreateModel(
            name='expertise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('mcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.main_category')),
                ('scategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.sub_category')),
            ],
        ),
    ]
