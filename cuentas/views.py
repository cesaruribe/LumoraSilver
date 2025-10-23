from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroForm
from django.contrib.auth.decorators import login_required
from .forms import DireccionForm
from .models import Direccion

def registro(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            usuario = form.save()
            login(request, usuario)
            return redirect('cuentas:perfil')
    else:
        form = RegistroForm()
    return render(request, 'cuentas/registro.html', {'form': form})


@login_required
def perfil(request):
    return render(request, 'cuentas/perfil.html', {'usuario': request.user})



@login_required
def direcciones(request):
    lista = request.user.direcciones.all()
    return render(request, 'cuentas/direcciones.html', {'direcciones': lista})

@login_required
def direccion_nueva(request):
    form = DireccionForm(request.POST or None)
    if form.is_valid():
        direccion = form.save(commit=False)
        direccion.usuario = request.user
        direccion.save()
        return redirect('cuentas:direcciones')
    return render(request, 'cuentas/direcciones_form.html', {'form': form})