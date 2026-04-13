from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import BlogActivity, Notification

@receiver(post_save, sender=BlogActivity)
def create_activity_notification(sender, instance, created, **kwargs):
    if created and instance.blog_entry.user != instance.user:
        verb_text = ""
        if instance.action == 'like':
            verb_text = "поставил/а лайк на вашу запись"
        elif instance.action == 'comment':
            verb_text = f"прокомментировал/а вашу запись: '{instance.comment[:20]}...'"
        if not verb_text:
            return

        Notification.objects.create(
            recipient=instance.blog_entry.user,
            actor=instance.user,
            verb=verb_text,
            post=instance.blog_entry  
        )

@receiver(post_delete, sender=BlogActivity)
def delete_notification_on_activity_remove(sender, instance, **kwargs):

    if instance.action == 'like':
       Notification.objects.filter(
            recipient=instance.blog_entry.user,
            actor=instance.user,
            post=instance.blog_entry, 
            verb="поставил/a лайк на вашу запись"
        ).delete()