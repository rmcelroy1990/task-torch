from django.shortcuts import render, redirect
from django.shortcuts import get_object_or_404
from django.contrib.auth import login
from .models import TaskPost, Comment
# from .models import Tasks
from .forms import TaskPostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.http import HttpResponse
from django.views.generic.edit import CreateView

def home(request):
    return render(request, 'home.html')


def task_detail(request, task_id):
    task = get_object_or_404(TaskPost, id=task_id)
    comments = Comment.objects.filter(task=task)
    
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                comment = form.save(commit=False)
                comment.task = task
                comment.user = request.user
                comment.save()
                return redirect('task_detail', task_id=task.id)
        else:
            return redirect('login')
    else:
        form = CommentForm()

    return render(request, 'tasks/task_detail.html', {
        'task': task, 
        'comments': comments, 
        'comment_form': form
    })

@login_required
def create_task(request):
    if request.method == 'POST':
        form = TaskPostForm(request.POST)
        if form.is_valid():
            task = form.save(commit=False)
            task.user = request.user
            task.save()
            return redirect('all_tasks')
    else:
        form = TaskPostForm()
    messages.success(request, 'Task created successfully!')

    return render(request, 'tasks/create_task.html', {'form': form})

@login_required
def edit_task(request, task_id):
    task = get_object_or_404(TaskPost, id=task_id)
    if task.user != request.user:
            return redirect('task_detail', task_id=task.id)
    if request.method == 'POST':
        form = TaskPostForm(request.POST, instance=task)
        if form.is_valid():
            form.save()
            return redirect('task_detail', task_id=task.id)
    else:
        form = TaskPostForm(instance=task)
    return render(request, 'tasks/task_form.html', {'form': form})

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(TaskPost, id=task_id)
    if task.user != request.user:
        return redirect('task_detail', task_id=task.id)
    if request.method == 'POST':
        task.delete()
        
        return redirect('all_tasks')
    return render(request, 'tasks/task_confirm_delete.html', {'task': task})

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
        messages.success(request, 'Offer submitted!')
        messages.error(request, 'There was an error. Please check the form and try again.')
    return render(request, 'tasks/comment_form.html', {'form': form, 'task': task})

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('welcome')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def welcome(request):
    return render(request, 'registration/welcome.html')

def all_tasks(request):
    tasks = TaskPost.objects.all()
    return render(request, 'all_tasks.html', {'tasks': tasks})

class TaskCreate(CreateView):
    model = TaskPost
    fields = '__all__'

# class Task:
#     def __init__(self, title, description, budget, location, date, user, created):
#     self.title = title
#     self.description = description
#     self.budget = budget
#     self.location = location
#     self.date = date
#     self.user = user
#     self.created = created

# tasks = [
#     Task('Task 1', 'Description 1', 100, 'Location 1', '2023-10-01', 'User 1', '2023-09-01'),
#     Task('Task 2', 'Description 2', 200, 'Location 2', '2023-10-02', 'User 2', '2023-09-02'),
#     Task('Task 3', 'Description 3', 300, 'Location 3', '2023-10-03', 'User 3', '2023-09-03'),
# ]