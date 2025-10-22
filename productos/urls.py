"""
URL configuration for joyeria project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views
from productos import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Manejo de Unidades
    path('unidades/new/', views.unidadesNew, name='unidadesnew'),
    path('unidades/show/', views.unidadesShow, name='unidadesshow'),
    path('unidades/edit/<int:id>/', views.unidadesEdit, name='unidadesedit'),
    path('unidades/update/<int:id>/', views.unidadesUpdate, name='unidadesupdate'),
    path('unidades/delete/<int:id>/', views.unidadesDestroy, name='unidadesdelete'),
    # Manejo de Categorias
    path('categorias/new/', views.categoriasNew, name='categoriasnew'),
    path('categorias/show/', views.categoriasShow, name='categoriasshow'),
    path('categorias/edit/<int:id>/', views.categoriasEdit, name='categoriasedit'),
    path('categorias/update/<int:id>/', views.categoriasUpdate, name='categoriasupdate'),
    path('categorias/delete/<int:id>/', views.categoriasDestroy, name='categoriasdelete'),
]

# Solo para servir archivos multimedia durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)