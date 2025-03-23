from django.db import models

# Create your models here.
class ProductCategory(models.Model):
    name = models.CharField(max_length=200)

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.FloatField()
    stock = models.IntegerField()
    category = models.ForeignKey(ProductCategory,on_delete=models.SET_NULL,null=True)
    department = models.ManyToManyField('Department',blank=True) 

class Purchase(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    vendor = models.ForeignKey('Vendor',on_delete=models.SET_NULL,null=True)

class Sell(models.Model):
    product = models.ForeignKey(Product,on_delete=models.SET_NULL,null=True)
    quantity = models.IntegerField()
    price = models.FloatField()
    customer = models.ForeignKey('Customer',on_delete=models.SET_NULL,null=True)

class Customer(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    address = models.CharField(max_length=200)

class Vendor(models.Model):
    name = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    email = models.EmailField()
    number = models.CharField(max_length=20)
    company_address = models.CharField(max_length=200)

class Department(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    floor = models.IntegerField()

# Important
# ID field (PK)
# Created_at, Updated_at