# Generated by Django 4.1.7 on 2023-05-22 20:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='certificate',
            fields=[
                ('courseid', models.AutoField(primary_key=True, serialize=False)),
                ('cname', models.CharField(max_length=64)),
                ('ccompany', models.CharField(max_length=64)),
            ],
        ),
        migrations.CreateModel(
            name='granted',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('grantedDate', models.DateField(null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Food.certificate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='certificate',
            name='users',
            field=models.ManyToManyField(blank=True, through='Food.granted', to=settings.AUTH_USER_MODEL),
        ),
    ]