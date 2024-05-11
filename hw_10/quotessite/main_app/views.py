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

    # Розбиваємо на сторінки, по 5 авторів на сторінку
    paginator = Paginator(authors_list, 5)

    # Отримуємо номер поточної сторінки
    page_number = request.GET.get('page')

    # Отримуємо об'єкт поточної сторінки
    page_obj = paginator.get_page(page_number)

    # Передаємо дані у контекст шаблону
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







def author_detail(request, author_id):
    # Отримання автора за його ідентифікатором
    author = get_object_or_404(Author, pk=author_id)
    print(author)
    return render(request, 'main_app/author_detail.html', {'author': author})
