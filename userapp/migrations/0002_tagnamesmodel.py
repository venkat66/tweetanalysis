# Generated by Django 4.0.5 on 2022-07-01 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userapp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='TagNamesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tagname', models.CharField(help_text='tagname', max_length=100)),
                ('count', models.BigIntegerField(help_text='Number_of_searches')),
                ('data', models.DateField(auto_now_add=True)),
            ],
            options={
                'db_table': 'tag_names',
            },
        ),
    ]
