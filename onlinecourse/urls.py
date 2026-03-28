from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'onlinecourse'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:course_id>/', views.detail, name='detail'),
    path('<int:course_id>/enroll/', views.enroll, name='enroll'),
    path('<int:course_id>/submit/', views.submit, name='submit'),
    path('<int:course_id>/submission/<int:submission_id>/result/', views.show_exam_result, name='show_exam_result'),
    path('login/', auth_views.LoginView.as_view(template_name='onlinecourse/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/onlinecourse/'), name='logout'),
]