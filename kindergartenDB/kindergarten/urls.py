from django.urls import path

from . import views

urlpatterns = [
    path('', views.index),
    path('kindergartens/', views.kindergarten_list),
    path('kindergarten/<int:kindergarten_id>', views.kindergarten_view),
    path('kindergarten/add', views.add_kindergarten),
    path('kindergarten/<int:kindergarten_id>/delete', views.delete_kindergarten),

]
