from django.db import models
from django.contrib.auth.models import User 
from datetime import date, datetime

class UserInfo(models.Model):
    user = models.OneToOneField(User, related_name='user_infos')
    class_of = models.IntegerField()
    #username = user.username
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 30)
    email = models.EmailField(max_length = 100) 
    #Staff = user.is_staff
    pub_date = models.DateField(default=date.today)
    grade = models.IntegerField()
    balance = models.DecimalField(max_digits=6, decimal_places=2)
    pin = models.DecimalField(max_digits=4, decimal_places=0)
    #first_name = models.CharField(max_length = 25)
    id = models.IntegerField(primary_key = True)
class Events(models.Model):
    name = models.CharField(max_length = 80)
    event_date = models.DateField(default=date.today)
    cost = models.DecimalField(max_digits = 6, decimal_places = 2)
    description = models.CharField(max_length = 500)
    class_of = models.CharField(max_length = 20)
    regular_lunch = models.BooleanField()
    def __unicode__(self):
        return str(self.name)

class Payment(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    payment_date = models.DateField(default=date.today)
    event = models.CharField(max_length = 25)
    user_id = models.IntegerField()
    quantity = models.DecimalField(max_digits = 3, decimal_places=0)
    price_of_each = models.DecimalField(max_digits = 5, decimal_places=2)
    total_cost = models.DecimalField(max_digits = 6, decimal_places=2)
    class_of = models.CharField(max_length = 20)
    def __unicode__(self):
        return str(self.total_cost)

class Cancel(models.Model):
    first_name = models.CharField(max_length = 25)
    last_name = models.CharField(max_length = 25)
    cancel_date = models.DateField(default=date.today)
    event = models.CharField(max_length = 25)
    class_of = models.CharField(max_length = 20)
    user_id = models.IntegerField()
    quantity = models.DecimalField(max_digits = 3, decimal_places=0)
    price_of_each = models.DecimalField(max_digits = 5, decimal_places=2)
    total_cost = models.DecimalField(max_digits = 6, decimal_places=2)
    def __unicode__(self):
        return str(self.total_cost)

class PastEvent(models.Model):
    name = models.CharField(max_length = 80)
    event_date = models.DateField(default=date.today)
    cost = models.DecimalField(max_digits = 6, decimal_places = 2)
    description = models.CharField(max_length = 500)
    class_of = models.CharField(max_length = 20)
    regular_lunch = models.BooleanField()
    def __unicode__(self):
        return str(self.name)

class Distribution(models.Model):
    name = models.CharField(max_length = 50)
    money = models.DecimalField(max_digits = 6, decimal_places=2)
    def __unicode__(self):
        return str(self.money)

class IOU(models.Model):
	first_name = models.CharField(max_length = 25)
	last_name = models.CharField(max_length = 30)
	student_id = models.IntegerField()
	class_of = models.CharField(max_length = 20)
	amount = models.DecimalField(max_digits = 6, decimal_places = 2)
	last_date = models.DateField(default=date.today)

class TempDate(models.Model):
    date = models.DateField()
