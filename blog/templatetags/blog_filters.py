from django import template
from django.contrib.auth.models import AnonymousUser

register = template.Library()


@register.filter
def is_liked_by(entry, user):
    """Проверяет, лайкнута ли запись пользователем."""
    if isinstance(user, AnonymousUser) or not user.is_authenticated:
        return False
    return entry.is_liked_by(user)
