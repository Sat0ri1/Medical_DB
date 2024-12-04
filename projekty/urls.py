"""
URL configuration for lims project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views



urlpatterns = [
    path("login/", views.loginPage, name="login"),
    path("logout/", views.logoutUser, name="logout"),
    path("", views.home, name="home"),
    path("registration/", views.RegistrationPage, name="reg"),
    path("dane/", views.dane, name = "dane"),
    path('check_login_status/', views.check_login_status, name='check_login_status'), 
   
    path('experiments/', views.experiments_list, name='experiments_list'),
    path('experiments/add/', views.create_experiment, name='create_experiment'),
    path('my_experiments/', views.my_experiments, name='my_experiments'),
    path('update_experiment/<str:pk>/', views.updateExp, name='upd_exp'),
    path('delete_experiment/<str:pk>/', views.deleteExp, name='del_exp'),
    
    path('employees/add/', views.create_employee, name='create_employee'),
    path('employees/', views.employees_list, name='employees_list'),
    path('update_employer/<str:pk>/', views.updateEmp, name='upd_emp'),
    path('delete_employer/<str:pk>/', views.deleteEmp, name='del_emp'),
    
    path('patients/add/', views.create_patient, name='create_patient'),
    path('patients/', views.patients_list, name='patients_list'),
    path('update_patient/<str:pk>/', views.updatePat, name='upd_pat'),
    path('delete_patient/<str:pk>/', views.deletePat, name='del_pat'),
    
    path('create/project/', views.create_project, name='create_project'),
    path('project/', views.projects_list, name='project_list'),
    path('my_projects/', views.my_projects, name='my_projects'),
    path('update_project/<str:pk>/', views.updatePro, name='upd_pro'),
    path('delete_project/<str:pk>/', views.deletePro, name='del_pro'),
    
    path('create/laboratory/', views.create_laboratory, name='create_laboratory'),
    path('laboratories/', views.laboratories_list, name='laboratory_list'),
    path('update_laboratory/<str:pk>/', views.updateLab, name='upd_lab'),
    path('delete_laboratory/<str:pk>/', views.deleteLab, name='del_lab'),
    
    path('create/method/', views.create_method, name='create_method'),
    path('methods/', views.methods_list, name='methods_list'),
    path('update_method/<str:pk>/', views.updateMeth, name='upd_meth'),
    path('delete_method/<str:pk>/', views.deleteMeth, name='del_meth'),
    
    path('create/keyword/', views.create_keyword, name='create_keyword'),
    path('keywords/', views.keywords_list, name='keywords_list'),
    path('update_key_words/<str:pk>/', views.updateKey, name='upd_key'),
    path('delete_key_words/<str:pk>/', views.deleteKey, name='del_key'),
    
    path('create/diagnosis/', views.create_diagnosis, name='create_diagnosis'),
    path('diagnosis/', views.diagnosis_list, name='diagnosis_list'),
    path('update_diagnosis/<str:pk>/', views.updateDiag, name='upd_diag'),
    path('delete_diagnosis/<str:pk>/', views.deleteDiag, name='del_diag'),
    

    
    path('choose/', views.choose, name='choose'),
    path('choosdane/', views.chooseDane, name='choose_Dane'),
    
    path('new_data/', views.new_data, name='new_data')
]



