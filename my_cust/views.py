from django.shortcuts import render
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_protect
from django.http import HttpResponse
from django.contrib import messages
from my_admin.models import Customer, Product
from .models import Bookingdetail
from django.shortcuts import get_object_or_404
import razorpay
from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone


# Create your views here.



def cust_dashboard(request):
    products = Product.objects.all()[:8]  # Limit to 8 recommended products
    return render(request, 'cust_dashboard.html', {'products': products})


def booking_form(request):


    if request.method == "POST":
        product_id = request.POST.get("product_id")
        product = Product.objects.get(id=product_id)


        request.session["save_address"] = request.POST.get("address")
        request.session["save_phone"] = request.POST.get("phone")
        altphone = request.POST.get("alt_phone")
        request.session["save_alt_phone"] = altphone

        request.session["save_note"] = request.POST.get("note")

        booking = Bookingdetail.objects.create(
            product=product,
            oilSize=request.POST.get("oilSize"),
            unitPrice=request.POST.get("unitPrice"),
            quantity=request.POST.get("quantity"),
            note=request.POST.get("note"),
            custName=request.POST.get("custName"),
            email=request.POST.get("email"),
            phone=request.POST.get("phone"),
            alt_phone=request.POST.get('alt_phone'),
            address=request.POST.get("address"),
        )
        return redirect("payment_page", booking_id=booking.id)


    product_id = request.GET.get("product_id")
    product = Product.objects.get(id=product_id)
    demo = request.session.get("save_alt_phone")

    return render(request, "booking_form.html", {
        "product": product,
        "saved_address": request.session.get("save_address", ""),
        "saved_phone": request.session.get("save_phone", ""),
        "save_alt_phone": request.session.get("save_alt_phone", ""),
        "saved_note": request.session.get("save_note", "")
    })




def add_to_cart(request, product_id):
    return redirect('dashboard')


def razorpay_success(request,booking_id):
    booking = Bookingdetail.objects.get(id=booking_id)
    total_amount = float(booking.unitPrice) * booking.quantity

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))



    order = client.order.create(dict(amount=1000, currency="INR", payment_capture=1))

    return render(request, "razorpay.html", {

        'razorpay_key': settings.RAZORPAY_KEY_ID,
        'order_id': order['id'],
        'amount': total_amount,
        'payment_method':"card",
        'booking_data': booking,


    })



def payment_page(request, booking_id):
    booking = Bookingdetail.objects.get(id=booking_id)

    total_amount = float(booking.unitPrice) * booking.quantity

    if request.method == "POST":
        booking.status = "Paid"
        booking.save()
        return razorpay_success(request,booking.id)

    return render(request, "payment_page.html", {
        "booking": booking,
        "total_amount": total_amount,
    })


def payment_success(request, booking_id):

    booking = get_object_or_404(Bookingdetail, id=booking_id)
    #booking=Bookingdetail.objects.get(id=booking_id)

    booking.payment_status = "Paid"



    subject = "Booking Confirmation - Payment Successful"

    message = f"""
                Dear {booking.custName},
                
                Thank you for your payment! Your booking is confirmed ✅
                
                Here are your booking details:
                
                Customer Name : {booking.custName}
                Mobile Number : {booking.phone}
                Quantity (QTY): {booking.quantity}
                Total Price   : ₹{booking.total_amount}
                Booking Date  : {timezone.localtime(booking.booked_at).strftime('%d-%m-%Y %I:%M %p')}
                
                Product       : {booking.product.product_name if booking.product else "N/A"}
                Payment Mode  : {booking.payment_method}
                
                Delivery Address:
                {booking.address}
                
                We appreciate your trust in Pure Essence Oil 🌿
                
                Warm Regards,
                Pure Essence Oil Team
                """


    send_mail(
        subject,
        message,
        "testpure8@gmail.com",
        [booking.email],
        fail_silently=False,
    )
    booking.save()

    context = {
        "order_id": booking.id,
        "product_name": booking.product.product_name if booking.product else "N/A",
        "amount": booking.total_amount,
        "order_date": timezone.localtime(booking.booked_at).strftime('%d-%m-%Y %I:%M %p'),
        "customer_name": booking.custName,
        "mobile": booking.phone,
        "qty": booking.quantity,
    }

    return render(request, "payment_success.html", context)
    # return render(request, "payment_success.html")




