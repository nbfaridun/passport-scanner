from django.contrib import admin
from django.urls import path
from main import urls
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("",views.index,name='index'),
    path("main",views.content,name="main"),
    path("logout", views.logout_view, name='logout'),
    path("datas", views.datas_view, name="datas"),
    path("success", views.success_view, name="success"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
