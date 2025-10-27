from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),

    # Perfil
    path('profile_list/', views.profile_list, name="profile_list"),
    path('profile/<int:pk>/', views.profile, name="profile"),
    path('profile/follow/<int:pk>/', views.follow, name='follow'),
    path('profile/unfollow/<int:pk>/', views.unfollow, name='unfollow'),
    
    path('profile/follows/<int:pk>/', views.follows, name='follows'),
    path('profile/followers/<int:pk>/', views.followers, name='followers'),

    # Pins
    path('pin/like/<int:pk>/', views.pin_like, name="pin_like"),
    path('pin/delete/<int:pk>/', views.delete_pin, name="delete_pin"),
    path('pin/edit/<int:pk>/', views.edit_pin, name="edit_pin"),

    # Autenticação
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('update_user/', views.update_user, name='update_user'),
]
