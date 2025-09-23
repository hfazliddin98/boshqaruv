# Test Data Generator Package

Bu paket loyihada katta hajmdagi test ma'lumotlarini yaratish va boshqarish uchun mo'ljallangan.

## Buyruqlar

### 1. Test ma'lumotlarini yaratish

```bash
python manage.py create_test_data --users 4000 --tasks 50000 --responses 30000
```

**Options:**
- `--users`: Yaratilishi kerak bo'lgan foydalanuvchilar soni (default: 4000)
- `--tasks`: Yaratilishi kerak bo'lgan topshiriqlar soni (default: 50000)  
- `--responses`: Yaratilishi kerak bo'lgan javoblar soni (default: 30000)
- `--clear`: Avvalgi test ma'lumotlarini o'chirish

**Misollar:**
```bash
# Standart hajmdagi ma'lumotlar yaratish
python manage.py create_test_data

# Kichik hajmdagi ma'lumotlar yaratish  
python manage.py create_test_data --users 100 --tasks 1000 --responses 500

# Avvalgi ma'lumotlarni o'chirib, yangilarini yaratish
python manage.py create_test_data --clear --users 1000 --tasks 10000
```

### 2. Test ma'lumotlarini kamaytirish

```bash
python manage.py reduce_test_data --reduce-users 1000 --reduce-tasks 5000
```

**Options:**
- `--clear-all`: Barcha test ma'lumotlarini to'liq o'chirish (superuser'lardan tashqari)
- `--reduce-users N`: Foydalanuvchilarni N tagacha kamaytirish
- `--reduce-tasks N`: Topshiriqlarni N tagacha kamaytirish  
- `--reduce-responses N`: Javoblarni N tagacha kamaytirish
- `--keep-recent`: Eng yangi ma'lumotlarni saqlab qolish (eskilarini o'chirish)
- `--keep-old`: Eng eski ma'lumotlarni saqlab qolish (yangilarini o'chirish)

**Misollar:**
```bash
# Barcha test ma'lumotlarini o'chirish
python manage.py reduce_test_data --clear-all

# Foydalanuvchilarni 500 tagacha kamaytirish (yangilarini saqlash)
python manage.py reduce_test_data --reduce-users 500 --keep-recent

# Topshiriqlarni 10000 tagacha kamaytirish (eskilarini saqlash)
python manage.py reduce_test_data --reduce-tasks 10000 --keep-old

# Javoblarni 5000 tagacha kamaytirish
python manage.py reduce_test_data --reduce-responses 5000

# Bir nechta parametrni birga ishlatish
python manage.py reduce_test_data --reduce-users 1000 --reduce-tasks 5000 --keep-recent
```

## Package Structure

```
test_data_generator/
├── __init__.py                           # Paket initializatsiyasi
├── README.md                             # Foydalanish yo'riqnomasi
├── config.py                             # Konfiguratsiya sozlamalari
├── fake_data.py                          # Test ma'lumotlari konstantalari
└── management/
    ├── __init__.py
    └── commands/
        ├── __init__.py
        ├── create_test_data.py           # Test ma'lumotlarini yaratish
        └── reduce_test_data.py           # Test ma'lumotlarini kamaytirish
```

## Xususiyatlar

### Yaratish (create_test_data):
- ✅ Bo'shliq bilan username yaratish
- ✅ UUID primary keylar
- ✅ Bulk create operatsiyalari (tez ishlash)
- ✅ Progress tracking
- ✅ Transaction safety
- ✅ Realistic test data
- ✅ Konfiguratsiya qilish imkoniyati

### Kamaytirish (reduce_test_data):
- ✅ Xavfsiz o'chirish (foreign key bog'liqliklarini hisobga olish)
- ✅ Superuser'larni saqlab qolish
- ✅ Sana bo'yicha tartibga solish (yangi/eski)
- ✅ Tasodifiy o'chirish
- ✅ Real-time statistika ko'rsatish
- ✅ Transaction safety

**Version:** 1.0.0
**Author:** Test Data Generator Team