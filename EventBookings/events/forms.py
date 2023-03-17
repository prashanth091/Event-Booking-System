from django import forms
from django.contrib.auth.models import User
from .models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm



class CategoryForm(forms.ModelForm):
    
    class Meta():
        model = Category
        fields =['name',]

class SubCategoryForm(forms.ModelForm):
    
    class Meta():
        model = Sub_category
        fields =['name', 'category',]

class LocationForm(forms.ModelForm):

    class Meta():
        model = Location
        fields = ['city', 'country', 'street', 'street_num', 'capacity',]

class UserForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='Required. Enter a valid email address.')
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username','email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)

        for fieldname in ['username', 'password1', 'password2']:
            self.fields[fieldname].help_text = None

class ProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('dob', 'events')

        widgets = {
                'dob': forms.DateInput(attrs={'type': 'date'}),
            }

    events = forms.ModelMultipleChoiceField(
        queryset=Event.objects.all(),
        widget=forms.CheckboxSelectMultiple
    )

class EventForm(forms.ModelForm):
    is_paid = forms.BooleanField(required=False)
    
    class Meta():
        model = Event
        fields =['title', 'date', 'duration', 'likes', 'image','category', 'sub_category','location','is_paid' ]
        
        widgets = {
                'date': forms.DateInput(attrs={'type': 'date'}),
            }
         
#payment
class PaymentForm(forms.Form):
    card_number = forms.CharField(max_length=16)
    expiration_date = forms.CharField(max_length=5)
    security_code = forms.CharField(max_length=3)
    name = forms.CharField(max_length=100)
