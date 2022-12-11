from django.http import HttpResponseRedirect, Http404

from ShoppingCart.shop.models import Cart


def authenticated_only(func):
    def wrapper(request, *args, **kwargs):
        if request.user.authenticated_only:
            return func(request, *args, **kwargs)
        return HttpResponseRedirect('/signup')

    return wrapper


def post_method_only(func):
    def wrapper(request, *args, **kwargs):
        if request.method == 'POST':
            return func(request, *args, **kwargs)
        raise Http404()

    return wrapper


def create_cart_if_not_exists(func):
    @authenticated_only
    def wrapper(request, *args, **kwargs):

        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            cart = Cart(user=request.user).save()

        return func(request, *args, **kwargs, cart=cart)

    return wrapper
