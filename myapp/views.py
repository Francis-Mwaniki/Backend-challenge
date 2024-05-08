from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, Customer
import africastalking

# Initialize AfricasTalking SDK
username = "sandbox"  # Use "sandbox" for development in the test environment
api_key = "YOUR_API_KEY"
africastalking.initialize(username, api_key)
sms = africastalking.SMS


# @login_required
def create_order(request):
    if request.method == 'POST':
        customer_email = request.POST.get('customer')
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        print(f'customer: {customer_email}, item: {item}, amount: {amount}')

        if customer_email and item and amount:
            customer = get_object_or_404(Customer, name=customer_email)
            order = Order.objects.create(
                customer=customer,
                item=item,
                amount=amount
            )
             # Send SMS notification
            recipient_number = "+254769982944"  # Replace with your phone number
            message = f"New order created: {item} - ${amount}"
            send_sms(message, [recipient_number])
            
            return redirect('order_detail', order_id=order.id)
        else:
            return HttpResponseBadRequest("Missing required data")
    else:
        form = OrderForm()
        return render(request, 'create_order.html', {'form': form})


def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'order_detail.html', {'order': order})

def send_sms(message, recipients):
    """Send SMS notification using AfricasTalking SDK"""
    try:
        response = sms.send(message, recipients)
        print(response)
    except Exception as e:
        print(f"Error sending SMS: {e}")