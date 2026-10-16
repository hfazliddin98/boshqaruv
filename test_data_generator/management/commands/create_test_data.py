import os
import sys
import django
from django.core.management.base import BaseCommand
from django.db import transaction
import random
from uuid import uuid4
from datetime import datetime, timedelta
from django.utils import timezone

# Django sozlamalarini import qilish
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'asosiy.settings')
django.setup()

from users.models import Users, Struktura
from users.choices import RoleChoice
from topshiriq.models import Topshiriq, TopshiriqJavob
from topshiriq.choices import StatusChoice as TopshiriqStatusChoice, XolatChoice
from ...fake_data import (
    FIRST_NAMES, LAST_NAMES, SHARIF_NAMES, TOPSHIRIQ_TITLES, 
    TOPSHIRIQ_BODIES, STRUKTURALAR_DATA
)


class Command(BaseCommand):
    help = 'Katta hajmdagi test ma\'lumotlari yaratadi (50,000+ topshiriq va 4,000+ foydalanuvchi)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--users',
            type=int,
            default=4000,
            help='Yaratilishi kerak bo\'lgan foydalanuvchilar soni',
        )
        parser.add_argument(
            '--tasks',
            type=int,
            default=50000,
            help='Yaratilishi kerak bo\'lgan topshiriqlar soni',
        )
        parser.add_argument(
            '--responses',
            type=int,
            default=30000,
            help='Yaratilishi kerak bo\'lgan topshiriq javoblari soni',
        )
        parser.add_argument(
            '--clear',
            action='store_true',
            help='Avvalgi test ma\'lumotlarini o\'chirish',
        )

    def handle(self, *args, **options):
        users_count = options['users']
        tasks_count = options['tasks']
        responses_count = options['responses']
        clear_data = options['clear']
        
        self.stdout.write(
            self.style.SUCCESS(
                f'Test ma\'lumotlarini yaratish boshlanmoqda:\n'
                f'- Foydalanuvchilar: {users_count}\n'
                f'- Topshiriqlar: {tasks_count}\n'
                f'- Javoblar: {responses_count}\n'
                f'- Avvalgi ma\'lumotlarni o\'chirish: {"Ha" if clear_data else "Yo\'q"}'
            )
        )

        try:
            with transaction.atomic():
                # Avvalgi ma'lumotlarni o'chirish
                if clear_data:
                    self.clear_existing_data()
                
                # 1. Strukturalarni yaratish
                self.create_structures()
                
                # 2. Foydalanuvchilarni yaratish
                self.create_users(users_count)
                
                # 3. Topshiriqlarni yaratish
                self.create_tasks(tasks_count)
                
                # 4. Topshiriq javoblarini yaratish
                self.create_task_responses(responses_count)
                
            self.stdout.write(
                self.style.SUCCESS(
                    f'Test ma\'lumotlari muvaffaqiyatli yaratildi!\n'
                    f'- Strukturalar: {Struktura.objects.count()}\n'
                    f'- Foydalanuvchilar: {Users.objects.count()}\n'
                    f'- Topshiriqlar: {Topshiriq.objects.count()}\n'
                    f'- Javoblar: {TopshiriqJavob.objects.count()}'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Xatolik yuz berdi: {str(e)}')
            )
            raise

    def clear_existing_data(self):
        """Mavjud test ma'lumotlarini o'chirish"""
        self.stdout.write('Avvalgi test ma\'lumotlari o\'chirilmoqda...')
        
        # Foreign key bog'liqligini hisobga olib ketma-ket o'chirish
        deleted_responses = TopshiriqJavob.objects.all().delete()[0]
        deleted_tasks = Topshiriq.objects.all().delete()[0]
        deleted_users = Users.objects.filter(is_superuser=False).delete()[0]  # Superuser'larni saqlab qolish
        deleted_structures = Struktura.objects.all().delete()[0]
        
        self.stdout.write(
            f'  ✓ O\'chirildi:\n'
            f'    - Javoblar: {deleted_responses}\n'
            f'    - Topshiriqlar: {deleted_tasks}\n'
            f'    - Foydalanuvchilar: {deleted_users}\n'
            f'    - Strukturalar: {deleted_structures}'
        )

    def create_structures(self):
        """Strukturalarni yaratish"""
        self.stdout.write('Strukturalar yaratilmoqda...')
        
        structures = []
        for name, role in STRUKTURALAR_DATA:
            if not Struktura.objects.filter(name=name).exists():
                structures.append(Struktura(
                    id=str(uuid4()),
                    name=name,
                    role=role
                ))
        
        if structures:
            Struktura.objects.bulk_create(structures, batch_size=1000)
            self.stdout.write(f'  ✓ {len(structures)} ta yangi struktura yaratildi')
        else:
            self.stdout.write('  ✓ Barcha strukturalar allaqachon mavjud')

    def create_users(self, count):
        """Foydalanuvchilarni yaratish"""
        self.stdout.write(f'{count} ta foydalanuvchi yaratilmoqda...')
        
        structures = list(Struktura.objects.all())
        if not structures:
            raise Exception("Avval strukturalar yaratilishi kerak")
        
        users = []
        existing_usernames = set(Users.objects.values_list('username', flat=True))
        
        for i in range(count):
            # Unique username yaratish
            username = self.generate_unique_username(existing_usernames)
            existing_usernames.add(username)
            
            # Tasodifiy ma'lumotlar
            first_name = random.choice(FIRST_NAMES)
            last_name = random.choice(LAST_NAMES)
            sharif = random.choice(SHARIF_NAMES)
            structure = random.choice(structures)
            
            # Email yaratish
            email_base = username.lower().replace(' ', '.').replace('_', '.')
            email = f"{email_base}@example.com"
            
            user = Users(
                id=str(uuid4()),
                username=username,
                first_name=first_name,
                last_name=last_name,
                sharif=sharif,
                email=email,
                role=structure.role,
                struktura=structure,
                is_active=random.choice([True, True, True, False]),  # 75% faol
            )
            users.append(user)
            
            # Progress ko'rsatish
            if (i + 1) % 1000 == 0:
                self.stdout.write(f'  - {i + 1}/{count} foydalanuvchi tayyorlandi')
        
        # Bulk create
        Users.objects.bulk_create(users, batch_size=1000)
        self.stdout.write(f'  ✓ {count} ta foydalanuvchi yaratildi')

    def generate_unique_username(self, existing_usernames):
        """Unique username yaratish"""
        while True:
            first = random.choice(FIRST_NAMES).lower()
            last = random.choice(LAST_NAMES).lower()
            
            # Turli formatlar (bo'shliq bilan ham)
            formats = [
                f"{first}.{last}",
                f"{first}_{last}",
                f"{first} {last}",  # Bo'shliq bilan
                f"{first}{random.randint(10, 99)}",
                f"{first}.{last}{random.randint(10, 99)}",
                f"{last}.{first}",
                f"{first}_{last}{random.randint(100, 999)}",
                f"{first} {last} {random.randint(1, 99)}",  # Bo'shliq va raqam bilan
            ]
            
            username = random.choice(formats)
            if username not in existing_usernames:
                return username

    def create_tasks(self, count):
        """Topshiriqlarni yaratish"""
        self.stdout.write(f'{count} ta topshiriq yaratilmoqda...')
        
        users = list(Users.objects.all())
        if not users:
            raise Exception("Avval foydalanuvchilar yaratilishi kerak")
        
        tasks = []
        for i in range(count):
            title = random.choice(TOPSHIRIQ_TITLES)
            body = random.choice(TOPSHIRIQ_BODIES)
            
            # Tasodifiy muddatlar
            created = timezone.now() - timedelta(days=random.randint(1, 365))
            deadline = created + timedelta(days=random.randint(1, 90))
            
            # Tasodifiy muddatlar
            boshlanish_vaqti = created + timedelta(hours=random.randint(1, 48))
            tugash_vaqti = boshlanish_vaqti + timedelta(days=random.randint(1, 30))
            
            task = Topshiriq(
                id=str(uuid4()),
                title=title,
                body=body,
                yaratuvchi_user=random.choice(users),
                bajaruvchi_user=random.choice(users),
                status=random.choice([choice[0] for choice in TopshiriqStatusChoice.choices]),
                xolat=random.choice([choice[0] for choice in XolatChoice.choices]),
                baxo=random.randint(0, 100),
                boshlanish_vaqti=boshlanish_vaqti,
                tugash_vaqti=tugash_vaqti,
                javob_yuborildi=random.choice([True, False]),
                urinishlar_soni=random.randint(1, 3),
                izoh=f"Test izoh #{random.randint(1000, 9999)}",
                created_at=created,
                updated_at=created + timedelta(hours=random.randint(1, 24)),
            )
            tasks.append(task)
            
            # Progress ko'rsatish
            if (i + 1) % 5000 == 0:
                self.stdout.write(f'  - {i + 1}/{count} topshiriq tayyorlandi')
        
        # Bulk create
        Topshiriq.objects.bulk_create(tasks, batch_size=1000)
        self.stdout.write(f'  ✓ {count} ta topshiriq yaratildi')

    def create_task_responses(self, count):
        """Topshiriq javoblarini yaratish"""
        self.stdout.write(f'{count} ta topshiriq javobi yaratilmoqda...')
        
        tasks = list(Topshiriq.objects.all())
        users = list(Users.objects.all())
        
        if not tasks or not users:
            raise Exception("Avval topshiriqlar va foydalanuvchilar yaratilishi kerak")
        
        responses = []
        response_texts = [
            "Topshiriq muvaffaqiyatli bajarildi.",
            "Barcha talablar bo'yicha ishlash tugallandi.",
            "Qo'shimcha ma'lumotlar bilan to'ldirildi.",
            "Muddatida tayyorlandi va topshirildi.",
            "Sifat talablariga javob beradi.",
            "Barcha hujjatlar tayyorlandi.",
            "Tekshiruv o'tkazildi va xatolar tuzatildi.",
            "Yakuniy natija tayyor.",
            "Qo'shimcha takomillashtirishlar kiritildi.",
            "Mijoz talablariga muvofiq bajarildi.",
            "Texnik talablar to'liq bajarildi.",
            "Loyiha muvaffaqiyatli yakunlandi.",
            "Barcha testlar o'tkazildi.",
            "Dokumentatsiya tayyorlandi.",
            "Deploy qilishga tayyor.",
            "Code review o'tkazildi.",  
            "Performance optimallashtirildi.",
            "Security tekshiruvdan o'tdi.",
            "User acceptance test muvaffaqiyatli.",
            "Production ga chiqarishga tayyor.",
            "Stakeholder'lar bilan kelishildi.",
            "Risk assessment o'tkazildi.",
            "Compliance talablariga javob beradi.",
            "Backup va recovery test qilindi.",
            "Load testing muvaffaqiyatli.",
            "Integration testlar o'tdi.",
            "User training materiallari tayyorlandi.",
            "Go-live rejasi tasdiqlandi.",
            "Rollback strategiyasi tayyor.",
            "Monitoring va alerting sozlandi."
        ]
        
        for i in range(count):
            task = random.choice(tasks)
            user = random.choice(users)
            
            response = TopshiriqJavob(
                id=str(uuid4()),
                topshiriq=task,
                bajaruvchi_user=user,
                title=f"Javob: {task.title[:50]}",
                body=random.choice(response_texts),
                urinishlar_soni=random.randint(1, 3),
                izoh=f"Test javob izoh #{random.randint(1000, 9999)}",
                created_at=task.created_at + timedelta(
                    hours=random.randint(1, 24 * 30)
                ),
            )
            responses.append(response)
            
            # Progress ko'rsatish
            if (i + 1) % 2000 == 0:
                self.stdout.write(f'  - {i + 1}/{count} javob tayyorlandi')
        
        # Bulk create
        TopshiriqJavob.objects.bulk_create(responses, batch_size=1000)
        self.stdout.write(f'  ✓ {count} ta topshiriq javobi yaratildi')