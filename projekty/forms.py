from django import forms
from .models import Experiments, Patients, Employes, Projects, Laboratories, Methods, KeyWords, Diagnosis

class ExperimentForm(forms.ModelForm):
    patients = forms.ModelMultipleChoiceField(
        queryset=Patients.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Patients"
    )

    class Meta:
        model = Experiments
        fields = ['experiment_name', 'project', 'status', 'description', 'method', 'patients', 'employe']
        
class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employes
        fields = ['user', 'name', 'surname', 'adres', 'email', 'team', 'phone_number', 'laboratory']

class PatientForm(forms.ModelForm):
    class Meta:
        model = Patients
        fields = ['name', 'surname', 'pesel', 'birth_name', 'adress', 'mail', 'phonenumber', 'status', 'diagnosis', 'sex']
        

class ProjectForm(forms.ModelForm):
    workers = forms.ModelMultipleChoiceField(
        queryset=Employes.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Workers"
    )

    class Meta:
        model = Projects
        fields = ['project_name', 'team_leader', 'workers', 'status', 'description']
        

class LaboratoriesForm(forms.ModelForm):
    class Meta:
        model = Laboratories
        fields = ['lab_name', 'adress', 'web_adress', 'mail']
        
        
class MethodsForm(forms.ModelForm):
    class Meta:
        model = Methods
        fields = ['name', 'description']
        
        
class KeyWordsForm(forms.ModelForm):
    class Meta:
        model = KeyWords
        fields = ['name', 'description', 'projects']
        
class DiagnosisForm(forms.ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['icd_10', 'patient']

class EmployeeSearchForm(forms.Form):
    query = forms.CharField(label='Search by name or surname', max_length=100, required=False)
    
    
class PatientSearchForm(forms.Form):
    query = forms.CharField(label='Search by name, surname, or PESEL', max_length=100, required=False)