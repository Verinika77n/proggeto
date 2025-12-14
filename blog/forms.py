from django import forms
from .models import BlogEntry, BlogActivity
from django.core.files.images import get_image_dimensions


class BlogEntryForm(forms.ModelForm):
    class Meta:
        model = BlogEntry
        fields = ['content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 6,
                'placeholder': 'Введите текст записи...'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'content': 'Текст записи',
            'image': 'Изображение',
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if content and len(content) < 5:
            raise forms.ValidationError('Текст записи должен содержать не менее 5 символов.')
        return content
    

class BlogActivityForm(forms.ModelForm):
    class Meta:
        model = BlogActivity
        fields = ['action', 'comment']
        widgets = {
            'action': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'comment': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите комментарий...'
            }),
        }
        labels = {
            'action': 'действие',

            'comment': 'Комментарий',
        }