from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Message
from django.forms import ModelForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )


class CustomProfileCreationForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['name', 'short_intro', 'full_intro', 'email', 'profile_image']

    def __init__(self, *args, **kwargs):
        super(CustomProfileCreationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )


class CustomMessageForm(ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'body']

    def __init__(self, *args, **kwargs):
        super(CustomMessageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update(
                {'class': 'input'}
            )
