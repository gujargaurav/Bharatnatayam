from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile

class UserProfileForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    profile_picture = forms.ImageField(required=False)
    address_line1 = forms.CharField(max_length=255)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100)
    pincode = forms.CharField(max_length=10)
    user_type = forms.ChoiceField(choices=UserProfile.USER_TYPE_CHOICES)

    class Meta:
        model = UserProfile
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2',
                  'profile_picture', 'address_line1', 'city', 'state', 'pincode', 'user_type']
