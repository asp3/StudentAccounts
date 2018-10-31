from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.conf.urls import url
from .models import UserInfo, Events, Payment, Cancel, Distribution, IOU, PastEvent, TempDate
from django import forms
from .forms import RegisterForm, LoginForm, OrderForm, PaymentForm, CancelForm, ForgotForm, ChangeForm, AddForm, DisplayForm, MessageForm, AddEventForm, TakeOutForm
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.utils.crypto import get_random_string
from django.db.models import Max, Sum
from datetime import date, timedelta
import time
# Create your views here.

def deleteevent():
    yesterday = date.today() - timedelta(1)
    if Events.objects.filter(event_date = yesterday).count():
        a = PastEvent()
        temp = 0
        c = Events.objects.filter(event_date = yesterday)
        for Event in Events.objects.filter(event_date = yesterday):
            b = c[temp]
            a.name = b.name
            a.event_date = b.event_date
            a.cost = b.cost
            a.description = b.description
            a.class_of = b.class_of
            a.regular_lunch = b.regular_lunch
            a.save()
            temp += 1
        Events.objects.filter(event_date = yesterday).delete()
    print 'ASDASDATHISWORKS THIS WORKS'

def home(request):
    deleteevent()
    if request.method == 'POST':
        form = MessageForm(request.POST)
        try:
            if form.is_valid():
                s = 'Feedback'
                m = "You have a new message from\n" + form.cleaned_data['name'] +" - " + form.cleaned_data['email'] + "\nMessage:\n" + form.cleaned_data['message']
                send_mail(s,m, 'from@support-team.com',['abhi12.p@gmail.com, kunaladhia01@gmail.com'], fail_silently=False)
            else:
                print form.errors
        except:
            raise
            
    else:
        print "hello"
        form = MessageForm()

    return render(request, 'student/index.html', {'form': form})

@csrf_exempt
def signin(request):
    deleteevent()
    print "login"
    if request.method == 'POST':
        form = LoginForm(request.POST)
        username = request.POST['username']
        password = request.POST['password']
        print "input username ", username
        try:
            if form.is_valid():
                user = authenticate(username=username, password=password)
                if user is not None:
                    print "user not none"
                    print user.username
                    print user.email
                    login(request,user)
                    return redirect("/student/dashboard")
                else:
                    print "login failed"
                    raise forms.ValidationError({'username':['Invalid username/password']})
            else:
                print form.errors
        except:
            raise
            

    else:
        print "hello"
        form = LoginForm()

    return render(request, 'student/login.html', {'form': form})

@csrf_exempt
def signup(request):
    deleteevent()
    print "signup"
    if request.method == 'POST':
        print "post signup"
        form = RegisterForm(request.POST)
        try:
            if form.is_valid():
                print form.cleaned_data
    	        if form.cleaned_data['passwd1'] != form.cleaned_data['passwd2']:
                        messages.add_message(request, messages.ERROR, 'Passwords do not match.')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if User.objects.filter(email=form.cleaned_data['emailid']).count():
                        messages.add_message(request, messages.ERROR, 'Email already in Use')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if UserInfo.objects.filter(pin=form.cleaned_data['pin']).count():
                        messages.add_message(request, messages.ERROR, 'Pin already taken')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if User.objects.filter(username=form.cleaned_data['username']).count():
                        messages.add_message(request, messages.ERROR, 'Username already taken')
                        return HttpResponseRedirect(request.META.get('HTTP_REFERER')) 
                u = User.objects.create_user(form.cleaned_data['username'], form.cleaned_data['emailid'], form.cleaned_data['passwd1'] )
                ui = UserInfo()
                ui.user = u
                ui.class_of = form.cleaned_data['gradyear']
                ui.grade = form.cleaned_data['grade']
                ui.balance = 0
                ui.pin = form.cleaned_data['pin']
		ui.id = u.id
                u.first_name = form.cleaned_data['first_name']
		ui.first_name = form.cleaned_data['first_name']
                u.last_name = form.cleaned_data['last_name']
		ui.last_name = form.cleaned_data['last_name']
		ui.email = form.cleaned_data['emailid']
                u.username = form.cleaned_data['username']
                u.save()
		print u.id
                ui.save()
		#j = User.objects.get(id = 3932)
		#print j
                print "DONE"
                user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['passwd1'])
                login(request,user)
                print "after login in signup"
                return redirect("/")


            else:
                print "error"
                print form.errors
        except:
            raise
            print "error here"
            print form.errors
            pass
            #return render(request, 'student/register.html', {'form': form})
            
    else:
        form = RegisterForm()

    return render(request, 'student/register.html', {'form': form})

