from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth import login, logout, authenticate
from .models import CustomUser, MobileCompany,Mobile, Cart
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import PasswordResetView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, get_object_or_404
from decimal import Decimal  
from django.db.models import Q
from django.http import JsonResponse

# Create your views here.
################### AUTHENTICATION VIEWS ####################

# register user
def register_user(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstname')
        last_name = request.POST.get('lastname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'This email is already taken. Please use a different one.')
            return render(request, 'register.html')
        user = CustomUser(first_name=first_name,last_name=last_name,email=email)
        password= user.set_password(password)        
        if user is not None:
            user.save()
            return redirect('login_user')
        else:
            return render(request, 'register.html')
    return render(request, 'register.html')

# Login user view 
def login_user(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, username=email, password=password) 
        if user is not None:
            login(request, user)
            messages.success(request, "You are successfully logged in.")
            return redirect('company') 
        else:
            messages.error(request, 'Invalid email or password.')
            return render(request, 'login.html')
    return render(request, 'login.html')

# home view 
@login_required(login_url='login_user')
def home_view(request):
    user = request.user
    print(user)
    contaxt = {'user':user}
    return render(request, 'home.html', contaxt)

# logout view 
def user_logout(request):
    logout(request)
    return redirect('login_user') 

# Password Reset view
class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'authentication/password_reset.html'
    email_template_name = 'authentication/password_reset_email.html'
    subject_template_name = 'authentication/password_reset_subject.html'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('login_user')


#################################### OTHER VIEWS ###########################
@login_required(login_url='login_user')
def company(request):
    company = MobileCompany.objects.all()
    print(company)
    return render(request, 'home.html', context={'company':company})


# search item view 
@login_required(login_url='login_user')
def search_mobile(request):
    product = MobileCompany.objects.all()
    if request.method == 'GET':
        product = request.GET.get('servicename')
        print(product)
        if product != None:
            product = MobileCompany.objects.filter(name__icontains=product)
    return render(request, 'home.html', context={'product':product})

        

# base view 
def base(request):
    return render(request, 'base.html', contaxt={})

# company view 
@login_required(login_url='login_user')
def company_mobile(request, company_id):
    company = get_object_or_404(MobileCompany, id=company_id)
    mobiles = Mobile.objects.filter(company=company)
    return render(request, 'shop.html', {'company': company, 'mobiles': mobiles})

# single product
@login_required(login_url='login_user')
def single_product(request, mobile_id):
    mobile = get_object_or_404(Mobile, id=mobile_id)
    return render(request, 'single-product.html', {'mobile': mobile})

# Cart view 
@login_required(login_url='login_user')
def cart_page(request):
    user = request.user
    product_id = request.GET.get('mobile_id')  
    product = get_object_or_404(Mobile, id=product_id)
    Cart(user=user, product=product).save()
    print(product)
    return redirect('showcart')

# Show cart view
@login_required(login_url='login_user')
def showcart(request):
    user = request.user
    showcart = Cart.objects.filter(user=user)
    amount = Decimal('0.0')  
    shipping_amount = Decimal('450.0')  
    total_amount = Decimal('0.0') 
    cart_product = Cart.objects.filter(user=user)  
    print(cart_product)
    if cart_product:
        for p in cart_product:
            tempamount = p.quantity * p.product.price
            amount += tempamount 
            total_amount = amount + shipping_amount
    return render(request, 'showcart.html', context={'showcart': showcart, 'amount': amount, 'total_amount': total_amount, 'cart_product':cart_product})

# plus cart vew
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity +=1
        c.save()
        amount = Decimal('0.0')  
        shipping_amount = Decimal('450.0') 
        total_amount = Decimal('0.0') 
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]  
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount 
                total_amount = amount + shipping_amount
            data = {
                'quantity':c.quantity,
                'amount': amount,
                'total_amount':total_amount,
            }
            return JsonResponse(data)

# minus cart view 
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount = Decimal('0.0')  
        shipping_amount = Decimal('450.0') 
        total_amount = Decimal('0.0') 
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]  
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount -= tempamount 
                total_amount = amount + shipping_amount
            data = {
                'quantity':c.quantity,
                'amount': amount,
                'total_amount':total_amount,
            }
            return JsonResponse(data)


# Remove cart view
@login_required(login_url='signin')
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount = Decimal('0.0')  
        shipping_amount = Decimal('450.0')  
        total_amount = Decimal('0.0') 
        cart_product = [p for p in Cart.objects.all() if p.user==request.user]  
        print(cart_product)
        if cart_product:
            for p in cart_product:
                tempamount = (p.quantity * p.product.price)
                amount += tempamount 
                total_amount = amount + shipping_amount
            data = {
                'amount': amount,
                'total_amount':total_amount,
            }
            return JsonResponse(data)

# Checkout view
@login_required(login_url='login_user')
def checkout(request):
    return render(request, 'checkout.html')

# Product view
@login_required(login_url='login_user')
def mobile(request):
    return render(request, 'mobile.html', contaxt={})

# wishlist view
def wishlist(request):
    return render(request, 'base.html')

# Review view 
@login_required(login_url='login_user')
def review(request):
    return render(request, 'contact.html', contaxt={})



