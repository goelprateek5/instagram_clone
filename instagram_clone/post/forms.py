from django import forms
from post.models import Post

from django.forms import ClearableFileInput

class NewPostForm(forms.ModelForm):
    content = forms.FileField(widget=ClearableFileInput(attrs={'multiple':True}), required=True)
    caption = forms.CharField(widget=forms.Textarea(attrs={'class':'input is-medium', 'placeholder':'Add a Caption'}), required=True)
    tags = forms.CharField(widget=forms.TextInput(attrs={'class':'input is-medium', 'placeholder':'Add tags separated by Commas'}), required=True)

    class Meta:
        model = Post
        fields = ('content', 'caption','tags') 