def forgot(request):
    deleteevent()
    if request.method == 'POST':
        form = ForgotForm(request.POST)
        print 'Test'
        if form.is_valid():
            print form.cleaned_data
        if not User.objects.filter(username=form.cleaned_data['username']).exists():
            messages.add_message(request, messages.ERROR, 'Invalid Username!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not User.objects.filter(email=form.cleaned_data['email']).exists():
            messages.add_message(request, messages.ERROR, 'Invalid Email!')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if User.objects.get(username=form.cleaned_data['username']).email != form.cleaned_data['email']:
            messages.add_message(request, messages.ERROR, 'Email and Username do not match')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        temppass = get_random_string(length=8)
        print temppass
        a = make_password(temppass, salt=None, hasher='default')
        c = User.objects.get(email=form.cleaned_data['email'])
        c.password = a
        temppin = str(UserInfo.objects.get(user_id=c.id).pin)
        c.save()
        name = form.cleaned_data['first_name']
        s = 'Password Recovery'
        m = 'Hello ' + name + '! You seem to have forgotten your password. No worries, we got you covered. Your new password (for now, you can change it later), is: ' + temppass + ' and your pin (if you forgot) is: ' + temppin
        t = form.cleaned_data['email']
        send_mail(s,m, 'from@support-team.com',[t], fail_silently=False)
    else:
         form = ForgotForm()

    return render(request, 'student/forgot.html', {'form': form})


def studentinfo(request):
    deleteevent()
    if request.user.is_anonymous():
        messages.add_message(request, messages.ERROR, '    Please Login First before Ordering')
        return redirect("/student/login")
    return render(request, 'student/studentinfo.html', {} )
    
def error(request):
    deleteevent()
    return render(request, 'student/LoginError.html', {} )

def site_logout(request):
    deleteevent()
    logout(request)
    return redirect("/")
    #return render(request, 'student/studentinfo.html', {} )

def order(request):
        deleteevent()
	if request.user.is_anonymous():
		messages.add_message(request, messages.ERROR, '    Please Login First before Ordering')
		return redirect("/student/login")
        a = Events.objects.all().count()
        print a
        c = Events.objects.all()
        latest_event_list = c.order_by('-id')[:a]
	latest_event_list = latest_event_list[::-1]
        #output = ', '.join([str(p.cost) for p in latest_event_list])
        output = {'latest_event_list': latest_event_list}
        print latest_event_list
        print output
	if request.method == 'POST':
		print "POST"
		form = OrderForm(request.POST)
		print form
        else:
		form = OrderForm()	
	return render(request, 'student/orderform.html', {'output': output})

def dashboard(request):
    deleteevent()
    if request.user.is_anonymous():
        messages.add_message(request, messages.ERROR, '    Please Login First before accessing the Dashboard')
        return redirect("/student/login")
    user = request.user

    temp = Payment.objects.filter(user_id=user.id)
    tempint = len(temp)
    a = Payment.objects.order_by('-id')[:tempint]
    a = a[::-1]
    b = {'latest_event_list': a}
    print a
    return render(request, 'student/dashboard.html', {'b': b})

def blog(request):
    deleteevent()
    if request.user.is_anonymous():
        messages.add_message(request, messages.ERROR, '    Please Login First before Viewing the Blog')
        return redirect("/student/login")
    return render(request, 'student/blog.html')

#def control(request):
#    return render(request, 'student/control.html')
def preorder(request, event_id):
        deleteevent()
        if request.user.is_anonymous():
            messages.add_message(request, messages.ERROR, '    Please Login First before Ordering')
            return redirect("/student/login")
        a = Events.objects.all().count()
        c = Events.objects.all()
	latest_event_list = c.order_by('-id')[:a]
	latest_event_list = latest_event_list[::-1]
	print latest_event_list
	print int(event_id) - 1
	event_name = str(latest_event_list[int(event_id)-1])
	print event_name
	u = Events.objects.get(id = int(event_id))
	description = u.description
	cost = u.cost
        u.regular_lunch = not u.regular_lunch
        if  u.regular_lunch == False:
            letorder = 0
        else:
            letorder = 1

        #output = ', '.join([str(p.cost) for p in latest_event_list])
        output = {'latest_event_list': latest_event_list}
        print 'pre-post data'
	if request.method == 'POST':
		print 'POST'
		form = OrderForm(request.POST)
		try:
		    if form.is_valid():
                        if letorder == 0:
                            messages.add_message(request, messages.ERROR, 'You Cannot Order this Item')
                            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
		    	print form.cleaned_data['pin']
			p = Payment()
			q = UserInfo.objects.get(id = request.user.id)
                        y = User.objects.get(id=request.user.id)
                        print q.pin
                        print form.cleaned_data['pin']
                        if q.pin != form.cleaned_data['pin']:
				messages.add_message(request, messages.ERROR, '    Incorrect Pin')
                		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			if Payment.objects.filter(first_name = y.first_name, last_name = y.last_name, event = event_name).count():
				messages.add_message(request, messages.ERROR, 'You have already purchaced this item!')
				return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
			else:
				p.first_name = y.first_name
				p.last_name = y.last_name
				p.event = event_name
				b = Events.objects.get(name=event_name)
                                if Distribution.objects.filter(name=b.class_of).count() == 0:
                                    f = Distribution(name=b.class_of, money='0')
                                    f.save()
				c = Distribution.objects.get(name=b.class_of)
				d = Distribution.objects.get(name='Total')
				p.class_of = b.class_of
				c.money += cost
				d.money -= cost
				c.save()
				d.save()
				p.quantity = 1
				p.price_of_each = cost
				p.total_cost = cost
				p.user_id = y.id
				original_balance = q.balance
                        	q.balance = q.balance - p.total_cost
				new_balance = q.balance
				if new_balance < 0:
                    
					amount_owed = 0
					if original_balance <= 0:
						amount_owed = cost
					else:
						print original_balance
						print cost
						amount_owed = cost - original_balance
					if IOU.objects.filter(class_of = p.class_of, student_id  = y.id).count():
						iou = IOU.objects.get(class_of = p.class_of, student_id  = y.id)
						iou.amount += amount_owed
						iou.save()
					else:
						iou = IOU()
						iou.first_name = q.first_name
						iou.last_name = q.last_name
						iou.student_id = y.id
						iou.class_of = p.class_of
						iou.amount = amount_owed
						iou.save()						 
				q.save()
				p.save()
		    else:
		    	print "error"
		except:
			raise
			pass
	else:
		form = OrderForm()
		
	return render(request, 'student/event.html', {'event': u})
    
def checkout(request):
    datetodisplay = 'N'
    deleteevent()
    print request.user.id
    if not request.user.is_superuser:
        messages.add_message(request, messages.ERROR, 'Please Login with a Superuser Account before using control')
        return redirect("/student/login")
    if request.method == 'POST':
        print "post payment"
        pay = PaymentForm(request.POST, prefix='pay')
        try:
            if pay.is_valid():
                print pay.cleaned_data
                u = Payment()
                if not UserInfo.objects.filter(pin=pay.cleaned_data['pin']).exists():
                    messages.add_message(request, messages.ERROR, 'Invalid Pin')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))          
                print request.user.id
                original = UserInfo.objects.get(id=request.user.id)
                if Distribution.objects.filter(name=original.class_of).count() == 0:
                    c = Distribution(name=original.class_of, money='0')
                    c.save()
                loaded_event = Events.objects.filter(regular_lunch = True).order_by('-event_date')[::-1][0]
                print loaded_event
                c = Distribution.objects.get(name=original.class_of)
                print original.balance
                q = UserInfo.objects.get(pin=pay.cleaned_data['pin'])
                a = User.objects.get(id=q.user_id)
                print a.id
                print original.balance
                u.pin = pay.cleaned_data['pin']
                u.quantity = pay.cleaned_data['quantity']
                u.price_of_each = loaded_event.cost
                u.total_cost = loaded_event.cost*pay.cleaned_data['quantity']
                u.first_name = a.first_name
                u.last_name = a.last_name
                u.class_of = original.class_of
                u.user_id = a.id
                u.event = loaded_event.name
                print u.first_name
                print u.last_name
                print c.money
                print u.total_cost
                c.money += u.total_cost
                original_balance = q.balance
                q.balance = q.balance - u.total_cost
                new_balance = q.balance
                print new_balance
                print original_balance
                c.save()
                print 'ASDASDASDASDASDSDSD'
                if new_balance < 0:
                    amount_owed = 0
                    if original_balance <= 0:
                        amount_owed = u.total_cost
                        print amount_owed
                    else:
                        print original_balance
                        print u.total_cost
                        amount_owed = u.total_cost - original_balance
                    if IOU.objects.filter(class_of = original.class_of, student_id  = a.id).count():
                        iou = IOU.objects.get(class_of = original.class_of, student_id  = a.id)
                        iou.amount += amount_owed
                        iou.save()
                    else:
                        iou = IOU()
                        iou.first_name = a.first_name
                        iou.last_name = a.last_name
                        iou.student_id = q.id
                        iou.class_of = original.class_of
                        iou.amount = amount_owed
                        iou.save()
                st = "%s spent $%s" % (u.first_name, u.total_cost)
                u.save()
                q.save()
                print "after login in signup"
                messages.add_message(request, messages.INFO, st)
                return redirect("/student/checkout")


            else:
                print "error"
                print pay.errors
        except:
            raise
            print "error here"
            print pay.errors
            pass
            #return render(request, 'student/register.html', {'pay': pay})
    if request.method == 'POST' and not pay.is_valid():
        add = AddForm(request.POST, prefix ='add')
        try:
            if add.is_valid():
                print add.cleaned_data
                pay = Payment()
                if not UserInfo.objects.filter(pin=add.cleaned_data['pinadd']).exists():
                    messages.add_message(request, messages.ERROR, 'Invalid Pin')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                if not check_password(add.cleaned_data['password'], User.objects.get(id=request.user.id).password):
                    messages.add_message(request, messages.ERROR, 'Password is Incorrect')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
                original = UserInfo.objects.get(pin=add.cleaned_data['pinadd'])
                user = User.objects.get(id=original.user_id)
                owes_money = False
                if IOU.objects.filter(student_id=original.id).exists():
                    owes_money = True
                print original.balance
                pay.pin = add.cleaned_data['pinadd']
                pay.quantity = 1
                pay.price_of_each = add.cleaned_data['total_to_add']
                dist = Distribution.objects.get(name='Total')
                pay.first_name = original.first_name
                pay.last_name = original.last_name
                pay.user_id = original.pin
                pay.total_cost = pay.price_of_each
                dist.money += pay.total_cost
                original.balance += pay.total_cost
                print "owes money:"
                print owes_money
                if owes_money:
                        owes_count = IOU.objects.filter(student_id = original.id).count()
                        pay.event = 'AddforIOU'
                        print owes_count
                        if owes_count == 1:
                                only_one = IOU.objects.get(student_id = original.id)
                                if pay.total_cost >= only_one.amount:
                                        print "done"
                                        only_one.delete()
                                else:
                                        only_one.amount -= pay.total_cost
                                        only_one.save()
                        else:
                                print "else"
                                owe_list = IOU.objects.filter(student_id = original.id).order_by('-class_of')[:10][::-1]
                                dist_list = [0 for x in range(len(owe_list))]
                                total_owed = 0
                                for i in range(owes_count):
                                        total_owed += owe_list[i].amount
                                        owe_list[i] = IOU.objects.get(student_id = original.id, class_of = owe_list[i].class_of)
                                        dist_list[i] = Distribution.objects.get(name = owe_list[i].class_of)
                                print dist_list
                                print total_owed
                                total_owed = pay.total_cost
                                print total_owed
                                payer_count = 0
                                while True:
                                        if owes_count == 0:
                                                break
                                        if total_owed <= 1 and total_owed <= owe_list[payer_count % owes_count].amount:
                                                print "a"
                                                owe_list[payer_count % owes_count].amount -= total_owed
                                                dist_list[payer_count % owes_count].money += total_owed
                                                if owe_list[payer_count % owes_count].amount == 0:
                                                        temp = owe_list[payer_count % owes_count] 
                                                        owe_list.pop(payer_count % owes_count)
                                                        dist_list.pop(payer_count % owes_count)
                                                        temp.delete()
                                                        owes_count -= 1
                                                break
                                        else:   
                                                if owe_list[payer_count % owes_count].amount <= 1 and total_owed:
                                                        print "b"
                                                        total_owed -= owe_list[payer_count % owes_count].amount
                                                        dist_list[payer_count % owes_count].money += owe_list[payer_count % owes_count].amount
                                                        temp = owe_list[payer_count % owes_count]
                                                        owe_list.pop(payer_count % owes_count)
                                                        dist_list.pop(payer_count % owes_count)
                                                        temp.delete()
                                                        owes_count -= 1
                                                else:   
                                                        print "c"
                                                        owe_list[payer_count % owes_count].amount -= 1
                                                        dist_list[payer_count % owes_count].money += 1
                                                        print dist_list[payer_count % owes_count].money
                                                        total_owed -= 1
                                                payer_count += 1    
                                                print total_owed
                                                print owe_list
                                                print owe_list[payer_count % owes_count].amount
                                for i in range(owes_count):
                                        owe_list[i].save()
                                        dist_list[i].save()
                                owe_list[0].save()
                else:
                    pay.event = 'Add'
                dist.save()
                pay.class_of = "None"
                st = "%s added $%s" % (pay.first_name, pay.total_cost)
                pay.save()
                original.save()
                messages.add_message(request, messages.INFO, st)
                return redirect("/student/checkout")
            else:
                print "error"
                print pay.errors
        except:
            raise
            print "error here"
            print add.errors
            pass
    if request.method == 'POST' and not pay.is_valid() and not add.is_valid():
        display = DisplayForm(request.POST, prefix ='display')
        print "HELLO WORLD"
        if display.is_valid():
            print 'asdfasdfasdfasdfasdfasdfasdfsad'
            temp = display.cleaned_data['date']
            c = TempDate()
            c.date = temp
            c.id = 1
            c.save()
            ui = UserInfo.objects.get(id = request.user.id)
            if not Payment.objects.filter(payment_date=display.cleaned_data['date'], class_of = ui.class_of).count():
                messages.add_message(request, messages.ERROR,'No Payments for this Date')
                return redirect("/student/checkout")
            return redirect ("/student/display")
        if request.method == 'POST' and not pay.is_valid() and not add.is_valid() and not display.is_valid():
            addevent = AddEventForm(request.POST, prefix ='addevent')
            if addevent.is_valid():
                print addevent.cleaned_data
                ui = UserInfo.objects.get(id = request.user.id)
                e = Events()
                if addevent.cleaned_data['pin'] != ui.pin:
                    messages.add_message(request, messages.ERROR,'Invalid Pin')
                    return redirect("/student/checkout")
                e.name = addevent.cleaned_data['name']
                e.description = addevent.cleaned_data['description']
                e.cost = addevent.cleaned_data['cost']
                e.class_of = ui.class_of
                if addevent.cleaned_data['regular_lunch'] == 'Y' or addevent.cleaned_data['regular_lunch'] == 'y':
                    lunchtype = False
                elif addevent.cleaned_data['regular_lunch'] == 'N' or addevent.cleaned_data['regular_lunch'] == 'n':
                    lunchtype = True
                else:
                    messages.add_message(request, messages.ERROR,'Invalid Input')
                    return redirect("/student/checkout")
                e.regular_lunch = lunchtype
                if not Events.objects.all().count():
                    dataid = 0
                else:
                    dataid = Events.objects.aggregate(Max('id')).values()[0]
                e.event_date = addevent.cleaned_data['event_date']
                e.regular_lunch = 0
                e.id = dataid + 1
                e.save()
                print 'DONEEEE'
                str = 'Successfully Added Event: ' + addevent.cleaned_data['name']
                messages.add_message(request, messages.INFO,str)
                return redirect("/student/checkout")
    form = { 'pay': PaymentForm(prefix='pay'),  'add': AddForm(prefix='add'), 'display': DisplayForm(prefix='display'), 'addevent': AddEventForm(prefix='addevent')}       
    return render(request, 'student/control.html', {'form': form})

