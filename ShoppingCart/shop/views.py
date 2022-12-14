from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from .decorators import create_cart_if_not_exists, post_method_only
from .forms import LoginForm, SignUpForm
from .models import Item, CartItem


def index(request):
    latest_items = Item.objects.order_by('-pub_date')[:10]
    return render(
        request,
        'shop/index.html',
        {'latest_items': latest_items}
    )


def items(request, page=1):
    latest_items = Item.objects.order_by('-pub_date')[(page - 1) * 10: page * 10]
    next_items = Item.objects.order_by('-pub_date')[page * 10: (page + 1) * 10]
    return render(request, 'shop/items.html', {
        'latest_items': latest_items,
        'page': page,
        'next_page': (page + 1 if next_items else None),
    })


def item(request, item_id):
    return render(request, 'shop/item.html', {'item': Item.objects.get(id=item_id)})


@create_cart_if_not_exists
def cart(request, cart):
    citems = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart.html', {
        'citems': citems,
        'count': len(citems),
        'total': sum((citem.price for citem in citems))
    })


@post_method_only
@create_cart_if_not_exists
def add_item_to_cart(request, item_id, cart):
    item = Item.objects.get(id=item_id)

    if item not in [citem.item for citem in CartItem.objects.filter(cart=cart)]:
        CartItem(cart=cart, item=item, count=1).save()

    return HttpResponseRedirect('/cart')


@post_method_only
@create_cart_if_not_exists
def increase_item_count_in_cart(request, citem_id, cart):
    citem = CartItem.objects.get(id=citem_id)

    if citem in CartItem.objects.filter(cart=cart):
        citem.count += 1
        citem.save()

    return HttpResponseRedirect('/cart')


@post_method_only
@create_cart_if_not_exists
def decrease_item_count_in_cart(request, citem_id, cart):
    citem = CartItem.objects.get(id=citem_id)

    if citem in CartItem.objects.filter(cart=cart):
        if citem.count <= 1:
            citem.delete()
        else:
            citem.count -= 1
            citem.save()

    return HttpResponseRedirect('/cart')


@post_method_only
@create_cart_if_not_exists
def remove_item_in_cart(request, citem_id, cart):
    citem = CartItem.objects.get(id=citem_id)

    if citem in CartItem.objects.filter(cart=cart):
        citem.delete()

    return HttpResponseRedirect('/cart')


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

        return render(request, 'registration/signup.html', {'form': form, 'error': 'Invalid form'})

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

                return render(request, 'shop/login.html', {'form': form, 'error': 'Disabled account'})
            else:
                return render(request, 'shop/login.html', {'form': form, 'error': 'Invalid login'})
    else:
        return render(request, 'shop/login.html', {'form': form})
