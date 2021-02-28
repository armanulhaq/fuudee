from django.contrib import admin
from .models import Food, User, Cart

# Register your models here.
admin.site.register(User)
admin.site.register(Food)
admin.site.register(Cart)
