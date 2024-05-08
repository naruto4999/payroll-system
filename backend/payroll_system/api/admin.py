from django.contrib import admin
from .models import User, Company, CompanyDetails, Deparment, Designation, SalaryGrade, OwnerToRegular, Category, LeaveGrade, Shift, Holiday, DeductionsHead, EarningsHead, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeeSalaryDetail, EmployeeSalaryEarning, EmployeePfEsiDetail, EmployeeFamilyNomineeDetial, WeeklyOffHolidayOff, Calculations, EmployeeShifts, EmployeeAttendance, EmployeeGenerativeLeaveRecord, EmployeeAdvancePayment, EmployeeMonthlyAttendanceDetails, PfEsiSetup, EmployeeSalaryPrepared, EmployeeAdvanceEmiRepayment, EmployeeLeaveOpening

admin.site.register(User)
admin.site.register(Company)
admin.site.register(CompanyDetails)
admin.site.register(Deparment)
admin.site.register(Designation)
admin.site.register(SalaryGrade)
admin.site.register(OwnerToRegular)
admin.site.register(Category)
admin.site.register(LeaveGrade)
admin.site.register(Shift)
admin.site.register(Holiday)
admin.site.register(DeductionsHead)
admin.site.register(EarningsHead)
admin.site.register(EmployeePersonalDetail)
admin.site.register(EmployeeProfessionalDetail)
admin.site.register(EmployeeSalaryDetail)
admin.site.register(EmployeeSalaryEarning)
admin.site.register(EmployeePfEsiDetail)
admin.site.register(EmployeeFamilyNomineeDetial)
admin.site.register(WeeklyOffHolidayOff)
admin.site.register(Calculations)
admin.site.register(EmployeeShifts)
admin.site.register(EmployeeAttendance)
admin.site.register(EmployeeGenerativeLeaveRecord)
admin.site.register(EmployeeAdvancePayment)
admin.site.register(EmployeeMonthlyAttendanceDetails)
admin.site.register(PfEsiSetup)
admin.site.register(EmployeeSalaryPrepared)
admin.site.register(EmployeeAdvanceEmiRepayment)
admin.site.register(EmployeeLeaveOpening)
