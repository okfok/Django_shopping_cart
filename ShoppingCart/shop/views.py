from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render

from .forms import LoginForm, SignUpForm
from .models import Item, Cart, CartItem


def is_authenticated(func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:

            return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/signup')

    return wrapper


def is_post_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':

            return func(request, *args, **kwargs)
        else:
            raise Http404()

    return wrapper


def create_cart_if_not_exists(func):
    @is_authenticated
    def wrapper(request, *args, **kwargs):
        cart = Cart.objects.get(user=request.user)
        if not cart:
            Cart(request.user).save()

        return func(request, *args, **kwargs)

    return wrapper


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


@create_cart_if_not_exists
def cart(request):
    cart = Cart.objects.get(user=request.user)

    citems = CartItem.objects.filter(cart=cart)
    return render(request, 'shop/cart.html', {
        'citems': citems,
        'count': len(citems),
        'total': sum([citem.price for citem in citems])
    })


@is_post_method
@create_cart_if_not_exists
def add_item_to_cart(request, item_id):
    cart = Cart.objects.get(user=request.user)

    item = Item.objects.get(id=item_id)

    if item not in [citem.item for citem in CartItem.objects.filter(cart=cart)]:
        CartItem(cart=cart, item=item, count=1).save()

    return HttpResponseRedirect('/cart')


@is_post_method
@create_cart_if_not_exists
def increase_item_count_in_cart(request, citem_id):
    cart = Cart.objects.get(user=request.user)
    citem = CartItem.objects.get(id=citem_id)

    if citem in CartItem.objects.filter(cart=cart):
        citem.count += 1
        citem.save()

    return HttpResponseRedirect('/cart')


@is_post_method
@create_cart_if_not_exists
def decrease_item_count_in_cart(request, citem_id):
    cart = Cart.objects.get(user=request.user)
    citem = CartItem.objects.get(id=citem_id)

    if citem in CartItem.objects.filter(cart=cart):
        if citem.count <= 1:
            citem.delete()
        else:
            citem.count -= 1
            citem.save()

    return HttpResponseRedirect('/cart')


@is_post_method
@create_cart_if_not_exists
def remove_item_in_cart(request, citem_id):
    cart = Cart.objects.get(user=request.user)
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
