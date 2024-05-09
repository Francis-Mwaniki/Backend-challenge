import json
import random
import string
from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render, redirect
from django.urls import reverse
from urllib.parse import quote_plus, urlencode

from  myapp.models import Customer, Order

oauth = OAuth()
oauth.register(
    "auth0",
    client_id=settings.AUTH0_CLIENT_ID,
    client_secret=settings.AUTH0_CLIENT_SECRET,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f"https://{settings.AUTH0_DOMAIN}/.well-known/openid-configuration",
)

def index(request):
    customer = None
    orders = None
    if request.session.get("user"):
        email = request.session.get("user").get("userinfo", {}).get("email")
        # print(f'phone number: {request.session.get("user").get("userinfo", {}).get("phone_number")}')
        
        customer, _ = Customer.objects.get_or_create(name=email, defaults={"code": generate_unique_code()})
        all_customers_phone_numbers = Customer.objects.values_list('phoneNumber', flat=True)
        orders = Order.objects.filter(customer=customer)

    return render(
        request,
        "index.html",
        context={
            "session": request.session.get("user"),
            "pretty": json.dumps(request.session.get("user"), indent=4),
            "customer": customer,
            "orders": orders,
        },
    )

def callback(request):
    token = oauth.auth0.authorize_access_token(request)
    request.session["user"] = token
    return redirect(request.build_absolute_uri(reverse("index")))

def login(request):
    return oauth.auth0.authorize_redirect(
        request, request.build_absolute_uri(reverse("callback"))
    )

def logout(request):
    request.session.clear()
    return redirect(
        f"https://{settings.AUTH0_DOMAIN}/v2/logout?"
        + urlencode(
            {
                "returnTo": request.build_absolute_uri(reverse("index")),
                "client_id": settings.AUTH0_CLIENT_ID,
            },
            quote_via=quote_plus,
        ),
    )

def generate_unique_code():
    """Generate a unique code for the Customer model."""
    code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    while Customer.objects.filter(code=code).exists():
        code = "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
    return code