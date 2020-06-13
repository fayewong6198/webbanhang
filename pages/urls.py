
from . import views

from django.urls import path, include
urlpatterns = [

    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('listings/', views.listings, name='listings'),
    path('listing/<int:id>/', views.listing, name='listing'),
    path('cart/', views.cart, name='cart'),
    path('contact/', views.contact, name='contact'),
    path('payment/', views.payment, name='payment'),
    path('addToCart/<int:id>/', views.addToCart, name='addToCart'),
    path('deleteFromCart/<int:id>/', views.deleteFromCart, name='deleteFromCart'),
    path('changeQuantity/<int:id>/', views.changeQuantity, name='changeQuantity'),
    path('buy/<int:id>/', views.buy, name='buy'),
]
