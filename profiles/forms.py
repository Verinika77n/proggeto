from django import forms
from .models import DataUser
from django.core.files.images import get_image_dimensions



class DataUserForm(forms.ModelForm):
    class Meta:
        model = DataUser
        fields = ['fname','lname','phone', 'birth_date', 'gender','about', 'photo',]
        widgets = {
            'fname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите имя'
            }),
            'lname': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Введите фамилию'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+7 (XXX) XXX-XX-XX'
            }),
           'birth_date': forms.DateInput(
            format='%Y-%m-%d',
            attrs={'class': 'form-control', 'type': 'date'}
            ),
            'gender': forms.RadioSelect(
                choices=[('Male', 'Мужской'), ('Female', 'Женский')],
                attrs={
                    'class': 'form-select'
                }
            ),
            'about': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Расскажите о себе...'
            }),
            'photo': forms.FileInput(attrs={
                'class': 'form-control'
            }),
        }
        labels = {
            'fname': 'Имя',
            'lname': 'Фамилия',
            'phone': 'Телефон',
            'birth_date': 'Дата рождения',
            'gender': 'Пол',
            'about': 'О себе',
            'photo': 'Фото профиля',
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone:
            # Удаляем пробелы, скобки, дефисы и прочие нецифровые символы (кроме + в начале)
            cleaned_phone = ''.join(c for c in phone if c.isdigit() or c == '+')
            if not cleaned_phone.startswith('+'):
                cleaned_phone = '+' + cleaned_phone
            # Проверяем минимальную длину
            if len(cleaned_phone) < 11:
                raise forms.ValidationError('Номер телефона слишком короткий.')
        return cleaned_phone

    def clean_birth_date(self):
        birth_date = self.cleaned_data.get('birth_date')
        if birth_date:
            from datetime import date
            if birth_date > date.today():
                raise forms.ValidationError('Дата рождения не может быть в будущем.')
        return birth_date

    def clean_photo(self):
        photo = self.cleaned_data.get('photo')
        if photo:
            try:
                w, h = get_image_dimensions(photo)
                if w < 100 or h < 100:
                    raise forms.ValidationError('Изображение слишком маленькое. Минимум 100×100 px.')
                if photo.size > 5 * 1024 * 1024:  # 5 МБ
                    raise forms.ValidationError('Файл изображения слишком большой (максимум 5 МБ).')
            except Exception:
                raise forms.ValidationError('Не удалось обработать изображение.')
        return photo
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля обязательными/необязательными при необходимости
        self.fields['about'].required = False
        self.fields['photo'].required = False

