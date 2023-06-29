import json
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from .models import Customer, Milk, MilkPricing, MpesaPayment
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt


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


def daraja(request):
    cl = MpesaClient()
    phone_number = '0790360980'
    amount = 1
    account_reference = 'reference'
    transaction_desc = 'Description'
    callback_url = 'https://9402-2c0f-fe38-2401-f86f-f40e-186c-569-1717.ngrok-free.app/daraja/callback'
    # callback_url = 'https://api.darajambili.com/express-payment'
    response = cl.stk_push(phone_number, amount,
                           account_reference, transaction_desc, callback_url)
    return HttpResponse(response)



@csrf_exempt
def lipa_na_mpesa_callback(request):
    # print("status code ",request.status_code)
    # mpesa_body = request
    mpesa_body = request.body.decode('utf-8')
    mpesa_payment = json.loads(mpesa_body)
    print("callback")
    print(mpesa_payment)
    result_code = mpesa_payment['Body']['stkCallback']['ResultCode']
    context = {}
    if (result_code == 1032):
        context = {
            "ResultCode": 1032,
            "ResultDesc": "Canceled by user"
        }
    elif (result_code == 1):
        context = {
            "ResultCode": 1,
            "ResultDesc": "Insufficient funds"
        }
    elif result_code == 0:

        res_exp = {'Body':
                   {'stkCallback':
                    {'MerchantRequestID': '18756-4165353-1',
                     'CheckoutRequestID': 'ws_CO_23062023073426024790360980',
                     'ResultCode': 0,
                     'ResultDesc': 'The service request is processed successfully.',
                     'CallbackMetadata':
                         {'Item': [
                             {'Name': 'Amount', 'Value': 1.0},
                             {'Name': 'MpesaReceiptNumber', 'Value': 'RFN6Q44Y94'},
                             {'Name': 'TransactionDate', 'Value': 20230623073330},
                             {'Name': 'PhoneNumber', 'Value': 254790360980}
                         ]
                         }
                     }
                    }
                   }

        payment = MpesaPayment(
            phone_number=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][3]['Value'],
            amount=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][0]['Value'],
            receipt_number=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][1]['Value'],
            transaction_date=mpesa_payment['Body']['stkCallback']['CallbackMetadata']['Item'][2]['Value'],
            merchant_request_id=mpesa_payment['Body']['stkCallback']['MerchantRequestID'],
            checkout_request_id=mpesa_payment['Body']['stkCallback']['CheckoutRequestID']
        )
        payment.save()
        context = {
            "ResultCode": 0,
            "ResultDesc": "Success"
        }
    else:
        context = {
            "ResultCode": result_code,
            "ResultDesc": "Error. Something went wrong"
        }
    print(context)
    return HttpResponse(content=context)
