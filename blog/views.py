from django.shortcuts import render ,redirect
from .models import Post, Comment, Category, Profile
from .forms import PostForm, SignUpForm, LoginForm, CommentForm, UserUpdateForm, profileUpdateForm, adminDashBoardForm
from django.contrib import messages                              
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.paginator import Paginator
from .decorators import admin_required


# Create your views here.
@login_required(login_url="login")
def create_post(request):
    formPost = PostForm()
    if request.method == "POST" :
        formPost = PostForm(request.POST,request.FILES)
        if formPost.is_valid():
            postData = formPost.save(commit=False)
            postData.author = request.user
            postData.save()
            messages.success(request, "Post created successfully!")
            return redirect("post-detail",id=postData.id)
    else :
        formPost = PostForm()
    
    context = {"form_post":formPost}
    return render(request,"blog/create_post.html",context)
    

def post_list(request):
    query = request.GET.get('q')

    if query:
        listOfPost = Post.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by("-created_at")
    else:
        listOfPost = Post.objects.order_by("-created_at")
    
    paginator = Paginator(listOfPost, 5)     # show 5 posts per page
    page_number = request.GET.get("page")  # ?page=2, ?page=3, etc.
    page_obj = paginator.get_page(page_number)

    context = {"page_obj":page_obj}
    return render(request,"blog/post_list.html",context) 
    
@login_required(login_url="login")
def post_detail(request,id):
    singlePost = Post.objects.get(id=id)
    comments = Comment.objects.filter(post=singlePost)
    if request.method == "POST" :
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            postCommentData = commentForm.save(commit=False)
            postCommentData.post = singlePost
            postCommentData.user = request.user
            postCommentData.save()
            return redirect("post-detail",id=singlePost.id)
    else :
        commentForm = CommentForm()
        
    context = {"postDetails" : singlePost,"comments":comments,"commentForm":commentForm}
    return render(request,"blog/post_detail.html",context)

@login_required(login_url="login")   
def post_edit(request, id):
    post = Post.objects.get(id=id)
    
    if request.user != post.author:
        messages.error(request, "You are not allowed to do that!")
        return redirect("post-detail", id=post.id)

    postData = PostForm(request.POST, request.FILES, instance=post)
    if request.method == "POST" :
        postData = PostForm(request.POST, instance=post)
        
        if postData.is_valid():
            postData.save()
            messages.success(request, "Post updated successfully!")
            return redirect("post-detail",id=post.id)
    else :
        postData = PostForm(instance=post)
    
    context = {"form":postData}
    return render(request,"blog/post_edit.html",context)

@login_required(login_url="login")   
def post_delete(request,id):
    post = Post.objects.get(id=id)
    
    if request.user != post.author:
        messages.error(request, "You are not allowed to do that!")
        return redirect("post-detail", id=post.id)
    
    context = {"post":post}
    if request.method == "POST" :
        post.delete()
        messages.success(request, "Post deleted successfully!")
        return redirect("post-list")
    else:
        return render(request,"blog/post_confirm_delete.html",context)

def signup_view(request):
    form = SignUpForm()
    
    if request.method == "POST" :
        form = SignUpForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data["username"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            confirm_password = form.cleaned_data["confirm_password"]
            
            if password != confirm_password :
                messages.error(request,"passwords are different")
            else:
                User.objects.create_user(username=username,\
                email=email,password=password)
                messages.success(request,"Account created successfully")
                return redirect("login")
    else:
        form = SignUpForm()
    
    context = {"form":form}
    return render(request,"blog/sign_up.html",context)

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, "Login Successful!")
                return redirect("home")
            else:
                messages.error(request, "Invalid username or password")
    else:
        form = LoginForm()

    context = {"form": form}
    return render(request, "blog/login.html", context)


def logout_view(request):
    logout(request)
    messages.success(request,"logged out successfully")
    return redirect("login")

@login_required(login_url="login")
def post_likes(request, id):
    postContent = Post.objects.get(id=id)

    if request.user in postContent.likes.all():
        postContent.likes.remove(request.user)
    else:
        postContent.likes.add(request.user)

    return redirect("post-detail", id=postContent.id)


@login_required(login_url="login")
def category_view(request, id):
    category = Category.objects.get(id=id)
    posts = Post.objects.filter(category_type=category)
    context = {"category": category, "posts": posts}
    return render(request, "blog/category_post.html", context)


@login_required(login_url="login")
def profile_view(request):
    user = request.user
    profile, created = Profile.objects.get_or_create(user=user)

    total_posts = Post.objects.filter(author=user).count()
    total_likes = sum(post.likes.count() for post in Post.objects.filter(author=user))

    context = {
        "user": user,
        "profile": profile,
        "total_posts": total_posts,
        "total_likes": total_likes,
    }
    return render(request, "blog/profile.html", context)

def my_posts(request):
    postData = Post.objects.filter(author = request.user)
    context = {"posts":postData}
    return render(request,"blog/my_post.html",context)
    
def edit_profile(request):
    if request.method == "POST" :
        user_form = UserUpdateForm(request.POST,instance=request.user)
        profile_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        
        if user_form.is_valid() and profile_form.is_valid() :
            user_form.save()
            profile_form.save()
            return redirect("user-profile")

    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = profileUpdateForm(instance=request.user.profile)
    
    context = {"user_form":user_form,"profile_form":profile_form}
    return render(request,"blog/edit_profile.html",context)


@admin_required
def admin_dashboard(request):
    total_users = User.objects.count()
    total_posts = Post.objects.count()
    total_categories = Category.objects.count()
    total_comments = Comment.objects.count()
    recent_posts = Post.objects.order_by("-created_at")[:5]

    context = {
        "total_users": total_users,
        "total_posts": total_posts,
        "total_categories": total_categories,
        "total_comments": total_comments,
        "posts": recent_posts,
    }

    return render(request, "blog/admin_dashboard.html", context)

    

def admin_Login(request):
    if not request.user.is_staff:
        messages.warning(request, "You don't have permission to access the admin dashboard.")
        return redirect("home")  # redirect normal users

    if request.method == "POST":
        adminForm = adminDashBoardForm(request.POST)

        if adminForm.is_valid():
            messages.success(request, "Successfully logged in as admin.")
            return redirect("admin-home")  
    else:
        adminForm = adminDashBoardForm()

    context = {"adminForm": adminForm}
    return render(request, "blog/admin_login.html", context)
