from xml.sax.xmlreader import Locator
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import get_object_or_404, redirect, render, get_list_or_404
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.core.mail import send_mail
from datetime import datetime
from events.models import Category, Sub_category
from django.utils import timezone
from django.conf import settings
from django.db.models import Count

from .models import *
from .forms import *

from utils import *

import logging
logger = logging.getLogger(__name__)

# Create your views here.

def index(req):


    context = {
        'events': Event.objects.all(),
        'sub_categories': Sub_category.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(req, 'events/index.html', context)

def register(req):
    logger.info('Loading register.html')
    if req.method == "POST":
        logger.info(f'Received POST request: {req.POST}')
        form = UserForm(req.POST)
        
        if form.is_valid():
            user = form.save()
            login(req, user)
            logger.info(f"Registration successful")
            logger.info('Redirecting to profile page')
            # send confirmation email to user
            subject = 'Welcome to our Edu event booking system'
            message = f'Dear {user},\n\nThank you for registering for our Edu-event booking system.\n\nBest regards,\nThe event team'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [req.user.email]
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponseRedirect(reverse('profile'))
        
        else:
            logger.error(f"Unsuccessful registration. Invalid information.")
            return render(req, 'events/register.html', {'message':'Invalid Credentials!'})

    else:
        form = UserForm()

    context = {
        'form':form
    }

    return render(req, 'events/register.html', context)

def login_view(req):
    logger.info('Loading login.html')
    if req.method == 'POST':
        logger.info(f'Received POST request: {req.POST}')
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(req, username=username, password= password)

        if user is not None:
            login(req, user)
            logger.info(f"Login successful")
            logger.info('Redirecting to profile page')
            return HttpResponseRedirect(reverse('profile'))
        else:

            logger.error(f"Unsuccessful registration. Invalid information.")
            return render(req, 'events/login.html', {'message':'Invalid Credentials!'})

    else:
        return render(req, 'events/login.html')

def logout_view(req):
    logger.info('Logout initiated')
    logout(req)
    logger.info('Logged out succesfully')
    logger.info('Redirecting to main page')
    return HttpResponseRedirect(reverse(index))

@staff_member_required
def edit(req):

    logger.info('Loading edit.html')
    if req.method == 'POST':
        logger.info(f'Received POST request: {req.POST}')
        form1 = EventForm(req.POST, req.FILES, prefix='form1')
        form2 = CategoryForm(req.POST, prefix='form2')
        form3 = SubCategoryForm(req.POST, prefix='form3')
        form4 = LocationForm(req.POST, prefix='form4')

        if form1.is_valid():
            logger.info('form1 saved')
            form1.save()
        if form2.is_valid():
            logger.info('form2 saved')
            form2.save()
        if form3.is_valid():
            logger.info('form3 saved')
            form3.save()
        if form4.is_valid():
            logger.info('form4 saved')
            form4.save()

        logger.info('Redirecting to main page')
        return HttpResponseRedirect(reverse('index'))

    else:
        form1 = EventForm(prefix='form1')
        form2 = CategoryForm(prefix='form2')
        form3 = SubCategoryForm(prefix='form3')
        form4 = LocationForm(prefix='form4') 

    context = {
    'form1' : form1,
    'form2' : form2,
    'form3' : form3,
    'form4' : form4, 
    'events': Event.objects.all(),
    'sub_categories': Sub_category.objects.all(),
    'locations': Location.objects.all(),
    }

    
    return render(req, 'events/edit.html', context)
@login_required
def create_event(req):
    if req.method == 'POST':
        form5 = EventForm(req.POST, req.FILES, prefix='form5')
        if form5.is_valid():
            event = form5.save()
            # send confirmation email to user
            subject = 'Your event has been created!'
            message = f'Dear {req.user.username},\n\nYour event "{event.title}" has been successfully created.\n\nBest regards,\nThe event team'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [req.user.email]
            send_mail(subject, message, from_email, recipient_list)
            return HttpResponseRedirect(reverse('index'))    
    else:
        form5 = EventForm(prefix='form5')
    context = {
        'form5': form5,
    }
    return render(req, 'events/create_event.html', context)

    
@login_required
def profile(req):
    logger.info('Loading profile.html')
    if req.method == 'POST':
        logger.info(f'Received POST request: {req.POST}')
        user_form = UserForm(req.POST, instance=req.user)
        profile_form = ProfileForm(req.POST, instance=req.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse(profile))
        logger.error('Error in updating the profile')
    else:
        user_form = UserForm(instance=req.user)
        profile_form = ProfileForm(instance=req.user.profile)

    currentUserProfile = Profile.objects.filter(pk = req.user.id)

    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'profile': Profile.objects.get(user=req.user),
        'events':currentUserProfile[0].events.all()
    }

    return render(req, 'events/profile.html', context)

