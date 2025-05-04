from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('tasks/', views.all_tasks, name='all_tasks'),
    path('tasks/new/', views.create_task, name='create_task'),
    path('tasks/<int:task_id>/', views.task_detail, name='task_detail'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/comment/', views.add_comment, name='add_comment'),
    path('signup/', views.signup, name='signup'),
    path('welcome/', views.welcome, name='welcome'),
   ]