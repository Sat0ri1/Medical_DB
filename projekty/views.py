from django.shortcuts import render, redirect

from django.http import HttpResponse
from .models import Employes, Experiments, RelationPatientsExperiments, Patients, Projects, Laboratories, Methods, KeyWords, Diagnosis
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.apps import apps
from django.contrib import messages
from .forms import ExperimentForm, EmployeeForm, PatientForm, LaboratoriesForm, KeyWordsForm, ProjectForm, MethodsForm, DiagnosisForm
from django.db.models import Q
from .forms import PatientSearchForm
from django.shortcuts import render, redirect, get_object_or_404
from .forms import EmployeeSearchForm




def emp(request, pk):
    emplo = Employes.objects.get(id=pk)
    contex = {"Employes": [emplo]}
    return render(request, "base_html.html", contex)

def home(request):
    return render(request, "base_html.html")


@login_required(login_url="home")
def dane(request):
    data = None
    table_name = None

    if request.method == "POST":
        table_name = request.POST.get("table")
        model = apps.get_model(app_label='projekty', model_name=table_name)
        data = model.objects.all().values()

        if data:
            data = [list(data[0].keys())] + [list(item.values()) for item in data]

    context = {
        'data': data,
        'table_name': table_name,
    }
    return render(request, 'dane.html', context)