def display(request):
    deleteevent()
    if not TempDate.objects.all().count():
        messages.add_message(request, messages.ERROR,'Please Enter a Date!')
        return redirect("/student/checkout")
    ui = UserInfo.objects.get(id = request.user.id)
    displaydate = TempDate.objects.get(id=1)
    a = Payment.objects.filter(payment_date=displaydate.date, class_of = ui.class_of).count()
    latest_event_list = Payment.objects.filter(payment_date=displaydate.date, class_of = ui.class_of).order_by('-payment_date')[:a]
    c = Payment.objects.filter(payment_date=displaydate.date, class_of = ui.class_of).aggregate(Sum('total_cost')).values()[0]
    b = {'latest_event_list': latest_event_list}
    TempDate.objects.get(id=1).delete()
    output = { 'b': b, 'c': c, 'date': displaydate.date}
    return render(request, 'student/display.html', {'output': output})

def cancel(request):
    deleteevent()
    print 'cancel'
    if request.method == 'POST':
        print "post cancel"
        form = CancelForm(request.POST)
        if form.is_valid():
            print form.cleaned_data
        u = Cancel()
	q = Events.objects.filter(name=form.cleaned_data['event'])
        a = Events.objects.filter(name=form.cleaned_data['event']).count()
        print a
        if form.cleaned_data['event'] == 'Pizza Lunch' or form.cleaned_data['event'] == 'School Lunch':
            messages.add_message(request, messages.ERROR, 'You cannot edit this Event')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if a < 1:
            messages.add_message(request, messages.ERROR, 'Invalid Event')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        y = User.objects.get(id=request.user.id)
        z = UserInfo.objects.get(user_id=y.id)
        if form.cleaned_data['first_name'] != y.first_name:
            messages.add_message(request, messages.ERROR, 'Invalid First Name')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if form.cleaned_data['pin'] != z.pin:
            messages.add_message(request, messages.ERROR, 'Invalid Pin')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if form.cleaned_data['last_name'] != y.last_name:
            messages.add_message(request, messages.ERROR, 'Invalid Last Name')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        if not Payment.objects.filter(user_id=y.id, first_name=y.first_name, last_name=y.last_name, event=form.cleaned_data['event']).count():
            messages.add_message(request, messages.ERROR, 'You haven\'t paid for this yet')
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        temp = Payment.objects.get(user_id=y.id, first_name=y.first_name, last_name=y.last_name, event=form.cleaned_data['event'])

        print temp
	c = Distribution.objects.get(name=temp.class_of)
	d = Distribution.objects.get(name='Total')
        u.first_name = y.first_name
        u.last_name = y.last_name
        u.user_id = y.id
        u.event = form.cleaned_data['event']
        u.quantity = temp.quantity
        u.price_of_each = temp.price_of_each
        u.total_cost = temp.total_cost
        u.cancel_date = temp.payment_date
	d.money += u.total_cost
	c.money -= u.total_cost
	c.save()
	d.save()
        z.balance = z.balance + u.total_cost
        Payment.objects.get(user_id=y.id, first_name=y.first_name, last_name=y.last_name, event=form.cleaned_data['event']).delete()
        u.save()
        z.save()
        return redirect("/student/dashboard/")
    else:
        form = CancelForm() 
            
    return render(request, 'student/cancel.html', {'form': form})

