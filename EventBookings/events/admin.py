from django.contrib import admin
from django.urls import path
from . import views
from django.urls import reverse
from django.utils.html import format_html
from .models import *

# Register your models here.

class EventAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'date', 'duration', 'image', 'created_at', 'updated_at', 'location', 'sub_category',)
    filter_horizontal = ('likes',)
    def booked_count(self, obj):
        return obj.bookings.count()
    booked_count.short_description = 'Booked'
class BookingAdmin(admin.ModelAdmin):
    list_display=('user', 'event',  'booking_date')
   # filter_horizontal=('events')  
class LocationAdmin(admin.ModelAdmin):
    list_display = ('id', 'city', 'country', 'street', 'street_num', 'capacity')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('id', 'comment', 'rating', 'event_id', 'user_id')

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'dob', 'created_at', 'updated_at')
    filter_horizontal = ('events',)

class SubscriptionAdmin(admin.ModelAdmin):

    list_display = ('user', 'get_subscribed')
    
    def get_subscribed(self, obj):
        return obj.subscribed
    get_subscribed.boolean = True
    get_subscribed.short_description = 'Subscribed'

class CustomAdminSite(admin.AdminSite):
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(views.dashboard), name='dashboard'),
        ]
        return custom_urls + urls

    def index(self, request, extra_context=None):
        dashboard_url = reverse('admin:dashboard')
        dashboard_link = format_html('<a href="{}">Dashboard</a>', dashboard_url)
        extra_context = extra_context or {}
        extra_context['dashboard_link'] = dashboard_link
        return super().index(request, extra_context)    

admin.site.register(Category)
admin.site.register(Sub_category)
admin.site.register(Event, EventAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Subscription, SubscriptionAdmin)
admin.site.register(Booking,BookingAdmin)
