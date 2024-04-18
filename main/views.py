from django.contrib.auth.models import User, Group
from django.shortcuts import render, redirect
from .forms import RegisterForm, PostForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth import login, logout
from .models import Post


@login_required(login_url='/login')
def home(request):
    posts = Post.objects.all().order_by('-created_at')
    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        user_id = request.POST.get('user-id')

        if post_id:
            post = Post.objects.get(id=post_id)

            if post and (post.author == request.user or request.user.has_perm('main.delete_post')):
                post.delete()
        elif user_id:
            user = User.objects.filter(id=user_id).first()

            if user and request.user.is_staff:

                try:
                    group = Group.objects.get(name='default')
                    group.user_set.remove(user)
                except:
                    pass

                try:
                    group = Group.objects.get(name='mod')
                    group.user_set.remove(user)
                except:
                    pass

    context = {'posts': posts}
    return render(request, 'main/home.html', context)


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()

            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'registration/sign_up.html', {'form': form})


def logout1(request):
    logout(request)
    return redirect('login')


@login_required(login_url='/login')
def my_post(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    context = {'posts': posts}
    return render(request, 'main/home.html', context)


@permission_required('main.add_post', login_url='/login', raise_exception=True)
@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')

    form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})