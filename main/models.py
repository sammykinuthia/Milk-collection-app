from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=200, default="")
    last_name = models.CharField(max_length=200, default="")
    username = models.CharField(max_length=200, default="")
    address = models.CharField(max_length=400, default="")
    phone = models.CharField(max_length=20, default="")
    is_active = models.BooleanField(default=True)
    registered_on = models.DateField(auto_now_add=True)
    class Meta:
        unique_together = [['first_name', 'last_name']]

    def __str__(self):
        return f"{self.username}"
        


class MilkPricing(models.Model):
    buying_price = models.DecimalField(max_digits=6, decimal_places=2)
    date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.buying_price)


class Milk(models.Model):
    date = models.DateTimeField(auto_now=True)
    is_payed = models.BooleanField(default=False)
    quantity = models.DecimalField(max_digits=6, decimal_places=2)
    price = models.DecimalField(max_digits=6, decimal_places=2, default=0.0)
    price_per_litre = models.ForeignKey(MilkPricing,on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)


class MpesaAuth(models.Model):
    initiation_time = models.DateTimeField(auto_now=True)
    token = models.CharField(max_length=20)
    expiration_time = models.DateTimeField(auto_now=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


# M-pesa Payment models

class MpesaCalls(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call'
        verbose_name_plural = 'Mpesa Calls'


class MpesaCallBacks(BaseModel):
    ip_address = models.TextField()
    caller = models.TextField()
    conversation_id = models.TextField()
    content = models.TextField()

    class Meta:
        verbose_name = 'Mpesa Call Back'
        verbose_name_plural = 'Mpesa Call Backs'


class MpesaPayment(BaseModel):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    type = models.TextField()
    reference = models.TextField()
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.TextField()
    organization_balance = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = 'Mpesa Payment'
        verbose_name_plural = 'Mpesa Payments'

    def __str__(self):
        return self.first_name
