from django.db import models
from datetime import date
from django.conf import settings

class DataUser(models.Model):
    fname = models.CharField('Имя', max_length=50) 
    lname = models.CharField('Фамилия', max_length=50)
    phone = models.CharField('Телефон', max_length=20)
    birth_date = models.DateField('Дата рождения', null=True, blank=True)
    gender = models.CharField('Пол', max_length=10)
    about = models.TextField('О себе', max_length=300, blank=True, null=True)
    photo = models.ImageField('Фото', upload_to='photos/', null=True, blank=True)
    created_at = models.DateTimeField('Создано', auto_now_add=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             related_name='profile', null=True, blank=True, verbose_name='user')



    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователей'

    def __str__(self):
        return f"{self.fname} {self.lname}"
    
    def get_age(self):
        today = date.today()
        age = today.year - self.birth_date.year
        if today.month < self.birth_date.month or (today.month == self.birth_date.month and today.day < self.birth_date.day):
            age -= 1
        return age