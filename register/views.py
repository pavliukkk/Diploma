from django.shortcuts import render


def save_user_data(request):
    if request.method == 'POST':
        surname = request.POST.get('surname')
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # Збереження даних у файлі
        with open('user_data.txt', 'a') as file:
            file.write(f'{surname}, {name}, {email}, {phone_number}, {password}, {confirm_password}\n')

        return render(request, 'success.html')  # Опрацьовано успішно, можна відобразити сторінку успіху
    else:
        return render(request, 'signup.html')  # Якщо це не POST-запит, повернути форму для заповнення
