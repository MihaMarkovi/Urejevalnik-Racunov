from django.db import models


# Create your models here.
class Company(models.Model):
    title = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    post_office = models.CharField(max_length=200)
    ddv_id = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Bill(models.Model):
    eor = models.CharField(max_length=100, primary_key=True)
    producer = models.ForeignKey(Company, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=200)
    seller = models.CharField(max_length=200)
    last_updated = models.DateTimeField('last updated')
    tax_level = models.FloatField()
    zoi = models.CharField(max_length=200)
    status = models.BooleanField()

    def __str__(self):
        return self.eor


class Product(models.Model):
    bill = models.ForeignKey(Bill, on_delete=models.CASCADE)
    product_title = models.CharField(max_length=200)
    quantity = models.IntegerField()
    value = models.FloatField()

    def __str__(self):
        return self.product_title
