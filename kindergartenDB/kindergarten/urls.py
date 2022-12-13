from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('about/', views.about),

    path('kindergartens/', views.kindergarten_list),
    path('kindergarten/<int:kindergarten_id>', views.kindergarten_view),
    path('kindergarten/add', views.add_kindergarten),
    path('kindergarten/<int:kindergarten_id>/delete', views.delete_kindergarten),

    path('groups/', views.group_list),
    path('group/<int:group_id>', views.group_view),
    path('group/add', views.add_group),
    path('group/<int:group_id>/delete', views.delete_group),
]
