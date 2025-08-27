# BILDIRISHNOMA VIEWS
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Xabarnoma
from .services import XabarnomaService

@login_required
def notifications_list(request):
    """Bildirishnomalar ro'yxati"""
    notifications = request.user.xabarlar.all()[:50]
    
    # Sahifa ma'lumotlari
    paginator = Paginator(notifications, 20)
    page = request.GET.get('page')
    
    try:
        notifications_page = paginator.page(page)
    except PageNotAnInteger:
        notifications_page = paginator.page(1)
    except EmptyPage:
        notifications_page = paginator.page(paginator.num_pages)
    
    return render(request, 'notifications/list.html', {
        'notifications': notifications_page,
        'unread_count': request.user.xabarlar.filter(is_read=False).count(),
    })

@login_required
def notification_detail(request, pk):
    """Bildirishnoma detallari va o'qilgan deb belgilash"""
    notification = get_object_or_404(Xabarnoma, pk=pk, recipient=request.user)
    
    # Bildirishnomani o'qilgan deb belgilash
    notification.mark_as_read()
    
    # Agar action_url mavjud bo'lsa, u yerga yo'naltirish
    if notification.action_url:
        return redirect(notification.action_url)
    
    # Aks holda, bildirishnomalar ro'yxatiga qaytish
    messages.success(request, f"'{notification.title}' bildirishnomasi o'qildi.")
    return redirect('notifications_list')

@login_required
def mark_all_notifications_read(request):
    """Barcha bildirishnomalarni o'qilgan deb belgilash"""
    if request.method == 'POST':
        count = XabarnomaService.mark_all_as_read(request.user)
        messages.success(request, f"{count} ta bildirishnoma o'qilgan deb belgilandi.")
    
    return redirect('notifications_list')

@login_required
def notification_count_ajax(request):
    """AJAX orqali bildirishnomalar sonini olish"""
    count = XabarnomaService.get_unread_count(request.user)
    recent = XabarnomaService.get_recent_notifications(request.user, 5)
    
    notifications_data = []
    for notification in recent:
        notifications_data.append({
            'id': notification.id,
            'title': notification.title,
            'message': notification.message[:100],
            'type': notification.notification_type,
            'created_at': notification.created_at.strftime('%d.%m.%Y %H:%M'),
            'is_read': notification.is_read,
        })
    
    return JsonResponse({
        'count': count,
        'notifications': notifications_data
    })
