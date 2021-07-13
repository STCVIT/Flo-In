from django.contrib import admin
from django.urls import path, include
from accounts import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('logout/', views.logoutuser, name='logoutuser'),
    path('profile/', views.profile, name='profile'),
    path('setpattern/', views.setpattern, name='setpattern'),
    path('api/', include('api.urls')),
    # path('faceregister/', include('faceregister.urls')),
    path('userdata/',views.savedata, name='userdata'),
    path('facedata/',views.savefacedata, name='savefacedata'),
    path('checkfacedata/',views.checkfacedata, name='checkfacedata'),
    path('checkfacedatapost/',views.checkfacedata, name='checkfacedata'),

#Password Reset
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='password_reset.html'), name='reset_password'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name='password_reset_complete'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)