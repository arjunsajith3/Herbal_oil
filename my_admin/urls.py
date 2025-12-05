from django.urls import path

from . import views

urlpatterns = [

    path("",views.home, name="home"),
    path("products", views.products, name="products"),
    path("benefits",views.benefits, name="benefits"),
    path("about",views.about, name="about"),

    path("contact",views.contact, name="contact"),

    path("book",views.book, name="book"),

    path("new_login",views.new_login, name="new_login"),

    path("inventory",views.inventory, name="inventory"),




    path("admin_dashboard",views.admin_dashboard, name="admin_dashboard"),

    path("edit_product",views.edit_product, name="edit_product"),
    path('products/<int:product_id>/edit/',views.edit_product, name="edit_product"),

    path("delete_product",views.delete_product, name="delete_product"),
    path('products/<int:product_id>/delete/', views.delete_product, name='delete_product'),
    path("add_product", views.add_product, name="add_product"),
    #path("product_details", views.product_details_view, name="product_details"),

    path('customers/', views.customers_list, name='customers_list'),

    path('customers/delete/<int:user_id>/', views.delete_customer, name='delete_customer')



]
