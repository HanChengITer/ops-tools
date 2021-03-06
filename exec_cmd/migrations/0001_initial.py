# Generated by Django 2.0.6 on 2018-06-05 14:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ExecCmd',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hosts', models.CharField(blank=True, max_length=200, null=True)),
                ('cmd', models.CharField(max_length=200)),
                ('date_added', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='ExecRecord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_executed', models.DateTimeField(auto_now_add=True)),
                ('result', models.CharField(choices=[('0', 'successed'), ('1', 'failed')], max_length=1)),
                ('cmd', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exec_cmd.ExecCmd')),
            ],
        ),
    ]
