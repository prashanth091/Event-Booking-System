from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return f"{self.name}"


class Sub_category(models.Model):
    name = models.CharField(max_length=32)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name}"


class Location(models.Model):
    city = models.CharField(max_length=64)
    country = models.CharField(max_length=32)
    street = models.CharField(max_length=64)
    street_num = models.IntegerField()
    capacity = models.IntegerField()

    def __str__(self):
        return f'{self.street} {self.street_num}, {self.city}. {self.country}'


class Event(models.Model):
    title = models.CharField(max_length=64)
    date = models.DateField()
    duration = models.IntegerField() #In minutes
    likes = models.ManyToManyField(User, blank= True, related_name='liked_events')
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    sub_category = models.ForeignKey(Sub_category, on_delete=models.CASCADE)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    is_paid = models.BooleanField(default=False)


    def __str__(self):
        return f'{self.title}, {self.sub_category}.'

    def get_duration(self):
        
        if self.duration>1440:
            days = self.duration // 1440
            hours = self.duration % 1440 // 60 
            minutes = self.duration % 60
            return f"{days}d, {hours}h, {minutes}min"

        if self.duration>60:
            hours = self.duration // 60
            minutes = self.duration % 60
            return f"{hours}h, {minutes}min"

        return f'{self.duration}min'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    dob = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    events = models.ManyToManyField(Event, blank=True, related_name='users')

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()

class Review(models.Model):
    comment = models.CharField(max_length=256)
    rating = models.FloatField()
    event_id = models.ForeignKey(Event, on_delete=models.CASCADE)
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.comment}, {self.rating}/5 stars.'
    
#booking
class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} booked {self.event.title} on {self.booking_date}"
    

#subscription
class Subscription(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subscribed = models.BooleanField(default=False)

