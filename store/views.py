from django.shortcuts import render,HttpResponse,redirect
from .models import *

from django.http import JsonResponse

import json

import datetime

import razorpay

from django.views.decorators.csrf import csrf_exempt


from .utils import cookieCart, cartData, guestUser

from django.contrib.auth.forms import UserCreationForm

from .forms import CreateUserForm

from django.contrib import messages

from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user

# Create your views here.


@unauthenticated_user
def registerUser(request):

    if request.method =="POST":
        form = CreateUserForm(request.POST)
        print("inside post method")
        if form.is_valid():
            print("inside valid form")
            user = form.save()
            username= form.cleaned_data.get('username')
            messages.success(request,'Account is created for' +' '+ username)
            group = Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(
                user = user,
                name = username,
            )
            return redirect("/loginUser")
        else:
            print("error occured")
    else:
        form=CreateUserForm()
    context ={'form':form}
    return render(request,"registration.html",context)

@unauthenticated_user
def loginUser(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request,username=username,password=password)

        print(user)
        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            messages.info(request,'Username or Password is incorrect')
        

    return render(request,'loginUser.html')

def logoutUser(request):
    logout(request)
    return redirect('/loginUser')

def store(request):

    data = cartData(request)
    cartItems = data['cartItems']
    

    products=Product.objects.all()
    context={'products':products,'cartItems':cartItems}
    return render(request,'store.html',context)

def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']



    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'cart.html',context)

def checkout(request):
    
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    # print("cart total :",order['get_cart_total'])

    # #Razorpay

    # if request.method == "POST":
    #     total = 3549

        
    #     order_receipt = 'order_rcptid_11'
    #     client = razorpay.Client(
    #         auth= ('rzp_test_qhjhcvlLqFxkPu','KnggQQmVxBRD9BQ2eNNAtOtS'))

    #     payment = client.order.create({'total':total, 'currency':'INR', 'receipt':'order_receipt', 'payment_capture':'1'})
        

    


    context={'items':items,'order':order,'cartItems':cartItems}
        
    return render(request,'checkout.html',context)

def updateItem(request):

    data=json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Product:',productId)
    print('Action:',action)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem , created =OrderItem.objects.get_or_create(order=order,product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()



    return JsonResponse("Item was added",safe=False)

def processOrder(request):

    data = json.loads(request.body)

    transaction_id = datetime.datetime.now().timestamp()

    

    if request.user.is_authenticated:
        customer = request.user.customer
        order , created = Order.objects.get_or_create(customer = customer, complete=False)
        

        
        
    
    else :

        customer , order =guestUser(request,data)
        
    order.transaction_id = transaction_id
    total = float(data['form']['total'])


    


    if total==order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer = customer,
                order = order,
                address = data['shippingInfo']['address'],
                city = data['shippingInfo']['city'],
                state = data['shippingInfo']['state'],
                zipcode = data['shippingInfo']['zipcode'],

            )

        
    


    

    return JsonResponse("Payment completed", safe = False)