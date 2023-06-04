from django.db import models


# Create your models here.
class Car(models.Model):
    id = models.BigAutoField(primary_key=True)
    carmake = models.CharField(max_length=15)

    def __str__(self):
        return f'{self.carmake}'


class Client(models.Model):
    clientcity = models.CharField(max_length=15)
    clientcar = models.ForeignKey(Car, on_delete=models.CASCADE)
    clientname = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.clientname}-{self.clientcity}-{self.clientcar}'


class Service(models.Model):
    id = models.BigAutoField(primary_key=True)
    servicename = models.CharField(max_length=100)
    price = models.IntegerField()

    def __str__(self):
        return f'{self.servicename}-{self.price}'


class Serviceclient(models.Model):
    id = models.BigAutoField(primary_key=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    service = models.ManyToManyField(Service)
    date_service = models.DateTimeField()

    def __str__(self):
        return f'{self.client}-{self.service}'
