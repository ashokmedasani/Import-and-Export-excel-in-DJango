from django import forms
from .models import ExcelData
from .models import ExcelIndividual


class UploadForm(forms.Form):
    Excel_file = forms.FileField()

class ExcelUploadForm(forms.ModelForm):
    class Meta:
        model = ExcelData
        fields = ['file']

class ExcelIndividualForm(forms.ModelForm):
    class Meta:
        model = ExcelIndividual
        fields = ['name','excel_file']


class ExcelDeleteForm(forms.Form):
    excel_file_id = forms.IntegerField(widget=forms.HiddenInput())


