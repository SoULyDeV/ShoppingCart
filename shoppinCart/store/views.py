from django.shortcuts import render
from .models import Product, Cart, CartItem
from django.http import JsonResponse
import json
# Create your views here.
def index(request):
    products = Product.objects.all()
    
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        
    context={'products':products}
    return render(request, 'index.html', context)

def cart(request):
    
    cart = None
    cartitems = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitems = cart.cartitems.all()
    
    context = {'cart':cart, 'items':cartitems}
    return render(request, 'cart.html', context)

def add_to_cart(request):
    data = json.loads(request.body)
    product_id = data['id']
    product = Product.objects.get(id=product_id)
    
    if request.user.is_authenticated:
        #get_or_create = if its already exist dont create a new one
        cart, created = Cart.objects.get_or_create(user=request.user, completed=False)
        cartitem, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cartitem.quantity += 1
        cartitem.save()
        
        
        num_of_item = cart.num_of_items
        
    return JsonResponse(num_of_item, safe=False)