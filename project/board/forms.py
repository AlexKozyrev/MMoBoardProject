from ckeditor.widgets import CKEditorWidget
from django import forms
from .models import Ad
from ckeditor.fields import RichTextField


class AdForm(forms.ModelForm): # форма редактирования. создания ckeditor
    content = forms.CharField(widget=CKEditorWidget())

    class Meta:
        model = Ad
        fields = ['category', 'title', 'content']