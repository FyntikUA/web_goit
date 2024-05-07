from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
]