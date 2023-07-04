from django.urls import path, include
from .views import CompanyListCreateAPIView, CompanyDetailsMixinView, CompanyRetrieveUpdateDestroyAPIView, DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView, DesignationListCreateAPIView, DesignationRetrieveUpdateDestroyAPIView, SalaryGradeListCreateAPIView, SalaryGradeRetrieveUpdateDestroyAPIView, RegularRegisterListCreateAPIViewView, RegularRetrieveDestroyAPIView, CompanyVisibilityPatchAPIView, CategoryListCreateAPIView, CategoryRetrieveUpdateDestroyAPIView, BankListCreateAPIView, BankRetrieveUpdateDestroyAPIView, LeaveGradeListCreateAPIView, LeaveGradeRetrieveUpdateDestroyAPIView, ShiftListCreateAPIView, ShiftRetrieveUpdateDestroyAPIView, HolidayListCreateAPIView, HolidayRetrieveUpdateDestroyAPIView, EarningsHeadListCreateAPIView, EarningsHeadRetrieveUpdateDestroyAPIView, DeductionsHeadListCreateAPIView, DeductionsHeadRetrieveUpdateDestroyAPIView, EmployeePersonalDetailListCreateView, EmployeeProfessionalDetailCreateAPIView
from .auth.views import LoginView, RegisterView, RefreshView, PasswordResetAPIView, PasswordResetConfirmView, VerifyOTPView
from django.contrib.auth.views import PasswordResetCompleteView


urlpatterns = [
    path('company', CompanyListCreateAPIView.as_view()),
    path('company-visible', CompanyVisibilityPatchAPIView.as_view()),
    path('edit-company/<int:id>', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    
    path('company-details', CompanyDetailsMixinView.as_view()),
    path('company-details/<int:company_id>', CompanyDetailsMixinView.as_view()),
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
    path('deductions-head/<int:company_id>', DeductionsHeadListCreateAPIView.as_view()),
    path('deductions-head/<int:company_id>/<int:id>', DeductionsHeadRetrieveUpdateDestroyAPIView.as_view()),

    # Use URLs like this from now on, separate for GET requests and POST request and don't use query params in POST request, only use them in GET requests
    path('employee-personal-detail/<int:company_id>', EmployeePersonalDetailListCreateView.as_view()),
    path('employee-personal-detail', EmployeePersonalDetailListCreateView.as_view()),
    path('employee-professional-detail', EmployeeProfessionalDetailCreateAPIView.as_view()),
    

    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/register/otp', VerifyOTPView.as_view(), name='otp'),
    
    path('auth/refresh/', RefreshView.as_view(), name='refresh'),
    path('auth/regular-register/', RegularRegisterListCreateAPIViewView.as_view()),
    path('regular', RegularRetrieveDestroyAPIView.as_view()),
    path('auth/password/reset/', PasswordResetAPIView.as_view(), name='password_reset'),
    # path('auth/password/reset/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('auth/password/reset-confirm/<uidb64>/<token>', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    # path('auth/reset_password_confirm/<str:uidb64>/<str:token>/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='api/password_reset_complete.html'), name='password_reset_complete')
    
]

