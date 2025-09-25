from django.contrib.auth.forms import UserCreationForm
from django import forms    
from django.contrib.auth.models import User
from django.forms import ModelForm
from .models import Record
from .models import Profile

class SignupForm(UserCreationForm):
    email = forms.EmailField(label="" , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label="" , max_length=50, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField( label="" , max_length=30,widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'})) 

# meta is used to specify the model and fields to be used in the form
    class Meta:
        model = User
        fields = ("username", "first_name" , "last_name" , "email", "password1", "password2")
# init method is used to customize the form
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = ''
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['password1'].widget.attrs['class'] = 'form-control'
        self.fields['password1'].widget.attrs['placeholder'] = 'Password'   
        self.fields['password1'].label = ''
        self.fields['password1'].help_text = '<ul class="form-text text-muted"><small><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></small></ul>'

        self.fields['password2'].widget.attrs['class'] = 'form-control'
        self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
        self.fields['password2'].label = ''
        self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'    



# we can create more forms here for other models if needed
# we can also create custom forms by inheriting from forms.Form or forms.ModelForm
# we can also customize the form fields by overriding the __init__ method
#
# 

#create a form for adding a record
class add_record_form(forms.ModelForm):

    first_name = forms.CharField(label="First Name", max_length=50 , required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label="Last Name", max_length=50 , required=True , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}))
    email = forms.EmailField(label="Email" , required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email Address'}))
    phone = forms.CharField(label="Phone", max_length=15 , required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone Number'}))
    address = forms.CharField(label="Address", max_length=100 , required=True  , widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address'}))
    city = forms.CharField(label="City", max_length=50 , required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City'}))
    state = forms.CharField(label="State", max_length=50 , required=True,  widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'State'}))
    zipcode = forms.CharField(label="Zipcode", max_length=10, required=True, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Zipcode'}))  
    latitude = forms.FloatField(label="Latitude", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Latitude'}))
    longitude = forms.FloatField(label="Longitude", required=False, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Longitude'}))
    
    class Meta:
        model = Record
        fields = ('first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode')      


# forms.py



class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
        required=True
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
        required=True
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )
    admin_category = forms.ChoiceField(
        choices=getattr(Profile, 'ADMIN_CATEGORY_CHOICES', []),
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label="Admin Category"
    )
    class Meta:
        model = Profile
        fields = ["first_name", "last_name", "email", "admin_category", "phone"]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Full Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone Number'}),
        }

    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        # Sync only supported fields from Profile to User
        user.first_name = self.cleaned_data.get('first_name', user.first_name)
        user.last_name = self.cleaned_data.get('last_name', user.last_name)
        user.email = self.cleaned_data.get('email', user.email)
        if commit:
            user.save()
            profile.save()
        return profile
