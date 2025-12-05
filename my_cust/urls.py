from django.urls import path

from . import views

urlpatterns = [

path("cust_dashboard",views.cust_dashboard, name="cust_dashboard"),

path("booking_form",views.booking_form, name="booking_form"),

path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),

path('booking_form/', views.booking_form, name='booking_form'),

path('payment/<int:booking_id>/', views.payment_page, name='payment_page'),

 # path('payment_success', views.payment_success, name='payment_success'),

path('payment_success/<int:booking_id>/', views.payment_success, name='payment_success'),



]