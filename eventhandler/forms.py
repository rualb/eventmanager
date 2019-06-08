from django import forms
from django.forms import ModelForm

import django.forms
from django.utils.translation import gettext_lazy as _

from . import models


class DateInput(forms.DateInput):
    input_type = 'date'


class SelectDateWidget(forms.SelectDateWidget):
    pass

 
class EventRecordForm(ModelForm):

    specode = forms.ModelChoiceField(
        initial='',
        #required = True,
        queryset=models.EventType.objects.only('code', 'title'),
        to_field_name='code',

        widget=forms.Select(
            attrs={
                "class": "form-control",
                'style': 'width:50ch',
               # "placeholder": "Növ"
            }),

        label = _('Type')
        
    )

    def __init__(self, *args, **kwargs):
        super(EventRecordForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.EventRecord
        fields = ('specode', 'recdate', 'duedate', 'textf1',
                  'textf2', 'textf3', 'textf4', 'status')
        # field_classes = {
        #     'specode': forms.ModelChoiceField #(to_field_name = 'code', queryset = models.EventType.objects.all())
        # }
        widgets = {
            'id': forms.TextInput(attrs={
                "class": "form-control",
                'style': 'width:50ch',
                #"placeholder": "Id"
            }),
            # 'specode': forms.TextInput(attrs={
            #     "class": "form-control",
            #     'style': 'width:50ch',
            #     "placeholder": "Növ"
            # }),
            # 'specode': forms.Select(

            #     #choices = models.EventType.objects.values_list('code','title'),
            #     attrs={
            #         "class": "form-control",
            #         'style': 'width:50ch',
            #         "placeholder": "Növ"
            #     }),
            # 'specode': forms.Select(attrs={
            #     "class": "form-control",
            #     'style': 'width:50ch',
            #     "placeholder": "Növ"
            # }),
       
            'recdate': DateInput(attrs={'style': 'width:25ch', 'class': 'form-control'}),
            'duedate': DateInput(attrs={'style': 'width:25ch', 'class': 'form-control'}),
            'textf1': forms.TextInput(attrs={
                "class": "form-control",
                'style': 'width:50ch',
               # "placeholder": "Obyektin Adı"
            }),
            'textf2': forms.TextInput(attrs={
                "class": "form-control",
                'style': 'width:50ch',
               # "placeholder": "Tapşırığın Adı"
            }),
            'textf3': forms.TextInput(attrs={
                "class": "form-control",
                'style': 'width:50ch',
               # "placeholder": "Tapşırığı Verənin Adı"
            }),
            'textf4': forms.TextInput(attrs={
                "class": "form-control",
                'style': 'width:50ch',
               # "placeholder": "İcraçı"
            }),
            'status': forms.Select(attrs={
                "class": "form-control",
                'style': 'width:25ch',
               # "placeholder": "İcra"
            }),


        }

        # labels = {
        #     'id': _('ID'),
        #     'specode': _('Type'),
        #     'recdate': _('Date'),
        #     'duedate': _('Due Date'),
        #     'textf1': _('Object Name'),
        #     'textf2': _('Task Title'),
        #     'textf3': _('Task From'),
        #     'textf4': _('Task Executor'),
        #     'status': _('Status'),
        # }
