from django.db import models
from datetime import datetime
from django.urls import reverse
from django.contrib.auth import get_user_model
#python manage.py runserver
# python manage.py makemigrations
# python manage.py migrate

User = get_user_model()

class Items(models.Model):
    name = models.CharField("Название", max_length=100)
    item_image = models.ImageField("Изображение", upload_to="items/")
    rarity = models.IntegerField('Редкость')
    price = models.IntegerField('Цена')
    url = models.SlugField('ссылка', default='aaa')

    class Meta:
        verbose_name = "Шмотка"
        verbose_name_plural = "Шмотки"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("item_detail", kwargs={"slug": self.url})

    def get_color(self):
        return self.rarity == 1

class Case(models.Model):
    name = models.CharField("Название", max_length=100)
    cases_items = models.ManyToManyField(Items, verbose_name="Предеметы", related_name="cases_items", through='Casesitems')
    case_image = models.ImageField("Изображение", upload_to="cases/")
    price = models.IntegerField('Цена')
    url = models.SlugField('ссылка', default='aaa')

    class Meta:
        verbose_name = "Кесй"
        verbose_name_plural = "Кейсы"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("case_detail", kwargs={"slug": self.url})

    def getamount(self):
        a = 0
        f = []
        for el in Casesitems.objects.filter(case=self.id).all():
            a = a + el.amount
            f.append(el.amount)
        #if a > 0:
        return a
        #№else:
            #return False

class User_info(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.IntegerField('баланс',default=0)
    user_items = models.ManyToManyField(Items, verbose_name="вещи", related_name="user_items", through='Useritems')
    avatar = models.ImageField("Изображение", upload_to="avatars/", default='default.jpg')

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = "Информация пользователя"
        verbose_name_plural = "Информация пользователей"

    def get_absolute_url(self):
        return reverse("user_detail", kwargs={"pk": self.user.id})

class Casesitems(models.Model):
    case = models.ForeignKey(Case, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    item_droprate = models.FloatField('Шанс дропа')
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = "Наполнение кейса"
        verbose_name_plural = "Наполнение кейсов"

    def __str__(self):
        return self.case.name + '    ' +  self.item.name

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    cases = models.ManyToManyField(Case, verbose_name="Кейсы", related_name="cases")
    image = models.ImageField("Изображение", upload_to="categories/")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name

class Useritems(models.Model):
    user = models.ForeignKey(User_info, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    amount = models.IntegerField('Количество')

    class Meta:
        verbose_name = "Предмет пользователя"
        verbose_name_plural = "Предметы пользователя"

    def __str__(self):
        return self.user.user.username
