# Generated by Django 5.1.6 on 2025-02-16 19:50

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cardgame', '0014_alter_card_card_image_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_image_link',
            field=models.ImageField(default='static/card_images/do_not_remove.png', upload_to='cardgame/static/card_images'),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400)),
                ('challenge', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cardgame.challenge')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=400)),
                ('correct', models.BooleanField()),
                ('question', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='cardgame.question')),
            ],
        ),
    ]
