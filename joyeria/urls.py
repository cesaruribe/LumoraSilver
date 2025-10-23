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
from django.contrib.auth import views as auth_views
from django.urls import path, include
from core import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),  # Página principal y menú
    path('productos/', include(('productos.urls', 'productos'), namespace='productos')),
    path('carrito/', include(('carrito.urls', 'carrito'), namespace='carrito')),
    path('pedidos/', include(('pedidos.urls', 'pedidos'), namespace='pedidos')),

    # Autenticación
    path('cuentas/login/', auth_views.LoginView.as_view(
        template_name='cuentas/login.html',
        redirect_authenticated_user=True,
        next_page='cuentas:perfil'
    ), name='login'),
    path('cuentas/logout/', auth_views.LogoutView.as_view(next_page='inicio'), name='logout'),

    # App cuentas
    path('cuentas/', include(('cuentas.urls', 'cuentas'), namespace='cuentas')),
]

# Archivos multimedia en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
