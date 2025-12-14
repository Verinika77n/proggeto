from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import DeleteView
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from .models import BlogEntry, BlogActivity
from django.views.generic import ListView
from django.db.models import Q
from .forms import BlogEntryForm
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404


class SearchMixin:
    def get_queryset(self):
        qs = super().get_queryset()
        q = self.request.GET.get('q', '').strip()
        if q:
            qs = qs.filter(Q(user__profile__fname__icontains=q)|Q(content__icontains=q) | Q(user__profile__lname__icontains=q))
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

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему.')
            return redirect('blog')

        e_id = request.POST.get('e_id')
        try:
            entry = BlogEntry.objects.get(id=e_id)
            activity, created = BlogActivity.objects.get_or_create(
                blog_entry=entry,
                user=request.user,
                action='like'
            )
            if not created and activity.action == 'like':
                activity.delete()
                messages.success(request, 'Лайк удалён.')
            else:
                messages.success(request, 'Лайк добавлен.')

        except BlogEntry.DoesNotExist:
            messages.error(request, 'Запись не найдена.')

        return redirect(request.META.get('HTTP_REFERER', 'blog'))

    
    

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

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Необходимо войти в систему.')
            return redirect('blog-detail', pk=self.kwargs['pk'])

        entry = get_object_or_404(BlogEntry, pk=self.kwargs['pk'])
        form_type = request.POST.get("form_type")

        if form_type == "form1":  # лайк
            activity = BlogActivity.objects.filter(
                blog_entry=entry, user=request.user, action='like'
            ).first()

            if activity:
                activity.delete()
                messages.success(request, 'Лайк удалён.')
            else:
                BlogActivity.objects.create(
                    blog_entry=entry, user=request.user, action='like'
                )
                messages.success(request, 'Лайк добавлен.')

        elif form_type == "form2":  
            comment_text = request.POST.get('comment_text', '').strip()
            if comment_text:
                BlogActivity.objects.create(
                    blog_entry=entry,
                    user=request.user,
                    action='comment',
                    comment=comment_text
                )
                messages.success(request, 'Комментарий добавлен.')
            else:
                messages.error(request, 'Комментарий не может быть пустым.')
        elif form_type == "delete_comment": 
            comment_id = request.POST.get('comment_id')
            comment = BlogActivity.objects.filter(
                pk=comment_id,
                blog_entry=entry,
                user=request.user,
                action='comment'
            ).first()
            if comment:
                comment.delete()
                messages.success(request, 'Комментарий удалён.')
            else:
                messages.error(request, 'Комментарий не найден или у вас нет прав на его удаление.')

        return redirect(reverse('blog-detail', kwargs={'pk': entry.pk}))

class BlogUpdateView(LoginRequiredMixin,OwnerOrStaffRequired, UpdateView):
    model = BlogEntry
    form_class = BlogEntryForm
    template_name = 'blog/new_entry.html'

    def get_object(self):
        return self.request.user.blog.get(pk=self.kwargs['pk'])

    def get_success_url(self):
        messages.success(self.request, 'Данные обновлены')
        return reverse('blog-detail', args=[self.object.pk])    
    

class BlogDeleteView(LoginRequiredMixin, OwnerOrStaffRequired, DeleteView):
    model = BlogEntry
    template_name = 'blog/delete_entry.html'
    success_url = reverse_lazy('blog')
    def get_object(self, queryset=None):
        return self.request.user.blog.get(pk=self.kwargs['pk'])
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Запись удалена')
        return super().delete(request, *args, **kwargs)

