from idlelib.iomenu import errors

from django.contrib import auth
from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse

from django.http import HttpResponseRedirect
from django.shortcuts import render

from orders.models import Order, OrderItem
from users.forms import UserRegistrationForm, UserLoginForm, UserProfileForm


# Create your views here.


def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(instance=request.user, data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('users:profile'))
        else:
            form.errors
    else:
        form = UserProfileForm(instance=request.user)

    orders = Order.objects.filter(user=request.user).prefetch_related(
        Prefetch(
            'items',
            queryset=OrderItem.objects.select_related('product'),
        )
    ).order_by('-id')
    context = {
        'form':form,
        'orders': orders,
    }

    return render(request, 'users/profile.html', context)

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = auth.authenticate(username=username,password=password)
            if user:
                auth.login(request,user)
                return HttpResponseRedirect(reverse('main:index'))

    else:
        form = UserLoginForm()

    context ={
        'form': form,
    }
    return render(request,'users/login.html',context)


def registration(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data = request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Успешная регистрация!')
            return HttpResponseRedirect(reverse('users:login'))
        else:
            print(form.errors)

    else:
        form = UserRegistrationForm()

    context = {
        'form': form
    }
    return render(request,'users/registration.html', context)



def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))