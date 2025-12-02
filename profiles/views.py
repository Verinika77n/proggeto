
from django.shortcuts import render, redirect
from .forms import DataUserForm
from .models import DataUser

def profiles_view(request):
    form = DataUserForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profiles_list')
    entries = DataUser.objects.all()
    return render(request, 'profiles/profiles_list.html', {'form': form, 'entries': entries})

