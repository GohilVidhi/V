# Generated by Django 4.2.4 on 2023-12-08 09:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0005_add_work_mentor_user_add_profile'),
    ]

    operations = [
        migrations.CreateModel(
            name='mentee_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50)),
                ('password', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='mentee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='img')),
                ('name', models.CharField(max_length=50)),
                ('email', models.EmailField(max_length=50)),
                ('title', models.CharField(max_length=50)),
                ('headline', models.CharField(max_length=50)),
                ('about_you', models.TextField()),
                ('country', models.CharField(blank=True, max_length=50, null=True)),
                ('state', models.CharField(blank=True, max_length=50, null=True)),
                ('city', models.CharField(blank=True, max_length=50, null=True)),
                ('cou', models.CharField(max_length=50)),
                ('sta', models.CharField(max_length=50)),
                ('cit', models.CharField(max_length=50)),
                ('languages', models.CharField(max_length=50)),
                ('ex_education', models.CharField(blank=True, max_length=50, null=True)),
                ('add_work', models.CharField(max_length=1000)),
                ('add_education', models.CharField(blank=True, max_length=1000, null=True)),
                ('blocked', models.BooleanField(default=False)),
                ('ecategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.expertise')),
                ('mcategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.main_category')),
                ('scategory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='myapp.sub_category')),
            ],
        ),
    ]