from django.contrib import admin
from .models import UserInfo, Payment,Cancel, Events, PastEvent, IOU, Distribution
# Register your models here.
class UserAdmin(admin.ModelAdmin):
    fields = ['user', 'id', 'first_name', 'last_name', 'email', 'grade', 'class_of', 'balance', 'pin']
    list_display = ['user', 'id', 'first_name','last_name', 'email', 'grade', 'class_of', 'balance', 'pin']

    def username(self,obj):
        return obj.user.username

    def first_name(self,obj):
        return obj.user.first_name

    def last_name(self,obj):
        return obj.user.last_name

    def user_email(self,obj):
        return obj.user.email

class EventsAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'class_of', 'event_date', 'cost', 'regular_lunch']
    list_display = ['name', 'description', 'class_of', 'event_date', 'cost', 'regular_lunch']

class PastEventAdmin(admin.ModelAdmin):
    fields = ['name', 'description', 'class_of', 'event_date', 'cost', 'regular_lunch']
    list_display = ['name', 'description', 'class_of', 'event_date', 'cost', 'regular_lunch']

class PaymentAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'user_id', 'payment_date', 'event', 'class_of', 'quantity', 'price_of_each', 'total_cost']
    list_display = ['first_name', 'last_name', 'user_id', 'payment_date', 'event', 'class_of', 'quantity', 'price_of_each', 'total_cost']

class CancelAdmin(admin.ModelAdmin):
    fields = ['first_name', 'last_name', 'user_id', 'cancal_date', 'event', 'class_of', 'quantity', 'price_of_each', 'total_cost']
    list_display = ['first_name', 'last_name', 'user_id', 'cancel_date', 'event', 'class_of', 'quantity', 'price_of_each', 'total_cost']

class IOUAdmin(admin.ModelAdmin):
	fields = ['first_name', 'last_name', 'student_id', 'class_of', 'amount', 'last_date']
	list_display = ['first_name', 'last_name', 'student_id', 'class_of', 'amount', 'last_date']  

class DistributionAdmin(admin.ModelAdmin):
	fields = ['name', 'money']
	list_display = ['name', 'money']
admin.site.register(UserInfo, UserAdmin)
admin.site.register(Events, EventsAdmin)
admin.site.register(PastEvent, PastEventAdmin)
admin.site.register(Payment, PaymentAdmin)
admin.site.register(Cancel, CancelAdmin)
admin.site.register(IOU, IOUAdmin)
admin.site.register(Distribution, DistributionAdmin)
