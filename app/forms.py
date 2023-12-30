from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from app.models import Comment, Subscribe


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'name', 'email', 'website')


class SubscribeForm(forms.ModelForm):
    class Meta:
        model = Subscribe
        fields = ('email',)
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder': "Enter your Email"}),
        }

    # =================================================================================
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['email'].widget.attrs['placeholder'] = 'Email Please!'
    # =================================================================================
    # This __init__ method will override any other widget attributes.
    # Even if it's declared after this __init__ method.
    # =================================================================================


class RegisterUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2',]
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = 'Enter your Username'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter your Email'
        self.fields['password1'].widget.attrs['placeholder'] = 'Enter your Password'
        self.fields['password2'].widget.attrs['placeholder'] = 'Repeat your Password'
    
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username):
            raise forms.ValidationError("Username already exists.")
        return username
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email):
            raise forms.ValidationError("Email already in use.")
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']
        
        if (password1 and password2 and password1 != password2):
            # i.e. if both password1 and password2 exists, but they don't match:
            raise forms.ValidationError("The Passwords DO NOT MATCH.")
        return password2
    