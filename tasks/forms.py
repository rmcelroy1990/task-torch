from django import forms
from .models import TaskPost
from .models import Comment

class TaskPostForm(forms.ModelForm):
    class Meta:
        model = TaskPost
        fields = ['title', 'description', 'budget', 'location', 'date_needed']
        widgets = {
            'date_needed': forms.DateInput(attrs={'type': 'date'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 4, '': 'Write your offer...'}),
        }