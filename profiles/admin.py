from django.contrib import admin
from .models import DataUser


@admin.register(DataUser)
class DataUserAdmin(admin.ModelAdmin):
    list_display = ('id','fname', 'lname', 'phone', 'birth_date', 'gender', 'created_at', 'photo')
    search_fields = ('fname', 'lname')
    ordering = ['-created_at']

    

