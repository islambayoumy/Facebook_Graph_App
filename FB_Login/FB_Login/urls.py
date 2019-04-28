from django.urls import path
from main import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('deauth/', views.deauth, name='deauth')
]
