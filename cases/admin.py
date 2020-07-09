from django.contrib import admin
from .models import User_info, Case, Items, Casesitems, Category, Useritems

admin.site.register(User_info)
admin.site.register(Case)
admin.site.register(Items)
admin.site.register(Casesitems)
admin.site.register(Category)
admin.site.register(Useritems)
