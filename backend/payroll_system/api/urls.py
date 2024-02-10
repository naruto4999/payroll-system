from django.urls import path, include
from .views import CompanyListCreateAPIView, CompanyDetailsMixinView, CompanyRetrieveUpdateDestroyAPIView, DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView, DesignationListCreateAPIView, DesignationRetrieveUpdateDestroyAPIView, SalaryGradeListCreateAPIView, SalaryGradeRetrieveUpdateDestroyAPIView, RegularRegisterListCreateAPIViewView, RegularRetrieveUpdateAPIView, CompanyVisibilityPatchAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, BankListCreateAPIView, BankRetrieveUpdateDestroyAPIView, LeaveGradeListCreateAPIView, LeaveGradeRetrieveUpdateDestroyAPIView, ShiftListCreateAPIView, ShiftRetrieveUpdateDestroyAPIView, HolidayListCreateAPIView, HolidayRetrieveUpdateDestroyAPIView, EarningsHeadListCreateAPIView, EarningsHeadRetrieveUpdateDestroyAPIView, EmployeePersonalDetailListCreateView, EmployeePersonalDetailRetrieveUpdateDestroyAPIView, EmployeeProfessionalDetailListCreateAPIView, EmployeeProfessionalDetailRetrieveUpdateDestroyAPIView, EmployeeSalaryEarningListCreateAPIView, EmployeeSalaryEarningListUpdateAPIView,EmployeeSalaryDetailListCreateAPIView, EmployeeSalaryDetailRetrieveUpdateAPIView, EmployeeFamilyNomineeDetialListCreateAPIView, EmployeePfEsiDetailListCreateAPIView, EmployeePfEsiDetailRetrieveUpdateDestroyAPIView, EmployeeFamilyNomineeDetialRetrieveUpdateDestroyAPIView, WeeklyOffHolidayOffCreateAPIView, WeeklyOffHolidayOffRetrieveUpdateDestroyAPIView, PfEsiSetupCreateAPIView, PfEsiSetupRetrieveUpdateDestroyAPIView, CalculationsCreateAPIView, CalculationsRetrieveUpdateDestroyAPIView, EmployeeShiftsListAPIView, EmployeeShiftsUpdateAPIView, EmployeeShiftsCreateAPIView, EmployeeShiftsPermanentUpdateAPIView, EmployeeAttendanceListCreateAPIView, EmployeeAttendanceUpdateAPIView, AllEmployeeMonthyShiftsListAPIView, EmployeeGenerativeLeaveRecordListAPIView, EmployeeLeaveOpeningListAPIView, EmployeeMonthlyAttendancePresentDetailsListAPIView, EmployeeAdvancePaymentListCreateAPIView, EmployeeAdvancePaymentRetrieveUpdateDestroyAPIView, EmployeeMonthlyAttendanceDetailsListAPIView, AllEmployeeSalaryEarningListAPIView, EmployeeSalaryPreparedCreateAPIView, SalaryOvertimeSheetCreateAPIView, EmployeeSalaryPreparedListAPIView, AttendanceReportsCreateAPIView, EmployeeAttendanceBulkAutoFillView, BulkPrepareSalariesView, MachineAttendanceAPIView, PersonnelFileReportsCreateAPIView, DefaultAttendanceAPIView, EmployeeResignationUpdateAPIView, EmployeeUnresignUpdateAPIView, BonusCalculationAPIView, BonusCalculationListAPIView, BonusPercentageListAPIView, EmployeeProfessionalDetailRetrieveAPIView, EarnedAmountPreparedSalaryListAPIView, FullAndFinalRetrieveAPIView, FullAndFinalCreateAPIView, EmployeeELLeftRetrieveAPIView, EmployeeBonusAmountYearlyRetrieveAPIView, FullAndFinalReportCreateAPIView, PfEsiReportsCreateAPIView, EmployeeVisibilityPatchAPIView, SubUserOvertimeSettingsMonthlyCreateUpdateAPIView, SubUserOvertimeSettingsListAPIView, SubUserMiscSettingsRetrieveUpdateDestroyAPIView, SubUserMiscSettingsCreateAPIView
from .auth.views import LoginView, RegisterView, RefreshView, PasswordResetAPIView, PasswordResetConfirmView, VerifyOTPView
from django.contrib.auth.views import PasswordResetCompleteView


