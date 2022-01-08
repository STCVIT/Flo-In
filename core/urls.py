from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.views.static import serve
from django.conf import settings
from django.conf.urls import url

urlpatterns = [
    # Admin Panel
    path("admin/", admin.site.urls),
    # Authentication
    path("loginuser/", views.loginuser, name="loginuser"),
    path("logout/", views.logoutuser, name="logoutuser"),
    # API
    path("api/", include("api.urls")),
    # Dashboard and user data
    path("", views.home, name="home"),
    path("userdata/", views.savedata, name="userdata"),
    path("profile/", views.profile, name="profile"),
    path("delete/<int:pk>/", views.delete_user_data, name="delete_user_data"),
    # Face Recognition routes
    path("facedata/", views.savefacedata, name="savefacedata"),
    path("checkfacedata/", views.checkfacedata, name="checkfacedata"),
    path("facedata/setpattern/", views.setpattern, name="setpattern"),
    path("checkfacedatapost/", views.checkfacedata, name="checkfacedata"),
    # Password Reset
    path(
        "password_reset/",
        auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
        name="reset_password",
    ),
    path(
        "password_reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="password_reset_done.html"
        ),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="password_reset_confirm.html"
        ),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="password_reset_complete.html"
        ),
        name="password_reset_complete",
    ),
    url(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    url(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
