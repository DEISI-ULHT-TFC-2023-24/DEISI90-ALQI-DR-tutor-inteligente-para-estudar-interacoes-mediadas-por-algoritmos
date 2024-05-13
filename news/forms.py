# forms.py
from django import forms


class CommentForm(forms.Form):
    comment_user = forms.CharField(max_length=120, label='', widget=forms.TextInput(attrs={'placeholder': 'Username...'}))
    comment_text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Comment...', 'width': '268px'}), label='')
