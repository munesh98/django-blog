from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("",views.post_list, name="home"),
    path("post/list/",views.post_list, name="post-list"),
    path("post/<int:id>/",views.post_detail, name="post-detail"),
    path("post/<int:id>/like/",views.post_likes, name="post-likes"),
    path("post/create/",views.create_post, name="post-create"),
    path("post/<int:id>/edit/",views.post_edit, name="post-edit"),
    path("post/<int:id>/delete/",views.post_delete, name="post-delete"), 
    path("signup/",views.signup_view, name="sign-up"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("category/<int:id>", views.category_view, name="category-posts"),
    path("user/profile", views.profile_view, name="user-profile"),
    path("user/posts", views.my_posts, name="user-posts"),
    path("user/profile/edit", views.edit_profile, name="user-profile-edit"),
    path("user/admin", views.admin_Login, name="admin-login"),
    path("user/admin/dashboard", views.admin_dashboard, name="admin-dashboard"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
