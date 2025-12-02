from django.db import models

class DataUser(models.Model):
    fname = models.CharField('Имя', max_length=50) 
    lname = models.CharField('Фамилия', max_length=50)
    email = models.EmailField('Email', max_length=100)
    phone = models.CharField('Телефон', max_length=20)
    birth_date = models.DateField('Дата рождения')
    gender = models.CharField('Пол', max_length=10)
    about = models.TextField('О себе', max_length=300)
    photo = models.ImageField('Фото', upload_to='photos/')
    created_at = models.DateTimeField('Создано', auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователей'

    def __str__(self):
        return f"{self.fname} {self.lname}"