def distribution(request):
    deleteevent()
    normal = Distribution.objects.get(name=UserInfo.objects.get(id=request.user.id).class_of)
    sumofiou = IOU.objects.filter(class_of=normal.name).aggregate(Sum('amount')).values()[0]
    print sumofiou
    if not IOU.objects.filter(student_id=request.user.id).count():
        sumofiou = 0
    st = 'You have $' + str(sumofiou) + ' worth of IOUs' 
    messages.add_message(request, messages.INFO, st)
    form = TakeOutForm(request.POST)
    print normal.money
    total = Distribution.objects.get(name='Total')
    if request.method == 'POST':
        print 'Test'
        if form.is_valid():
            print 'asdfasdfasdfasdfasdfasdfasdfsad'
            if not check_password(form.cleaned_data['password'], User.objects.get(id=request.user.id).password):
                messages.add_message(request, messages.ERROR, 'Password is Incorrect')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            a = Distribution.objects.get(name=normal.name)
            b = Distribution.objects.get(name='Total')
            print form.cleaned_data['amount']
            print b.money - sumofiou
            print '^^^^^'
            if form.cleaned_data['amount'] > (a.money - sumofiou):
                messages.add_message(request, messages.ERROR, 'Not enough money in the box')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if b.money < form.cleaned_data['amount']:
                messages.add_message(request, messages.ERROR, 'Not Enough Money In Box')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            b.money = b.money - form.cleaned_data['amount']
            a.money = a.money - form.cleaned_data['amount']
            a.save()
            b.save()
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    output = { 'normal': normal, 'total': total, 'form': form}
    return render(request, 'student/distribution.html', {'output': output})

