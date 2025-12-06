from django.shortcuts import render, redirect
from .forms import DataUserForm
from .models import DataUser
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login as auth_login
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

class SearchMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(fname__icontains=q) | Q(lname__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '').strip()
        return ctx

class EntryListView(SearchMixin, ListView):
    model = DataUser
    template_name = 'profiles/entry_list.html'
    #context_object_name = 'page_obj'
    paginate_by = 5

class EntryDetailView(DetailView):
    model = DataUser
    template_name = 'profiles/entry_detail.html'
    context_object_name = 'entry'

from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import CreateView
from .models import DataUser
from .forms import DataUserForm

class EntryCreateView(LoginRequiredMixin, CreateView):
    model = DataUser
    form_class = DataUserForm
    template_name = 'profiles/entry_form.html'

    def dispatch(self, request, *args, **kwargs):
        if hasattr(request.user, 'profile'):
            messages.info(request, 'У вас уже есть данные профиля.')
            return redirect('my_prof')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def get_success_url(self):
        messages.success(self.request, 'Запись добавлена')
        return reverse('profiles-detail', args=[self.object.pk])

class OwnerOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (obj.user == self.request.user) or self.request.user.is_staff
    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, 'Недостаточно прав')
        return super().handle_no_permission()

class EntryUpdateView(LoginRequiredMixin, UpdateView):
    model = DataUser
    form_class = DataUserForm
    template_name = 'profiles/entry_form.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        messages.success(self.request, 'Запись обновлена')
        return reverse('profiles-detail', args=[self.object.pk])

class EntryDeleteView(LoginRequiredMixin, OwnerOrStaffRequired, DeleteView):
    model = DataUser
    template_name = 'profiles/entry_confirm_delete.html'
    success_url = reverse_lazy('profiles')
    def delete(self, request, *args, **kwargs):
        from django.contrib import messages
        messages.success(self.request, 'Запись удалена')
        return super().delete(request, *args, **kwargs)

class MyProfileView(LoginRequiredMixin, DetailView):
    model = DataUser
    template_name = 'profiles/my_prof.html'
    context_object_name = 'entry'

    def get_object(self, queryset=None):
        # если профиль есть — возвращаем его
        try:
            return self.request.user.profile
        except DataUser.DoesNotExist:
            # если профиля нет — редиректим на создание
            return redirect('profiles-create')

#
#
#
#ef profiles_view(request):
#   form = DataUserForm(request.POST or None)
#   if request.method == 'POST' and form.is_valid():
#       form.save()
#       return redirect('profiles_list')
#   entries = DataUser.objects.all()
#   return render(request, 'profiles/profiles_list.html', {'form': form, 'entries': entries})
#
#
#
def signup(request):
  if request.method == 'POST':
      form = UserCreationForm(request.POST)
      if form.is_valid():
          user = form.save()
          auth_login(request, user)  # сразу войдём
         
          messages.success(request, 'Аккаунт создан и выполнен вход')
          return redirect('profiles')
  else:
      form = UserCreationForm()
  return render(request, 'registration/signup.html', {'form': form})

