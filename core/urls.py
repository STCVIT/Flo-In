from django.contrib import admin
from django.urls import path, include
from accounts import views
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
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)