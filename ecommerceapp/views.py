from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Banner, Product, ProductAttribute, Category, Size, Color
import requests
import json
from django.views.decorators.csrf import csrf_exempt
rom django.contrib.auth.models import User
# Create your views here.

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
    print(country.text)
    return render(req, 'index.html', {'banner' : banner})

def category(req, id):
    category = Category.objects.get(id = id)
    products = Product.objects.filter(category=category).order_by('-id')
    return render(req, 'category.html', {'data' : products,})

def product(req, slug):
    fetchProduct = Product.objects.get(slug=slug)
    colors=ProductAttribute.objects.filter(product=fetchProduct).values('color__id','color__title','color__color_code').distinct()
    sizes=ProductAttribute.objects.filter(product=fetchProduct).values('size__id','size__title','price','color__id').distinct()
    print(colors)
    print(sizes)
    return render(req, 'product.html', {'data' : fetchProduct, 'colors' : colors, 'sizes' : sizes})

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

@csrf_exempt
def add_to_cart(request):
    if request.method == 'POST':
        data = json.load(request)
        body = data.get('payload')
        cart_p = []
        data={
            'id' : str(body['id']),
            'image':body['image'],
            'title':body['title'],
            'qty':body['qty'],
            'price':body['price'],
            'color':body['color'],
            'length':body['length'],
        }
	
        if 'cartdata' in request.session:           
            cartdata = request.session['cartdata']
            cartdataupdated = cartdata.append(cart_p)
            request.session['cartdata'] = cartdataupdated
            return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
        else:
            newCartdata = cart_p.append(data)
            request.session['cartdata']=newCartdata
            return JsonResponse({'data':request.session['cartdata']})
	
	    #     if str(body['id']) in request.session['cartdata']:
        #         cart_data=request.session['cartdata']
        #         if cart_data[str(body['id'])] == int(cart_p[str(body['id'])]):
        #             if cart_data[str(body['id'])]['color'] == int(cart_p[str(body['id'])]['color']) and cart_data[str(body['id'])]['length']==int(cart_p[str(body['id'])]['length']):          
        #                 cart_data[str(body['id'])]['qty']=int(cart_p[str(body['id'])]['qty'])
        #                 return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})     
        #             else:
        #                 cart_data=request.session['cartdata']
        #                 cart_data.update(cart_p)
        #                 request.session['cartdata']=cart_data
        #                 return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})                 
        #         else:
        #             cart_data=request.session['cartdata']
        #             cart_data.update(cart_p)
        #             request.session['cartdata']=cart_data
        #             return JsonResponse({'data':request.session['cartdata'],'totalitems':len(request.session['cartdata'])})
    
def delete_cart(req) :
	del req.session['cartdata']
	return HttpResponse('ok')
# Cart List Page
def cart_list(request):
	total_amt=0
	if 'cartdata' in request.session:
		for p_id,item in request.session['cartdata'].items():
			total_amt+=int(item['qty'])*float(item['price'])
		return render(request, 'cart.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	else:
		return render(request, 'cart.html',{'cart_data':'','totalitems':0,'total_amt':total_amt})


# Delete Cart Item
def delete_cart_item(request):
	p_id=str(request.GET['id'])
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			del request.session['cartdata'][p_id]
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

# Delete Cart Item
def update_cart_item(request):
	p_id=str(request.GET['id'])
	p_qty=request.GET['qty']
	if 'cartdata' in request.session:
		if p_id in request.session['cartdata']:
			cart_data=request.session['cartdata']
			cart_data[str(request.GET['id'])]['qty']=p_qty
			request.session['cartdata']=cart_data
	total_amt=0
	for p_id,item in request.session['cartdata'].items():
		total_amt+=int(item['qty'])*float(item['price'])
	t=render_to_string('ajax/cart-list.html',{'cart_data':request.session['cartdata'],'totalitems':len(request.session['cartdata']),'total_amt':total_amt})
	return JsonResponse({'data':t,'totalitems':len(request.session['cartdata'])})

def login(req):
	if req.method == 'POST':
		username = req.POST.get['username']
		password = req.POST.get['password']
	return render(req, 'login.html')

def signup(req):
	return render(req, 'signup.html')
