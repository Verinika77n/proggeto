from django.contrib import admin
from .models import DataUser


@admin.register(DataUser)
class DataUserAdmin(admin.ModelAdmin):
    list_display = ('fname', 'lname', 'email', 'phone', 'birth_date', 'gender', 'created_at')
    search_fields = ('fname', 'lname', 'email')
    ordering = ['-created_at']

    

