from django.urls import path, include
from .views import ImageAPIView, LogoutAndBlacklistRefreshTokenForUserView
from . import views

urlpatterns = [
    # Face Recognition routes
    path("id/<id>/", ImageAPIView.as_view()),
    path("upload/", ImageAPIView.as_view()),
    # Authentication
    path("authenticate/", include("djoser.urls")),
    path("authenticate/", include("djoser.urls.jwt")),
    path("logout/", views.LogoutAndBlacklistRefreshTokenForUserView, name="blacklist"),
    # Stored Passwords CRUD
    path("data-detail/<path:url>/", views.dataDetail, name="data-Detail"),
    path("data-create/", views.dataCreate, name="data-Create"),
    path("data-update/<path:url>/", views.dataUpdate, name="data-update"),
    path("data-delete/<path:url>/", views.dataDelete, name="data-delete"),
    path("data-list/", views.dataList, name="data-list"),
    path("checkpattern/", views.checkPattern, name="checkpattern"),
]
