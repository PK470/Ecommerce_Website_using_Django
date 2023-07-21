from django.shortcuts import render,redirect
from .models import*
from django.http import JsonResponse
import json
from django.contrib.auth.models import User
import uuid
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.contrib import messages
import random
from django.core.mail import send_mail



# Create your views here.
def store(request):
    products = Product.objects.all()
    context ={'products': products}
    print('id',Product.id)
    return render(request,'store/store.html',context)

def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        item = order.orderitem_set.all()
    else:
        item = ''
    context = {'items':item, 'order':order}
    # jprint(context)
    return render(request,'store/cart.html',context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order,created = Order.objects.get_or_create(customer = customer, complete = False)
        item = order.orderitem_set.all()
    else:
        item = ''
    context = {'items':item, 'order':order}
    return render(request,'store/checkout.html',context)



def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print(productId,action)

    customer = request.user.customer
    print('customer',customer)
    product = Product.objects.get(id=productId)
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    orderItem,created = OrderItem.objects.get_or_create(order=order, product=product)
    if action == 'add':
        orderItem.quantity = orderItem.quantity+1
    elif action =='remove':
        orderItem.quantity = orderItem.quantity-1
    orderItem.save()
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item is addes',safe=False)

def processorder(request):
    transaction_id = uuid.uuid4()
    print(transaction_id)
    data = json.loads(request.body)
    customer = request.user.customer
    order,created = Order.objects.get_or_create(customer=customer,complete=False)
    order.complete = True
    order.trans_id = transaction_id
    order.save()
    ShippingAdd.objects.create(
        customer = customer,
        order = order,
        address = data['userdata']['address'],
        city = data['userdata']['city'],
        state = data['userdata']['state'],
        pincode = data['userdata']['zipcode'],
    )

    #print('Data:',request.body)
    return JsonResponse('order done',safe=False)

def register(request):
    message=''
    if request.method == "POST":
        uname = request.POST.get('uname')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1!=pass2:
            messages.success(request,'First and second passwords are not same')
            return render(request,'store/register.html')
        if User.objects.filter(username=uname).exists() or User.objects.filter(email=email).exists():
            messages.success(request,'Username or email already exists')
            return render(request, 'store/register.html')   

        else:
            my_user=User.objects.create_user(uname,email,pass1)
            my_user.save()
            
            customer = Customers.objects.create(user=my_user, name=uname, email=email)
            customer.save()
            #print(uname,email,pass1,pass2)
            return redirect('login')

        

        
        
    return render(request,'store/register.html',{'mess':message})

def ulogin(request):
    message=''
    if request.method == "POST":
        uname = request.POST.get('uname')
        password = request.POST.get('password')
        print(uname,password)
        user = authenticate(request, username=uname,password = password)
        print(user)
        if user is not None:
            login(request,user)
            return redirect('store')
        else:
            messages.success(request,'Please enter correct username or password')
            return render (request,'store/login.html')


        #print(uname, pass1)
    return render (request,'store/login.html',{'mess':message})
def uLogout(request):
    logout(request)
    return redirect('store')

def pView(request,pk):
    try:
        product = Product.objects.get(id=pk)
        context = {'product':product}
        return render(request,'store/view.html',context)
    except:
        return redirect('store')
    
def search(request):
    if request.method == 'POST':
        querry = request.POST.get('search')
        s_product = Product.objects.filter(Q(p_name__icontains= querry))
        context ={'products': s_product}
        print(s_product)
        if s_product.exists():
            return render(request,'store/store.html',context)
    messages.success(request,'No result Found')
    return redirect('store')

def forgotpassword(request):
    if request.method == 'POST':
        username = request.POST.get('uname')
        user = User.objects.get(username=username)
        if ForgetPass.objects.filter(user=user).exists():
            otp = ForgetPass.objects.get(user = user)
            otp = otp.forget_password
            print(otp)
            sendEmail(username,otp)
            messages.success(request,'An email with otp is sended to your registerd email Id')

        elif user is not None:
            otp = random.randint(1000, 9999)
            sendEmail(username,otp)
            forgotpass = ForgetPass.objects.create(user = user,forget_password = otp)
            forgotpass.save()
            messages.success(request,'An email with otp is sended to your registerd email Id')
            print(otp)
        else:
            messages.success(request,'username does not exist ')
            
    return render(request,'store/forgotpass.html')

def sendEmail(username,otp):
    email = User.objects.get(username = username)
    subject = 'Hello from Django Email'
    message = f'Use this opt to change your password :- {otp}'
    from_email = 'kinipranav-cmpn@atharvacoe.ac.in'
    recipient_list = [email.email]
    print(email.email)
    send_mail(subject, message, from_email, recipient_list,fail_silently=False)
    
    
def chgpass(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        username = request.POST.get('uname')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        try:
            user = User.objects.get(username = username)
            print(1)
            if user is not None:
                otp1 = ForgetPass.objects.get(user = user)
                if otp == otp1.forget_password:
                    if pass1 == pass2:
                            user.set_password(pass1)
                            user.save()
                            ForgetPass.objects.get(user = user).delete()
                            print('done')
                            messages.success(request,'Password changed succesfully')
                            return redirect('login')
                    else:
                            messages.success(request,'Both Password must be same')
                else:
                        messages.success(request,'Invalid Otp')
            else:
                    messages.success(request,'User does not exist')
    

        except:

            messages.success(request,'something wents wrong')
    return render (request,'store/changepass.html')