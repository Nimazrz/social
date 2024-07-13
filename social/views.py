from django.contrib.postgres.search import TrigramSimilarity
from django.core.paginator import Paginator
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.views.generic import View
from .models import *
from .forms import *
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from taggit.models import Tag
from django.db.models import Count, Q


# Create your views here.
class LoginView(View):
    template_name = 'registration/login.html'

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('blog:index')
        return render(request, self.template_name, {'form': form})


def profile(request):
    return HttpResponse('you logged in')


def log_out(request):
    logout(request)
    return HttpResponse('you logged out')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html', {'user': user})
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def edit_user(request):
    if request.method == 'POST':
        user_form = UserEditForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
    else:
        user_form = UserEditForm(instance=request.user)
    context = {
        'user_form': user_form,
    }
    return render(request, 'registration/edit_user.html', context)


def ticket(request):
    send = False
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # message = f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}"
            send_mail(cd['subject'],
                      f"{cd['name']}\n{cd['email']}\n{cd['phone']}\n\n{cd['message']}",
                      'Nimaaa8413@gmail.com',
                      ['Nimaa1030@gmail.com'],
                      fail_silently=False, )
            send = True
    else:
        form = TicketForm()
    return render(request, 'forms/ticket.html', {'form': form, 'send': send})


def post_list(request, tag_slug=None):
    posts = Post.objects.all()
    # tags
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        posts = posts.filter(tags__in=[tag])

    # paginations
    paginator = Paginator(posts, 4) #
    page_number = request.GET.get('page',1)
    posts = paginator.page(page_number)

    context = {
        'posts': posts,
        'tag': tag,
    }

    return render(request, 'social/list.html', context)


@login_required
def craete_post(request):
    if request.method == 'POST':
        form = CraetePostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            form.save_m2m()
            return redirect('social:profile')
    else:
        form = CraetePostForm()
    return render(request, 'forms/craete_post.html', {'form': form})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_post = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_post = similar_post.annotate(same_tags=Count('tags')).order_by('-same_tags', 'created')[:2]
    #comments
    comments = post.comments.all()
    form = CommentForm()

    context = {
        'post': post,
        'similar_post': similar_post,
        'comments': comments,
        'form': form,
    }
    return render(request, "social/detail.html", context)


def search(request):
    query = None
    results = []
    if 'query' in request.GET:
        form = SearchForm(data=request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            print(query)
            result1 = Post.objects.filter(description__icontains=query)
            result2 = Post.objects.filter(tags__name__icontains=query)  # this is for many to many fields
            results = (result1 | result2)

            print(results)
            #bug in here

    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'forms/search.html', context)


def post_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comment = None
    form = CommentForm(data=request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.post = post
        comment.writer = request.user
        comment.save()
    context = {
        'post': post,
        'form': form,
        'comment': comment
    }
    return render(request, "forms/comment.html", context)
