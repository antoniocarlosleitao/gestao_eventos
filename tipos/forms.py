import datetime
from django import forms
from decimal import Decimal
from django.db.models import Q
from tipos.models import Evento, Participante, Inscricao, ImagemEvento


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput())
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result


class ImagemEventoForm(forms.ModelForm):
    class Meta:
        model = ImagemEvento
        fields = ['imagem', 'destaque']


class EventoForm(forms.ModelForm):
    imagens = forms.FileField(widget=forms.ClearableFileInput(attrs={'allow_multiple_selected': True}), required=False)

    # imagem = MultipleFileField(label='Selecione as fotos', required=False)

    class Meta:
        model = Evento
        fields = ['nome_do_evento', 'data_inicio', 'hora_inicio', 'data_final', 'hora_final', 'endereco', 'cidade', 'estado', 'email_contato', 'valor_inscricao', 'descricao']
        labels = {
            'nome_do_evento': 'Nome do Evento',
            'data_inicio': 'Data do Início',
            'hora_inicio': 'Hora do Início',
            'data_final': 'Data Final',
            'hora_final': 'Hora Final',
            'endereco': 'Endereço',
            'cidade': 'Cidade',
            'estado': 'Estado',
            'email_contato': 'Email Contato',
            'valor_inscricao': 'Valor da Inscrição',
            'descricao': 'Descrição',
        }

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
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite uma descrição da conferência (opcional)','rows': 3, 'maxlength': 150}),
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

    def clean_imagens(self):
        imagens = self.files.getlist('imagens')
        if len(imagens) > 5:
            raise forms.ValidationError('Você pode fazer upload de no máximo 5 imagens.')
        return imagens


class ParticipanteForm(forms.ModelForm):
    class Meta:
        model = Participante
        fields = ['nome', 'cpf', 'telefone', 'email']
        labels = {
            'nome': 'Nome',
            'cpf': 'CPF',
            'telefone': 'Telefone',
            'email': 'Email'
        }
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome'}),
            'cpf': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite seu CPF'}),
            'telefone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o email'}),
        }
    def clean_cpf(self):
        cpf = self.cleaned_data.get('cpf')
        if not cpf:
            raise forms.ValidationError("O campo cpf é obrigatório.")
        return cpf

    def clean_telefone(self):
        telefone = self.cleaned_data.get('telefonel')
        if not telefone:
            raise forms.ValidationError("O campo telefone é obrigatório.")
        return telefone

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("O campo email é obrigatório.")
        return email

class InscricaoForm(forms.ModelForm):
    class Meta:
        model = Inscricao
        fields = ['participante', 'evento', 'data_pagamento', 'valor_inscricao', 'material', 'almoco', 'certificado',
                  'outras_taxas', 'pago']
        labels = {
            'participante': 'Participante',
            'evento': 'Evento',
            'data_pagamento': 'Data do Pagamento',
            'valor_insrcicao': 'Valor da Inscrição',
            'material': 'Material',
            'almoco': 'Almoço',
            'certificado': 'Certificado',
            'outras_taxas': 'Outras Taxas',
            'pago': 'Pago',
        }
        widgets = {
            'participante': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o participante'}),
            'evento': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Escolha o evento'}),
            'data_pagamento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'valor_inscrição': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço o valor da inscrição', 'readonly': 'readonly'}),
            'material': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do material'}),
            'almoco': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do almoço'}),
            'certificado': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o preço do certificado'}),
            'outras_taxas': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Digite o somatório de taxas extras'}),
            'pago': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtra eventos
        # No caso de edição, inclui a inscrição já feita
        if self.instance and self.instance.pk:
            # Adiciona o inscrição do evento atual à queryset para que ele apareça na lista
            self.fields['inscricao'].queryset = Inscricao.objects.filter(
                Q(id=self.instance.inscricao.id) | ~Q(id__in=Inscricao.objects.values('inscricao_id'))
            )
        else:
            # Em caso de criação, mostra apenas inscrições não feitas
            self.fields['inscricao'].queryset = Inscricao.objects.exclude(id__in=Inscricao.objects.values('inscricao_id'))

        # Formata a data de pagamento no formato YYYY-MM-DD se houver uma data inicial
        if self.instance and self.instance.data_pagamento:
            self.initial['data_pagamento'] = self.instance.data_pagamento.strftime('%Y-%m-%d')

    def clean(self):
        cleaned_data = super().clean()

        evento = cleaned_data.get('evento')
        if evento:
            valor_inscricao = evento.preco_inscricao
        else:
            valor_inscricao = Decimal(0.0)

        material = cleaned_data.get('material') or Decimal(0.0)
        almoco = cleaned_data.get('almoco') or Decimal(0.0)
        certificado = cleaned_data.get('certificado') or Decimal(0.0)
        outras_taxas = cleaned_data.get('outras_taxas') or Decimal(0.0)

        valor_final = valor_inscricao + material + almoco + certificado + outras_taxas
        cleaned_data['valor'] = valor_final

        return cleaned_data

    def clean_data_pagamento(self):
        data_pagamento = self.cleaned_data.get('data_pagamento')
        if data_pagamento < datetime.date.today():
            raise forms.ValidationError("A data de pagamento não pode ser no passado.")
        return data_pagamento
