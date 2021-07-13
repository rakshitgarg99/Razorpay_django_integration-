from django.shortcuts import render
import razorpay
from .models import Coffee
from django.views.decorators.csrf import csrf_exempt

from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
# Create your views here.


def home(request):
    if request.method == 'POST':
        name = request.POST.get("name")
        amount = int(request.POST.get("amount")) * 100
        email = request.POST.get("email")
        client = razorpay.Client(auth=(settings.RAZORPAY_YOUR_ID, settings.RAZORPAY_YOUR_SECRET))
        payment = client.order.create({'amount': amount, 'currency':'INR', 'payment_capture': '1'})
        # print(payment)
        coffee = Coffee(name = name, amount = amount, email = email, order_id = payment['id'])
        coffee.save()
        return render(request, "index.html", {'payment': payment})

    return render(request, "index.html")

@csrf_exempt
def success(request):
    if request.method == "POST":
        a = request.POST
        order_id = ""
        data = {}
        for key, val in a.items():
            if key == 'razorpay_order_id':
                data['razorpay_order_id'] = val
                order_id = val
            elif key == 'razorpay_payment_id':
                data['razorpay_payment_id'] = val
            elif key == 'razorpay_signature':
                data['razorpay_signature'] = val
        user = Coffee.objects.filter(order_id=order_id).first()
        
        # print(order_id)


        client = razorpay.Client(auth=(settings.RAZORPAY_YOUR_ID, settings.RAZORPAY_YOUR_SECRET))
        check = client.utility.verify_payment_signature(data)
        if check:
            return render(request, "error.html")

        user.paid = True
        user.save()

        # print(data)
        msg_plain =  render_to_string('email.txt')
        msg_html =  render_to_string('email.html')
        # print(user.email)
        send_mail("Your donation has been received", msg_plain, settings.EMAIL_HOST_USER,
                 [user.email], html_message=msg_html
                 )

    return render(request, "success.html")