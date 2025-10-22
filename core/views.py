from django.shortcuts import render

# Vistas principales
def inicio(request):
    return render(request, 'core/inicio.html')

def menu(request):
    return render(request, 'core/menu.html')

