from django.db import models

class BlogEntry(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='blog')

    def is_liked_by(self, user):
        return self.activities.filter(user=user, action='like').exists()

    def likes_count(self):
        return self.activities.filter(action='like').count()
    
    def comments(self):
        return self.activities.filter(action='comment')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def __str__(self):
        return self.content[:50]
    
class BlogActivity(models.Model):
    ACTION_CHOICES = [
        ('like', 'Лайк'),
        ('hide', 'Скрытие'),
        ('comment', 'Комментарий'),
    ]

    blog_entry = models.ForeignKey(BlogEntry, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='user_activities')
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, null=True, blank=True)
    comment = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Активность блога'
        verbose_name_plural = 'Активности блога'
        

    def __str__(self):
        return f"{self.user.username} {self.action} on {self.blog_entry.id}"
    
  