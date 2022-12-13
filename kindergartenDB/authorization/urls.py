from django.urls import path

from . import views

urlpatterns = [
    path('signup/', views.user_signup),
    path('logout/', views.user_logout),
    path('login/', views.user_login),
    path('profile/<int:user_id>/', views.profile),
    path('profile/', views.profile),

]
