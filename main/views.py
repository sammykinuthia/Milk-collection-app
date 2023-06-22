from django.http import HttpResponse, JsonResponse
from .models import MpesaPayment
from django.views.decorators.csrf import csrf_exempt
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPpassword, MpesaC2bCredential
import json
from requests.auth import HTTPBasicAuth
import requests
from django_daraja.mpesa.core import MpesaClient
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Customer, Milk, MilkPricing
from django.urls import reverse


@login_required(login_url='/accounts/login')
def index(request):
    try:
        if request.method == "GET":
            return render(request, 'index.html')
        if request.method == "POST":
            quantity = float(request.POST['quantity'])
            customerid = request.POST['customer']
            customer = Customer.objects.get(pk=customerid)
            milk_price = MilkPricing.objects.last()
            price = float(milk_price.buying_price) * quantity
            print(price)
            milk = Milk.objects.create(
                quantity=quantity, customer=customer, price_per_litre=milk_price, price=price)
            return HttpResponseRedirect(reverse(index))
    except ValueError as e:
        return render(request, 'index.html', {'error': e})


@login_required(login_url='/accounts/login')
def get_customers(request):
    customers = list(Customer.objects.all().values(
        'username', 'id', 'address'))
    return JsonResponse(customers, safe=False)


@login_required(login_url='/accounts/login')
def get_customer(request, username):
    try:
        customer = Customer.objects.get(username=username, is_active=True)
        # return HttpResponse("DATA")
        return JsonResponse({"firstname": customer.first_name, "username": customer.username,  "phone": customer.phone, "lastName": customer.last_name, "address": customer.address, "id": customer.id}, safe=False)
    except Exception as e:
        return JsonResponse({"error": username+" not found"}, safe=False)


@login_required
def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse(index))


def pay(request):
    cl = MpesaClient()
    phone_number = '0790360980'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount,
                           account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


def daraja(request):
    cl = MpesaClient()
    phone_number = '0790360980'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https:127.0.0.1:8000/daraja/callback'
    # callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount,
                           account_reference, transaction_desc, callback_url)
    return HttpResponse(response)


def getAccessToken(request):
    consumer_key = MpesaC2bCredential.consumer_key
    consumer_secret = MpesaC2bCredential.consumer_secret
    api_URL = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r = requests.get(api_URL, auth=HTTPBasicAuth(
        consumer_key, consumer_secret))
    mpesa_access_token = json.loads(r.text)
    validated_mpesa_access_token = mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)


def lipa_na_mpesa_online(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": "Bearer %s" % access_token}
    request = {
        "BusinessShortCode": LipanaMpesaPpassword.Business_short_code,
        "Password": LipanaMpesaPpassword.decode_password,
        "Timestamp": LipanaMpesaPpassword.lipa_time,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": 1,
        "PartyA": 254790360980,  # replace with your phone number to get stk push
        "PartyB": LipanaMpesaPpassword.Business_short_code,
        "PhoneNumber": 254790360980,  # replace with your phone number to get stk push
        "CallBackURL": "https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference": "Samuel",
        "TransactionDesc": "Testing stk push"
    }

    response = requests.post(api_url, json=request, headers=headers)
    return HttpResponse(response)


@csrf_exempt
def register_urls(request):
    access_token = MpesaAccessToken.validated_mpesa_access_token
    api_url = "https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers = {"Authorization": "Bearer %s" % access_token}
    options = {"ShortCode": LipanaMpesaPpassword.Business_short_code,
               "ResponseType": "Completed",
               "ConfirmationURL": "https://9402-2c0f-fe38-2401-f86f-f40e-186c-569-1717.ngrok-free.app/app/c2b/confirmation",
               "ValidationURL": "https://9402-2c0f-fe38-2401-f86f-f40e-186c-569-1717.ngrok-free.app/c2b/validation"}
    response = requests.post(api_url, json=options, headers=headers)

    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass


@csrf_exempt
def validation(request):

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }
    print(request)
    return JsonResponse(dict(context))


@csrf_exempt
def confirmation(request):
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)

    payment = MpesaPayment(
        first_name=mpesa_payment['FirstName'],
        last_name=mpesa_payment['LastName'],
        middle_name=mpesa_payment['MiddleName'],
        description=mpesa_payment['TransID'],
        phone_number=mpesa_payment['MSISDN'],
        amount=mpesa_payment['TransAmount'],
        reference=mpesa_payment['BillRefNumber'],
        organization_balance=mpesa_payment['OrgAccountBalance'],
        type=mpesa_payment['TransactionType'],

    )
    payment.save()

    context = {
        "ResultCode": 0,
        "ResultDesc": "Accepted"
    }

    return JsonResponse(dict(context))
