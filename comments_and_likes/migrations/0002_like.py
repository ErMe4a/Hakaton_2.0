# Generated by Django 3.2 on 2022-08-24 14:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('dishes', '0001_initial'),
        ('comments_and_likes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dishes', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='likes', to='dishes.dishes')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='liked', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('dishes', 'owner')},
            },
        ),
    ]
