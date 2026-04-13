from .models import Notification

def notifications_data(request):
    if request.user.is_authenticated:
        return {
            'unread_notifications_count': Notification.objects.filter(recipient=request.user, is_read=False).count(),
            'last_notifications': Notification.objects.filter(recipient=request.user)[:5]
        }
    return {}