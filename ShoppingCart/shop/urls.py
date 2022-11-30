from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signup/', views.sign_up),
    path('item/<int:item_id>', views.item),
    path('item/<int:item_id>/add_to_cart', views.add_item_to_cart),
    path('items/', views.items),
    path('cart/', views.cart),
]
