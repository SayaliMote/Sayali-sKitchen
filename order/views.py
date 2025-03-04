from django.shortcuts import render, get_object_or_404
from .models import Order, OrderItem
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


# Create your views here.
def thanks(request, order_id):
    if order_id:
        customer_order = get_object_or_404(Order, id=order_id)

        # Send Order Confirmation Email
        subject = "Order Confirmation - Sayali's Kitchen"
        html_message = render_to_string('order/order_confirmation_email.html', {'order': customer_order})
        plain_message = strip_tags(html_message)
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [customer_order.emailAddress]

        send_mail(subject, plain_message, from_email, recipient_list, html_message=html_message)

        print("📧 Order confirmation email sent!")

    return render(request, 'thanks.html', {'customer_order': customer_order})

class orderHistory(LoginRequiredMixin, View):
    def get (self, request):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order_details = Order.objects.filter(emailAddress=email)
        return render(request, 'order/orders_list.html', {'order_details': order_details})

class orderDetail(LoginRequiredMixin, View):
    def get(self, request, order_id):
        if request.user.is_authenticated:
            email = str(request.user.email)
            order = Order.objects.get(id=order_id, emailAddress=email)
            order_items = OrderItem.objects.filter(order=order)

        return render(request, 'order/order_detail.html', {'order': order, 'order_items': order_items})



