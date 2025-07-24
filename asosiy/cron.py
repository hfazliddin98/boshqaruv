from django.core.management import call_command

def my_backup_file():
  try:
    call_command('dbbackup')
    call_command('mediabackup')
  except:
    pass