from django.contrib import admin
from django.contrib.auth.models import Group, User
from .models import Profile, Tweet
from django import forms

# Unregister Groups
admin.site.unregister(Group)

# Mix profile info into User info
class ProfileInfo(admin.StackedInline):
    model = Profile

class UserAdminForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        widgets = {
            'password': forms.TextInput(attrs={'readonly': 'readonly'})
        }

class UserAdmin(admin.ModelAdmin):
    model = User
    # Use the custom form
    form = UserAdminForm
    # just display username fields on admin page
    fields = ['username', 'first_name', 'last_name', 'email', 'is_active', 'is_staff', 'is_superuser']
    inlines = [ProfileInfo]

# Unregister initial user
admin.site.unregister(User)

# Reregister User and Profile
admin.site.register(User, UserAdmin)
# admin.site.register(Profile)

# Register user tweets
admin.site.register(Tweet)