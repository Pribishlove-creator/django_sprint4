from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Category, Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .forms import PostForm, CommentForm
from django.contrib import messages
from django.http import Http404
from django.db.models import Count
# Create your views here.


def index(request):
    template = 'blog/index.html'
    current_time = timezone.now()

    posts = Post.objects.filter(
        is_published=True,
        pub_date__lte=current_time,
        category__is_published=True
    ).annotate(comment_count=Count('comments')).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj}
    return render(request, template, context)


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if not post.is_published or not post.category.is_published:
        if request.user != post.author:
            raise Http404("Пост снят с публикации")

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    comments = Comment.objects.filter(post=post).order_by('created_at')
    template = 'blog/detail.html'
    context = {
        'post': post,
        'form': form,
        'comments': comments,
    }
    return render(request, template, context)


def category_posts(request, category_slug):
    template = 'blog/category.html'
    current_time = timezone.now()

    category = get_object_or_404(
        Category,
        slug=category_slug,
        is_published=True
    )

    posts = Post.objects.filter(
        category=category,
        is_published=True,
        pub_date__lte=current_time
    ).order_by('-pub_date')

    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'page_obj': page_obj
    }
    return render(request, template, context)


def profile(request, username):
    user = get_object_or_404(User, username=username)

    if request.user.is_authenticated and request.user == user:
        user_posts = Post.objects.filter(
            author=user
        ).annotate(comment_count=Count('comments')
        ).order_by('-pub_date')
    else:
        user_posts = Post.objects.filter(
            author=user, is_published=True, pub_date__lte=timezone.now()
        ).annotate(comment_count=Count('comments')
        ).order_by('-pub_date')
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'profile': user, 
        'page_obj': page_obj,
        'is_staff': request.user.is_authenticated and request.user == user,
    }
    return render(request, 'blog/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = UserChangeForm(instance=request.user)

    return render(request, 'blog/user.html', {'form': form})


@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blog:profile', username=request.user.username)
    else:
        form = PostForm()
    return render(request, 'blog/create.html', {'form': form})


@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', pk=post_id)

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post.id)
    else:
        form = PostForm(instance=post)

    context = {
        'form': form,
        'is_edit': True,
        'post': post,
    }
    return render(request, 'blog/create.html', context)


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('blog:post_detail', pk=post_id)
    else:
        form = CommentForm()
    return render(request, 'blog/comment.html', {'form': form, 'post': post})


@login_required
def edit_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id, author=request.user)
    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=post_id)
    else:
        form = CommentForm(instance=comment)
    return render(request, 'blog/comment.html',
    {
        'form': form,
        'post_id': post_id,
        'comment': comment
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)

    if request.user != post.author:
        return redirect('blog:post_detail', pk=post_id)

    if request.method == 'POST':
        post.delete()
        messages.success(request, "Публикация успешно удалена.")
        return redirect('blog:profile', username=request.user.username)

    return render(request, 'blog/create.html', {'post': post})


@login_required
def delete_comment(request, post_id, comment_id):
    comment = get_object_or_404(Comment, pk=comment_id)
    post = get_object_or_404(Post, pk=post_id)

    if request.user != comment.author:
        return redirect('blog:post_detail', pk=post_id)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, "Комментарий успешно удалён.")
        return redirect('blog:post_detail', pk=post_id)

    return render(request, 'blog/comment.html', {'post': post})
