from django.shortcuts import render, HttpResponse, redirect

from django.http import JsonResponse
from .models import Banner, Product, ProductAttribute, Category, Size, Color, CartOrderDetails
import requests
import json
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login
# Create your views here.

def get_cart_length(request):
	user = request.user
	if user.is_authenticated:
		cartItems = CartOrderDetails.objects.filter(user=user)
		cartlength = len(cartItems)
		return cartlength
	return 0


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def home(req):
    banner = Banner.objects.first()
    ipaddr = get_client_ip(req)
    country = requests.get(f'http://ip-api.com/json/{ipaddr}')
    cart_length = get_cart_length(req)
    return render(req, 'index.html', {'banner': banner, 'cart_length':cart_length})


def category(req, id):
    category = Category.objects.get(id=id)
    products = Product.objects.filter(category=category).order_by('-id')
    return render(req, 'category.html', {'data': products, })


def product(req, slug):
    fetchProduct = Product.objects.get(slug=slug)
    colors = ProductAttribute.objects.filter(product=fetchProduct).values(
        'color__id', 'color__title', 'color__color_code').distinct()
    sizes = ProductAttribute.objects.filter(product=fetchProduct).values(
        'size__id', 'size__title', 'price', 'color__id').distinct()
    cart_length = get_cart_length(req)
    return render(req, 'product.html', {'data': fetchProduct, 'colors': colors, 'sizes': sizes, 'cart_length':cart_length})


@csrf_exempt
def getProductPrice(req):
    if req.method == 'POST':
        data = json.load(req)
        body = data.get('payload')

        color_id = body['color_id']
        size_id = body['size_id']
        slug = body['slug']
        product = Product.objects.get(slug=slug)
        color = Color.objects.get(id=color_id)
        size = Size.objects.get(id=size_id)
        result = ProductAttribute.objects.get(product=product, color=color, size=size)
        return HttpResponse(result.price)
    return HttpResponse('Not allowed')


@csrf_exempt
def add_to_cart(request):
	if request.method == 'POST':
		user = request.user
		if user.is_authenticated:
			data = json.load(request)
			prod_attrs = data.get('payload')
			price = prod_attrs['price']
			prod_id = prod_attrs['prod_id']
			qty = prod_attrs['qty']
			final_price = int(price[1:]) * int(qty)
			print(final_price)
			product = Product.objects.get(id=prod_id)
			color = Color.objects.get(id=prod_attrs['color'])
			size = Size.objects.get(id=prod_attrs['size'])
			prod_details = ProductAttribute.objects.get(product=product, color=color, size=size)
			new_cart_order = CartOrderDetails(user=user, product=product, price=final_price, qty=qty, details=prod_details)
			new_cart_order.save()
			return JsonResponse({'message' : "success"})
		else:
			return JsonResponse({'message' : 'user_not_auth'})
	return render(request, 'login.html')
		    

def loginuser(req):
	if req.method == 'POST':
		username = req.POST['username']
		password = req.POST['password']
		user = authenticate(req, username=username, password=password)
		if user is not None:
			login(request=req,user=user)
			messages.success(req, 'Logged in successfully!')
			return redirect('/')
		else:
			messages.warning(req, 'wrong username or password')
			return render(req, 'login.html')
	else:
		return render(req, 'login.html')


def signup(req):
	if req.method == 'POST':
		username = req.POST['username']
		password = req.POST['password']
		first_name = req.POST['first_name']
		last_name = req.POST['last_name']
		email = req.POST['email']
		isalreadyuser = User.objects.filter(username=username)
		isemailexists = User.objects.filter(email=email)
		if len(isalreadyuser) <= 0:
			if len(isemailexists) <= 0:
				User.objects.create_user(first_name=first_name, last_name=last_name, email=email, password=password, username=username)
				messages.success(req, 'Account Created Successfullt !')
				return redirect('/login')
			else:
				messages.warning(req, 'Email already registered')
				return render(req, 'signup.html')	
		else:
			messages.warning(req, 'Username already taken')
			return render(req, 'signup.html')	
	return render(req, 'signup.html')

def cart(request):
	user = request.user
	if user.is_authenticated:
		cart_items = CartOrderDetails.objects.filter(user=user)
		print(cart_items)
		return render(request, 'cart.html', {'items' : cart_items})
	else:
		return redirect('/login')
