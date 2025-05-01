from django.shortcuts import render, redirect
from .models import TaskPost, Comment
# from .forms import TaskPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

def home(request):
    return render(request, 'base.html')

def task_list(request):
    tasks = TaskPost.objects.all()
    return render(request, 'task_list.html', {'tasks': tasks})

def task_detail(request, task_id):
    task = TaskPost.objects.get(id=task_id)
    comments = Comment.objects.filter(task=task)
    return render(request, 'task_detail.html', {'task': task, 'comments': comments})

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskPostForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('task_list')
    else:
        form = TaskPostForm()
    return render(request, 'tasktorch_app/task_form', {'form': form})

@login_required
def edit_task(request, task_id):
    task = TaskPost.objects.get(id=task_id)
    if task.posted_by != request.user:
            return redirect('task_detail')
    if request.metod == 'POST':
        form = TaskPostForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskPostForm(instance=task)
    return render(request, 'tasktorch_app/task_form', {'form': form})

@login_required
def delete_task(request, task_id):
    task = TaskPost.objects.get(id=task_id)
    if request.method == 'POST':
        task.delete()
        return redirect('task_list')
    return render(request, 'tasktorch_app/task_confirm_delete.html', {'task': task})

@login_required
def add_comment(request, task_id):
    task = TaskPost.objects.get(id=task_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.task = task
            comment.user = request.user
            comment.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = CommentForm()
    return render(request, 'tasktorch_app/comment_form.html', {'form': form, 'task': task})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})