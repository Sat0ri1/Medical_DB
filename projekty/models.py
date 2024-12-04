from django.db import models
from django.contrib.auth.models import User

# tabela pracownicy
class Employes(models.Model):
    name = models.CharField(max_length=40)   
    surname = models.CharField(max_length=40)
    adres = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True) 
    email = models.EmailField(max_length=50, default='email@example.com')
    team = models.CharField(max_length=40, default='Default Team')  # Domyślna wartość
    phone_number = models.CharField(max_length=15, default='111111111')
    laboratory = models.ForeignKey('Laboratories', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.surname}"

# tabela projekty
class Projects(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    )
    project_name = models.CharField(max_length=60)
    team_leader = models.ForeignKey(Employes, on_delete=models.CASCADE, related_name="led_projects", null=True, blank=True)
    workers = models.ManyToManyField(Employes, through='RelationEmployesProjects')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')  # Domyślny status
    description = models.TextField()

    def __str__(self):
        return f"{self.project_name}"

class RelationEmployesProjects(models.Model):
    employee = models.ForeignKey(Employes, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)

# tabela laboratoria
class Laboratories(models.Model):
    lab_name = models.CharField(max_length=30)
    adress = models.CharField(max_length=100)
    web_adress = models.URLField(max_length=100)
    mail = models.EmailField(max_length=40)

    def __str__(self):
        return f"{self.lab_name}"

# tabela eksperymenty
class Experiments(models.Model):
    STATUS_CHOICES = (
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('paused', 'Paused'),
    )
    experiment_name = models.CharField(max_length=40)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    employe = models.ManyToManyField(Employes, through='RelationEmployesExperiments')
    patients = models.ManyToManyField('Patients', through='RelationPatientsExperiments')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')  # Domyślny status
    description = models.TextField()
    method = models.ForeignKey('Methods', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.experiment_name}"

class RelationEmployesExperiments(models.Model):
    employe = models.ForeignKey(Employes, on_delete=models.CASCADE)
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)

class RelationPatientsExperiments(models.Model):
    experiment = models.ForeignKey(Experiments, on_delete=models.CASCADE)
    patient = models.ForeignKey('Patients', on_delete=models.CASCADE)

class Methods(models.Model):
    name = models.CharField(max_length=20) 
    description = models.TextField()

    def __str__(self):
        return f"{self.name}"

class KeyWords(models.Model):
    name = models.CharField(max_length=20)
    description = models.TextField(blank=True, null=True)
    projects = models.ForeignKey(Projects, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

class Patients(models.Model):
    SEX_CHOICES = (
        ('0', 'Not specified'),
        ('1', 'Male'),
        ('2', 'Female'),
    )
    STATUS_CHOICES = (
        ('deceased', 'Deceased'),
        ('alive', 'Alive'),
        ('cured', 'Cured'),
    )
    name = models.CharField(max_length=20)
    surname = models.CharField(max_length=40)
    pesel = models.CharField(max_length=11, unique=True)
    birth_name = models.DateField()
    adress = models.CharField(max_length=100)
    mail = models.EmailField(max_length=40, default="write@your.mail")
    phonenumber = models.CharField(max_length=40)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ongoing')
    diagnosis = models.TextField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, default='0')

    def __str__(self):
        return f"{self.name} {self.surname} ({self.pesel})"

class Diagnosis(models.Model):
    icd_10 = models.CharField(max_length=4)
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name="diagnoses")

    def __str__(self):
        return self.icd_10