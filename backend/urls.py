"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import (UserCreateAPIView, UserLoginAPIView,
                       getApp, createApp, deleteApp, isDoctor, get_doctors, change_doctor_status, updateApp, bookApp,
                       get_my_appointments, ChangeBook, getHistory, createHistory)

urlpatterns = [
    path('admin/', admin.site.urls),

    path('login/', UserLoginAPIView.as_view()),
    path('signup/', UserCreateAPIView.as_view()),
    path('get_app/', getApp.as_view()),
    path("create_app/", createApp.as_view()),
    path("del_app/", deleteApp.as_view()),
    path("is_doctor/", isDoctor.as_view()),
    path("get_doctors/", get_doctors.as_view()),
    path("change_doctor_status/", change_doctor_status.as_view()),
    path('update_app/', updateApp.as_view()),
    path('book_app/', bookApp.as_view()),
    path('get_my_app/', get_my_appointments.as_view()),
    path('del_app/', deleteApp.as_view()),
    path('change_book/', ChangeBook.as_view()),
    path('get_history/', getHistory.as_view()),
    path('create_history/', createHistory.as_view()),


]
