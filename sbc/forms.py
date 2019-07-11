from django import forms

class SbcForm(forms.Form):
    consulta = forms.CharField(label='', required=True, widget=forms.Textarea(
        attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese texto.',
            'rows': '4'
        }))                                                                         