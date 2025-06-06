from django import forms
from .models import WebDesignRequest, WebDesignFile

class WebDesignRequestForm(forms.ModelForm):
    class Meta:
        model = WebDesignRequest
        fields = ['client_name', 'additional_resources']
        widgets = {
            'additional_resources': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Describe aquí cualquier recurso adicional que necesites incluir en tu sitio web...'}),
            'client_name': forms.TextInput(attrs={'placeholder': 'Ingresa tu nombre o el nombre de tu empresa'}),
        }

class WebDesignFileForm(forms.ModelForm):
    class Meta:
        model = WebDesignFile
        fields = ['file_type', 'file']
        widgets = {
            'file_type': forms.HiddenInput(),
        }

WebDesignFileFormSet = forms.inlineformset_factory(
    WebDesignRequest,
    WebDesignFile,
    form=WebDesignFileForm,
    extra=1,
    can_delete=True
) 