from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .forms import LoginForm, SignUpForm
from .models import Item, Cart, CartItem


def index(request):
    latest_items = Item.objects.order_by('-pub_date')[:10]
    return render(
        request,
        'shop/index.html',
        {'latest_items': latest_items}
    )


def items(request):
    ...


def item(request, item_id):
    return render(request, 'shop/item.html', {'item': Item.objects.get(id=item_id)})


def cart(request):
    if request.user.is_authenticated:
        cart = Cart.objects.get(user=request.user)
        if not cart:
            cart = Cart(request.user)

        citems = CartItem.objects.filter(cart=cart)
        return render(request, 'shop/cart.html', {
            'citems': citems,
            'count': len(citems),
            'total': sum([citem.item.price for citem in citems])
        })


def add_item_to_cart(request, item_id):
    ...


def sign_up(request):
    if request.method == 'POST':

        form = SignUpForm(request.POST)

        if form.is_valid():

            cd = form.cleaned_data

            if User.objects.filter(username=cd['username']).exists():
                return render(request, 'registration/signup.html', {'form': form, 'error': 'Username already used'})
            if User.objects.filter(email=cd['email']).exists():
                return render(request, 'registration/signup.html', {'form': form, 'error': 'Email already used'})
            if cd['password'] != cd['password_confirm']:
                return render(request, 'registration/signup.html',
                              {'form': form, 'error': 'Passwords are not the same'})

            user = User.objects.create_user(cd['username'], cd['email'], cd['password'])
            login(request, user)
            return HttpResponseRedirect('/')

        else:
            return render(request, 'registration/signup.html', {'form': form, 'error': 'Invalid form'})
    else:
        form = SignUpForm()

    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    form = LoginForm()

    if request.method == 'POST':
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return render(request, 'shop/login.html', {'form': form, 'error': 'Disabled account'})
            else:
                return render(request, 'shop/login.html', {'form': form, 'error': 'Invalid login'})
    else:
        return render(request, 'shop/login.html', {'form': form})
