from django import template
from cases.models import Case, Items, Category, User_info
from django.contrib.auth import get_user_model
from random import choices

User = get_user_model()

register = template.Library()

@register.simple_tag()
def get_cases():
    """Вывод всех категорий"""
    return Case.objects.all()

@register.simple_tag()
def get_ctgs():
    """Вывод всех категорий"""
    return Category.objects.all()

@register.simple_tag()
def get_users():
    """Вывод всех категорий"""
    return User.objects.all()

@register.simple_tag()
def get_items():
    """Вывод всех категорий"""
    return Items.objects.all()

