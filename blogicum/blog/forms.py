# forms.py
from django import forms
from .models import Post
from .models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'text', 'image', 'pub_date', 'category', 'location', 'is_published']
        widgets = {
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'title': 'Заголовок',
            'text': 'Текст',
            'image': 'Изображение',
            'pub_date': 'Дата и время публикации',
            'category': 'Категория',
            'location': 'Местоположение',
            'is_published': 'Опубликовать',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Напишите ваш комментарий...'}),
        }
        labels = {
            'text': ''
        }

