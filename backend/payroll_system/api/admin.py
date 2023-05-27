from django.contrib import admin
from .models import User, Company, CompanyDetails, Deparment, Designation, SalaryGrade, OwnerToRegular, Category

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanyDetails)
admin.site.register(Deparment)
admin.site.register(Designation)
admin.site.register(SalaryGrade)
admin.site.register(OwnerToRegular)
admin.site.register(Category)