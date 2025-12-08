from django.db import models

class BlogEntry(models.Model):
    content = models.TextField()
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, related_name='blog')


    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Запись блога'
        verbose_name_plural = 'Записи блога'

    def __str__(self):
        return self.content[:50]
    
class BlogActivity(models.Model):
    blog_entry = models.ForeignKey(BlogEntry, on_delete=models.CASCADE, related_name='activities')
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    like = models.BooleanField(default=False)
    hide = models.BooleanField(default=False)
    comment = models.CharField(max_length=50, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        verbose_name = 'Активность блога'
        verbose_name_plural = 'Активности блога'

    def __str__(self):
        return f"{self.user.username} {self.action} on {self.blog_entry.id}"