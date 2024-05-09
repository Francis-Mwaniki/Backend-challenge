from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest
from django.shortcuts import render, redirect, get_object_or_404
from .forms import OrderForm
from .models import Order, Customer
import africastalking
import os
import requests
from dotenv import load_dotenv, find_dotenv

# import urllib3
# ssl._create_default_https_context = ssl._create_unverified_context
#load environment variables
load_dotenv(find_dotenv())  # Load environment variables from .env file

# Initialize AfricasTalking SDK
username = os.environ.get('AFRICAS_TALKING_USERNAME')
api_key =os.environ.get('AFRICAS_TALKING_API_KEY')
africastalking.initialize(username, api_key)
sms = africastalking.SMS

# @login_required
def create_order(request):
    if request.method == 'POST':
        
        customer_email = request.POST.get('customer')
        item = request.POST.get('item')
        amount = request.POST.get('amount')
        phoneNumber = request.POST.get('phoneNumber')
        print(f'customer: {customer_email}, item: {item}, amount: {amount}, phoneNumber: {phoneNumber}')

        if customer_email and item and amount and phoneNumber:
            customer = get_object_or_404(Customer, name=customer_email)
            # number must start with +254
            if phoneNumber.startswith('07'):
                # remove the first 0
                phoneNumber = phoneNumber[1:]
            if phoneNumber.startswith('254'):
                phoneNumber = f'+{phoneNumber}'
            if phoneNumber.startswith('7'):
                phoneNumber = f'+254{phoneNumber}'
            print(f'phone number: {phoneNumber}')            
            # add phone number to customer
            customer.phoneNumber = phoneNumber
            customer.save()
            print(f'customer new data-: {customer}')
            order = Order.objects.create(
                customer=customer,
                item=item,
                amount=amount
            )
             # Send SMS notification
            # recipients = ["+254769982944"]
            recipients=[phoneNumber]
            message = f"New order created: {item} - ${amount}"
            """Send SMS notification using AfricasTalking SDK"""
            send_sms(message, recipients)
            
            
            return redirect('order_detail', order_id=order.id)
        else:
            return HttpResponseBadRequest("Missing required data")
    else:
        form = OrderForm()
        return render(request, 'create_order.html', {'form': form})

# delete order
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('/')
    return render(request, 'delete_order.html', {'order': order})

    


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

# def send_sms(message, recipients):
#     """Send SMS notification using AfricasTalking API"""
#     username = "sandbox"  # Use "sandbox" for development in the test environment
#     api_key = "99c356dbdb8ab316795723f448a9c82121d8699fb52335d557a1ece6988fe1e5"
#     url = "https://api.sandbox.africastalking.com/version1/messaging"
#     headers = {
#         "ApiKey": api_key,
#         "Content-Type": "application/x-www-form-urlencoded",
#         "Accept": "application/json",
#         #certificate = True
        
        
#     }
#     data = {
#         "username": username,
#         "to": ",".join(recipients),
#         "message": message
#     }

#     try:
#         response = requests.post(url, headers=headers, data=data)
#         response.raise_for_status()  # Raise an exception for non-2xx status codes
#         print(response.text)
#     except requests.exceptions.RequestException as e:
#         print(f"Error sending SMS: {e}")