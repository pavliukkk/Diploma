import datetime
from django.utils import timezone
from django.http import HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.http import JsonResponse
from django.contrib.auth import logout
from .models import *
from django.utils.http import urlsafe_base64_decode
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.forms import SetPasswordForm
from django.utils.encoding import smart_bytes
from django.contrib.auth.decorators import user_passes_test
import calendar
import re
from django.db.models import Q
from django.core.mail import send_mail
from threading import Thread
from .tasks import schedule_table_update
from django.utils.translation import activate, check_for_language, gettext_lazy as _
from PIL import Image, ImageDraw
from io import BytesIO
from django.db.models import Avg, Count
from django.utils.translation import activate, get_language
from pytz import timezone as tz
from django.contrib.auth import get_user_model
from django.utils.encoding import force_str
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.hashers import check_password
from django.contrib.auth import update_session_auth_hash

@user_passes_test(lambda u: u.is_anonymous, login_url='/home/')
def register(request):
    if request.method == 'POST':
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        try:
            # Перевірка, чи існує користувач із вказаною електронною адресою
            if User.objects.get(username=email):
                return render(request, 'registration.html', {'user_exist': True})
        except User.DoesNotExist:
            pass

        try:
            # Перевірка, чи існує користувач із вказаною електронною адресою
            if User.objects.get(email=email):
                return render(request, 'registration.html', {'user_exist': True})
        except User.DoesNotExist:
            pass    

        try:
            # Перевірка, чи існує користувач із вказаним номером телефону
            if UserProfile.objects.get(phone_number=phone_number):
                return render(request, 'registration.html', {'user_exist': True})
        except UserProfile.DoesNotExist:
            pass
            

        # Create user if email doesn't exist
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = name
        user.last_name = surname
        user.is_active = False  # Користувач буде неактивний до підтвердження електронної пошти
        user.save()

        # Create UserProfile instance and save it
        user_profile = UserProfile.objects.create(user=user, surname=surname, name=name, phone_number=phone_number, email=email)
        user_profile.save()

        # Створіть токен для активації акаунту
        token = default_token_generator.make_token(user)

        # Відправте електронний лист із посиланням для активації
        activation_link = f"https://foodzero.up.railway.app/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/"
        send_activation_email(email, activation_link)

        # Authenticate and log in the user
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/home/')
        else:
            return render(request, 'login.html', {'registered': True})
    else:
        return render(request, 'registration.html')

def send_activation_email(email, activation_link):
    subject = 'Активація акаунту на FoodZero'
    message = f'Дякуємо за реєстрацію на FoodZero. Для активації акаунту перейдіть за посиланням: {activation_link}'
    from_email = 'foodzero.restaurant@gmail.com'
    recipient_list = [email]
    send_mail(subject, message, from_email, recipient_list, fail_silently=False)

def activation_email_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')

        # Пошук користувача за адресою електронної пошти
        user = User.objects.get(email=email)

        # Генерація токена для активації
        token = default_token_generator.make_token(user)

        # Генерація посилання для активації
        activation_link = f"https://foodzero.up.railway.app/activate/{urlsafe_base64_encode(force_bytes(user.pk))}/{token}/"

        # Відправлення електронного листа з посиланням для активації
        send_activation_email(email, activation_link)

        return render(request, 'login.html', {'activate_link_sent': True})
    else:
        return render(request, 'login.html')

def activate_account(request, uidb64, token):
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        # Оновіть is_active в auth_user
        user.is_active = True
        user.save()

        # Отримайте відповідний запис у UserProfile та оновіть його is_active
        user_profile = UserProfile.objects.get(user=user)
        user_profile.is_active = True
        user_profile.save()

        # Здійсніть вхід
        return HttpResponseRedirect('/login/')
    else:
        return HttpResponse("This link is invalid.")

