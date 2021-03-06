# Generated by Django 2.1.3 on 2018-12-09 18:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0007_three_slide_news'),
    ]

    operations = [
        migrations.CreateModel(
            name='Special_offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('new', models.BooleanField(default=True)),
                ('sale', models.BooleanField(default=True)),
                ('best_selling', models.BooleanField(default=True)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.Product')),
            ],
        ),
    ]