def credits(request):
    deleteevent()
    return render(request, 'student/credits.html')

def change(request):
    deleteevent()
    if request.user.is_anonymous():
        messages.add_message(request, messages.ERROR, '    Please Login First before Changing a Password')
        return redirect("/student/login")
    if request.method == 'POST':
        form = ForgotForm(request.POST)
    	a = User.objects.get(id=request.user.id)
        if form.is_valid():
            print 'hello'
            if not check_password(form.cleaned_data['username'], User.objects.get(id=request.user.id).password):
                messages.add_message(request, messages.ERROR, 'Password is Incorrect')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if form.cleaned_data['first_name'] != form.cleaned_data['last_name']:
                messages.add_message(request, messages.ERROR, 'Passwords Do Not Match')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if form.cleaned_data['pin'] != UserInfo.objects.get(id=request.user.id):
                messages.add_message(request, messages.ERROR, 'Incorrect Pin')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            if not check_password(form.cleaned_data['old_passwd1'], a.password):
                messages.add_message(request, messages.ERROR, 'Incorrect Old Password')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            a.password = make_password(form.cleaned_data['first_name'], salt=None, hasher='default')
            a.save()
            site_logout()
            return redirect("/student/login")
    else:
        form = ForgotForm()
    return render(request, 'student/change.html', {'form': form})
