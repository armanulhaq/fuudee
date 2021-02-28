import json
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse


from .models import Cart, User, Food


def index(request):
    all_food = Food.objects.all()
    for food in all_food:
        cart = Cart.objects.filter(user=request.user.id, food=food.id)
        if cart.exists():
            count = cart[0].count
        else:
            count = 0
        setattr(food, 'count', count)
    return render(request, "foodie/index.html", {
        "all_food": all_food
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "foodie/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "foodie/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "foodie/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "foodie/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "foodie/register.html")

def food(request, food_id):
    food = Food.objects.filter(id=food_id)[0]
    return render(request, "foodie/food.html", {
        "food": food
    })

def addtocart(request, food_id):
    # If user already added the food to cart.
    user = User.objects.filter(id=request.user.id)[0]
    cart = Cart.objects.filter(user=request.user.id, food=food_id)
    food = Food.objects.filter(id=food_id)[0]
    if (cart.exists()):
        cart_count = cart[0].count + 1
        cart.update(count=cart_count)

    # If user is adding the food for the first time in the cart.
    else:
        cart_count = 1
        cart = Cart(user=user, food=food, count=cart_count)
        cart.save()

    return JsonResponse({
       "cart_count_add": cart_count
    })

def removefromcart(request, food_id):
    cart = Cart.objects.filter(user=request.user.id, food=food_id)
    if (cart.exists()):
        if (cart[0].count > 1):
            cart_count = cart[0].count - 1
            cart.update(count=cart_count)
            return JsonResponse({
                "cart_count_remove": cart_count
            })
        else:
            cart.delete()
            return JsonResponse({
                "cart_count_remove": 0
            })
    else:
        raise Exception('Cannot remove further')

def cart(request):
    cart_items = Cart.objects.filter(user=request.user.id)

    items = []
    total_price = 0

    for cart_item in cart_items:
        food = Food.objects.filter(id=cart_item.food.id)[0]
        items.append({
            "name": food.name,
            "price_of_each": food.price,
            "price": cart_item.count * food.price,
            "count": cart_item.count,
            "image": food.image
        })
        total_price = total_price + cart_item.count * food.price

    return render(request, "foodie/cart.html", {
        "items": items,
        "total_price": total_price
    })
