from django import forms
from django.forms import ModelForm
from datetime import date
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from .models import UserInfo, Payment
from django.contrib.auth import authenticate, login
from django.contrib import messages
import datetime
class RegisterForm(forms.Form):
    GRADE_CHOICES = ( 
                (9,'9'), (10,'10'), (11,'11'), (12,'12') , 
            )
    curr_year = date.today().year
    if date.today().month > 6:
        curr_year=curr_year+1
    GRAD_YEAR_CHOICES = ( 
                (curr_year,curr_year), (curr_year+1,curr_year+1), (curr_year+2,curr_year+2), (curr_year+3,curr_year+3) , 
                 )
    first_name = forms.CharField(max_length = 25)
    username = forms.CharField(max_length = 25)
    last_name = forms.CharField( max_length = 25)
    emailid = forms.EmailField()
    passwd1 = forms.CharField(max_length=100,widget=forms.PasswordInput)
    passwd2 = forms.CharField(max_length=100,widget=forms.PasswordInput)
    gradyear = forms.ChoiceField( choices=GRAD_YEAR_CHOICES)
    grade = forms.ChoiceField( choices=GRADE_CHOICES)
    pin = forms.DecimalField(max_digits=4, decimal_places=0)
    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        print cleaned_data   
        return cleaned_data

class PaymentForm(forms.Form):
    pin = forms.DecimalField(max_digits = 4, decimal_places = 0)
    quantity = forms.DecimalField(max_digits = 3, decimal_places=0)
    def clean(self):
        cleaned_data = super(PaymentForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class LoginForm(forms.Form):
    username = forms.CharField(max_length = 25)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        try:
            username = cleaned_data['username']
            password = cleaned_data['password']
        except:
            raise forms.ValidationError({'username':['username/password required']})

        user = authenticate(username=username, password=password)
        if user is not None:
            print "user not none"
            print user.username
            print user.email
        else:
            print "login failed"
            raise forms.ValidationError({'username':['Invalid username/password']})

        return cleaned_data

class OrderForm(forms.Form):
    pin = forms.DecimalField(max_digits=4, decimal_places=0)
    #if pin < 0:
	   #raise forms.ValidationError({'pin':['Invalid PIN']})
    def clean(self):
        cleaned_data = super(OrderForm, self).clean()

        return cleaned_data

class CancelForm(forms.Form):
    first_name = forms.CharField(max_length = 25)
    last_name = forms.CharField( max_length = 25)
    pin = forms.DecimalField(max_digits=4, decimal_places=0)
    event = forms.CharField( max_length = 25)
    #if pin < 0:
       #raise forms.ValidationError({'pin':['Invalid PIN']})
    def clean(self):
        cleaned_data = super(CancelForm, self).clean()

        return cleaned_data

class ForgotForm(forms.Form):
    first_name = forms.CharField( max_length = 25)
    last_name = forms.CharField( max_length = 25)
    username = forms.CharField( max_length = 25)
    pin = forms.DecimalField(max_digits = 4, decimal_places = 0)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super(ForgotForm, self).clean()

        return cleaned_data

class ChangeForm(forms.Form):
    pinadd = forms.DecimalField(max_digits = 4, decimal_places = 0)
    total_to_add = forms.DecimalField(max_digits = 5, decimal_places=2)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(ChangeForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class AddForm(forms.Form):
    pinadd = forms.DecimalField(max_digits = 4, decimal_places = 0)
    total_to_add = forms.DecimalField(max_digits = 5, decimal_places=2)
    password = forms.CharField(max_length=100,widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(AddForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class DisplayForm(forms.Form):
    date = forms.DateField()
    def clean(self):
        cleaned_data = super(DisplayForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class ChangeForm(forms.Form):
    name = forms.CharField(max_length = 100)
    email = forms.EmailField()
    message = forms.CharField(max_length=300)
    pin = forms.DecimalField(max_digits=4, decimal_places=0,widget=forms.PasswordInput)
    def clean(self):
        cleaned_data = super(ChangeForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class MessageForm(forms.Form):
    name = forms.CharField(max_length = 100, widget=forms.TextInput(attrs={'placeholder': 'Name'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Email'}))
    message = forms.CharField(max_length=300, widget=forms.TextInput(attrs={'placeholder': 'Message'}))
    def clean(self):
        cleaned_data = super(MessageForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class AddEventForm(forms.Form):
    description = forms.CharField(max_length = 300)
    name = forms.CharField(max_length = 300)
    cost = forms.DecimalField(max_digits=5, decimal_places=2)
    event_date = forms.DateField(initial=datetime.date.today)
    pin = forms.DecimalField(max_digits=4, decimal_places=0,widget=forms.PasswordInput)
    regular_lunch = forms.CharField(max_length=1)
    def clean(self):
        cleaned_data = super(AddEventForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data

class TakeOutForm(forms.Form):
    amount = forms.DecimalField(max_digits=7, decimal_places=2)
    password = forms.CharField(max_length = 300,widget=forms.PasswordInput(attrs={'color': 'black'}))
    def clean(self):
        cleaned_data = super(TakeOutForm, self).clean()

        #if User.objects.filter(first_name != cleaned_data['first_name']).count():
            #raise forms.ValidationError({'first_name':['Name does not exist']})
        #if User.objects.filter(pin != cleaned_data['pin']).count():
            #raise forms.ValidationError({'pin':['pin']})

        return cleaned_data
