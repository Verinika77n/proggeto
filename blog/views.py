from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import BlogEntry
from django.views.generic import ListView
from django.db.models import Q
from .forms import BlogEntryForm
from django.contrib.auth.mixins import UserPassesTestMixin




class SearchMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(content__icontains=q))
        return qs
    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['q'] = self.request.GET.get('q', '').strip()
        return ctx


class blog(SearchMixin, ListView):
    model = BlogEntry
    template_name = 'blog/news_band.html'
    #context_object_name = 'page_obj'
    paginate_by = 10

class OwnerOrStaffRequired(UserPassesTestMixin):
    def test_func(self):
        obj = self.get_object()
        return (obj.user == self.request.user) or self.request.user.is_staff
    def handle_no_permission(self):
        from django.contrib import messages
        messages.error(self.request, 'Недостаточно прав')
        return super().handle_no_permission()

class BlogCreateView(LoginRequiredMixin, CreateView):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/new_entry.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.user = self.request.user
        obj.save()
        return super().form_valid(form)
    def get_success_url(self):
        messages.success(self.request, 'Запись блога успешно создана.')
        return reverse('blog')
    
class BlogDetailView(DetailView):
    model = BlogEntry
    template_name = 'blog/detail_entry.html'
    context_object_name = 'entry'

class BlogUpdateView(LoginRequiredMixin,OwnerOrStaffRequired, UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/new_entry.html'

    def get_object(self, queryset=None):
        return self.request.user.blogentry_set.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, 'Данные обновлены')
        return reverse('blog-detail', args=[self.object.pk])    
    

class BlogDeleteView(LoginRequiredMixin, OwnerOrStaffRequired, DeleteView):
    model = BlogEntry
    template_name = 'blog/delete_entry.html'
    success_url = reverse_lazy('blog')
    def get_object(self, queryset=None):
        return self.request.user.blogentry_set.get(pk=self.kwargs['pk'])
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Запись удалена')
        return super().delete(request, *args, **kwargs)
