from django.contrib import admin
from .models import User, Company, CompanyDetails, Deparment

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanyDetails)
admin.site.register(Deparment)