# Generated by Django 4.1.3 on 2023-11-22 03:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0002_remove_refund_id1'),
    ]

    operations = [
        migrations.CreateModel(
            name='refund_req',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id1', models.IntegerField()),
                ('menter_name', models.CharField(max_length=100)),
                ('mentee_name', models.CharField(max_length=100)),
                ('order_date', models.DateTimeField(auto_now_add=True)),
                ('resone', models.CharField(max_length=200)),
                ('api', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.appointment')),
            ],
        ),
    ]