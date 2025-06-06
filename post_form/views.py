from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import WebDesignRequestForm, WebDesignFileFormSet

# Create your views here.


def index(request):
    if request.method == 'POST':
        form = WebDesignRequestForm(request.POST)
        if form.is_valid():
            web_design_request = form.save()
            formset = WebDesignFileFormSet(request.POST, request.FILES, instance=web_design_request)
            if formset.is_valid():
                formset.save()
                messages.success(request, '¡Tu solicitud de diseño web ha sido enviada con éxito!')
                return redirect('post_form:index')
            else:
                # Mostrar errores específicos del formset
                for error in formset.non_form_errors():
                    messages.error(request, f'Error general: {error}')
                for form in formset:
                    if form.errors:
                        for field, errors in form.errors.items():
                            for error in errors:
                                messages.error(request, f'Error en {form.instance.file_type if form.instance else "archivo"}: {error}')
        else:
            # Mostrar errores específicos del formulario principal
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error en {field}: {error}')
    else:
        form = WebDesignRequestForm()
        formset = WebDesignFileFormSet()
    
    return render(request, 'post_form/files_form.html', {
        'form': form,
        'formset': formset,
    })