def normalize_login_identifier(login_identifier):
    """Функція для нормалізації введеного ідентифікатора логіну."""
    # Перевіряємо, чи введений ідентифікатор є номером телефону
    if re.match(r'^\+?\d{10,12}$', login_identifier):  
        # Видаляємо всі символи, крім цифр
        login_identifier = re.sub(r'\D', '', login_identifier)
        # Додаємо префікс "+380", якщо його немає
        if not login_identifier.startswith('380'):
            login_identifier = '380' + login_identifier[1:]
        # Форматуємо номер телефону до вигляду +380 (xx) xxx-xx-xx
        return '+380 ({}) {}-{}-{}'.format(login_identifier[3:5], login_identifier[5:8], login_identifier[8:10], login_identifier[10:12])
    else:
        # Інакше повертаємо ідентифікатор без змін
        return login_identifier

@user_passes_test(lambda u: u.is_anonymous, login_url='/home/')
@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        login_identifier = request.POST.get('email')
        password = request.POST.get('password')

        # Нормалізуємо введений ідентифікатор логіну
        normalized_login_identifier = normalize_login_identifier(login_identifier)

        try:
            # Шукаємо користувача в базі даних за іменем користувача або електронною поштою
            user = User.objects.get(username=normalized_login_identifier)

            # Перевіряємо, чи активований користувач
            if not user.userprofile.is_active:
                return render(request, 'login.html', {'activation_error': True, 'no_user': False, 'wrong_password': False})

            # Аутентифікуємо користувача
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                # Успішний логін
                login(request, user)
                return HttpResponseRedirect('/home/')
            else:
                # Існуючий користувач, але неправильний пароль
                return render(request, 'login.html', {'wrong_password': True, 'no_user': False, 'activation_error': False})

        except User.DoesNotExist:
            # Перевіряємо користувача за номером телефону
            try:
                # Шукаємо користувача в базі даних за номером телефону
                user_profile = UserProfile.objects.get(phone_number=normalized_login_identifier)

                if not user_profile.is_active:
                    return render(request, 'login.html', {'activation_error': True, 'no_user': False, 'wrong_password': False})

                user = user_profile.user
                # Аутентифікуємо користувача
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    # Успішний логін
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    # Існуючий користувач, але неправильний пароль
                    return render(request, 'login.html', {'wrong_password': True, 'no_user': False, 'activation_error': False})

            except UserProfile.DoesNotExist:
                # Неіснуючий користувач ні за ім'ям користувача, ні за номером телефону
                return render(request, 'login.html', {'no_user': True, 'wrong_password': False, 'activation_error': False})

    else:
        return render(request, 'login.html', {'no_user': False, 'wrong_password': False})

@user_passes_test(lambda u: u.is_anonymous, login_url='/home/')
@csrf_exempt
def admin_login(request):
    if request.method == 'POST':
        login_identifier = request.POST.get('email')
        password = request.POST.get('password')

        # Нормалізуємо введений ідентифікатор логіну
        normalized_login_identifier = normalize_login_identifier(login_identifier)

        try:
            # Шукаємо користувача в базі даних за іменем користувача або електронною поштою
            user = User.objects.get(username=normalized_login_identifier)

            # Перевіряємо, чи активований користувач
            if not user.userprofile.is_active:
                return render(request, 'admin_login.html', {'activation_error': True, 'no_user': False, 'wrong_password': False})

            # Аутентифікуємо користувача
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                if user.is_superuser:
                    # Успішний логін для адміна
                    login(request, user)
                    return HttpResponseRedirect('/home/')
                else:
                    # Користувач не є адміном, відмова в авторизації
                    request.user = None
                    return render(request, 'admin_login.html', {'not_admin_error': True})
            else:
                # Неправильний пароль
                return render(request, 'admin_login.html', {'wrong_password': True, 'no_user': False, 'activation_error': False})

        except User.DoesNotExist:
            # Перевіряємо користувача за номером телефону
            try:
                # Шукаємо користувача в базі даних за номером телефону
                user_profile = UserProfile.objects.get(phone_number=normalized_login_identifier)

                if not user_profile.is_active:
                    return render(request, 'admin_login.html', {'activation_error': True, 'no_user': False, 'wrong_password': False})

                user = user_profile.user
                # Аутентифікуємо користувача
                user = authenticate(request, username=user.username, password=password)

                if user is not None:
                    if user.is_superuser:
                        # Успішний логін для адміна
                        login(request, user)
                        return HttpResponseRedirect('/home/')
                    else:
                        # Користувач не є адміном, відмова в авторизації
                        request.user = None
                        return render(request, 'admin_login.html', {'not_admin_error': True})
                else:
                    # Неправильний пароль
                    return render(request, 'admin_login.html', {'wrong_password': True, 'no_user': False, 'activation_error': False})

            except UserProfile.DoesNotExist:
                # Неіснуючий користувач ні за ім'ям користувача, ні за номером телефону
                return render(request, 'admin_login.html', {'no_user': True, 'wrong_password': False, 'activation_error': False})

    else:
        return render(request, 'admin_login.html', {'no_user': False, 'wrong_password': False})

