from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch import receiver
from django.utils import timezone
from topshiriq.models import TopshiriqJavob, TopshiriqReport, Topshiriq

@receiver(post_save, sender=TopshiriqJavob)
def create_or_update_topshiriq_report(sender, instance, created, **kwargs):
    """
    TopshiriqJavob yaratilganda yoki yangilanganda TopshiriqReport'ni yaratish yoki yangilash
    """
    try:
        # Report'ni yaratish yoki olish
        report, report_created = TopshiriqReport.objects.get_or_create(
            topshiriq=instance.topshiriq,
            defaults={
                'javob': instance,
                'yaratuvchi': instance.topshiriq.yaratuvchi_user,
                'bajaruvchi': instance.bajaruvchi_user,
                'title': f"Hisobot: {instance.topshiriq.title}",
                'summary': f"Topshiriq '{instance.topshiriq.title}' bajarildi va javob yuborildi.",
                'status': 'completed',
                'completed_at': timezone.now(),
                'deadline': instance.topshiriq.tugash_vaqti,
            }
        )
        
        # Agar report mavjud bo'lsa, uni yangilash
        if not report_created:
            report.javob = instance
            report.completed_at = timezone.now()
            if report.status in ['rejected', 'revision']:
                report.status = 'completed'
                report.rejected_at = None
                report.comment = ''
        
        # Priority moslashtirish
        if instance.topshiriq.xolat == 'SHOSHILINCH':
            report.priority = 'urgent'
        elif instance.topshiriq.xolat == 'MUHIM':
            report.priority = 'high'
        elif instance.topshiriq.xolat == 'O`RTA':
            report.priority = 'medium'
        else:
            report.priority = 'low'
        
        # Full report'ni generatsiya qilish
        report.generate_full_report()
        report.save()
        
        # Topshiriq holatini yangilash
        instance.topshiriq.javob_yuborildi = True
        instance.topshiriq.status = 'YUBORILDI'
        instance.topshiriq.bajarilgan_vaqti = timezone.now()
        instance.topshiriq.save()
        
        print(f"TopshiriqReport {'yaratildi' if report_created else 'yangilandi'}: {report.id}")
        
    except Exception as e:
        print(f"TopshiriqReport yaratishda/yangilashda xatolik: {str(e)}")


@receiver(pre_delete, sender=TopshiriqJavob)
def handle_topshiriq_javob_delete(sender, instance, **kwargs):
    """
    TopshiriqJavob o'chirilishidan oldin tegishli ma'lumotlarni saqlash
    """
    instance._topshiriq_pk = instance.topshiriq.pk


@receiver(post_delete, sender=TopshiriqJavob)
def delete_topshiriq_report(sender, instance, **kwargs):
    """
    TopshiriqJavob o'chirilganda tegishli TopshiriqReport'ni ham o'chirish
    """
    try:
        # Tegishli topshiriqni olish
        topshiriq = Topshiriq.objects.get(pk=instance._topshiriq_pk)
        
        # Tegishli report'ni topish va o'chirish
        reports = TopshiriqReport.objects.filter(topshiriq=topshiriq)
        
        for report in reports:
            report.delete()
            print(f"TopshiriqReport o'chirildi: {report.id}")
        
        # Topshiriq holatini qaytarish
        topshiriq.javob_yuborildi = False
        topshiriq.status = 'YANGI'
        topshiriq.bajarilgan_vaqti = None
        topshiriq.save()
        
        print(f"Topshiriq holati qaytarildi: {topshiriq.pk}")
        
    except Exception as e:
        print(f"TopshiriqReport o'chirishda xatolik: {str(e)}")


@receiver(post_save, sender=Topshiriq)
def update_report_on_topshiriq_change(sender, instance, created, **kwargs):
    """
    Topshiriq yangilanganda tegishli report'ni ham yangilash
    """
    if not created:  # Faqat yangilanishda
        try:
            # Tegishli report'ni topish
            report = TopshiriqReport.objects.filter(topshiriq=instance).first()
            
            if report:
                # Report ma'lumotlarini yangilash
                report.title = f"Hisobot: {instance.title}"
                report.deadline = instance.tugash_vaqti
                
                # Priority yangilash
                if instance.xolat == 'SHOSHILINCH':
                    report.priority = 'urgent'
                elif instance.xolat == 'MUHIM':
                    report.priority = 'high'
                elif instance.xolat == 'O`RTA':
                    report.priority = 'medium'
                else:
                    report.priority = 'low'
                
                # Full report'ni qayta generatsiya qilish
                report.generate_full_report()
                report.save()
                
                print(f"TopshiriqReport yangilandi: {report.id}")
                
        except Exception as e:
            print(f"TopshiriqReport yangilashda xatolik: {str(e)}")