from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.template import loader
from .forms import AuthorForm, QuoteForm
from .models import Author, Quote
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .forms import UserRegistrationForm, UserLoginForm
from django.core.paginator import Paginator


def index(request):
    # Отримуємо всіх авторів з бази даних
    authors_list = Author.objects.all()
    paginator = Paginator(authors_list, 5)  # Розбиваємо на сторінки, по 5 авторів на сторінку

    page_number = request.GET.get('page')  # Отримуємо номер поточної сторінки
    page_obj = paginator.get_page(page_number)  # Отримуємо об'єкт поточної сторінки

    context = {
        'page_obj': page_obj,
    }
    return render(request, 'main_app/index.html', context)




@login_required
def add_author(request):
    if request.method == 'POST':
        # Створюємо форму для додавання автора на основі POST-даних
        form = AuthorForm(request.POST)
        if form.is_valid():
            # Якщо форма є валідною, зберігаємо дані у базу даних
            form.save()
            # Перенаправляємо користувача на сторінку зі списком авторів або на іншу відповідну сторінку
            return redirect('index')  
    else:
        # Якщо запит не є POST, створюємо пусту форму для відображення на сторінці
        form = AuthorForm()
    # Відображаємо шаблон з формою для додавання автора
    return render(request, 'main_app/add_author.html', {'form': form})

@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = QuoteForm()
    return render(request, 'main_app/add_quote.html', {'form': form})


def signup(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request)
            #login(request, user)
            return redirect('index')  
    else:
        form = UserRegistrationForm()
    return render(request, 'main_app/signup.html', {'form': form})

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('index')  
    else:
        form = UserLoginForm()
    return render(request, 'main_app/login.html', {'form': form})




def author_detail(request, author_id):
    # Отримання автора за його ідентифікатором
    author = get_object_or_404(Author, pk=author_id)
    print(author)
    return render(request, 'main_app/author_detail.html', {'author': author})
