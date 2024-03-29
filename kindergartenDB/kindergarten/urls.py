from django.urls import path

from . import views

urlpatterns = [
    path('', views.user.index),
    path('about/', views.user.about),

    path('child/add/', views.user.parent_add_child),
    path('child/<int:child_id>/delete/', views.user.parent_delete_child),
    path('child/<int:child_id>/payments/', views.user.payments_by_child_list),
    path('payment/<int:payment_id>/pay/', views.user.child_pay),

    path('child/<int:child_id>/', views.staff.child_view),
    path('child/<int:child_id>/add_payment/', views.staff.child_add_payment),
    path('child/<int:child_id>/edit_payment/month/<int:month_id>/group', views.staff.child_edit_payment_group),
    path('child/<int:child_id>/edit_payment/month/<int:month_id>/kindergarten', views.staff.child_edit_payment_kindergarten),

    path('kindergartens/', views.user.kindergarten_list),

    path('kindergarten/<int:kindergarten_id>/', views.staff.kindergarten_view),
    path('kindergarten/<int:kindergarten_id>/payments/', views.staff.kindergarten_list_payments),
    path('kindergarten/<int:kindergarten_id>/payments/month/<int:month_id>', views.staff.payments_by_kindergarten_month),
    path('kindergarten/add/', views.staff.add_kindergarten),
    path('kindergarten/<int:kindergarten_id>/delete/', views.staff.delete_kindergarten),

    path('groups/', views.user.group_list),

    path('group/add/', views.staff.add_group),
    path('group/<int:group_id>/', views.staff.group_view),
    path('group/<int:group_id>/delete/', views.staff.delete_group),
    path('group/<int:group_id>/children/', views.staff.children_by_group_list),
    path('group/<int:group_id>/children/month/<int:month_id>/', views.staff.children_by_group_by_month_list),
    path('group/<int:group_id>/children/add_payment/', views.staff.child_add_payment_multiple),
    path('group/<int:group_id>/children/show_payments/', views.staff.child_show_payment_multiple),
    path('group/<int:group_id>/children/<int:child_id>/delete/', views.staff.delete_child),

    path('months/', views.staff.month_list),
    path('month/add/', views.staff.add_month),
    path('month/<int:month_id>/', views.staff.month_view),
    path('month/<int:month_id>/delete/', views.staff.delete_month),

]
