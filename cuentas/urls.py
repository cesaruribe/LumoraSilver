from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

# Nombre de la app para namespaces
app_name = 'cuentas' 

urlpatterns = [
    # --- Autenticación básica ---
    path('login/', auth_views.LoginView.as_view(template_name='cuentas/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('registro/', views.registro, name='registro'),
    path('activar/<uidb64>/<token>/', views.activar_cuenta, name='activar'),
    
    # --- Perfil y Cuenta ---
    path('perfil/', views.perfil, name='perfil'),
    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),


    # --- Gestión de Direcciones ---
    path('direcciones/agregar/', views.agregar_direccion, name='agregar_direccion'), 
    path('direcciones/editar/<int:pk>/', views.editar_direccion, name='editar_direccion'),
    path('direcciones/eliminar/<int:pk>/', views.eliminar_direccion, name='eliminar_direccion'),
    path('direcciones/predeterminada/<int:pk>/', views.marcar_predeterminada, name='marcar_predeterminada'),
    path('ajax/municipios/', views.ajax_cargar_municipios, name='ajax_municipios'),

    # --- Cambio de contraseña (Usuario Logueado) ---
    path('password_change/', auth_views.PasswordChangeView.as_view(
        template_name='cuentas/password_change.html',
        success_url=reverse_lazy('cuentas:password_change_done')
    ), name='password_change'),
    
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(
        template_name='cuentas/password_change_done.html'
    ), name='password_change_done'),

    # --- Recuperación de contraseña (Contraseña Olvidada) ---
    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name='cuentas/password_reset.html',
        email_template_name='cuentas/password_reset_email.html',
        success_url=reverse_lazy('cuentas:password_reset_done')
    ), name='password_reset'),
    
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='cuentas/password_reset_done.html'
    ), name='password_reset_done'),
    
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='cuentas/password_reset_confirm.html',
        success_url=reverse_lazy('cuentas:password_reset_complete')
    ), name='password_reset_confirm'),
    
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='cuentas/password_reset_complete.html'
    ), name='password_reset_complete'),
]