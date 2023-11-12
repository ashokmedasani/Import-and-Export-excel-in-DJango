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
        fields = ['user_name','excel_file',]


class ExcelDeleteForm(forms.Form):
    excel_file_id = forms.IntegerField(widget=forms.HiddenInput())



from .models import UserData

class UserDataForm(forms.ModelForm):
    class Meta:
        model = UserData
        fields = ['username', 'excel_file']
    
    #adding dropdown to select people

    username = forms.ChoiceField(choices = [], required=True, label='Select username')

    def __init__ (self, *args, **kwargs):
        super(UserDataForm, self).__init__(*args, **kwargs)

        username_choices = [('user1', 'User1'), ('user2', 'User2'), ('user3', 'User3')]

        self.fields['username'].choices = [('', 'Select Username')] + username_choices