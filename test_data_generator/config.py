# Test Data Generator Configuration

# Ma'lumotlar miqdori sozlamalari
DEFAULT_USERS_COUNT = 4000
DEFAULT_TASKS_COUNT = 50000
DEFAULT_RESPONSES_COUNT = 30000

# Bulk create sozlamalari
BULK_CREATE_BATCH_SIZE = 1000

# Progress reporting sozlamalari  
PROGRESS_REPORT_INTERVAL = {
    'users': 1000,
    'tasks': 5000,
    'responses': 2000,
}

# Username generation sozlamalari
USERNAME_FORMATS = [
    "{first}.{last}",
    "{first}_{last}",
    "{first} {last}",  # Bo'shliq bilan
    "{first}{number}",
    "{first}.{last}{number}",
    "{last}.{first}",
    "{first}_{last}{number}",
    "{first} {last} {number}",  # Bo'shliq va raqam bilan
]

# Email domain sozlamalari
EMAIL_DOMAINS = [
    "example.com",
    "test.org", 
    "demo.uz",
    "sample.net"
]

# Telefon raqami prefixlari (O'zbekiston)
PHONE_PREFIXES = [
    "+99890",  # Beeline
    "+99891",  # Ucell
    "+99893",  # Ucell  
    "+99894",  # Ucell
    "+99895",  # UMS
    "+99897",  # Beeline
    "+99898",  # Perfectum Mobile
    "+99899",  # Beeline
]

# Faol foydalanuvchilar foizi
ACTIVE_USERS_PERCENTAGE = 0.75  # 75% faol

# Sana oralig'i sozlamalari (kunlarda)
DATE_RANGES = {
    'task_created_days_ago': (1, 365),  # 1 kundan 1 yilgacha
    'task_deadline_days_ahead': (1, 90),  # 1 kundan 3 oygacha
    'response_delay_hours': (1, 24 * 30),  # 1 soatdan 30 kungacha
}

# Database connection sozlamalari
DATABASE_SETTINGS = {
    'timeout': 30,  # Connection timeout (seconds)
    'max_retries': 3,  # Maximum retry attempts
}