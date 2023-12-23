from django import forms

from app.models import Comment, Subscribe


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content', 'name', 'email', 'website')
        widgets = {
            'content': forms.Textarea(attrs={'placeholder': 'Type your comment here...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Name'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'website': forms.TextInput(attrs={'placeholder': 'Website'}),
        }


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