urlpatterns = [
    path('company', CompanyListCreateAPIView.as_view()),
    path('company-visible', CompanyVisibilityPatchAPIView.as_view()),
    path('edit-company/<int:id>', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    
    path('company-details', CompanyDetailsMixinView.as_view()),
    path('company-details/<int:company>', CompanyDetailsMixinView.as_view()),
    # path('', include('api.routers',)),
    path('department/<int:company_id>', DepartmentListCreateAPIView.as_view()),
    path('department/<int:company_id>/<int:id>', DepartmentRetrieveUpdateDestroyAPIView.as_view()),
    path('designation/<int:company_id>', DesignationListCreateAPIView.as_view()),
    path('designation/<int:company_id>/<int:id>', DesignationRetrieveUpdateDestroyAPIView.as_view()),
    path('salary-grade/<int:company_id>', SalaryGradeListCreateAPIView.as_view()),
    path('salary-grade/<int:company_id>/<int:id>', SalaryGradeRetrieveUpdateDestroyAPIView.as_view()),
    path('category/<int:company_id>', CategoryListCreateAPIView.as_view()),
    path('category/<int:company_id>/<int:id>', CategoryRetrieveUpdateDestroyAPIView.as_view()),
    path('bank/<int:company_id>', BankListCreateAPIView.as_view()),
    path('bank/<int:company_id>/<int:id>', BankRetrieveUpdateDestroyAPIView.as_view()),
    path('leave-grade/<int:company_id>', LeaveGradeListCreateAPIView.as_view()),
    path('leave-grade/<int:company_id>/<int:id>', LeaveGradeRetrieveUpdateDestroyAPIView.as_view()),
    path('shift/<int:company_id>', ShiftListCreateAPIView.as_view()),
    path('shift/<int:company_id>/<int:id>', ShiftRetrieveUpdateDestroyAPIView.as_view()),
    path('holiday/<int:company_id>', HolidayListCreateAPIView.as_view()),
    path('holiday/<int:company_id>/<int:id>', HolidayRetrieveUpdateDestroyAPIView.as_view()),
    path('earnings-head/<int:company_id>', EarningsHeadListCreateAPIView.as_view()),
    path('earnings-head/<int:company_id>/<int:id>', EarningsHeadRetrieveUpdateDestroyAPIView.as_view()),
    # path('deductions-head/<int:company_id>', DeductionsHeadListCreateAPIView.as_view()),
    # path('deductions-head/<int:company_id>/<int:id>', DeductionsHeadRetrieveUpdateDestroyAPIView.as_view()),

    # Use URLs like this from now on, separate for GET requests and POST request and don't use query params in POST request, only use them in GET requests
    path('employee-personal-detail/<int:company_id>', EmployeePersonalDetailListCreateView.as_view()),
    path('employee-personal-detail', EmployeePersonalDetailListCreateView.as_view()),
    path('employee-personal-detail/<int:company_id>/<int:id>', EmployeePersonalDetailRetrieveUpdateDestroyAPIView.as_view()),
    path('employee-visible', EmployeeVisibilityPatchAPIView.as_view()),

    path('employee-professional-detail', EmployeeProfessionalDetailListCreateAPIView.as_view()),
    path('all-employee-professional-detail/<int:company_id>', EmployeeProfessionalDetailListCreateAPIView.as_view()),
    path('employee-professional-detail/<int:company_id>/<int:employee>', EmployeeProfessionalDetailRetrieveUpdateDestroyAPIView.as_view()),
    path('get-employee-professional-detail/<int:company_id>/<int:employee>', EmployeeProfessionalDetailRetrieveAPIView.as_view()), #Used in resignationApiSlice
    path('resignation/<int:company_id>/<int:employee>', EmployeeResignationUpdateAPIView.as_view()),
    path('unresign/<int:company_id>/<int:employee>', EmployeeUnresignUpdateAPIView.as_view()),

    # path('employee-salary-earning', EmployeeSalaryEarningListCreateAPIView.as_view()),
    path('employee-salary-earning/<int:company_id>/<int:employee>/<int:year>', EmployeeSalaryEarningListCreateAPIView.as_view()),
    path('employee-salary-earning/<int:company_id>/<int:employee>', EmployeeSalaryEarningListCreateAPIView.as_view()),

    path('employee-salary-earning-update/<int:company_id>/<int:employee>', EmployeeSalaryEarningListUpdateAPIView.as_view()),
    path('employee-salary-detail/<int:company_id>', EmployeeSalaryDetailListCreateAPIView.as_view()),
    path('all-employee-salary-detail/<int:company_id>', EmployeeSalaryDetailListCreateAPIView.as_view()),

    path('employee-salary-detail/<int:company_id>/<int:employee>', EmployeeSalaryDetailRetrieveUpdateAPIView.as_view()),
    path('employee-family-nominee-detail', EmployeeFamilyNomineeDetialListCreateAPIView.as_view()),
    path('employee-family-nominee-detail/<int:company_id>/<int:employee>', EmployeeFamilyNomineeDetialListCreateAPIView.as_view()),
    path('employee-family-nominee-detail-update/<int:company_id>/<int:employee>', EmployeeFamilyNomineeDetialRetrieveUpdateDestroyAPIView.as_view()),
    path('employee-family-nominee-detail-delete/<int:company_id>/<int:employee>/<int:id>', EmployeeFamilyNomineeDetialRetrieveUpdateDestroyAPIView.as_view()),

    path('employee-pf-esi-detail', EmployeePfEsiDetailListCreateAPIView.as_view()),
    path('all-employee-pf-esi-detail/<int:company_id>', EmployeePfEsiDetailListCreateAPIView.as_view()),
    path('employee-pf-esi-detail/<int:company_id>/<int:employee>', EmployeePfEsiDetailRetrieveUpdateDestroyAPIView.as_view()),
    path('weekly-off-holiday-off-create/<int:company_id>', WeeklyOffHolidayOffCreateAPIView.as_view()),
    path('weekly-off-holiday-off/<int:company_id>', WeeklyOffHolidayOffRetrieveUpdateDestroyAPIView.as_view()),
    path('pf-esi-setup-create', PfEsiSetupCreateAPIView.as_view()),
    path('pf-esi-setup/<int:company_id>', PfEsiSetupRetrieveUpdateDestroyAPIView.as_view()),
    path('calculations-create', CalculationsCreateAPIView.as_view()),
    path('calculations/<int:company_id>', CalculationsRetrieveUpdateDestroyAPIView.as_view()),
    path('employee-shifts/<int:company_id>/<int:employee>/<int:year>', EmployeeShiftsListAPIView.as_view()),
    path('employee-shifts-update/<int:company_id>/<int:employee>', EmployeeShiftsUpdateAPIView.as_view()),
    path('employee-shift-permanent-update/<int:company_id>/<int:employee>', EmployeeShiftsPermanentUpdateAPIView.as_view()),
    path('employee-shifts', EmployeeShiftsCreateAPIView.as_view()),
    path('all-employee-monthly-shifts/<int:company_id>/<int:year>/<int:month>/', AllEmployeeMonthyShiftsListAPIView.as_view()),
    
    path('employee-attendance/<int:company_id>/<int:employee>', EmployeeAttendanceListCreateAPIView.as_view()),
    # path('employee-attendance/<int:company_id>/<int:employee>/<str:from_date>/<str:to_date>', EmployeeAttendanceListCreateAPIView.as_view()),
    path('employee-attendance-update/<int:company_id>/<int:employee>', EmployeeAttendanceUpdateAPIView.as_view()),
    path('employee-attendance-bulk-autofill', EmployeeAttendanceBulkAutoFillView.as_view()),
    path('all-employee-attendance/<int:company_id>/<int:year>/<int:month>', EmployeeAttendanceListCreateAPIView.as_view()),
    path('all-employee-generative-leave-record/<int:company_id>/<int:year>', EmployeeGenerativeLeaveRecordListAPIView.as_view()),
    path('all-employee-present-count/<int:company_id>/<int:year>', EmployeeMonthlyAttendancePresentDetailsListAPIView.as_view()),
    path('all-employee-monthly-attendance-details/<int:company_id>/<int:year>', EmployeeMonthlyAttendanceDetailsListAPIView.as_view()),
    path('all-employee-leave-opening/<int:company_id>/<int:year>', EmployeeLeaveOpeningListAPIView.as_view()),
    path('employee-advance-payment/<int:company_id>/<int:employee_id>', EmployeeAdvancePaymentListCreateAPIView.as_view()),
    path('employee-advance-payment-update/<int:company_id>/<int:employee_id>', EmployeeAdvancePaymentRetrieveUpdateDestroyAPIView.as_view()),
    path('employee-advance-payment-delete/<int:company_id>/<int:employee_id>/<str:ids>', EmployeeAdvancePaymentRetrieveUpdateDestroyAPIView.as_view()),
    path('all-employee-salary-earning/<int:company_id>/<int:year>', AllEmployeeSalaryEarningListAPIView.as_view()),
    path('employee-salary-prepared', EmployeeSalaryPreparedCreateAPIView.as_view()),
    path('employee-bulk-salary-prepared', BulkPrepareSalariesView.as_view()),
    path('employee-machine-attendance', MachineAttendanceAPIView.as_view()),
    path('bulk-default-attendance', DefaultAttendanceAPIView.as_view()),

    path('generate-salary-overtime-sheet', SalaryOvertimeSheetCreateAPIView.as_view()),
    path('generate-attendance-reports', AttendanceReportsCreateAPIView.as_view()),
    path('generate-pf-esi-reports', PfEsiReportsCreateAPIView.as_view()),
    path('generate-personnel-file-reports', PersonnelFileReportsCreateAPIView.as_view()),
    path('prepared-salaries/<int:company_id>/<int:year>/<int:month>', EmployeeSalaryPreparedListAPIView.as_view()),
    path('bonus-calculation/<int:company_id>', BonusCalculationAPIView.as_view()),
    path('get-bonus-calculation/<int:company_id>/<str:start_date>/<str:end_date>', BonusCalculationListAPIView.as_view()),
    path('get-bonus-percentage/<int:company_id>', BonusPercentageListAPIView.as_view()),
    path('earned-amount-prepared-salary/<int:company_id>/<int:employee_id>', EarnedAmountPreparedSalaryListAPIView.as_view()),
    path('get-full-and-final/<int:company_id>/<int:employee>', FullAndFinalRetrieveAPIView.as_view()),
    path('full-and-final/<int:company_id>/<int:employee_id>', FullAndFinalCreateAPIView.as_view()),
    path('el-left/<int:company_id>/<int:employee_id>', EmployeeELLeftRetrieveAPIView.as_view()),
    path('bonus-amount/<int:company_id>/<int:employee_id>/<int:year>', EmployeeBonusAmountYearlyRetrieveAPIView.as_view()),
    path('generate-full-and-final-report', FullAndFinalReportCreateAPIView.as_view()),
    path('subuser-overtime-settings', SubUserOvertimeSettingsMonthlyCreateUpdateAPIView.as_view()),
    path('get-subuser-overtime-settings/<int:company_id>/<int:year>/<int:month>', SubUserOvertimeSettingsListAPIView.as_view()),
    path('sub-user-misc-settings-create', SubUserMiscSettingsCreateAPIView.as_view()),
    path('sub-user-misc-settings/<int:company_id>', SubUserMiscSettingsRetrieveUpdateDestroyAPIView.as_view()),



    # path('company-statistics/<int:company_id>', CompanyEmployeeStatisticsListAPIView.as_view()),




    
    

    



    




    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/register/otp', VerifyOTPView.as_view(), name='otp'),
    
    path('auth/refresh/', RefreshView.as_view(), name='refresh'),
    path('auth/regular-register/', RegularRegisterListCreateAPIViewView.as_view()),
    # path('auth/regular-register/', RegularRetrieveUpdateAPIView.as_view()),
    path('regular', RegularRetrieveUpdateAPIView.as_view()),
    path('auth/password/reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    # path('auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('auth/reset_password_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='api/password_reset_complete.html'), name='password_reset_complete')
    
]

