from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasktorch_app/', views.task_list, name='task_list'),
    path('tasktorch_app/<int:pk>/', views.task_detail, name='task_detail'),
    path('tasktorch_app/new/', views.create_task, name='create_task'),
    path('tasktorch_app/<int:pk>/edit/', views.edit_task, name='edit_task'),
    path('tasktorch_app/<int:pk>/delete/', views.delete_task, name='delete_task'),
    path('tasktorch_app/<int:pk>/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.signup, name='signup'),
   ]