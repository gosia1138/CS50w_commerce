# Generated by Django 3.2 on 2021-06-11 04:49

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_auto_20210602_1514'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.IntegerField(blank=True, choices=[(1, 'Electronics'), (2, 'Fashion'), (3, 'House & Garden'), (4, 'Beauty'), (5, 'Health'), (6, 'Culture & Entertainment'), (7, 'Sport & Outdors'), (8, 'Moto'), (9, 'Art & Collectibles'), (99, 'Other')]),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(default='default.jpg', upload_to='profile_pics')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
