from django.contrib import admin
from django.urls import path
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("addtocart/<int:food_id>", views.addtocart, name='addtocart'),
    path("removefromcart/<int:food_id>", views.removefromcart, name='removefromtocart'),
    path("cart", views.cart, name='cart')
]