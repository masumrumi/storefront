from django.db import models

class Promotion(models.Model):
    description = models.CharField(max_length=255)
    discount = models.FloatField(max_length=255)

class Collection(models.Model):
    title = models.CharField(max_length=255)
    feature_product = models.ForeignKey('Product', on_delete=models.SET_NULL, null=True, related_name='+')
    

# Create your models here.
class Product(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    description = models.TextField()
    # for storing monatory values we should always use decimal field. 
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    inventory = models.IntegerField()
    # DateTimeField comes in with a couple of built-in validators, for example, auto_now_add will automatically set the value of the field to the current date and time whenever the object is first created. and auto_now will automatically update the value of the field to the current date and time whenever the object is saved.
    last_updated = models.DateTimeField(auto_now=True)
    # models.PROTECT is used to prevent the deletion of a related object and models.SET_NULL is used to set the foreign key to null. and models.CASCADE is used to delete the related object and models.DO_NOTHING is used to do nothing. and models.SET is used to set the foreign key to a specified value. and models.SET_DEFAULT is used to set the foreign key to a specified value. and models.
    # one to many relationship between product and collection
    collection = models.ForeignKey(Collection, on_delete=models.PROTECT)
    promotions = models.ManyToManyField(Promotion)
    
class Customer(models.Model):
    MEMBERSHIP_BRONZE = 'B'
    MEMBERSHIP_GOLD = 'G'
    MEMBERSHIP_SILVER = 'S'
    MEMBERSHIP_CHOICES = [
        (MEMBERSHIP_BRONZE, 'Bronze'),
        (MEMBERSHIP_GOLD, 'Gold'),
        (MEMBERSHIP_SILVER, 'Silver'),
    ]
    
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone = models.CharField(max_length=255)
    # null field is used to store null values, blank field is used to store empty values
    birth_date = models.DateField(null=True)
    membership = models.CharField(max_length=1, choices=MEMBERSHIP_CHOICES, default=MEMBERSHIP_BRONZE)
    
class Order(models.Model):
    PAYMENT_STATUS_PENDING = 'P'
    PAYMENT_STATUS_COMPLETED = 'C'
    PAYMENT_STATUS_FAILED = 'F'
    
    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_STATUS_PENDING, 'Pending'),
        (PAYMENT_STATUS_COMPLETED, 'Completed'),
        (PAYMENT_STATUS_FAILED, 'Failed'),
    ]
    placed_at = models.DateField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES, default=PAYMENT_STATUS_PENDING)
    # a customer can have multiple orders   
    # we are never deleting our orders because all these orders represet sales.
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT)
    

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveSmallIntegerField()
    
    # we need unit_price here because the price of the product can change anytime. So, we should have the price of the unit_price at the time the item was added to the order.
    unit_price = models.DecimalField(max_digits=6, decimal_places=2)
    
class Cart(models.Model):
    # auto_add_now_add is used to set the value of the field to the current date and time whenever the object is first created.
    created_at = models.DateTimeField(auto_now_add=True)
    
class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    
class Address(models.Model):
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zip = models.CharField(max_length=255, null=True)
    # models.OneToOneField() for one to one relationship and models.ForeignKey() for one to many relationship and models.ManyToManyField() for many to many relationship.
    
    customer = models.ForeignKey(
        Customer, 
        on_delete=models.CASCADE,
    )


