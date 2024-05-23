import schedule
import time
from datetime import datetime
from django.utils import timezone
from .models import Reservation, Reservation_main, Tables

def update_table_data():
    # Оновлення даних про столики
    tables = Tables.objects.all()
    for table in tables:
        table.date = datetime.now()
        table.time = datetime.now()
        table.save()

def delete_past_reservations():
    current_datetime = timezone.now()

    # Видаляємо бронювання, які мінули
    past_reservations_main = Reservation_main.objects.filter(date__lt=current_datetime.date())
    past_reservations_contact = Reservation.objects.filter(date__lt=current_datetime.date())

    past_reservations_main.delete()
    past_reservations_contact.delete()

def update_table_status():
    current_datetime = datetime.now()
    
    # Якщо так, оновлюємо статуси таблиць
    tables = Tables.objects.all()
    
    for table in tables:
        if (Reservation_main.objects.filter(table=table.table_name, date=current_datetime.date(), time__lte=current_datetime).exists() or \
            Reservation.objects.filter(table=table.table_name, date=current_datetime.date(), time__lte=current_datetime).exists()):
            table.available = 0
        else:
            # Перевіряємо, чи час 20:00
            if current_datetime.hour >= 20:
                table.available = 1
        table.date = current_datetime
        table.time = current_datetime
        table.save()

def schedule_table_update():
    # Планування оновлення даних про столики кожну хвилину
    schedule.every(1).seconds.do(update_table_data)
    schedule.every(1).seconds.do(delete_past_reservations)
    schedule.every(1).seconds.do(update_table_status)

    while True:
        schedule.run_pending()
        time.sleep(1)