@login_required
def book_view(req, pk):

    event = get_object_or_404(Event, id=req.POST.get('event_id'))
    subscribed = Subscription.objects.filter(user=req.user).exists()
    booked = False

    if event.is_paid:
        if not subscribed:
            return redirect('payment_form')

            

    
    if event.location.capacity > event.users.count():

        if event.users.filter(id=req.user.profile.id).exists():
            event.users.remove(req.user.profile)
            booked = False
        else:
            event.users.add(req.user.profile)
            booked = True
             # Send email to user
            subject = f"You've booked the {event.title} event"
            message = f"Hi {req.user.first_name},\n\nYou've successfully booked the {event.title} event on {event.date}. We look forward to seeing you there!\n\nBest,\nThe Event Team"
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient_list = [req.user.email]
            send_mail(subject, message, from_email, recipient_list)

            """one_day_before = event.date - timezone.timedelta(days=1)
            if timezone.now() < one_day_before:
                subject=f'Reminder: Your booking for {event.title} is tomorrow!'
                message = f"Hi {req.user.first_name},\n\n This is a reminder that you have a booking for the { event.name }. \nevent tomorrow, on { event.date }."
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [req.user.email]
                send_mail(subject, message, from_email, recipient_list)
            """
    else:
        HttpResponseRedirect(reverse(index))
    if event.is_paid:
        if subscribed:
            button_text = 'Book Event!'
        else:
            button_text = 'Subscribe!'
    else:
        button_text = 'Book Event!'

    context = {
        'event': event,
        'booked': booked,
        'button_text': button_text,
        
    }
    

    return HttpResponseRedirect(reverse('profile'))


@login_required
def like_view(req, pk):
    
    event = get_object_or_404(Event, id=req.POST.get('event_id'))
    liked = False

    if event.likes.filter(id=req.user.id).exists():
        event.likes.remove(req.user)
        liked = False
    else:
        event.likes.add(req.user)
        liked = True
    

    return HttpResponseRedirect(reverse('index'))

@staff_member_required
def edit_event(req, pk):

    event = Event.objects.get(id=pk)

    if req.method == 'POST':
        eventForm = EventForm(req.POST, instance=event)
        
        if eventForm.is_valid():
            eventForm.save()

        return redirect('index')
        
    else:
        eventForm = EventForm(instance=event)

    context = {
        'eventForm' : eventForm,
    }

    return render(req, 'events/edit.html', context)

@staff_member_required
def edit_sub_category(req, pk):

    sub_category = Sub_category.objects.get(id=pk)

    if req.method == 'POST':
        subCategoryForm = SubCategoryForm(req.POST, instance=sub_category)

        if subCategoryForm.is_valid():
            subCategoryForm.save()

        return redirect('index')
        
    else:
        subCategoryForm = SubCategoryForm(instance=sub_category)


    context = {
        'subCategoryForm' : subCategoryForm,
    }

    return render(req, 'events/edit.html', context)

@staff_member_required
def edit_location(req, pk):

    location = Location.objects.get(id=pk)

    if req.method == 'POST':
        locationForm = LocationForm(req.POST, instance=location)

        if locationForm.is_valid():
            locationForm.save()


        return redirect('index')
        
    else:
        locationForm = LocationForm(instance=location)


    context = {
        'locationForm' : locationForm,
    }

    return render(req, 'events/edit.html', context)

@staff_member_required
def delete_event(req, pk):

    event = Event.objects.get(id=pk)
    event.delete()

    return redirect('edit')

@staff_member_required
def delete_sub_category(req, pk):

    sub_category = Sub_category.objects.get(id=pk)
    sub_category.delete()

    return redirect('edit')

@staff_member_required
def delete_location(req, pk):

    location = Location.objects.get(id=pk)
    location.delete()

    return redirect('edit')

#payment

@login_required
def payment_form(request):
    form6 = PaymentForm(request.POST or None)
    if request.method == 'POST' and form6.is_valid():
        # Process payment (replace with your own payment processing code)
        payment_status = 'success'

        if payment_status == 'success':
            # Update user's subscription status
            user = request.user
            subscription = Subscription.objects.filter(user=user).first()
            if subscription:
                subscription.subscribed = True
                subscription.save()
            else:
                subscription = Subscription(user=user, subscribed=True)
                subscription.save()

            # Display success message
            return render(request, 'events/payment_success.html')
        else:
            # Payment failed
            error_message = 'Payment failed. Please try again.'
    else:
        # Display payment form
        error_message = ''
    return render(request, 'events/payment_form.html', {'form6': form6, 'error_message': error_message})

#dashboard
@staff_member_required
def dashboard(request):
    total_users = User.objects.count()
    total_subscriptions = Subscription.objects.count()
    total_events = Event.objects.count()
    upcoming_events = Event.objects.filter(date__gte=datetime.today()).count()
    total_profiles = Profile.objects.count()
    total_reviews = Review.objects.count()
    total_location= Location.objects.count()
    total_category=Category.objects.count()
    total_subcategory=Sub_category.objects.count()
    #total_bookings = Booking.objects.count()
    context = {
        'total_users': total_users,
        'total_subscriptions': total_subscriptions,
        'total_events': total_events,
        'upcoming_events': upcoming_events,
        'total_profiles': total_profiles,
        'total_reviews': total_reviews,
        'total_location':total_location,
        'total_category':total_category,
        'total_subcategory':total_subcategory
        #'total_bookings': total_bookings
    }

    return render(request, 'events/dashboard.html', context)


