from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('signup/', views.sign_up),
    path('item/<int:item_id>', views.item),
    path('item/<int:item_id>/add_to_cart', views.add_item_to_cart),
    path('items/<int:page>', views.items),
    path('items/', views.items),
    path('cart/', views.cart),
    path('cart/<int:citem_id>/increase', views.increase_item_count_in_cart),
    path('cart/<int:citem_id>/decrease', views.decrease_item_count_in_cart),
    path('cart/<int:citem_id>/remove', views.remove_item_in_cart),

]
