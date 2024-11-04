from django import forms
from tipos.models import Conferencia, Palestra, Workshop


class ConferenciaForm(forms.ModelForm):
    class Meta:
        model = Conferencia
        fields = ['nome_do_evento', 'data_inicio', 'hora_inicio', 'data_final', 'hora_final', 'endereco', 'cidade', 'estado', 'email_contato', 'valor_inscricao', 'descricao']
        widgets = {
            'nome_do_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite nome do evento'}),
            'data_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data do início'}),
            'hora_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora do início'}),
            'data_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data final'}),
            'hora_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora final'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
            'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
            'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o estado'}),
            'email_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email de contato'}),
            'valor_inscricao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite valor da inscrição'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição da conferência (opcional)', 'rows': 3, 'maxlength': 150}),
        }

    class PalestraForm(forms.ModelForm):
        class Meta:
            model = Palestra
            fields = ['nome_do_evento', 'data_inicio', 'hora_inicio', 'data_final', 'hora_final', 'endereco', 'cidade','estado', 'email_contato', 'valor_inscricao', 'descricao']
            widgets = {
                'nome_do_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite nome do evento'}),
                'data_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data do início'}),
                'hora_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora do início'}),
                'data_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data final'}),
                'hora_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora final'}),
                'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
                'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
                'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o estado'}),
                'email_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email de contato'}),
                'valor_inscricao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite valor da inscrição'}),
                'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição da palestra (opcional)','rows': 3, 'maxlength': 150}),
            }
    class WorkshopForm(forms.ModelForm):
        class Meta:
            model = Workshop
            fields = ['nome_do_evento', 'data_inicio', 'hora_inicio', 'data_final', 'hora_final', 'endereco', 'cidade','estado', 'email_contato', 'valor_inscricao', 'descricao']
            widgets = {
                'nome_do_evento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite nome do evento'}),
                'data_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data do início'}),
                'hora_inicio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora do início'}),
                'data_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a data final'}),
                'hora_final': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite a hora final'}),
                'endereco': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o endereço'}),
                'cidade': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite a cidade'}),
                'estado': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o estado'}),
                'email_contato': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email de contato'}),
                'valor_inscricao': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite valor da inscrição'}),
                'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição da palestra (opcional)','rows': 3, 'maxlength': 150}),
            }

    def clean_data_inicio(self):
        data_inicio = self.cleaned_data.get('data_inicio')
        if data_inicio <= 0:
            raise forms.ValidationError("O valor da data inicio deve ser um valor positivo.")
        return data_inicio

    def clean_hora_inicio(self):
        hora_inicio = self.cleaned_data.get('hora_inicio')
        if hora_inicio <= 0:
            raise forms.ValidationError("O valor da hora inicio deve ser um valor positivo.")
        return hora_inicio

    def clean_data_final(self):
        data_final = self.cleaned_data.get('data_final')
        if data_final <= 0:
            raise forms.ValidationError("O valor da data final deve ser um valor positivo.")
        return data_final

    def clean_hora_final(self):
        hora_final = self.cleaned_data.get('hora_final')
        if hora_final <= 0:
            raise forms.ValidationError("O valor da hora final deve ser um valor positivo.")
        return hora_final

    def clean_valor_inscricao(self):
        valor_inscricao = self.cleaned_data.get('valor_inscricao')
        if valor_inscricao <= 0:
            raise forms.ValidationError("O preço do valor da inscriçãoo deve ser um valor positivo.")
        return valor_inscricao