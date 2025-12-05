from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib import messages
from my_admin.models import Customer
from my_admin.models import Product
from django.shortcuts import get_object_or_404
from my_cust.models import Bookingdetail





def home(request):
    return render(request, 'home.html')

def products(request):
    return render(request,'products.html')

def benefits(request):
    return render(request,'benefits.html')

def about(request):
    return render(request,'about.html')

def contact(request):
    return render(request,'contact.html')



def new_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect('admin_dashboard')
            else:
                return redirect('cust_dashboard')

        else:
            return render(request, 'new_login.html', {'error': 'Invalid credentials'})
    return render(request, 'new_login.html')


def book(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirmPassword')

        if password == confirm_password:
            user = User.objects.create_user(username=username, email=email, password=password, first_name=first_name, last_name=last_name)
            customer = Customer.objects.create(user=user,mobile_number=phone, age=age, gender=gender)
            user.save()
            customer.save()
            messages.success(request, "You have successfully registered")
            return redirect('new_login')
        else:
            messages.error(request, "Passwords don't match.")
            return redirect('book')


    return render(request, 'book.html')



def admin_dashboard(request):
    recent_orders = Bookingdetail.objects.order_by('-id')[:5]  # Latest 5 orders
    return render(request, "admin_dashboard.html", {"recent_orders": recent_orders})


def inventory(request):
    products = Product.objects.all()

    return render(request, 'inventory.html', {'products':products})




def add_product(request):
    if request.method == 'POST':
        product_name = request.POST.get('productName')
        description = request.POST.get('description')
        price = request.POST.get('price')
        stock = request.POST.get('stock')
        available = request.POST.get('availability')
        image = request.FILES.get('image')

        product = Product.objects.create(product_name=product_name, description=description, price=price, stock=stock,available=available, image=image)
        product.save()
        messages.success(request, "You have successfully product added")
        return redirect('inventory')

    return render(request, "add_product.html")



# def product_details_view(request):
#     product = Product.objects.all()
#     return render(request, 'product_details.html', {'products': product})

def edit_product(request, product_id):
    product = Product.objects.get(id=product_id)

    if request.method == 'POST':
        product.product_name = request.POST.get('productName')
        product.description = request.POST.get('description')
        product.price = float(request.POST.get('price'))
        product.stock = int(request.POST.get('stock'))
        product.available = request.POST.get('available') == 'on'

        product.save()
        messages.success(request, "Product updated successfully.")
        return redirect('inventory')

    return render(request, 'edit_product.html', {'product': product})


def delete_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    if request.method == 'POST':
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect('inventory')

    return redirect('edit_product', product_id=product_id)


def customers_list(request):
    customers = User.objects.all()  # Fetch all registered users
    return render(request, "customers_list.html", {"customers": customers})


def delete_customer(request, user_id):
    user = get_object_or_404(User, id=user_id)

    # Prevent deleting superuser/admin accounts
    if user.is_superuser:
        messages.error(request, "You cannot delete an admin account.")
        return redirect('customers_list')

    user.delete()
    messages.success(request, "Customer deleted successfully.")
    return redirect('customers_list')



