# models.py
from django.contrib.auth.models import User
from django.db import models
import os
from django.core.files.storage import default_storage
from django.conf import settings

class Reservation(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    time = models.TimeField()
    num_people = models.CharField(max_length=20)
    table = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'reservation_from_contact'

class Reservation_main(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=150)  # Додаємо поле для зберігання імені користувача
    user_email = models.EmailField()  # Додаємо поле для зберігання пошти користувача
    user_phone = models.CharField(max_length=20)  # Додаємо поле для зберігання номера телефону користувача
    date = models.DateField()
    time = models.TimeField()
    people = models.CharField(max_length=50)
    table = models.CharField(max_length=50)

    def __str__(self):
        return f"Reservation - {self.date} at {self.time} for {self.people} at {self.table}"
    
    def save(self, *args, **kwargs):
        # Перевіряємо, чи вказаний користувач у замовленні
        if self.user_id:
            user = User.objects.get(id=self.user_id)
            # Заповнюємо поля імені, пошти та номера телефону замовника
            self.user_name = user.get_full_name()
            self.user_email = user.email
            self.user_phone = user.userprofile.phone_number
        super().save(*args, **kwargs)
    
    class Meta:
        db_table = 'reservation'
  
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    surname = models.CharField(max_length=100)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=25)
    email = models.CharField(max_length=50)
    is_active = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photos/')

    def __str__(self):
        return f'{self.user.username} - {self.surname}, {self.name}, {self.email}'
    
    class Meta:
        db_table = 'user_info'

class Tables(models.Model):
    table_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    available = models.BooleanField()
    photo = models.ImageField(upload_to='tables/')

    def __str__(self):
        return f'{self.table_name} - {self.date}, {self.time}, {self.available}'
    
    class Meta:
        db_table = 'tables'

class Meal(models.Model):
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    starters = models.BooleanField()
    launch = models.BooleanField()
    dinner = models.BooleanField()
    drinks = models.BooleanField()
    sweets = models.BooleanField()
    fruits = models.BooleanField()
    alcohol = models.BooleanField()
    photo = models.ImageField(upload_to='meals/')
    photo_size = models.CharField(max_length=20)

    def __str__(self):
        return f'{self.name} - {self.description}, {self.starters}, {self.launch}, {self.dinner}, {self.drinks}, {self.sweets}, {self.fruits}, {self.alcohol}'
    
    class Meta:
        db_table = 'meals'

class Review(models.Model):
    meal = models.ForeignKey('Meal', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')])

    def __str__(self):
        return f'Review for {self.meal.name} by {self.user.username} - Rating: {self.rating}'

    class Meta:
        db_table = 'reviews'

class ReservationMeal(models.Model):
    reservation = models.ForeignKey(Reservation_main, on_delete=models.CASCADE)
    meal = models.ForeignKey(Meal, on_delete=models.CASCADE)
    meal_name = models.CharField(max_length=100)
    date = models.DateField()
    time = models.TimeField()
    people = models.CharField(max_length=50)
    table = models.CharField(max_length=50)

    def __str__(self):
        return f"ReservationMeal - {self.date} at {self.time} for {self.people} at {self.table} with {self.meal_name}"
    
    class Meta:
        db_table = 'Reservation_Meal'