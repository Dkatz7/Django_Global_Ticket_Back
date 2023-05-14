from django.db import models
from django.contrib.auth.models import User


### This model hold the Images of Events ###
class EventImage(models.Model):
    title=models.CharField(max_length=100, default='Default Title')
    image=models.ImageField(upload_to='static\images')
    alt_text = models.CharField("Image Alt Text", max_length=100, blank=True)

### This model hold the Event's information ####
class Event(models.Model):
    event_name = models.CharField("Event Name", max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    date_and_time = models.DateTimeField()
    image = models.ForeignKey(EventImage, on_delete=models.SET_NULL,null=True)
    location = models.CharField("Location", max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.DecimalField(max_digits=10, decimal_places=2)
    created_time = models.DateTimeField(auto_now_add=True)
    meta_title = models.CharField("Meta Title", max_length=100, blank=True)
    meta_description = models.TextField(blank=True)
 
    def __str__(self):
           return self.event_name

### This model hold the User's Information ####
class UserInformation(models.Model):
    user = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    firstname = models.CharField("First Name", max_length=20)
    lastname = models.CharField("Last Name", max_length=20)
    age = models.FloatField()
    email = models.EmailField(default='example@domain.com')
    city = models.CharField(max_length=20)
    address = models.CharField(max_length=75)
    postalcode = models.FloatField()

    def __str__(self):
        return self.firstname

### This model hold the information about Orders ###
class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    date_and_time = models.DateTimeField("Order Date and Time", auto_now_add=True)
    quantity = models.PositiveIntegerField("Quantity")
    subtotal = models.DecimalField("Subtotal", max_digits=10, decimal_places=2)

### This model hold the information about Purchase ###
class Purchase(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    date = models.DateTimeField(auto_now_add=True)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)

