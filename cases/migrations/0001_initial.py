# Generated by Django 3.0.7 on 2020-07-09 13:23

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
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('case_image', models.ImageField(upload_to='cases/', verbose_name='Изображение')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('url', models.SlugField(default='aaa', verbose_name='ссылка')),
            ],
            options={
                'verbose_name': 'Кесй',
                'verbose_name_plural': 'Кейсы',
            },
        ),
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('item_image', models.ImageField(upload_to='items/', verbose_name='Изображение')),
                ('rarity', models.IntegerField(verbose_name='Редкость')),
                ('price', models.IntegerField(verbose_name='Цена')),
                ('url', models.SlugField(default='aaa', verbose_name='ссылка')),
            ],
            options={
                'verbose_name': 'Шмотка',
                'verbose_name_plural': 'Шмотки',
            },
        ),
        migrations.CreateModel(
            name='User_info',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.IntegerField(default=0, verbose_name='баланс')),
                ('avatar', models.ImageField(default='default.jpg', upload_to='avatars/', verbose_name='Изображение')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Информация пользователя',
                'verbose_name_plural': 'Информация пользователей',
            },
        ),
        migrations.CreateModel(
            name='Useritems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Items')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.User_info')),
            ],
            options={
                'verbose_name': 'Предмет пользователя',
                'verbose_name_plural': 'Предметы пользователя',
            },
        ),
        migrations.AddField(
            model_name='user_info',
            name='user_items',
            field=models.ManyToManyField(related_name='user_items', through='cases.Useritems', to='cases.Items', verbose_name='вещи'),
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Название')),
                ('image', models.ImageField(upload_to='categories/', verbose_name='Изображение')),
                ('cases', models.ManyToManyField(related_name='cases', to='cases.Case', verbose_name='Кейсы')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
            },
        ),
        migrations.CreateModel(
            name='Casesitems',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_droprate', models.FloatField(verbose_name='Шанс дропа')),
                ('amount', models.IntegerField(verbose_name='Количество')),
                ('case', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Case')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cases.Items')),
            ],
            options={
                'verbose_name': 'Наполнение кейса',
                'verbose_name_plural': 'Наполнение кейсов',
            },
        ),
        migrations.AddField(
            model_name='case',
            name='cases_items',
            field=models.ManyToManyField(related_name='cases_items', through='cases.Casesitems', to='cases.Items', verbose_name='Предеметы'),
        ),
    ]
