import os
import sys
import django
from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

# Django sozlamalarini import qilish
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asosiy.settings')
django.setup()

from django.db import models
from django.db.models import Q
from users.models import Users, Struktura
from topshiriq.models import Topshiriq, TopshiriqJavob


class Command(BaseCommand):
    help = 'Test ma\'lumotlarini kamaytirish yoki to\'liq o\'chirish'

    def add_arguments(self, parser):
        parser.add_argument(
            '--clear-all',
            action='store_true',
            help='Barcha test ma\'lumotlarini to\'liq o\'chirish (superuser\'lardan tashqari)',
        )
        parser.add_argument(
            '--reduce-users',
            type=int,
            help='Foydalanuvchilarni berilgan songacha kamaytirish',
        )
        parser.add_argument(
            '--reduce-tasks',
            type=int,
            help='Topshiriqlarni berilgan songacha kamaytirish',
        )
        parser.add_argument(
            '--reduce-responses',
            type=int,
            help='Javoblarni berilgan songacha kamaytirish',
        )
        parser.add_argument(
            '--keep-recent',
            action='store_true',
            help='Eng yangi ma\'lumotlarni saqlab qolish (eskilarini o\'chirish)',
        )
        parser.add_argument(
            '--keep-old',
            action='store_true',
            help='Eng eski ma\'lumotlarni saqlab qolish (yangilarini o\'chirish)',
        )

    def handle(self, *args, **options):
        clear_all = options['clear_all']
        reduce_users = options['reduce_users']
        reduce_tasks = options['reduce_tasks']
        reduce_responses = options['reduce_responses']
        keep_recent = options['keep_recent']
        keep_old = options['keep_old']

        if not any([clear_all, reduce_users, reduce_tasks, reduce_responses]):
            self.stdout.write(
                self.style.ERROR(
                    'Hech bo\'lmasa bitta parametr ko\'rsating:\n'
                    '  --clear-all: Barchasini o\'chirish\n'
                    '  --reduce-users N: Foydalanuvchilarni N tagacha kamaytirish\n'
                    '  --reduce-tasks N: Topshiriqlarni N tagacha kamaytirish\n'
                    '  --reduce-responses N: Javoblarni N tagacha kamaytirish'
                )
            )
            return

        # Joriy holatni ko'rsatish
        self.show_current_stats()

        try:
            with transaction.atomic():
                if clear_all:
                    self.clear_all_data()
                else:
                    if reduce_responses:
                        self.reduce_responses(reduce_responses, keep_recent, keep_old)
                    
                    if reduce_tasks:
                        self.reduce_tasks(reduce_tasks, keep_recent, keep_old)
                    
                    if reduce_users:
                        self.reduce_users(reduce_users, keep_recent, keep_old)

            # Yangi holatni ko'rsatish
            self.stdout.write(self.style.SUCCESS('\n--- Operatsiyadan keyin ---'))
            self.show_current_stats()
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Xatolik yuz berdi: {str(e)}')
            )
            raise

    def show_current_stats(self):
        """Joriy ma'lumotlar statistikasini ko'rsatish"""
        users_count = Users.objects.count()
        superusers_count = Users.objects.filter(is_superuser=True).count()
        regular_users_count = users_count - superusers_count
        tasks_count = Topshiriq.objects.count()
        responses_count = TopshiriqJavob.objects.count()
        structures_count = Struktura.objects.count()

        self.stdout.write(
            self.style.SUCCESS(
                f'Joriy ma\'lumotlar holati:\n'
                f'- Strukturalar: {structures_count}\n'
                f'- Jami foydalanuvchilar: {users_count}\n'
                f'  * Superuser\'lar: {superusers_count}\n'
                f'  * Oddiy foydalanuvchilar: {regular_users_count}\n'
                f'- Topshiriqlar: {tasks_count}\n'
                f'- Javoblar: {responses_count}'
            )
        )

    def clear_all_data(self):
        """Barcha test ma'lumotlarini o'chirish"""
        self.stdout.write('Barcha test ma\'lumotlari o\'chirilmoqda...')
        
        # Foreign key bog'liqligini hisobga olib ketma-ket o'chirish
        deleted_responses = TopshiriqJavob.objects.all().delete()[0]
        deleted_tasks = Topshiriq.objects.all().delete()[0]
        deleted_users = Users.objects.filter(is_superuser=False).delete()[0]  # Superuser'larni saqlab qolish
        deleted_structures = Struktura.objects.all().delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(
                f'O\'chirildi:\n'
                f'  ✓ Javoblar: {deleted_responses}\n'
                f'  ✓ Topshiriqlar: {deleted_tasks}\n'  
                f'  ✓ Foydalanuvchilar: {deleted_users}\n'
                f'  ✓ Strukturalar: {deleted_structures}\n'
                f'  ℹ Superuser\'lar saqlab qolindi'
            )
        )

    def reduce_users(self, target_count, keep_recent=False, keep_old=False):
        """Foydalanuvchilarni kamaytirish"""
        current_count = Users.objects.filter(is_superuser=False).count()
        
        if current_count <= target_count:
            self.stdout.write(f'Foydalanuvchilar soni allaqachon {target_count} dan kam yoki teng ({current_count})')
            return

        to_delete = current_count - target_count
        
        self.stdout.write(f'Foydalanuvchilarni {current_count} dan {target_count} gacha kamaytirish...')
        
        # Qaysi foydalanuvchilarni o'chirish kerakligini aniqlash
        queryset = Users.objects.filter(is_superuser=False)
        
        if keep_recent:
            # Eng eski foydalanuvchilarni o'chirish
            users_to_delete = queryset.order_by('date_joined')[:to_delete]
        elif keep_old:
            # Eng yangi foydalanuvchilarni o'chirish
            users_to_delete = queryset.order_by('-date_joined')[:to_delete]
        else:
            # Tasodifiy foydalanuvchilarni o'chirish
            users_to_delete = queryset.order_by('?')[:to_delete]
        
        # Foydalanuvchilar bilan bog'liq topshiriq va javoblarni ham o'chirish
        user_ids = list(users_to_delete.values_list('id', flat=True))
        
        # Bu foydalanuvchilarning javoblarini o'chirish
        deleted_responses = TopshiriqJavob.objects.filter(bajaruvchi_user_id__in=user_ids).delete()[0]
        
        # Bu foydalanuvchilar yaratgan yoki olgan topshiriqlarni o'chirish
        deleted_tasks = Topshiriq.objects.filter(
            Q(yaratuvchi_user_id__in=user_ids) | Q(bajaruvchi_user_id__in=user_ids)
        ).delete()[0]
        
        # Foydalanuvchilarni o'chirish
        deleted_users = users_to_delete.delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(
                f'  ✓ {deleted_users} ta foydalanuvchi o\'chirildi\n'
                f'  ✓ {deleted_tasks} ta bog\'liq topshiriq o\'chirildi\n'
                f'  ✓ {deleted_responses} ta bog\'liq javob o\'chirildi'
            )
        )

    def reduce_tasks(self, target_count, keep_recent=False, keep_old=False):
        """Topshiriqlarni kamaytirish"""
        current_count = Topshiriq.objects.count()
        
        if current_count <= target_count:
            self.stdout.write(f'Topshiriqlar soni allaqachon {target_count} dan kam yoki teng ({current_count})')
            return

        to_delete = current_count - target_count
        
        self.stdout.write(f'Topshiriqlarni {current_count} dan {target_count} gacha kamaytirish...')
        
        # Qaysi topshiriqlarni o'chirish kerakligini aniqlash
        queryset = Topshiriq.objects.all()
        
        if keep_recent:
            # Eng eski topshiriqlarni o'chirish
            tasks_to_delete = queryset.order_by('created_at')[:to_delete]
        elif keep_old:
            # Eng yangi topshiriqlarni o'chirish
            tasks_to_delete = queryset.order_by('-created_at')[:to_delete]
        else:
            # Tasodifiy topshiriqlarni o'chirish
            tasks_to_delete = queryset.order_by('?')[:to_delete]
        
        # Topshiriqlar bilan bog'liq javoblarni ham o'chirish
        task_ids = list(tasks_to_delete.values_list('id', flat=True))
        deleted_responses = TopshiriqJavob.objects.filter(topshiriq_id__in=task_ids).delete()[0]
        
        # Topshiriqlarni o'chirish
        deleted_tasks = tasks_to_delete.delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(
                f'  ✓ {deleted_tasks} ta topshiriq o\'chirildi\n'
                f'  ✓ {deleted_responses} ta bog\'liq javob o\'chirildi'
            )
        )

    def reduce_responses(self, target_count, keep_recent=False, keep_old=False):
        """Javoblarni kamaytirish"""
        current_count = TopshiriqJavob.objects.count()
        
        if current_count <= target_count:
            self.stdout.write(f'Javoblar soni allaqachon {target_count} dan kam yoki teng ({current_count})')
            return

        to_delete = current_count - target_count
        
        self.stdout.write(f'Javoblarni {current_count} dan {target_count} gacha kamaytirish...')
        
        # Qaysi javoblarni o'chirish kerakligini aniqlash
        queryset = TopshiriqJavob.objects.all()
        
        if keep_recent:
            # Eng eski javoblarni o'chirish
            responses_to_delete = queryset.order_by('created_at')[:to_delete]
        elif keep_old:
            # Eng yangi javoblarni o'chirish
            responses_to_delete = queryset.order_by('-created_at')[:to_delete]
        else:
            # Tasodifiy javoblarni o'chirish
            responses_to_delete = queryset.order_by('?')[:to_delete]
        
        # Javoblarni o'chirish
        deleted_responses = responses_to_delete.delete()[0]
        
        self.stdout.write(
            self.style.SUCCESS(f'  ✓ {deleted_responses} ta javob o\'chirildi')
        )