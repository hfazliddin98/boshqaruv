from .services import NotificationService

def xabarlar_context(request):
    """Barcha sahifalarda bildirishnomalar ko'rsatish uchun context"""
    if request.user.is_authenticated:
        try:
            unread_count = NotificationService.get_unread_count(request.user)
            recent_xabarlar = NotificationService.get_recent_notifications(request.user, 5)
            
            return {
                'unread_notifications_count': unread_count,
                'recent_notifications': recent_xabarlar,
                'unread_xabarlar_count': unread_count,
                'recent_xabarlar': recent_xabarlar,
            }
        except Exception as e:
            print(f"Context processor error: {e}")
            return {
                'unread_notifications_count': 0,
                'recent_notifications': [],
                'unread_xabarlar_count': 0,
                'recent_xabarlar': [],
            }
    return {
        'unread_notifications_count': 0,
        'recent_notifications': [],
        'unread_xabarlar_count': 0,
        'recent_xabarlar': [],
    }