def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '')
        
        # Отримання адреси електронної пошти з форми
        if email:
            try:
                # Відправлення листа за допомогою Django
                send_mail(
                    'FoodZero Recipes',
                    'INGREDIENTS for 1 portion Basic:\n• Beef TM Organic Meat.100 g\n• garlic ½ pc.\n• Bulgarian red pepper ½ pc.\n• chicken broth 1 st. l\n• soy sauce ¾ pc.\n• sugar brown ¼ tsp.\n• corn starch ½ tsp.\n• sesame oil 1 tsp.Mustard Sauce:\n• mustard Dijon ½ st. l\n• water 1 tbsp l\n• brown sugar ½ tsp.\n• Lemon juice 1 tsp.\nSTEP 1\nMix all the ingredients for mustard sauce. Put aside Beef is cut across the fibers. Slender meat strips mixed with marinade. Set aside for 20 minutes.\nSTEP 2\nHeat the oil in a saucepan on medium heat. Quickly fry the garlic. Add strips of red pepper. Stir until smooth, add chicken broth. Cook for about 5 minutes, add salt, put it in a saucepan. Add oil to the stew. Put beef with marinade in one layer without overlapping pieces of each other. Fry until the color changes. Turn to the other side. Add from a bowl of fried pepper and mustard sauce. Mix quickly and place on a serving dish.\nSTEP 3\nGarnish sesame seeds and green onions at will. Serve immediately after cooking.',
                    'foodzero.restaurant@gmail.com',
                    [email],
                    fail_silently=False,
                )
            except Exception as e:
                return JsonResponse({'error': str(e)})
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@csrf_exempt
def save_reservation(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            date = request.POST.get('date')
            time = request.POST.get('time')
            people = request.POST.get('people')
            table_name = request.POST.get('table')

            # Convert date to datetime object
            reservation_datetime = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

            # Calculate start and end times for the existing reservations within the 2-hour window
            existing_reservation_start_time = reservation_datetime - datetime.timedelta(hours=2)
            existing_reservation_end_time = reservation_datetime + datetime.timedelta(hours=2)

            # Check for existing reservations for both main and contact tables
            existing_reservations_main = Reservation_main.objects.filter(
                date=date,
                time__gte=existing_reservation_start_time.time(),
                time__lte=existing_reservation_end_time.time()
            ).values_list('table', flat=True)

            existing_reservations_contact = Reservation.objects.filter(
                date=date,
                time__gte=existing_reservation_start_time.time(),
                time__lte=existing_reservation_end_time.time()
            ).values_list('table', flat=True)

            existing_reservation_main_user = Reservation_main.objects.filter(
                user=request.user,
                date=date,
                time__gte=existing_reservation_start_time.time(),
                time__lte=existing_reservation_end_time.time()
            ).exists()

            # Combine reserved tables from both types of reservations
            existing_reservations = list(existing_reservations_main) + list(existing_reservations_contact)

            if existing_reservation_main_user:
                # Handle case where selected table is already reserved by the user
                return render(request, 'index.html', {'existing_reservation_user': True})

            # Створення словника з українськими та англійськими назвами столиків
            all_tables = {
                f'Столик №{i}': f'Table №{i}' for i in range(1, 7)
            }

            translated_existing_reservations = [all_tables.get(t, t) for t in existing_reservations]

            # Find available tables by subtracting reserved tables from all tables
            available_tables = list(set(all_tables.values()) - set(translated_existing_reservations))
            available_tables.sort()

            # Initialize dictionary for table translations
            table_translations = {
                'uk': {v: k for k, v in all_tables.items()},
                'en': {v: v for k, v in all_tables.items()}
            }

            # Get available tables in the selected language
            language_code = get_language()
            available_tables_in_selected_language = [table_translations[language_code].get(table, table) for table in available_tables]

            # Check if the table is in the available tables
            translated_table = all_tables.get(table_name, table_name)

            if translated_table not in available_tables:
                # Handle case where selected table is occupied
                return render(request, 'index.html', {
                    'table_is_not_available': True, 
                    'available_tables': available_tables_in_selected_language
                })

            occupied_tables = []
            for table_name in available_tables_in_selected_language:
                translated_table_name = all_tables.get(table_name, table_name)  # Translate table name if needed
                table_obj = get_object_or_404(Tables, table_name=translated_table_name)
                if table_obj.available == 0 or \
                    (table_obj.date == date and 
                        (table_obj.time >= (reservation_datetime - datetime.timedelta(hours=1)).time() and 
                        table_obj.time <= reservation_datetime.time())):
                    occupied_tables.append(table_name)

            if translated_table in occupied_tables:
                # Remove all occupied tables from the list of available tables
                for occupied_table in occupied_tables:
                    available_tables_in_selected_language.remove(occupied_table)

                return render(request, 'index.html', {
                    'table_is_not_available': True, 
                    'available_tables': available_tables_in_selected_language
                })

            # Convert date to display month name
            month_name = datetime.datetime.strptime(date, '%Y-%m-%d').strftime('%B')

            # Save the reservation
            reservation = Reservation_main(user=request.user, date=date, time=time, people=people, table=translated_table)
            reservation.save()

            # Mark table as unavailable
            table_obj.available = False
            table_obj.date = date
            table_obj.time = reservation_datetime.time()
            table_obj.save()

            # Sending email notification
            subject = 'Table Reservation Confirmation'
            message = f'{translated_table} has been successfully reserved for {people} at {time} on {month_name} {date}.\n Thank you for choosing us ❤️'
            from_email = 'foodzero.restaurant@gmail.com'
            to_email = [request.user.email]  # Assuming user's email is stored in User model

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            return render(request, 'index.html', {'success_reservation_modal': True})
        else:
            return HttpResponseRedirect('/sign_up/')
    else:
        return HttpResponseRedirect(reverse('home'))

@login_required
def logout_view(request):
    current_page = request.META.get('HTTP_REFERER')
    logout(request)
    return redirect(current_page)

@csrf_exempt
def reservation_from_contact(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        num_people = request.POST.get('people')
        table = request.POST.get('table')

        # Convert date to datetime object
        reservation_datetime = datetime.datetime.strptime(date + ' ' + time, '%Y-%m-%d %H:%M')

        # Calculate start and end times for the existing reservations within the 2-hour window
        existing_reservation_start_time = reservation_datetime - datetime.timedelta(hours=2)
        existing_reservation_end_time = reservation_datetime + datetime.timedelta(hours=2)

        # Check for existing reservations for both main and contact tables
        existing_reservations_main = Reservation_main.objects.filter(
            date=date,
            time__gte=existing_reservation_start_time.time(),
            time__lte=existing_reservation_end_time.time()
        ).values_list('table', flat=True)

        existing_reservations_contact = Reservation.objects.filter(
            date=date,
            time__gte=existing_reservation_start_time.time(),
            time__lte=existing_reservation_end_time.time()
        ).values_list('table', flat=True)

        # Combine reserved tables from both types of reservations
        existing_reservations = list(existing_reservations_main) + list(existing_reservations_contact)

        # Створення словника з українськими та англійськими назвами столиків
        all_tables = {
            f'Столик №{i}': f'Table №{i}' for i in range(1, 7)
        }

        translated_existing_reservations = [all_tables.get(t, t) for t in existing_reservations]

        # Find available tables by subtracting reserved tables from all tables
        available_tables = list(set(all_tables.values()) - set(translated_existing_reservations))
        available_tables.sort()

        # Initialize dictionary for table translations
        table_translations = {
            'uk': {v: k for k, v in all_tables.items()},
            'en': {v: v for k, v in all_tables.items()}
        }

        # Get available tables in the selected language
        language_code = get_language()
        available_tables_in_selected_language = [table_translations[language_code].get(table, table) for table in available_tables]

        # Check if the table is in the available tables
        translated_table = all_tables.get(table, table)
        if User.objects.filter(email=email).exists() or UserProfile.objects.filter(phone_number=phone).exists():
            # Handle case where email or phone number is already registered
            return render(request, 'contact.html', {'user_exist': True})
        
        if translated_table not in available_tables:
            # Handle case where selected table is occupied
            return render(request, 'index.html', {
                'table_is_not_available': True, 
                'available_tables': available_tables_in_selected_language
            })

        occupied_tables = []
        for table_name in available_tables_in_selected_language:
            translated_table_name = all_tables.get(table_name, table_name)  # Translate table name if needed
            table_obj = get_object_or_404(Tables, table_name=translated_table_name)
            if table_obj.available == 0 or \
                (table_obj.date == date and 
                    (table_obj.time >= (reservation_datetime - datetime.timedelta(hours=1)).time() and 
                    table_obj.time <= reservation_datetime.time())):
                occupied_tables.append(table_name)

        if translated_table in occupied_tables:
            # Remove all occupied tables from the list of available tables
            for occupied_table in occupied_tables:
                available_tables_in_selected_language.remove(occupied_table)

            return render(request, 'index.html', {
                'table_is_not_available': True, 
                'available_tables': available_tables_in_selected_language
            })
        else:
            # Create a new reservation
            reservation = Reservation.objects.create(
                first_name=first_name,
                last_name=last_name,
                email=email,
                phone=phone,
                date=date,
                time=time,
                num_people=num_people,
                table=table
            )
            # Convert date to display month name
            day, month, year = map(int, date.split('-'))
            month_name = calendar.month_name[month]

            # Sending email notification
            subject = 'Table Reservation Confirmation'
            if num_people == '1 Person' or num_people == '1 Людина':
                message = f'Your table has been successfully reserved for 1 person at {time} on {month_name} {year}, {day}.\n Thank you for choosing us ❤️'
            else:
                message = f'{translated_table} has been successfully reserved for {num_people} at {time} on {month_name} {date}.\n Thank you for choosing us ❤️'

            from_email = 'your_restaurant_email@example.com'
            to_email = [email]

            send_mail(subject, message, from_email, to_email, fail_silently=False)

            return render(request, 'contact.html', {'success_reservation_modal': True})

    return redirect(request.META.get('HTTP_REFERER'))

@login_required(login_url='/home/')
def profile_info(request, username):
    user = get_object_or_404(User, username=username)

    reservations = Reservation_main.objects.filter(user=user)
    
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    # Перевірка, чи поточний користувач відповідає користувачу у URL
    if request.user != user:
        # Якщо ні, перенаправте користувача на власний профіль
        return redirect('profile', username=request.user.username)

    return render(request, 'profile.html', {'reservations': reservations, 'user_profile': user_profile})

def crop_to_circle(image_path):
    # Відкриття завантаженої фотографії за допомогою Pillow
    with Image.open(image_path) as img:
        # Отримання мінімальної сторони фотографії для створення круглої форми
        size = min(img.width, img.height)
        
        # Обрізка фотографії до квадратної форми
        img_cropped = img.crop(((img.width - size) // 2, (img.height - size) // 2, (img.width + size) // 2, (img.height + size) // 2))
        
        # Створення маски для обрізання фотографії до круглої форми
        mask = Image.new('L', (size, size), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0, size, size), fill=255)
        
        # Обрізка фотографії за допомогою маски
        img_cropped.putalpha(mask)
        
        # Збереження обрізаної фотографії у форматі PNG (який підтримує альфа-канал)
        output = BytesIO()
        img_cropped.save(output, format='PNG')
        output.seek(0)
        
        return output

@login_required(login_url='/home/')
def profile_edit(request, username):
    user = get_object_or_404(User, username=username)

    # Перевірка, чи поточний користувач відповідає користувачу у URL
    if request.user != user:
        # Якщо ні, перенаправте користувача на власний профіль
        return redirect('profile_edit', username=request.user.username)
    
    try:
        user_profile = UserProfile.objects.get(user=user)
    except UserProfile.DoesNotExist:
        user_profile = None
    
    initial_data = {}
    if user_profile:
        # Заповнення полів початковими даними з профілю користувача
        initial_data['surname'] = user_profile.surname
        initial_data['name'] = user_profile.name
        initial_data['email'] = user.email
        initial_data['phone_number'] = user_profile.phone_number

    if request.method == 'POST':
        # Отримання даних з форми
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')

        # Перевірка, чи введені дані ідентичні зі збереженими в базі даних
        if (surname == user_profile.surname and 
            name == user_profile.name and 
            email == user.email and 
            phone_number == user_profile.phone_number):
            uploaded_photo = request.FILES.get('photo')

            # Перевірка, чи фото таке ж, як у БД
            if uploaded_photo == user_profile.photo:
                # Якщо дані і фото ідентичні, повернутися на сторінку профілю без змін
                return redirect('profile', username=request.user.username)

        # Перевірка, чи існує користувач із вказаною електронною адресою
        existing_user_email = User.objects.filter(email=email).exclude(username=user.username)
        if existing_user_email.exists():
            return render(request, 'edit_profile.html', {'user_exist': True, 'user_profile': user_profile, 'initial_data': initial_data, 'form': AvatarChangeForm(instance=user_profile, prefix='user_profile')})

        # Перевірка, чи існує користувач із вказаним номером телефону
        existing_user_phone = UserProfile.objects.filter(phone_number=phone_number).exclude(user=user)
        if existing_user_phone.exists():
            return render(request, 'edit_profile.html', {'user_exist': True, 'user_profile': user_profile, 'initial_data': initial_data, 'form': AvatarChangeForm(instance=user_profile, prefix='user_profile')})
        
        # Обробка завантаженого зображення та збереження обрізаного зображення
        if request.FILES.get('photo'):
            cropped_image = crop_to_circle(request.FILES['photo'])
            user_profile.photo.save(request.FILES['photo'].name, cropped_image)

        # Оновлення об'єкту профілю користувача з новими значеннями
        if user_profile or user:
            user_profile.surname = surname
            user_profile.name = name
            user_profile.phone_number = phone_number
            user_profile.save()
            user.first_name = surname
            user.last_name = name
            user.email = email
            user.username = email
            user.save()

            # Перевірка, чи змінюється пошта
            if email != request.user.email:
                return redirect('profile', username=user.username)
        # Перенаправлення на сторінку профілю
        return redirect('profile', username=request.user.username)
    
    return render(request, 'edit_profile.html', {'user_profile': user_profile, 'initial_data': initial_data, 'form': AvatarChangeForm(instance=user_profile, prefix='user_profile')})

def delete_reservation(request, reservation_id):
    reservation = get_object_or_404(Reservation_main, id=reservation_id, user=request.user)
    reservation.delete()

    # Отримати ім'я користувача з поточного запиту
    username = request.user.username

    # Перенаправлення на сторінку профілю конкретного користувача
    return redirect(reverse('profile', args=[username]))

@login_required
def change_avatar(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    username = request.user.username
    if request.method == 'POST':
        form = AvatarChangeForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect(reverse('profile_edit', args=[username]))

    return render(request, 'edit_profile.html', {'form': AvatarChangeForm(instance=user_profile, prefix='user_profile')})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user = User.objects.filter(email=email).first()
            if user:
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_link = f"http://{request.get_host()}/reset_password_confirm/{uid}/{token}/"
                send_mail(
                    'Reset Your Password',
                    f'Click the following link to reset your password: {reset_link}',
                    'from@example.com',
                    [email],
                    fail_silently=False,
                )
                return render(request, 'password-recover.html', {'email_sent': True})
            else:
                return render(request, 'reset_password.html', {'no_user': True})
    else:
        form = PasswordResetForm()
    return render(request, 'password-recover.html', {'form': form})

UserModel = get_user_model()
def reset_password_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = UserModel._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, UserModel.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            # Отримуємо дані з власних полів паролю
            new_password1 = request.POST.get('password')
            new_password2 = request.POST.get('confirm_password')
            # Перевіряємо, чи введені паролі співпадають
            if new_password1 == new_password2 and not request.user.is_authenticated:
                # Змінюємо пароль користувача тільки якщо вони співпадають
                user.set_password(new_password1)
                user.save()
                return render(request, 'login.html', {'password_changed': True})
            else:
                # Змінюємо пароль користувача тільки якщо вони співпадають
                user.set_password(new_password1)
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')

                return redirect('profile', username=request.user.username)
        else:
            form = SetPasswordForm(user)
        return render(request, 'reset_password_confirm.html', {'form': form, 'uidb64': uidb64, 'token': token})
    else:
        return render(request, 'password-recover.html', {'link_invalid': True})

@login_required(login_url='/home/')
def change_password(request):
    user=request.user
    if request.method == 'POST':
        if user is not None:
            old_password = request.POST.get('old_password')
            new_password = request.POST.get('password')
            new_password_repeat = request.POST.get('confirm_password')
            if check_password(old_password, request.user.password):
                if new_password == new_password_repeat:
                    request.user.set_password(new_password)
                    request.user.save()
                    # Keep the user logged in after password change
                    update_session_auth_hash(request, request.user)
                    return render(request, 'profile.html', {'password_changed': True})
                else:
                    return HttpResponse('New passwords do not match!')
            else:
               return render(request, 'change_password.html', {'wrond_old_password': True})
        else:
            # If form is not valid, re-render the change password form with errors
            return render(request, 'change_password.html')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'change_password.html')

@login_required
def delete_account(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        if password and confirm_password:
            if password == confirm_password:
                # перевірка введеного паролю користувача з поточним паролем
                if request.user.check_password(password):
                    # Видалення облікового запису користувача
                    request.user.delete()
                    messages.success(request, 'Your account has been successfully deleted.')
                    return redirect('home')  # перенаправлення на головну сторінку після видалення облікового запису
                else:
                    return render(request, 'profile.html', {'wrong_password': True})
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'Please fill in all fields.')
    else:
        messages.error(request, 'Invalid request method.')
    return render(request, 'profile.html', {'wrong_password': True})

@user_passes_test(lambda u: u.is_superuser, login_url='/home/')
@login_required
def table_status(request):
    tables = Tables.objects.all()  # Отримуємо всі столики з бази даних
    context = {'tables': tables}
    return render(request, 'tables.html', context)

def update_table_status(request, table_id):
    if request.method == 'POST':
        table = get_object_or_404(Tables, id=table_id)
        
        # Set time to Kyiv time zone
        kyiv_tz = tz('Europe/Kiev')
        kyiv_time = timezone.localtime(timezone.now(), kyiv_tz).time()
        
        # Check if the table is becoming unavailable
        if table.available == 0:
            # Delete reservations associated with this table
            Reservation_main.objects.filter(table=table.table_name).delete()
            table.available = 1
        else:
            table.available = 0
        
        table.date = timezone.now().date()  # Update date
        table.time = kyiv_time  # Update time to Kyiv time
        table.save()
        return redirect('tables')
    else:
        return redirect('tables')

def meal_list(request):
    meals = Meal.objects.all()
    for meal in meals:
        avg_rating = meal.review_set.aggregate(avg_rating=Avg('rating'))['avg_rating']
        if avg_rating is not None:  # Перевіряємо, чи є середній рейтинг не None
            meal.avg_rating = str(avg_rating).replace(',', '.')  # Якщо так, замінюємо кому на крапку
        else:
            meal.avg_rating = None  # Якщо середній рейтинг None, зберігаємо його як None

    # Додаємо параметр preorder до контексту, якщо метод запиту POST
    context = {'meals': meals}
    if request.method == 'POST':
        context['preorder'] = True

    return render(request, 'portfolio.html', context)

@login_required
def save_reservation_meals(request):
    if request.method == 'POST':
        meal_ids = request.POST.get('meal_ids', '').split(',')
        
        # Отримання бронювання користувача
        user_reservations = Reservation_main.objects.filter(user=request.user)
        
        # Перевірка, чи є бронювання користувача
        if user_reservations.exists():
            # Взяття першого бронювання для отримання його ідентифікатора
            reservation_id = user_reservations.first().id

            for meal_id in meal_ids:
                meal = Meal.objects.get(id=meal_id)
                ReservationMeal.objects.create(
                    reservation_id=reservation_id,
                    meal=meal,
                    meal_name=meal.name,
                    date=user_reservations.first().date,
                    time=user_reservations.first().time,
                    people=user_reservations.first().people,
                    table=user_reservations.first().table
                )

            return redirect('portfolio')
        else:
            # Якщо бронювання користувача не існує, повернути помилку або виконати потрібні дії
            return render(request, 'portfolio.html', {'error': 'User has no reservation'})

    return render(request, 'portfolio.html', {'error': 'Invalid request method'})

def save_review(request):
    if request.method == 'POST':
        meal_id = request.POST.get('meal_id')
        rating = int(request.POST.get('rating'))
        meal = Meal.objects.get(pk=meal_id)
        # Перевірте, чи користувач вже залишив відгук для цього обіду
        existing_review = Review.objects.filter(meal=meal, user=request.user).first()
        if existing_review:
            # Якщо відгук вже існує, оновіть його рейтинг
            existing_review.rating = rating
            existing_review.save()
        else:
            # Якщо відгуку ще не існує, створіть новий відгук
            review = Review.objects.create(meal=meal, user=request.user, rating=rating)
            review.save()
        return redirect('portfolio')
    else:
        return redirect('portfolio')

def switch_language(request, language_code):
    if check_for_language(language_code):
        activate(language_code)
    else:
        language_code = settings.LANGUAGE_CODE
        activate(language_code)
        
    redirect_to = request.GET.get('next', 'home')  # Отримуємо наступну сторінку з параметру 'next' у запиті GET
    response = redirect(redirect_to)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language_code)
    return response

def index(request):
    output = _('StatusMsg')
    return HttpResponse(output)

update_thread = Thread(target=schedule_table_update)
update_thread.daemon = True
update_thread.start()
