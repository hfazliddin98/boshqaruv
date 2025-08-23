from .services import NotificationService

def notifications_context(request):
    """Barcha sahifalarda bildirishnomalar ko'rsatish uchun context"""
    if request.user.is_authenticated:
        try:
            unread_count = NotificationService.get_unread_count(request.user)
            recent_notifications = NotificationService.get_recent_notifications(request.user, 5)
            
            return {
                'unread_notifications_count': unread_count,
                'recent_notifications': recent_notifications,
            }
        except:
            return {
                'unread_notifications_count': 0,
                'recent_notifications': [],
            }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
    }
