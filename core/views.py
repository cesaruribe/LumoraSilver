from django.shortcuts import render, get_object_or_404,redirect
from django.db import IntegrityError
from productos.models import UnidadMedida, Categoria, Producto
from productos.forms  import UnidadMedidaForm
# Create your views here.
def inicio(request):
    return render(request, 'core/inicio.html')
def menu(request):
    return render(request, 'core/menu.html')

#  ****************************************************
#            MANEJO DE UNIDADES DE SERVICIOS
#  ****************************************************
def unidadesNew(request):
    if request.method == "POST":
        form = UnidadMedidaForm(request.POST)
        if form.is_valid():
            try:
                form.save()
                return redirect('/unidades/show/')
            except Exception as e:
                #messages.warning(request, "Error al guardar el formulario: "+{e})
                print(f"Error al guardar el formulario: {e}")
    else:
        form = UnidadMedidaForm()
    
    return render(request, 'unidadesNew.html', {
        'form': form
    })

def unidadesShow(request):
    unidades = UnidadMedida.objects.all()
    return render(request,'productos/unidadesShow.html',{'unidades':unidades})

def unidadesEdit(request, id):
    unidades = get_object_or_404(id, id=id)
    form = UnidadMedidaForm(instance=unidades)  # Inicializa el formulario con la instancia de unidades
    return render(request, 'unidadesEdit.html', {'form': form, 'unidades':unidades})

def unidadesUpdate(request, id):
    unidades = get_object_or_404(id, id= id)
    if request.method == "POST":
        form = UnidadMedidaForm(request.POST, instance=unidades)
        if form.is_valid():
            form.save()
            return redirect('/unidades/show/')
        else:
            return render(request, 'unidadesEdit.html', {'form': form})  # Vuelve a renderizar el formulario con errores
    else:
        form = UnidadMedidaForm(instance=unidades)
    return render(request, 'unidadesEdit.html', {'form': form})

def unidadesDestroy(request, id):
    try:
        unidades = UnidadMedida.objects.get(id=id)
        unidades.delete()
        print(f"La Unidad ha sido eliminada exitosamente.")
    except IntegrityError:
        print(f"No se puede eliminar la Unidad porque está referenciada por otros registros.")
    return redirect("/unidades/show/")