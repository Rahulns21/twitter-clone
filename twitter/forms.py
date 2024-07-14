from django import forms
from .models import Tweet
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile

class TweetForm(forms.ModelForm):

    class Meta:
        model = Tweet
        exclude = ("user", "likes",)

    body = forms.CharField( required=True, 
                            max_length=200, 
                            widget=forms.widgets.Textarea(
                               attrs={
                                   "placeholder": "Write your Tweet...",
                                   "class": "form-control",
                               }
                           ), 
                           label="",
                        )
    
class ProfilePicForm(forms.ModelForm):
     
    class Meta:
        model = Profile
        fields = ('account_type', 'profile_image', 'profile_bio', 'website_link', 'instagram_link')

    profile_bio = forms.CharField(label='Profile Bio', widget=forms.Textarea(attrs={'class':'form-control', 'placeholder':'Write your Bio...'}))
    website_link = forms.URLField(label='Website Link', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Homepage Link'}))
    instagram_link = forms.URLField(label='Instagram Link', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Instagram Link'}))

class SignUpForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
            super(SignUpForm, self).__init__(*args, **kwargs)

            self.fields['username'].widget.attrs['class'] = 'form-control'
            self.fields['username'].widget.attrs['placeholder'] = 'User Name'
            self.fields['username'].label = ''
            self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

            self.fields['password1'].widget.attrs['class'] = 'form-control'
            self.fields['password1'].widget.attrs['placeholder'] = 'Password'
            self.fields['password1'].label = ''
            self.fields['password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to your other personal information.</li><li>Your password must contain at least 8 characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your password can\'t be entirely numeric.</li></ul>'

            self.fields['password2'].widget.attrs['class'] = 'form-control'
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
            self.fields['password2'].label = ''
            self.fields['password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, for verification.</small></span>'

    email = forms.EmailField(label='', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Email Address'}))
    first_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'First Name'}))
    last_name = forms.CharField(label='', max_length=50, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Last Name'}))

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

    def __init__(self, *args, **kwargs):
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        # Customize widgets, labels, placeholders, etc., if needed
        self.fields['username'].widget.attrs['class'] = 'form-control'
        self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['username'].label = 'Username'
        self.fields['username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</small></span>'

        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your email'
        self.fields['email'].label = 'Email'
        self.fields['email'].widget.attrs['readonly'] = True # email field cannot be edited 

        self.fields['first_name'].widget.attrs['class'] = 'form-control'
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter your first name'
        self.fields['first_name'].label = 'First Name'

        self.fields['last_name'].widget.attrs['class'] = 'form-control'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter your last name'
        self.fields['last_name'].label = 'Last Name'
