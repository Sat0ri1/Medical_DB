from django.contrib import admin
from projekty.models import Employes, Projects, Laboratories, Experiments, Methods, KeyWords, Patients, Diagnosis, RelationEmployesProjects, RelationEmployesExperiments, RelationPatientsExperiments

admin.site.register(Employes)
admin.site.register(Projects)
admin.site.register(Laboratories)
admin.site.register(Experiments)
admin.site.register(Methods)
admin.site.register(KeyWords)
admin.site.register(Patients)
admin.site.register(Diagnosis)
admin.site.register(RelationEmployesProjects)
admin.site.register(RelationEmployesExperiments)
admin.site.register(RelationPatientsExperiments)