def logoutUser(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("home")
    


def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            user = User.object.get(username=username)
        except:
            messages.error(request, "User does not exist ")
        
        user = authenticate(request, username=username, password=password)    
        
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Username or password does not exist")
        
    context = {}
    return render(request, 'login.html', context)

def RegistrationPage(request):
    if request.method == 'POST':
        if 'username' in request.POST:  
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if not username or not password1 or not password2:
                messages.error(request, 'Please fill in all fields in Step 1.')
                return render(request, 'registration.html', {'step1': True})

            if password1 != password2:
                messages.error(request, 'Passwords do not match.')
                return render(request, 'registration.html', {'step1': True})

            if len(password1) < 8:
                messages.error(request, 'Password must be at least 8 characters long.')
                return render(request, 'registration.html', {'step1': True})

            request.session['username'] = username
            request.session['password'] = password1

            return render(request, 'registration.html', {'step2': True})

        elif 'name' in request.POST:  
            username = request.session.get('username')
            password = request.session.get('password')
            name = request.POST.get('name')
            surname = request.POST.get('surname')
            adres = request.POST.get('adres')
            email = request.POST.get('email')
            team = request.POST.get('team')
            phone_number = request.POST.get('phone_number')

            if not username or not password:
                messages.error(request, 'Session expired. Please start over.')
                return render(request, 'registration.html', {'step1': True})

            user = User.objects.create_user(username=username, password=password)

            employe = Employes.objects.create(
                name=name,
                surname=surname,
                adres=adres,
                email=email,
                team=team,
                phone_number=phone_number,
                user=user  
            )

            del request.session['username']
            del request.session['password']

            messages.success(request, 'Registration successful! You can now log in.')
            return redirect('login')

    return render(request, 'registration.html', {'step1': True})

def check_login_status(request):
    if request.user.is_authenticated:
        return HttpResponse("You are logged in as {}.".format(request.user.username))
    else:
        return HttpResponse("You are not logged in.")

@login_required
def experiments_list(request):
    experiments = Experiments.objects.all()

    query = request.GET.get('q')
    if query:
        experiments = experiments.filter(experiment_name__icontains=query)

    return render(request, 'experiments_list.html', {'experiments': experiments})

@login_required
def my_experiments(request):
    try:
        user_employee = Employes.objects.get(user=request.user)
        experiments = Experiments.objects.filter(employe=user_employee)

        query = request.GET.get('q')
        if query:
            experiments = experiments.filter(experiment_name__icontains=query)

    except Employes.DoesNotExist:
        experiments = []
        query = None

    return render(request, 'experiments_list.html', {'experiments': experiments, 'my_experiments': True, 'query': query})




@login_required
def projects_list(request):
    projects = Projects.objects.all()

    query = request.GET.get('q')
    if query:
        projects = projects.filter(project_name__icontains=query) | projects.filter(team_leader__name__icontains=query) | projects.filter(team_leader__surname__icontains=query)

    return render(request, 'project_list.html', {'projects': projects, 'query': query})

@login_required
def my_projects(request):
    try:
        employe = Employes.objects.get(user=request.user)
        projects = Projects.objects.filter(workers=employe)
    except Employes.DoesNotExist:
        projects = []

    return render(request, 'project_list.html', {'projects': projects, 'my_projects': True})


def laboratories_list(request):
    laboratories = Laboratories.objects.all()

    query = request.GET.get('q')
    if query:
        laboratories = laboratories.filter(
            Q(lab_name__icontains=query) | Q(adress__icontains=query)
        )

    return render(request, 'laboratory_list.html', {'laboratories': laboratories, 'query': query})


@login_required
def methods_list(request):
    query = request.GET.get('q')
    if query:
        methods = Methods.objects.filter(name__icontains=query)
    else:
        methods = Methods.objects.all()
    return render(request, 'method_list.html', {'methods': methods})

def keywords_list(request):
    query = request.GET.get('q')
    if query:
        keywords = KeyWords.objects.filter(name__icontains=query)
    else:
        keywords = KeyWords.objects.all()
    return render(request, 'keyword_list.html', {'keywords': keywords})

def patients_list(request):
    form = PatientSearchForm(request.GET)
    patients = Patients.objects.all()
    query = ""

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            query_parts = query.split()
            q_objects = Q()
            for part in query_parts:
                q_objects &= Q(name__icontains=part) | Q(surname__icontains=part) | Q(pesel__icontains=part)
            patients = patients.filter(q_objects)

    return render(request, 'patient_list.html', {'patients': patients, 'form': form, 'query': query})

def diagnosis_list(request):
    query = request.GET.get('q')
    if query:
        diagnoses = Diagnosis.objects.filter(icd_10__icontains=query)
    else:
        diagnoses = Diagnosis.objects.all()
    return render(request, 'diagnosis_list.html', {'diagnoses': diagnoses})



def employees_list(request):
    form = EmployeeSearchForm(request.GET)
    employees = Employes.objects.all()
    query = ""

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            query_parts = query.split()
            q_objects = Q()
            for part in query_parts:
                q_objects &= Q(name__icontains=part) | Q(surname__icontains=part)
            employees = employees.filter(q_objects)

    return render(request, 'employee_list.html', {'employees': employees, 'form': form, 'query': query})


def create_experiment(request):
    if request.method == 'POST':
        form = ExperimentForm(request.POST)
        if form.is_valid():
            experiment = form.save()
            patients = form.cleaned_data['patients']
            for patient in patients:
                RelationPatientsExperiments.objects.create(experiment=experiment, patient=patient)
            return redirect('experiments_list')  
    else:
        form = ExperimentForm()
    return render(request, 'create_experiment.html', {'form': form})


def create_employee(request):
    if request.method == 'POST':
        form = EmployeeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('employee_list')  
    else:
        form = EmployeeForm()
    return render(request, 'create_employee.html', {'form': form})

def create_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('patients_list')  
    else:
        form = PatientForm()
    return render(request, 'create_patient.html', {'form': form})



def create_project(request):
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        if form.is_valid():
            project = form.save()
            team_leader = form.cleaned_data['team_leader']
            if team_leader:
                project.team_leader = team_leader
                project.save()
            return redirect('project_list')  
    else:
        form = ProjectForm()
    return render(request, 'create_project.html', {'form': form})

def create_laboratory(request):
    if request.method == 'POST':
        form = LaboratoriesForm(request.POST)
        if form.is_valid():
            laboratory = form.save()
            return redirect('laboratory_list')  
    else:
        form = LaboratoriesForm()
    return render(request, 'create_laboratory.html', {'form': form})


def create_method(request):
    if request.method == 'POST':
        form = MethodsForm(request.POST)
        if form.is_valid():
            method = form.save()
            return redirect('methods_list')  
    else:
        form = MethodsForm()
    return render(request, 'create_method.html', {'form': form})


def create_keyword(request):
    if request.method == 'POST':
        form = KeyWordsForm(request.POST)
        if form.is_valid():
            keyword = form.save()
            return redirect('keywords_list')  
    else:
        form = KeyWordsForm()
    return render(request, 'create_keyword.html', {'form': form})


def create_diagnosis(request):
    if request.method == 'POST':
        form = DiagnosisForm(request.POST)
        if form.is_valid():
            diagnosis = form.save()
            return redirect('diagnosis_list')  
    else:
        form = DiagnosisForm()
    return render(request, 'create_diagnosis.html', {'form': form})

@login_required(login_url="home")
def choose(request):
    contex = {}
    return render(request, "choose.html", contex)


@login_required(login_url="home")
def chooseDane(request):
    contex = {}
    return render(request, "choose_dane.html", contex)

@login_required(login_url="home")
def new_data(request):
    contex = {}
    return render(request, "add_new_data.html", contex)




def updateEmp(request, pk):
    emplo = Employes.objects.get(id=pk)
    form = EmployeeForm(instance=emplo)
    
    if request.method == "POST":
        form = EmployeeForm(request.POST, instance=emplo)
        if form.is_valid():
            form.save()
            return redirect('employees_list')
        
    context = {"form": form}
    return render(request, "update.html", context)

def updateDiag(request, pk):
    diagno = Diagnosis.objects.get(id=pk)
    form = DiagnosisForm(instance=diagno)
    
    if request.method == "POST":
        form = DiagnosisForm(request.POST, instance=diagno)
        if form.is_valid():
            form.save()
            return redirect('diagnosis_list')
    
    context = {"form": form}
    return render(request, "update.html", context)


def updateExp(request, pk):
    experi = Experiments.objects.get(id=pk)
    form = ExperimentForm(instance=experi)
    
    if request.method == "POST":
        form = ExperimentForm(request.POST, instance=experi)
        if form.is_valid():
            form.save()
            return redirect('experiments_list')
    
    context = {"form": form}
    return render(request, "update.html", context)


def updateKey(request, pk):
    keys = KeyWords.objects.get(id=pk)
    form = KeyWordsForm(instance=keys)
    
    if request.method == "POST":
        form = KeyWordsForm(request.POST, instance=keys)
        if form.is_valid():
            form.save()
            return redirect('keywords_list')
    
    context = {"form": form}
    return render(request, "update.html", context)


def updateLab(request, pk):
    labo = Laboratories.objects.get(id=pk)
    form = LaboratoriesForm(instance=labo)
    
    if request.method == "POST":
        form = LaboratoriesForm(request.POST, instance=labo)
        if form.is_valid():
            form.save()
            return redirect('laboratory_list')
    
    context = {"form": form}
    return render(request, "update.html", context)



def updateMeth(request, pk):
    metho = get_object_or_404(Methods, id=pk)
    form = MethodsForm(instance=metho)
    
    if request.method == "POST":
        form = MethodsForm(request.POST, instance=metho)
        if form.is_valid():
            form.save()
            return redirect('methods_list')
    
    context = {"form": form, "model_name": "Method", "instance": metho}
    return render(request, "update.html", context)


def updatePat(request, pk):
    pati = Patients.objects.get(id=pk)
    form = PatientForm(instance=pati)
    
    if request.method == "POST":
        form = PatientForm(request.POST, instance=pati)
        if form.is_valid():
            form.save()
            return redirect('patients_list')
    
    context = {"form": form}
    return render(request, "update.html", context)

def updatePro(request, pk):
    proj = Projects.objects.get(id=pk)
    form = ProjectForm(instance=proj)
    
    if request.method == "POST":
        form = ProjectForm(request.POST, instance=proj)
        if form.is_valid():
            form.save()
            return redirect('project_list')
    
    context = {"form": form}
    return render(request, "update.html", context)

def deleteEmp(request, pk):
    
    emplo = Employes.objects.get(id=pk)
    if request.method == "POST":
        emplo.delete()
        return redirect("employees_list")
    return render(request, "delete.html", {"obj":emplo})

def deleteDiag(request, pk):
    
    diago = Diagnosis.objects.get(id=pk)
    if request.method == "POST":
        diago.delete()
        return redirect("diagnosis_list")
    return render(request, "delete.html", {"obj":diago})

def deleteExp(request, pk):
    
    expo = Experiments.objects.get(id=pk)
    if request.method == "POST":
        expo.delete()
        return redirect("experiments_list")
    return render(request, "delete.html", {"obj":expo})


def deleteKey(request, pk):
    
    keys = KeyWords.objects.get(id=pk)
    if request.method == "POST":
        keys.delete()
        return redirect("keywords_list")
    return render(request, "delete.html", {"obj":keys})


def deleteLab(request, pk):
    
    labo = Laboratories.objects.get(id=pk)
    if request.method == "POST":
        labo.delete()
        return redirect("laboratory_list")
    return render(request, "delete.html", {"obj":labo})


def deleteMeth(request, pk):
    metho = get_object_or_404(Methods, id=pk)
    
    if request.method == "POST":
        metho.delete()
        return redirect("methods_list")
    context = {"instance": metho, "model_name": "Method"}
    return render(request, "delete.html", context)

def deletePat(request, pk):
    
    pati = Patients.objects.get(id=pk)
    if request.method == "POST":
        pati.delete()
        return redirect("patients_list")
    return render(request, "delete.html", {"obj":pati})


def deletePro(request, pk):
    
    proj = Projects.objects.get(id=pk)
    if request.method == "POST":
        proj.delete()
        return redirect("project_list")
    return render(request, "delete.html", {"obj":proj})
