from django.shortcuts import render, redirect
from .forms import UserRegistrationForm
from django.contrib.auth import login
from django.contrib import messages

def index(request):
    # Код для обработки запроса к главной странице
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)
            return redirect('profile')  # Убедитесь, что url 'profile' определен в urls.py
        else:
            messages.error(request, 'Ошибка регистрации: ' + str(form.errors))
            return render(request, 'main/register.html', {'form': form})
    else:
        form = UserRegistrationForm()
        return render(request, 'main/register.html', {'form': form})