# Generated by Django 4.0.6 on 2022-08-11 16:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('eor', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('bill_number', models.CharField(max_length=200)),
                ('seller', models.CharField(max_length=200)),
                ('last_updated', models.DateTimeField(verbose_name='last updated')),
                ('tax_level', models.FloatField()),
                ('zoi', models.CharField(max_length=200)),
                ('status', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('address', models.CharField(max_length=200)),
                ('post_office', models.CharField(max_length=200)),
                ('ddv_id', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product_title', models.CharField(max_length=200)),
                ('quantity', models.IntegerField()),
                ('value', models.FloatField()),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='racuni.bill')),
            ],
        ),
        migrations.AddField(
            model_name='bill',
            name='producer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='racuni.company'),
        ),
    ]
