import markdown
from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.


def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})


def new_post(request):
    if request.method == "POST":
        form = PostForm(request.POST, files=request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, "new_post.html", {'form': form})


def delete_post(request, slug):
    post = Post.objects.get(slug=slug)
    if request.method == "POST":
        post.delete()
        return redirect("home")
    return render(request, 'delete.html', {'post': post})


def post_details(request, slug):
    post = Post.objects.get(slug=slug)
    md_parser = markdown.Markdown(extensions=["fenced_code"])
    post.body = md_parser.convert(post.body)
    comments = Comment.objects.filter(post=post.id).order_by("-created_on")
    new_comment = None
    if request.method == "POST":
        form = CommentForm(request.POST or None)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return render(request, "add_comment.html")
    else:
        form = CommentForm()
    return render(request, "add_comment.html", {'form': form, 'post': post, 'comments': comments, 'new_comment': new_comment})


def contact(request):
    contact_methods = ContactMethod.objects.order_by("-created_on")
    return render(request, "contact.html", {'contact_methods': contact_methods})
