from django.forms import ValidationError
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, status, mixins, serializers
from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer, RegularRegisterSerializer, CategorySerializer, BankSerializer, LeaveGradeSerializer, ShiftSerializer, HolidaySerializer, EarningsHeadSerializer, EmployeePersonalDetailSerializer, EmployeeProfessionalDetailSerializer, EmployeeListSerializer, EmployeeSalaryEarningSerializer, EmployeeSalaryDetailSerializer, EmployeeFamilyNomineeDetialSerializer, EmployeePfEsiDetailSerializer, WeeklyOffHolidayOffSerializer, PfEsiSetupSerializer, CalculationsSerializer, EmployeeSalaryEarningUpdateSerializer, EmployeeShiftsSerializer, EmployeeShiftsUpdateSerializer, EmployeeAttendanceSerializer, EmployeeGenerativeLeaveRecordSerializer, EmployeeLeaveOpeningSerializer, EmployeeMonthlyAttendancePresentDetailsSerializer, EmployeeAdvancePaymentSerializer, EmployeeMonthlyAttendanceDetailsSerializer, EmployeeSalaryPreparedSerializer, EarnedAmountSerializer, SalaryOvertimeSheetSerializer, AttendanceReportsSerializer, EmployeeAttendanceBulkAutofillSerializer, BulkPrepareSalariesSerializer, MachineAttendanceSerializer, PersonnelFileReportsSerializer, DefaultAttendanceSerializer, EmployeeResignationSerializer, EmployeeUnresignSerializer, BonusCalculationSerializer, BonusPercentageSerializer, EmployeeProfessionalDetailRetrieveSerializer, EarnedAmountSerializerPreparedSalary, FullAndFinalSerializer, EmployeeELLeftSerializer, EmployeeYearlyBonusAmountSerializer, FullAndFinalReportSerializer, PfEsiReportsSerializer, RegularRetrieveUpdateSerializer, EmployeeVisibilitySerializer, AllEmployeeCurrentMonthAttendanceSerializer, SubUserOvertimeSettingsSerializer, SubUserMiscSettingsSerializer, TransferAttendanceFromOwnerToRegularSerializer, EmployeeStrengthReportsSerializer, EmployeeLeaveOpeningCreateUpdateSerializer, LeaveClosingTransferSerializer, EmployeeMonthlyMissPunchSerializer, EmployeeYearlyAdvanceTakenDeductedSerializer, AttendanceMachineConfigSerializer, EmployeeSalaryPreparedWithEarnedAmountSerializer
from .models import Company, CompanyDetails, User, OwnerToRegular, Regular, LeaveGrade, Shift, Holiday, EmployeeSalaryEarning, EarningsHead, EmployeeShifts, EmployeeGenerativeLeaveRecord, EmployeeSalaryPrepared, EarnedAmount, EmployeeAdvanceEmiRepayment, EmployeeAdvancePayment, EmployeeAttendance, EmployeeAttendanceOvertimeDetail, EmployeePersonalDetail, EmployeeProfessionalDetail, BonusCalculation, BonusPercentage, EmployeeSalaryDetail, FullAndFinal, Calculations, SubUserOvertimeSettings, EmployeeLeaveOpening, EmployeeMonthlyAttendanceDetails, employee_photo_handler
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound, PermissionDenied
from .auth.views import MyTokenObtainPairView
from django.db.models.functions import Lower
from rest_framework.parsers import MultiPartParser, FormParser
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db.models import Q
from datetime import datetime, timedelta, date
from dateutil.relativedelta import relativedelta
import pytz
import calendar
from django.db.models import Sum
from decimal import Decimal
import math
from .services.attendance_overtime import reclassify_many, replace_many_attendance_overtime
from fpdf import FPDF
from django.http import HttpResponse, StreamingHttpResponse
from .reports.generate_salary_sheet import generate_salary_sheet
from .reports.generate_payment_sheet import generate_payment_sheet
from .reports.generate_payment_sheet_as_per_compliance import generate_payment_sheet_as_per_compliance
from .reports.generate_attendance_register import generate_attendance_register
from .reports.generate_full_and_final_report import generate_full_and_final_report
from .reports.generate_payslip import generate_payslip
from .reports.generate_overtime_sheet import generate_overtime_sheet
from .reports.generate_advance_report import generate_advance_report
from .reports.generate_yearly_advance_report import generate_yearly_advance_report
from .reports.generate_present_report import generate_present_report
from .reports.generate_daily_attendance_report import generate_daily_attendance_report
from .reports.generate_absent_report import generate_absent_report
from .reports.generate_miss_punch_report import generate_miss_punch_report
from .reports.generate_bonus_calculation_sheet import generate_bonus_calculation_sheet
from .reports.generate_bonus_form_c import generate_bonus_form_c
from .reports.pf_esi_reports.generate_pf_statement import generate_pf_statement
from .reports.employee_strength_reports.generate_strength_report import generate_strength_report
from .reports.employee_strength_reports.generate_resign_report import generate_resign_report
from .reports.pf_esi_reports.generate_esi_statement_xlsx import generate_esi_statement_xlsx
from .reports.pf_esi_reports.generate_pf_statement_txt import generate_pf_statement_txt
from .reports.pf_esi_reports.generate_pf_exempt_xlsx import generate_pf_exempt_xlsx
from .reports.generate_form_14 import generate_form_14
from .reports.personnnel_file_forms.id_card.id_card_landscape import generate_id_card_landscape
from .reports.personnnel_file_forms.id_card.id_card_portrait import generate_id_card_portrait
from .reports.generate_overtime_sheet_daily import generate_overtime_sheet_daily
from .reports.personnnel_file_forms.personnnel_file_reports.generate_personnel_file_reports import generate_personnel_file_reports
from .reports.generate_payment_sheet_xlsx import generate_payment_sheet_xlsx
from .templates.master_entry.generate_add_edit_employee_using_excel_template import generate_add_edit_employee_using_excel_template
# from .reports.personnnel_file_reports.generate_application_form import generate_application_form
from itertools import groupby
from operator import attrgetter
import re
import time
from django.db.models import F, Value, CharField, Func, Exists, OuterRef
from .permissions import isOwnerAndAdmin
from .serializers import OvertimePolicySerializer
from .models import OvertimePolicy, EmployeeSalaryPreparedOvertimeDetail
from .services.overtime_policy import calculate_attendance_overtime, delete_overtime_policy
from .serializers import EmployeeSalaryPreparationRequestSerializer, SalaryOvertimePreviewSerializer, SalaryPreparationPreviewSerializer
from .services.salary_preparation import (
    bulk_prepare_salaries,
    prepare_employee_salary,
    preview_employee_overtime,
    preview_employee_salary,
    serialize_overtime_result,
)
# import sys
from django.db import connection, reset_queries 
from rest_framework.exceptions import APIException
from django.db.models import Case, When
from django.db.models import Prefetch

# from django.db import IntegrityError, transaction



# Create your views here.


def _calendar_attendance_scope(*, owner, company):
    account_ids = [owner.pk]
    account_ids.extend(
        OwnerToRegular.objects.filter(owner=owner).values_list('user_id', flat=True)
    )
    return EmployeeAttendance.objects.filter(company=company, user_id__in=account_ids)


def _reclassify_holiday_dates(*, owner, company, dates):
    if not dates:
        return
    attendances = _calendar_attendance_scope(owner=owner, company=company).filter(
        overtime_details__work_date__in=dates,
    ).distinct()
    if attendances.exists():
        reclassify_many(attendances=attendances, actor=owner)


def _is_employee_off_date(work_date, *, weekly_off, extra_off):
    weekday = work_date.strftime('%a').lower()
    occurrence = f'{weekday}{(work_date.day - 1) // 7 + 1}'
    return weekly_off == weekday or extra_off == occurrence


def _reclassify_employee_off_dates(*, owner, professional_detail, old_weekly_off, old_extra_off):
    details = EmployeeAttendanceOvertimeDetail.objects.filter(
        attendance__in=_calendar_attendance_scope(
            owner=owner,
            company=professional_detail.company,
        ),
        attendance__employee=professional_detail.employee,
    )
    affected_attendances = {
        detail.attendance.pk: detail.attendance
        for detail in details
        if (
            _is_employee_off_date(
                detail.work_date,
                weekly_off=old_weekly_off,
                extra_off=old_extra_off,
            )
            or _is_employee_off_date(
                detail.work_date,
                weekly_off=professional_detail.weekly_off,
                extra_off=professional_detail.extra_off,
            )
        )
    }
    if affected_attendances:
        reclassify_many(
            attendances=affected_attendances.values(),
            actor=owner,
        )

class NaturalOrdering(Func):
    function = 'CAST'
    template = '%(function)s(%(expressions)s AS CHAR)'

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.companies.all()
        print(Company.objects.filter(visible=True, user__in=OwnerToRegular.objects.filter(owner=user).values('user')))
        return user.regular_to_owner.owner.companies.filter(visible=True)
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            serializer.save(user=user)
        else:
            serializer.save(user=user.regular_to_owner.owner, visible=True)


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.companies.all()
        return user.regular_to_owner.owner.companies.filter(visible=True)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            serializer.save(user=user)
        else:
            serializer.save(user=user.regular_to_owner.owner)




class CompanyDetailsMixinView(generics.GenericAPIView,
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.ListModelMixin,
mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    # queryset = CompanyDetails.objects.all()
    serializer_class = CompanyEntrySerializer
    lookup_field = 'company'

    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companies_details.all()
        # instance = OwnerToRegular.objects.get(user=user)
        return user.regular_to_owner.owner.all_companies_details.filter(company__visible=True)
        

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request,  *args, **kwargs)
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        # instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=user.regular_to_owner.owner)
        
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        # instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=user.regular_to_owner.owner)


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DepartmentSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.departments.filter(company=company_id)
        return user.regular_to_owner.owner.departments.filter(company=company_id)

    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        return serializer.save(user=user.regular_to_owner.owner, company=company)
        

class DepartmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.departments.filter(company=company_id)
        return user.regular_to_owner.owner.departments.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return serializer.save(user=user.regular_to_owner.owner)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # Check if any employee is associated with the department
            associated_employees = EmployeeProfessionalDetail.objects.filter(department=instance)
            if associated_employees.exists():
                return Response({'error': 'Already assigned to employee(s)'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class DesignationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = DesignationSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.designations.filter(company=company_id)
        return user.regular_to_owner.owner.designations.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        return serializer.save(user=user.regular_to_owner.owner, company=company)


class DesignationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DesignationSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.designations.filter(company=company_id)
        return user.regular_to_owner.owner.designations.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return serializer.save(user=user.regular_to_owner.owner)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # Check if any employee is associated with the designation
            associated_employees = EmployeeProfessionalDetail.objects.filter(designation=instance)
            if associated_employees.exists():
                return Response({'error': 'Already assigned to employee(s)'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class SalaryGradeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalaryGradeSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.salary_grades.filter(company=company_id)
        return user.regular_to_owner.owner.salary_grades.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        return serializer.save(user=user.regular_to_owner.owner, company=company)

class SalaryGradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = SalaryGradeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.salary_grades.filter(company=company_id)
        return user.regular_to_owner.owner.salary_grades.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return serializer.save(user=user.regular_to_owner.owner)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # Check if any employee is associated with the designation
            associated_employees = EmployeeProfessionalDetail.objects.filter(salary_grade=instance)
            if associated_employees.exists():
                return Response({'error': 'Already assigned to employee(s)'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CategorySerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.categories.filter(company=company_id)
        return user.regular_to_owner.owner.categories.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        return serializer.save(user=user.regular_to_owner.owner, company=company)

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.categories.filter(company=company_id)
        return user.regular_to_owner.owner.categories.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return serializer.save(user=user.regular_to_owner.owner)
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            # Check if any employee is associated with the designation
            associated_employees = EmployeeProfessionalDetail.objects.filter(category=instance)
            if associated_employees.exists():
                return Response({'error': 'Already assigned to employee(s)'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class BankListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = BankSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.banks.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.banks.filter(company=company_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        name = serializer.validated_data.get('name').lower()
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name)
        if clashing_names.exists():
            error_message = "Bank grade with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class BankRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = BankSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.banks.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.banks.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        if clashing_names.exists():
            print(clashing_names)
            error_message = "Bank with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.role == "OWNER":
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)
            return Response(serializer.data, status=status.HTTP_200_OK)

class LeaveGradeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = LeaveGradeSerializer
    lookup_field = 'company_id'

    def get_company(self):
        if not hasattr(self, '_company'):
            user = self.request.user
            owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
            self._company = get_object_or_404(
                Company, pk=self.kwargs['company_id'], user=owner
            )
        return self._company

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.leave_grades.filter(company=company_id).prefetch_related('payable_earnings_heads')
        return user.regular_to_owner.owner.leave_grades.filter(company=company_id).prefetch_related('payable_earnings_heads')
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        try:
            serializer.save(user=user, company=self.get_company())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Leave Grade with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

class LeaveGradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = LeaveGradeSerializer
    lookup_field = 'id'

    def get_company(self):
        if not hasattr(self, '_company'):
            user = self.request.user
            owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
            self._company = get_object_or_404(
                Company, pk=self.kwargs['company_id'], user=owner
            )
        return self._company

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.leave_grades.filter(company=company_id).prefetch_related('payable_earnings_heads')
        return user.regular_to_owner.owner.leave_grades.filter(company=company_id).prefetch_related('payable_earnings_heads')
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=user, company=self.get_company())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Leave Grade with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)\

    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            if instance.mandatory_leave:
                return Response({"detail": "Cannot delete a mandatory leave grade."}, status=status.HTTP_403_FORBIDDEN)

            #Check if associated attendance or generative leave object exists
            associated_attendance = EmployeeAttendance.objects.filter(Q(first_half=instance) | Q(second_half=instance))
            if associated_attendance.exists():
                return Response({'error': 'Already used in attendance'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        

class ShiftListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShiftSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.shifts.filter(company=company_id)
        return user.regular_to_owner.owner.shifts.filter(company=company_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        company_id = self.kwargs.get('company_id')
        try:
            serializer.save(user=user, company_id=company_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Shift with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

    
class ShiftRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = ShiftSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        if user.role == "OWNER":
            return user.shifts.filter(company_id=company_id)
        # instance = OwnerToRegular.objects.get(user=user)
        return user.regular_to_owner.owner.shifts.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        company_id = self.kwargs.get('company_id')
        try:
            serializer.save(user=user, company_id=company_id)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Shift with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        try:
            associated_employee_shift = EmployeeShifts.objects.filter(shift=instance)
            if associated_employee_shift.exists():
                return Response({'error': 'Already used in Employee(s) Shift'}, status=status.HTTP_400_BAD_REQUEST)
            
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    
class HolidayListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = HolidaySerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.holidays.filter(company=company_id)
        return user.regular_to_owner.owner.holidays.filter(company=company_id)
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        company_id = self.kwargs.get('company_id')
        try:
            with transaction.atomic():
                holiday = serializer.save(user=user, company_id=company_id)
                if not Holiday.objects.filter(
                    user=user,
                    company=holiday.company,
                    date=holiday.date,
                ).exclude(pk=holiday.pk).exists():
                    _reclassify_holiday_dates(
                        owner=user,
                        company=holiday.company,
                        dates={holiday.date},
                    )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"error" : "Holiday with this name on this day already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    
class HolidayRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = HolidaySerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.holidays.filter(company=company_id)
        # instance = OwnerToRegular.objects.get(user=user)
        return user.regular_to_owner.owner.holidays.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)

        # Cheking if mandatory Holiday
        if instance.mandatory_holiday:
            return Response({"detail": "Cannot edit a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
        try:
            old_date = instance.date
            with transaction.atomic():
                holiday = serializer.save(user=user)
                affected_dates = set()
                if old_date != holiday.date:
                    for holiday_date in (old_date, holiday.date):
                        if not Holiday.objects.filter(
                            user=user,
                            company=holiday.company,
                            date=holiday_date,
                        ).exclude(pk=holiday.pk).exists():
                            affected_dates.add(holiday_date)
                _reclassify_holiday_dates(
                    owner=user,
                    company=holiday.company,
                    dates=affected_dates,
                )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            return Response({"error" : "Holiday with this name on this day already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            if instance.mandatory_holiday:
                return Response({"detail": "Cannot delete a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
            
            holiday_leave_grade = LeaveGrade.objects.filter(user=instance.user, name='HD', company=instance.company).first()
            associated_attendance_with_same_date = EmployeeAttendance.objects.filter(Q(date=instance.date) & (Q(first_half=holiday_leave_grade) | Q(second_half=holiday_leave_grade)))
            if associated_attendance_with_same_date.exists():
                return Response({'error': 'Already used in Employee(s) Attendance'}, status=status.HTTP_400_BAD_REQUEST)
            
            with transaction.atomic():
                owner = instance.user
                company = instance.company
                holiday_date = instance.date
                self.perform_destroy(instance)
                if not Holiday.objects.filter(
                    user=owner,
                    company=company,
                    date=holiday_date,
                ).exists():
                    _reclassify_holiday_dates(
                        owner=owner,
                        company=company,
                        dates={holiday_date},
                    )
            return Response(status=status.HTTP_204_NO_CONTENT)

        except ValidationError as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        
class EarningsHeadListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = EarningsHeadSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.earnings_heads.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.earnings_heads.filter(company=company_id)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        name = serializer.validated_data.get('name').lower()
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name)
        if clashing_names.exists():
            error_message = "Earnings Head with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class EarningsHeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EarningsHeadSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.earnings_heads.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.earnings_heads.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Cheking if mandatory Earning
        if instance.mandatory_earning:
            return Response({"detail": "Cannot edit a mandatory earning."}, status=status.HTTP_403_FORBIDDEN)
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        if clashing_names.exists():
            print(clashing_names)
            error_message = "Earnings Head with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.role == "OWNER":
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.mandatory_earning:
            print("yes")
            return Response({"detail": "Cannot delete a mandatory earning."}, status=status.HTTP_403_FORBIDDEN)
        # Perform deletion
        self.perform_destroy(instance)
        return Response({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)


class OvertimePolicyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OvertimePolicySerializer
    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.role != 'OWNER':
            raise PermissionDenied('Only owner accounts can manage overtime policies.')

    def get_company(self):
        if not hasattr(self, '_company'):
            self._company = get_object_or_404(Company, pk=self.kwargs['company_id'], user=self.request.user)
        return self._company

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        return OvertimePolicy.objects.filter(company=self.get_company()).prefetch_related('day_rules', 'selected_earning_heads__earnings_head')


class OvertimePolicyRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = OvertimePolicySerializer
    lookup_field = 'id'

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)
        if request.user.role != 'OWNER':
            raise PermissionDenied('Only owner accounts can manage overtime policies.')

    def get_company(self):
        if not hasattr(self, '_company'):
            self._company = get_object_or_404(Company, pk=self.kwargs['company_id'], user=self.request.user)
        return self._company

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        return OvertimePolicy.objects.filter(company=self.get_company()).prefetch_related('day_rules', 'selected_earning_heads__earnings_head')

    def delete(self, request, *args, **kwargs):
        policy = self.get_object()
        try:
            delete_overtime_policy(actor=request.user, company=self.get_company(), policy=policy)
        except ValidationError as exc:
            detail = getattr(exc, 'message_dict', None) or getattr(exc, 'messages', None)
            raise serializers.ValidationError(detail) from exc
        return Response(status=status.HTTP_204_NO_CONTENT)
         

# class DeductionsHeadListCreateAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     # queryset = Company.objects.all()
#     serializer_class = DeductionsHeadSerializer
#     lookup_field = 'company_id'

#     def get_queryset(self, *args, **kwargs):
#         company_id = self.kwargs.get('company_id')
#         user = self.request.user
#         if user.role == "OWNER":
#             return user.deductions_head.filter(company=company_id)
#         instance = OwnerToRegular.objects.get(user=user)
#         return instance.owner.deductions_head.filter(company=company_id)

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = self.request.user
#         company_id = self.kwargs.get('company_id')
#         company = Company.objects.get(id=company_id)
#         name = serializer.validated_data.get('name').lower()
        
#         # Check uniqueness
#         clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name)
#         if clashing_names.exists():
#             error_message = "Deductions Head with this name already exists."
#             return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

#         if user.role == "OWNER":
#             serializer.save(user=user, company=company)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             instance = OwnerToRegular.objects.get(user=user)
#             serializer.save(user=instance.owner, company=company)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
        

# class DeductionsHeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes= [IsAuthenticated]
#     serializer_class = DeductionsHeadSerializer
#     lookup_field = 'id'

#     def get_queryset(self, *args, **kwargs):
#         company_id = self.kwargs.get('company_id')
#         user = self.request.user
#         if user.role == "OWNER":
#             return user.deductions_head.filter(company=company_id)
#         instance = OwnerToRegular.objects.get(user=user)
#         return instance.owner.deductions_head.filter(company=company_id)
    
#     def update(self, request, *args, **kwargs):
#         user = self.request.user
#         instance = self.get_object()
#         serializer = self.get_serializer(instance, data=request.data)
#         serializer.is_valid(raise_exception=True)
#         name = serializer.validated_data.get('name').lower()

#         # Cheking if mandatory Deduction
#         if instance.mandatory_deduction:
#             return Response({"detail": "Cannot edit a mandatory deduction."}, status=status.HTTP_403_FORBIDDEN)
        
#         # Check uniqueness
#         clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
#         print(clashing_names)
#         if clashing_names.exists():
#             print(clashing_names)
#             error_message = "Deductions Head with this name already exists."
#             return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
#         if user.role == "OWNER":
#             serializer.save(user=self.request.user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#         else:
#             instance = OwnerToRegular.objects.get(user=user)
#             serializer.save(user=instance.owner)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
#     def destroy(self, request, *args, **kwargs):
#         instance = self.get_object()
#         if instance.mandatory_deduction:
#             print("yes")
#             return Response({"detail": "Cannot delete a mandatory deduction."}, status=status.HTTP_403_FORBIDDEN)
#         # Perform deletion
#         self.perform_destroy(instance)
#         return Response({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    

class EmployeePersonalDetailListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeePersonalDetailSerializer
    lookup_field = 'company_id'
    parser_classes = [CamelCaseMultiPartParser, CamelCaseFormParser]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return EmployeeListSerializer
        return EmployeePersonalDetailSerializer  # Use the default serializer for other methods

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            personal_details_list = user.employee_personal_details.filter(company=company_id)
        else:
            personal_details_list = user.regular_to_owner.owner.employee_personal_details.filter(company=company_id, visible=True)
        combined_queryset = personal_details_list.prefetch_related('employee_professional_detail', 'employee_pf_esi_detail')
        return combined_queryset


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        try:
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
                serializer.save(user=user, visible=True)
            else:
                serializer.save(user=user, visible=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            error_string = str(e)
            print(error_string)
            if "user_id" in error_string and "company_id" in error_string and "paycode" in error_string:
                error_message = {"paycode": "This Paycode already exists"}
            elif "user_id" in error_string and "company_id" in error_string and "attendance_card_no" in error_string:
                error_message = {"attendance_card_no": "This Attendance Card No. already exists"}
            else:
                error_message = {"error": "Some error occurred"}
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeePersonalDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeePersonalDetailSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
            return user.employee_personal_details.filter(company=company_id, visible=True)
        return user.employee_personal_details.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
            serializer.save(user=user)
        except IntegrityError as e:
            error_string = str(e)
            print(error_string)
            if "user_id" in error_string and "company_id" in error_string and "paycode" in error_string:
                error_message = {"paycode": "This Paycode already exists"}
            elif "user_id" in error_string and "company_id" in error_string and "attendance_card_no" in error_string:
                error_message = {"attendance_card_no": "This Attendance Card No. already exists"}
            else:
                error_message = {"error": "Some error occurred"}
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data, status=status.HTTP_200_OK)
        

class EmployeeProfessionalDetailListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeProfessionalDetailSerializer
    # lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companys_employee_professional_details.filter(company=company_id)
        return user.regular_to_owner.owner.all_companys_employee_professional_details.filter(company=company_id, employee__visible=True)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data['professional_detail'])
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner

        try:
            with transaction.atomic():
                professional_detail_created_instance = serializer.save(user=user)
                # Check if the ProfessionalDetail instance was created successfully
                if not professional_detail_created_instance:
                    raise IntegrityError("Failed to create ProfessionalDetail")

                shift_instance = EmployeeShifts.objects.create(
                    user=professional_detail_created_instance.user,
                    company=professional_detail_created_instance.company,
                    from_date=professional_detail_created_instance.date_of_joining,
                    to_date=date(9999, 1, 1),
                    employee=professional_detail_created_instance.employee,
                    shift_id=request.data['shift']
                )

                print(f"Shift Instance: {shift_instance}")

                return Response(serializer.data, status=status.HTTP_201_CREATED)

        except IntegrityError as e:
            # Handle integrity errors
            error_string = str(e)
            print(error_string)
            if "user_id" in error_string and "company_id" in error_string and "paycode" in error_string:
                error_message = {"paycode": "This Paycode already exists"}
            elif "user_id" in error_string and "company_id" in error_string and "attendance_card_no" in error_string:
                error_message = {"attendance_card_no": "This Paycode already exists"}
            else:
                error_message = {"error": "Some error occurred"}
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
            

class EmployeeProfessionalDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeProfessionalDetailSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companys_employee_professional_details.filter(company_id=company_id)
        return user.regular_to_owner.owner.all_companys_employee_professional_details.filter(company_id=company_id, employee__visible=True)
    
    @transaction.atomic
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        old_doj = instance.date_of_joining
        old_weekly_off = instance.weekly_off
        old_extra_off = instance.extra_off
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if 'date_of_joining' in validated_data:
            instance = self.get_queryset().filter(employee=validated_data['employee'])
            if old_doj != validated_data['date_of_joining']:
                earning_instances = EmployeeSalaryEarning.objects.filter(user=user, employee=validated_data['employee'], from_date=old_doj.replace(day=1))
                shift_instances = EmployeeShifts.objects.filter(user=user, employee=validated_data['employee'], from_date=old_doj)
                if len(shift_instances)>0:
                    shift = shift_instances[0]
                    shift.from_date=validated_data['date_of_joining']
                    shift.save()
                if len(earning_instances) > 0:
                    for earning in earning_instances:
                        earning.from_date=validated_data['date_of_joining'].replace(day=1)
                        earning.save()
                
                #Deleting Old Attendances if present
                employee_old_attendances = EmployeeAttendance.objects.filter(employee=validated_data['employee'], date__lt=validated_data['date_of_joining'])
                if employee_old_attendances.exists():
                    employee_old_attendances.delete()

                print(f"New DOJ: {validated_data['date_of_joining']} ")
                #Re-evaluating Weekly and Holiday Off
                if validated_data['date_of_joining']>old_doj:
                    EmployeeAttendance.objects.reevaluate_first_weekly_holiday_off_after_doj(user=request.user, employee=validated_data['employee'], date_of_joining=validated_data['date_of_joining'])
                    if OwnerToRegular.objects.filter(owner=user).exists():
                        EmployeeAttendance.objects.reevaluate_first_weekly_holiday_off_after_doj(user=user.owner_to_regular.user, employee=validated_data['employee'], date_of_joining=validated_data['date_of_joining'])
                
        professional_detail = serializer.save(user=user)
        if (
            professional_detail.weekly_off != old_weekly_off
            or professional_detail.extra_off != old_extra_off
        ):
            _reclassify_employee_off_dates(
                owner=user,
                professional_detail=professional_detail,
                old_weekly_off=old_weekly_off,
                old_extra_off=old_extra_off,
            )
        print(f"Validated Data: {validated_data}, Instance: {old_doj}")
        if 'date_of_joining' in validated_data and validated_data['date_of_joining']<old_doj:
            num_days_in_month = calendar.monthrange(validated_data['date_of_joining'].year, validated_data['date_of_joining'].month)[1]
            from_date = date(validated_data['date_of_joining'].year, validated_data['date_of_joining'].month, 1)
            to_date = date(validated_data['date_of_joining'].year, validated_data['date_of_joining'].month, num_days_in_month)
            print(f"From Date: {from_date} To Date: {to_date}")
            operation_result, message = EmployeeAttendance.objects.mark_default_attendance(from_date=from_date, to_date=to_date, company_id=validated_data['employee'].company.id, user=user)
            if OwnerToRegular.objects.filter(owner=user).exists():
                operation_result, message = EmployeeAttendance.objects.mark_default_attendance(from_date=from_date, to_date=to_date, company_id=validated_data['employee'].company.id, user=user.owner_to_regular.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EmployeeProfessionalDetailRetrieveAPIView(generics.RetrieveAPIView): #used in resignationApiSlice
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeProfessionalDetailRetrieveSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companys_employee_professional_details.filter(company_id=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_companys_employee_professional_details.filter(company_id=company_id)
    
        
class EmployeeSalaryEarningListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryEarningSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_earnings.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.all_employees_earnings.filter(company=company_id, employee=employee, employee__visible=True)

    def create(self, request, *args, **kwargs):
        print(request.data)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        employee_earnings = request.data['employee_earnings']
        for data in employee_earnings:
            earnings_head_id = data['earnings_head']
            print(f"Earnings Head ID: {earnings_head_id}")
            earnings_head_instance = EarningsHead.objects.get(pk=earnings_head_id)
            earnings_head_instance_data = EarningsHeadSerializer(earnings_head_instance).data
            data["earnings_head"] = earnings_head_instance_data
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            instance = self.get_queryset().filter(earnings_head_id=earnings_head_id)
            if instance.exists():
                print("nuuuuu")
                return Response({"error": "Salary Earnings Already Exists"}, status=status.HTTP_409_CONFLICT)
            else:
                validated_data['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
            new_earning = EmployeeSalaryEarning.objects.create(
                    user=user,
                    employee=validated_data['employee'],
                    company=validated_data['company'],
                    earnings_head_id=earnings_head_id,
                    value=validated_data['value'],
                    from_date=validated_data['from_date'],
                    to_date=validated_data['to_date']
                )
            print(new_earning)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def list(self, request, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        year = self.kwargs.get('year')
        user = self.request.user
        if user.role == "OWNER":
            queryset = user.all_employees_earnings.filter(
                company=company_id,
                employee=employee,
                from_date__year__lte=year,
                to_date__year__gte=year
            )
        else:
            # instance = OwnerToRegular.objects.get(user=user)
            queryset = user.regular_to_owner.owner.all_employees_earnings.filter(
                company=company_id,
                employee=employee,
                from_date__year__lte=year,
                to_date__year__gte=year,
                employee__visible=True
            )

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
           
        
class EmployeeSalaryEarningListUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeSalaryEarningUpdateSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_earnings.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.all_employees_earnings.filter(company=company_id, employee=employee, employee__visible=True)
    
    def update(self, request, *args, **kwargs):
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(indian_timezone)
        current_indian_year = current_datetime.year
        employee_earnings = request.data['employee_earnings']
        partial = kwargs.pop('partial', False)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        categorized_earnings = {}
        for earning_record in employee_earnings:
            earnings_head_id = earning_record['earnings_head']

            # If the earnings_head_id is not already a key in the categorized_earnings dictionary, add it
            if earnings_head_id not in categorized_earnings:
                categorized_earnings[earnings_head_id] = []

            # Append the earning record to the corresponding list based on earnings_head_id
            categorized_earnings[earnings_head_id].append(earning_record)

        for earnings_head_id, earning_records in categorized_earnings.items():
            serializer = self.get_serializer(data=earning_records, many=True)
            serializer.is_valid(raise_exception=True)
            validated_earning_records = serializer.validated_data

            sorted_earning_records = sorted(validated_earning_records, key=lambda x: x['from_date'])

            first_object = sorted_earning_records[0]
            last_object = sorted_earning_records[-1]

            existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')
            #Delete Childs
            existing_earnings.filter(from_date__gte=first_object['from_date'], to_date__lte=last_object['to_date']).delete()
            existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')

            #Checking if parent exists
            parent_queryset = existing_earnings.filter(from_date__lte=first_object['from_date'], to_date__gte=last_object['to_date'])
            if parent_queryset.exists():
                parent_instance = parent_queryset[0]
                print(f'this is parent info from date: {parent_instance.from_date}, to date: {parent_instance.to_date}')
                if parent_instance.from_date == first_object['from_date']:
                    if parent_instance.value == last_object['value']:
                        #infinity earning not required here
                        parent_instance.from_date = last_object['from_date']
                        parent_instance.save()
                        #Pop last object since value was same
                        sorted_earning_records.pop(-1)
                    else:
                        #Infinity Earning might be required here
                        if last_object['to_date'].year == current_indian_year and last_object['to_date'].month == 12:
                            print('time to set to infinity!!')
                            parent_queryset.delete()
                            sorted_earning_records[-1]['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                        else:
                            parent_instance.from_date = last_object['to_date'] + relativedelta(months=1)
                            parent_instance.save()
                            print(f'saved a parent whose from date was common with first object, here is parent info => from date: {parent_instance.from_date}, to date: {parent_instance.to_date}')

                    if len(sorted_earning_records)!=0:
                        print("here after infinity statement")
                        front_object_non_interfering_queryset = self.get_queryset().filter(earnings_head=earnings_head_id, to_date=(first_object['from_date'] - relativedelta(months=1)))
                        if front_object_non_interfering_queryset.exists():
                            front_object_non_interfering_instance = front_object_non_interfering_queryset[0]
                            if front_object_non_interfering_instance.value == first_object['value']:
                                front_object_non_interfering_instance.to_date = first_object['to_date']
                                front_object_non_interfering_instance.save()
                                sorted_earning_records.pop(0)
                                front_object_non_interfering_has_same_value = True
                        else:
                            print("something is wrong")

                elif parent_instance.to_date == last_object['to_date']:
                    #incoming earning will nerver have a to_date = "9999-01-01" so infinity object won't be made here
                    if parent_instance.value == first_object['value']:
                        parent_instance.to_date = first_object['to_date']
                        parent_instance.save()
                        #Pop first object since value was same
                        sorted_earning_records.pop(0)
                    else:
                        parent_instance.to_date = first_object['from_date'] - relativedelta(months=1)
                        parent_instance.save()
                        print(f'saved a parent whose to date was common with last object, here is parent info => from date: {parent_instance.from_date}, to date: {parent_instance.to_date}')

                    if len(sorted_earning_records)!=0:
                        end_object_non_interfering_queryset = self.get_queryset().filter(earnings_head=earnings_head_id, from_date=(last_object['to_date'] + relativedelta(months=1)))
                        if end_object_non_interfering_queryset.exists():
                            end_object_non_interfering_instance = end_object_non_interfering_queryset[0]
                            end_object_non_interfering_instance.from_date = last_object['from_date']
                            end_object_non_interfering_instance.save()
                            sorted_earning_records.pop(-1)
                        else:
                            print("something is wrong")

                else:
                    #Divide Parent into two
                    parent_original_value = parent_instance.value
                    parent_original_from_date = parent_instance.from_date
                    parent_original_to_date = parent_instance.to_date

                    #Create first half 
                    if parent_instance.value == first_object['value']:
                        parent_instance.to_date = first_object['to_date']
                        parent_instance.save()
                        #Pop first object since value was same
                        sorted_earning_records.pop(0)
                    else:
                        parent_instance.to_date = first_object['from_date'] - relativedelta(months=1)
                        parent_instance.save()
                        print(f'Saved 1st half of parent info is => from date: {parent_instance.from_date}, to date: {parent_instance.to_date}')

                    #Create 2nd half
                    #Inifinity Earning Could exist here
                    if parent_original_value == last_object['value']:
                        if len(sorted_earning_records)==0:
                            if last_object['to_date'].year == current_indian_year and last_object['to_date'].month == 12:
                                parent_instance.to_date = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                                parent_instance.save()
                            else:
                                parent_instance.to_date = parent_original_to_date
                                parent_instance.save()
                        else:
                            parent_second_half_from_date = last_object['from_date']
                            sorted_earning_records.pop(-1)
                    else:
                        if last_object['to_date'].year == current_indian_year and last_object['to_date'].month == 12:
                            sorted_earning_records[-1]['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                            print(f'Puting the sorted earning records to infity {sorted_earning_records[-1]}')
                        else:
                            parent_second_half_from_date = last_object['to_date'] + relativedelta(months=1)
                    if len(sorted_earning_records)!=0 and sorted_earning_records[-1]['to_date']!=datetime.strptime('9999-01-01', "%Y-%m-%d").date():
                        parent_second_half = EmployeeSalaryEarning.objects.create(
                        user=user,
                        employee=first_object['employee'],
                        company=first_object['company'],
                        earnings_head_id=earnings_head_id,
                        value=parent_original_value,
                        from_date=parent_second_half_from_date,
                        to_date=parent_original_to_date)
                        print(f'Saved 2nd half of parent info is => from date: {parent_second_half.from_date}, to date: {parent_second_half.to_date}')

                for sorted_earning_record in sorted_earning_records:
                    sorted_earning_record['user'] = user
                    print(sorted_earning_record)
                    EmployeeSalaryEarning.objects.create(**sorted_earning_record)

            else:
                front_object_interfering_has_same_value = False
                front_object_non_interfering_has_same_value = False
                #Checking if an existing earning is overlapping from the front
                front_object_interfering_queryset = existing_earnings.filter(from_date__lt=first_object['from_date'], to_date__gte=first_object['from_date'])
                if front_object_interfering_queryset.exists():
                    front_object_interfering_instance = front_object_interfering_queryset[0]
                    print(f'front object intering info => from date: {front_object_interfering_instance.from_date}, to date: {front_object_interfering_instance.to_date}')
                    print(f'front_object_interfering_instance value: {front_object_interfering_instance.value} and first object value: {first_object["value"]}')
                    if front_object_interfering_instance.value == first_object['value']:
                        front_object_interfering_instance.to_date = first_object['to_date']
                        front_object_interfering_instance.save()
                        sorted_earning_records.pop(0)
                        front_object_interfering_has_same_value = True
                        print('front interfering has same value')
                    else:
                        front_object_interfering_instance.to_date = first_object['from_date'] - relativedelta(months=1)
                        front_object_interfering_instance.save()
                else:
                    front_object_non_interfering_queryset = existing_earnings.filter(to_date=(first_object['from_date'] - relativedelta(months=1)))
                    if front_object_non_interfering_queryset.exists():
                        front_object_non_interfering_instance = front_object_non_interfering_queryset[0]
                        print(f'front object non interfering info => from date: {front_object_non_interfering_instance.from_date}, to date: {front_object_non_interfering_instance.to_date}')

                        if front_object_non_interfering_instance.value == first_object['value']:
                            front_object_non_interfering_instance.to_date = first_object['to_date']
                            front_object_non_interfering_instance.save()
                            sorted_earning_records.pop(0)
                            front_object_non_interfering_has_same_value = True
                            print('front non interfering has same value')
                    else:
                        print("something is wrong")

                #Checking if an existing earning is overlapping from the end
                end_object_interfering_queryset = existing_earnings.filter(from_date__lte=last_object['to_date'], to_date__gt=last_object['to_date'])
                if end_object_interfering_queryset.exists():
                    end_object_interfering_instance = end_object_interfering_queryset[0]
                    print(f'end object interfering info => from date: {end_object_interfering_instance.from_date}, to date: {end_object_interfering_instance.to_date}')
                    print(f'end_object_interfering_instance value: {end_object_interfering_instance.value} and last object value: {last_object["value"]}')
                    if end_object_interfering_instance.value == last_object['value']:
                        print('inside if of end object interfering instance whose value is same')
                        if len(sorted_earning_records) == 0:
                            # print(f"front interfering queryset: {front_object_interfering_queryset} and true? :{front_object_interfering_queryset.exists()}")
                            print(f'front interfering object has same value {front_object_interfering_has_same_value}')


                            # print(f"front non interfering queryset: {front_object_non_interfering_queryset} and true? :{front_object_non_interfering_queryset.exists()}")
                            print(f'front non interfering object has same value {front_object_non_interfering_has_same_value}')

                            print('lenght of sorted earinng records is 0')
                            if front_object_interfering_has_same_value:
                                print('front object interfering quryset exists')
                                front_object_interfering_instance.to_date = end_object_interfering_instance.to_date
                                end_object_interfering_queryset.delete()
                                front_object_interfering_instance.save()
                            elif front_object_non_interfering_has_same_value:
                                print('front object non interfering quryset exists')
                                front_object_non_interfering_instance.to_date = end_object_interfering_instance.to_date
                                end_object_interfering_queryset.delete()
                                front_object_non_interfering_instance.save()
                            
                        else:
                            end_object_interfering_instance.from_date = last_object['from_date']
                            end_object_interfering_instance.save()
                            sorted_earning_records.pop(-1)
                    else:
                        if last_object['to_date'].year == current_indian_year and last_object['to_date'].month == 12:
                            if len(sorted_earning_records) == 0:
                                if front_object_interfering_has_same_value:
                                    front_object_interfering_instance.to_date = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                                    print('about to delete 9999 earning')
                                    end_object_interfering_queryset.delete() #Deleting existing "9999-01-01" earning
                                    front_object_interfering_instance.save()
                                elif front_object_non_interfering_has_same_value:
                                    front_object_non_interfering_instance.to_date = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                                    end_object_interfering_queryset.delete() #Deleting existing "9999-01-01" earning
                                    print('about to delete 9999 earning in else block')
                                    front_object_non_interfering_instance.save()
                            else:
                                sorted_earning_records[-1]['to_date'] = "9999-01-01"
                                end_object_interfering_queryset.delete()
                        else:
                            end_object_interfering_instance.from_date = last_object['to_date'] + relativedelta(months=1)
                            end_object_interfering_instance.save()
                else:
                    #Infinity Earning will never exist here becuase this would mean it has to start from current year + 1 year which we don't want
                    end_object_non_interfering_queryset = existing_earnings.filter(from_date=(last_object['to_date'] + relativedelta(months=1)))
                    if end_object_non_interfering_queryset.exists():
                        end_object_non_interfering_instance = end_object_non_interfering_queryset[0]

                        if len(sorted_earning_records) == 0:
                            print(f'front interfering object has same value {front_object_interfering_has_same_value}')
                            print(f'front non interfering object has same value {front_object_non_interfering_has_same_value}')
                            if front_object_interfering_has_same_value:
                                front_object_interfering_instance.to_date = end_object_non_interfering_instance.to_date
                                end_object_non_interfering_instance.delete()
                                front_object_interfering_instance.save()
                            elif front_object_non_interfering_has_same_value:
                                front_object_non_interfering_instance.to_date = end_object_non_interfering_instance.to_date
                                end_object_non_interfering_queryset.delete()
                                front_object_non_interfering_instance.save()
                        elif end_object_non_interfering_instance.value == last_object['value']:
                            end_object_non_interfering_instance.from_date = last_object['from_date']
                            end_object_non_interfering_instance.save()
                            sorted_earning_records.pop(-1)
                    else:
                        print("something is wrong")


                for sorted_earning_record in sorted_earning_records:
                    sorted_earning_record['user'] = user
                    print(sorted_earning_record)
                    EmployeeSalaryEarning.objects.create(**sorted_earning_record)

        # print(categorized_earnings)
        return Response({"message": "Employee earnings updated successfully"}, status=status.HTTP_200_OK)


    
class EmployeeSalaryDetailListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryDetailSerializer
    lookup_field = 'company_id'

    def get_company(self):
        user = self.request.user
        owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
        return get_object_or_404(Company, pk=self.kwargs['company_id'], user=owner)

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_salary_details.filter(company=company_id)
        return user.regular_to_owner.owner.employee_salary_details.filter(company=company_id, employee__visible=True)


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            # try:
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
            serializer.save(user=user, company=self.get_company())
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_string = str(e)
            return Response({'overtimeRate': "Overtime Rate cannot be blank if overtime is allowed"}, status=status.HTTP_400_BAD_REQUEST)

        
class EmployeeSalaryDetailRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeSalaryDetailSerializer
    lookup_field = 'employee'

    def get_company(self):
        user = self.request.user
        owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
        return get_object_or_404(Company, pk=self.kwargs['company_id'], user=owner)

    def get_serializer_context(self):
        return {**super().get_serializer_context(), 'company': self.get_company()}

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_salary_details.filter(company=company_id)
        return user.regular_to_owner.owner.employee_salary_details.filter(company=company_id, employee__visible=True)
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
            serializer.save(user=user, company=self.get_company(), employee=instance.employee)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            error_string = str(e)
            return Response({'overtimeRate': "Overtime Rate cannot be blank if overtime is allowed"}, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeePfEsiDetailListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeePfEsiDetailSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_pf_esi_details.filter(company=company_id)
        return user.regular_to_owner.owner.employee_pf_esi_details.filter(company=company_id, employee__visible=True)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_string = str(e)
            print(error_string)
            return Response({'error': error_string}, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeePfEsiDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeePfEsiDetailSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_pf_esi_details.filter(company=company_id)
        return user.regular_to_owner.owner.employee_pf_esi_details.filter(company=company_id, employee__visible=True)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        serializer.save(user=user)

        return Response(serializer.data, status=status.HTTP_200_OK)

        
class EmployeeFamilyNomineeDetialListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeFamilyNomineeDetialSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_family_nominee_details.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.employee_family_nominee_details.filter(company=company_id, employee=employee, employee__visible=True)

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data['family_nominee_detail'], many=True)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            if user.role != "OWNER":
                user = user.regular_to_owner.owner
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
class EmployeeFamilyNomineeDetialRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeFamilyNomineeDetialSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_family_nominee_details.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.employee_family_nominee_details.filter(company=company_id, employee=employee, employee__visible=True)

    
    def update(self, request, *args, **kwargs):
        family_nominee_detail = request.data['family_nominee_detail']
        # partial = kwargs.pop('partial', False)
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner

        for data in family_nominee_detail:
            instance = self.get_queryset().filter(id=data['id'])
            serializer = self.get_serializer(instance.first(), data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
        
class WeeklyOffHolidayOffCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeeklyOffHolidayOffSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return serializer.save(user=user)
    
class WeeklyOffHolidayOffRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = WeeklyOffHolidayOffSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            return user.weekly_off_holiday_off_entries
        return user.regular_to_owner.owner.weekly_off_holiday_off_entries
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class PfEsiSetupCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PfEsiSetupSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
class PfEsiSetupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = PfEsiSetupSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_companies_pf_esi_setup_details
        # return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)            
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

class CalculationsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculationsSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    
class CalculationsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = CalculationsSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.calculations
        # return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            print(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)


class EmployeeShiftsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        queryset = self.get_queryset().filter(from_date__year__lte=year, to_date__year__gte=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class AllEmployeeMonthyShiftsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id)
        return user.regular_to_owner.owner.all_employees_shifts.filter(company=company_id)
    
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        start_date = datetime(year, month, 1).date()
        end_date = (start_date + relativedelta(months=1)) - relativedelta(days=1)
        queryset = self.get_queryset().filter(
            from_date__lte=end_date,  # Shifts that start before or in the specified year
            to_date__gte=start_date,    # Shifts that end in the specified year or later
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
    
class EmployeeShiftsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsUpdateSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return serializer.save(user=user.regular_to_owner.owner)

class EmployeeShiftsUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeShiftsUpdateSerializer
    lookup_field = 'employee'
    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        employee_shifts = request.data['employee_shifts']
        for shift in employee_shifts:
            serializer = self.get_serializer(data=shift)
            serializer.is_valid(raise_exception=True)
            validated_shift = serializer.validated_data
            EmployeeShifts.objects.process_employee_shifts(user=user, employee_shift_data=validated_shift)
        return Response({"message": "Employee earnings updated successfully"}, status=status.HTTP_200_OK)
    
class EmployeeShiftsPermanentUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeShiftsUpdateSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id, employee=employee)
        return user.regular_to_owner.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        employee_shift = request.data
        employee_shift['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
        serializer = self.get_serializer(data=employee_shift)
        serializer.is_valid(raise_exception=True)
        validated_shift = serializer.validated_data
        EmployeeShifts.objects.process_employee_permanent_shift(user=user, employee_shift_data=validated_shift)
        return Response({"message": "Employee earnings updated successfully"}, status=status.HTTP_200_OK)
    
    
class EmployeeAttendanceListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAttendanceSerializer

    def _authorized_scope(self, require_employee=False):
        actor = self.request.user
        owner = actor if actor.role == 'OWNER' else actor.regular_to_owner.owner
        company_id = self.kwargs['company_id']
        company = get_object_or_404(Company, id=company_id, user=owner)
        employee_id = self.kwargs.get('employee')
        employee = None
        if require_employee or employee_id is not None:
            employee = get_object_or_404(
                EmployeePersonalDetail,
                id=employee_id,
                company=company,
                user=owner,
            )
        return actor, company, employee

    @staticmethod
    def _validate_rows_scope(rows, company, employee):
        if not rows:
            raise serializers.ValidationError({'employee_attendance': 'At least one attendance row is required.'})
        months = set()
        for index, row in enumerate(rows):
            if 'company' in row and str(row['company']) != str(company.id):
                raise serializers.ValidationError({index: {'company': 'Company is bound by the URL.'}})
            if 'employee' in row and str(row['employee']) != str(employee.id):
                raise serializers.ValidationError({index: {'employee': 'Employee is bound by the URL.'}})
            if 'date' in row:
                try:
                    row_date = date.fromisoformat(str(row['date']))
                except (TypeError, ValueError):
                    continue
                months.add((row_date.year, row_date.month))
        if len(months) > 1:
            raise serializers.ValidationError({'date': 'One manual attendance request may cover only one calendar month.'})

    @staticmethod
    def _replacement_from(instance, validated_row):
        return {
            'attendance': instance,
            'intervals': validated_row.get('overtime_intervals', ()),
            'duration_entries': validated_row.get('overtime_duration_entries', ()),
            'source': 'MANUAL',
        }

    @staticmethod
    def _regenerate_months(actor, company, employee, months):
        for year, month in sorted(months):
            EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(
                user=actor,
                year=year,
                month=month,
                employee_id=employee.id,
                company_id=company.id,
            )

    def get_queryset(self, *args, **kwargs):
        actor, company, employee = self._authorized_scope()
        queryset = actor.all_employees_attendance.filter(company=company).prefetch_related('overtime_details')
        if employee is not None:
            queryset = queryset.filter(employee=employee)
        return queryset

    def create(self, request, *args, **kwargs):
        rows = request.data.get('employee_attendance', [])
        try:
            actor, company, employee = self._authorized_scope(require_employee=True)
            self._validate_rows_scope(rows, company, employee)
            for index, row in enumerate(rows):
                if 'overtime_intervals' not in row and 'overtime_duration_entries' not in row:
                    raise serializers.ValidationError({index: {'overtime_details': 'A complete overtime replacement is required.'}})
            serializer = self.get_serializer(data=rows, many=True)
            serializer.is_valid(raise_exception=True)
            months = {(item['date'].year, item['date'].month) for item in serializer.validated_data}
            with transaction.atomic():
                instances = serializer.save(user=actor, company=company, employee=employee)
                replace_many_attendance_overtime(
                    replacements=[
                        self._replacement_from(instance, validated_row)
                        for instance, validated_row in zip(instances, serializer.validated_data)
                    ],
                    actor=actor,
                )
                months.update(
                    (work_date.year, work_date.month)
                    for work_date in EmployeeAttendanceOvertimeDetail.objects.filter(
                        attendance__in=instances,
                    ).values_list('work_date', flat=True)
                )
                self._regenerate_months(actor, company, employee, months)
            instances = self.get_queryset().filter(
                date__in=[item.date for item in instances],
            ).prefetch_related('overtime_details')
            return Response(self.get_serializer(instances, many=True).data, status=status.HTTP_200_OK)
        except DjangoValidationError as exc:
            return Response({'error': getattr(exc, 'message_dict', exc.messages)}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        start_time = time.time()
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        from_date = datetime(year, month, 1).date() - relativedelta(days=6)
        last_day = calendar.monthrange(year, month)[1]
        to_date = datetime(year, month, last_day).date()
        queryset = self.get_queryset().filter(date__range=[from_date, to_date]).prefetch_related(None)
        attendance_rows = list(queryset.values(
            'id', 'user', 'employee', 'company', 'machine_in', 'machine_out', 'manual_in',
            'manual_out', 'first_half', 'second_half', 'date', 'ot_min', 'late_min',
            'manual_mode',
        ))
        attendance_ids_by_scope = {
            (row['employee'], row['date'], row['user']): row['id']
            for row in attendance_rows
        }

        overtime_details_by_attendance = {}
        exclusion_reason_labels = dict(EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES)
        overtime_details = EmployeeAttendanceOvertimeDetail.objects.filter(
            attendance__in=queryset
        ).values(
            'id', 'employee', 'attendance_date', 'user', 'company', 'work_date', 'day_type', 'source', 'start_datetime',
            'end_datetime', 'gross_minutes', 'excluded_minutes', 'eligible_minutes',
            'exclusion_reason', 'exclusion_note', 'created_at', 'updated_at',
        ).order_by('employee_id', 'attendance_date', 'user_id', 'company_id', 'id')
        for detail in overtime_details:
            attendance_date = detail.pop('attendance_date')
            attendance_id = attendance_ids_by_scope[(
                detail.pop('employee'),
                attendance_date,
                detail.pop('user'),
            )]
            detail.pop('company')
            detail['attendance'] = attendance_date
            detail['exclusion_reason_display'] = exclusion_reason_labels[detail['exclusion_reason']]
            overtime_details_by_attendance.setdefault(attendance_id, []).append(detail)

        for attendance in attendance_rows:
            attendance['overtime_details'] = overtime_details_by_attendance.get(attendance['id'], [])
            attendance.pop('user')

        return Response(attendance_rows)
        
class EmployeeAttendanceUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeAttendanceSerializer
    lookup_field = 'id'

    _authorized_scope = EmployeeAttendanceListCreateAPIView._authorized_scope
    _validate_rows_scope = staticmethod(EmployeeAttendanceListCreateAPIView._validate_rows_scope)
    _replacement_from = staticmethod(EmployeeAttendanceListCreateAPIView._replacement_from)
    _regenerate_months = staticmethod(EmployeeAttendanceListCreateAPIView._regenerate_months)

    def get_queryset(self, *args, **kwargs):
        actor, company, employee = self._authorized_scope(require_employee=True)
        return actor.all_employees_attendance.filter(company=company, employee=employee).prefetch_related('overtime_details')
    
    def update(self, request, *args, **kwargs):
        rows = request.data.get('employee_attendance', [])
        print("rows: ", rows)
        actor, company, employee = self._authorized_scope(require_employee=True)
        self._validate_rows_scope(rows, company, employee)
        row_dates = []
        for row in rows:
            try:
                row_dates.append(date.fromisoformat(str(row.get('date'))))
            except (TypeError, ValueError):
                raise serializers.ValidationError({'date': 'Every update row requires a valid attendance date.'})
        if len(row_dates) != len(set(row_dates)):
            raise serializers.ValidationError({'date': 'Every update row requires a unique attendance date.'})
        instances_by_date = {item.date: item for item in self.get_queryset().filter(date__in=row_dates)}
        if len(instances_by_date) != len(row_dates):
            raise NotFound('One or more attendance rows do not belong to the URL scope.')

        row_serializers = []
        for index, row in enumerate(rows):
            instance = instances_by_date[date.fromisoformat(str(row['date']))]
            replacement_supplied = 'overtime_intervals' in row or 'overtime_duration_entries' in row
            if not replacement_supplied and instance.ot_min and not instance.overtime_details.exists():
                return Response(
                    {'unbackfilled_overtime': {'row': index, 'attendance_id': instance.id}},
                    status=status.HTTP_409_CONFLICT,
                )
            if not replacement_supplied:
                raise serializers.ValidationError({index: {'overtime_details': 'A complete overtime replacement is required.'}})
            serializer = self.get_serializer(instance, data=row)
            serializer.is_valid(raise_exception=True)
            row_serializers.append(serializer)

        months = {(item.date.year, item.date.month) for item in instances_by_date.values()}
        months.update(
            (work_date.year, work_date.month)
            for work_date in EmployeeAttendanceOvertimeDetail.objects.filter(
                attendance__in=instances_by_date.values(),
            ).values_list('work_date', flat=True)
        )
        months.update(
            (serializer.validated_data['date'].year, serializer.validated_data['date'].month)
            for serializer in row_serializers
        )
        try:
            with transaction.atomic():
                updated = [serializer.save(user=actor, company=company, employee=employee) for serializer in row_serializers]
                replace_many_attendance_overtime(
                    replacements=[
                        self._replacement_from(instance, serializer.validated_data)
                        for instance, serializer in zip(updated, row_serializers)
                    ],
                    actor=actor,
                )
                months.update(
                    (work_date.year, work_date.month)
                    for work_date in EmployeeAttendanceOvertimeDetail.objects.filter(
                        attendance__in=updated,
                    ).values_list('work_date', flat=True)
                )
                self._regenerate_months(actor, company, employee, months)
        except DjangoValidationError as exc:
            return Response({'error': getattr(exc, 'message_dict', exc.messages)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(self.get_serializer(updated, many=True).data, status=status.HTTP_200_OK)
                
class EmployeeAttendanceBulkAutoFillView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = EmployeeAttendanceBulkAutofillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
        company = get_object_or_404(Company, id=validated_data['company'], user=owner)
        if user.role == 'REGULAR' and not company.visible:
            raise PermissionDenied('Company is not available to this account.')
        num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
        if validated_data['month_to_date']>num_days_in_month:
            validated_data['month_to_date'] = num_days_in_month
        from_date = date(validated_data['year'], validated_data['month'], validated_data['month_from_date'])
        to_date = date(validated_data['year'], validated_data['month'], validated_data['month_to_date'])

        try:
            EmployeeAttendance.objects.bulk_autofill(
                from_date=from_date,
                to_date=to_date,
                company_id=company.id,
                user=user,
                employee_ids=validated_data['employee_ids'],
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(getattr(exc, 'message_dict', exc.messages)) from exc
        return Response({"message": "Bulk autofill successful"}, status=status.HTTP_200_OK)


class EmployeeGenerativeLeaveRecordListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeGenerativeLeaveRecordSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        # if user.role == "OWNER":
        return user.all_company_employees_generative_leave_record.filter(company=company_id, date__year=year)
        
class EmployeeMonthlyAttendancePresentDetailsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeMonthlyAttendancePresentDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        # if user.role == "OWNER":
        return user.all_company_employees_monthly_attendance_details.filter(company=company_id, date__year=year)
            
class EmployeeMonthlyAttendanceDetailsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeMonthlyAttendanceDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        # if user.role == "OWNER":
        return user.all_company_employees_monthly_attendance_details.filter(company=company_id, date__year=year)

class EmployeeLeaveOpeningListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeLeaveOpeningSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        # if user.role == "OWNER":
        return user.all_company_employees_leave_openings.filter(company=company_id, year=year)

class EmployeeLeaveOpeningCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(request.data)
        serializer = EmployeeLeaveOpeningCreateUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        print(validated_data)
        for leave_opening in validated_data['leave_openings']:
            if leave_opening['leave_count'] != 0:
                print(leave_opening)
                obj, created = EmployeeLeaveOpening.objects.update_or_create(
                    user=user,
                    employee=leave_opening['employee'],
                    year=validated_data['year'],
                    leave=leave_opening['leave'],
                    defaults={"leave_count": leave_opening['leave_count']},
                    create_defaults={"user": user, "employee": leave_opening['employee'], "year": validated_data['year'], "leave": leave_opening['leave'], "leave_count": leave_opening['leave_count'], "company_id": validated_data['company']},
                )
            else:
                EmployeeLeaveOpening.objects.filter(user=user, employee=leave_opening['employee'], year=validated_data['year'], leave=leave_opening['leave']).delete()

        return Response({"message": "successful"}, status=status.HTTP_200_OK)

class LeaveClosingTransferCreateUpdateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(request.data)
        serializer = LeaveClosingTransferSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        year = validated_data['from_year']
        start_date = datetime(year, 1, 1)
        end_date = datetime(year, 12, 31)
        for employee_id in validated_data["employee_ids"]:
            #Getting Yearly Present Count
            monthly_attendance_details = EmployeeMonthlyAttendanceDetails.objects.filter(user=user, employee_id=employee_id, company_id=validated_data['company'], date__range=[start_date, end_date]).order_by('date') 
            present_count = 0 
            if monthly_attendance_details.exists():
                for monthly_detail in monthly_attendance_details:
                    present_count += monthly_detail.present_count

            #Calculating leaves earned
            for leave_id in validated_data['leave_ids']:
                leave = LeaveGrade.objects.get(id=leave_id)
                leaves_earned = present_count//leave.generate_frequency
                leaves_availed = EmployeeGenerativeLeaveRecord.get_yearly_leave_count(user, validated_data['from_year'], leave_id, employee_id)
                leave_opening = EmployeeLeaveOpening.objects.filter(user=user, employee_id=employee_id, company_id=validated_data['company'], leave=leave, year=validated_data['from_year'])
                if not leave_opening.exists():
                    leave_opening=0
                else:
                    print(f'Length of queryset: {len(leave_opening)}')
                    leave_opening = leave_opening.first().leave_count
                
                next_year_leave_opening = leave_opening+leaves_earned-leaves_availed
                if next_year_leave_opening != 0:
                    print(leave_opening)
                    obj, created = EmployeeLeaveOpening.objects.update_or_create(
                        user=user,
                        employee_id=employee_id,
                        year=validated_data['from_year']+1,
                        leave=leave,
                        defaults={"leave_count": next_year_leave_opening},
                        create_defaults={"user": user, "employee_id": employee_id, "year": validated_data['from_year']+1, "leave": leave, "leave_count": next_year_leave_opening, "company_id": validated_data['company']},
                    )
                else:
                    EmployeeLeaveOpening.objects.filter(user=user, employee_id=employee_id, year=validated_data['from_year']+1, leave=leave).delete()


                print(f'Leave Name: {leave.name} Leaves Earned: {leaves_earned} Present Count: {present_count} Leaves Availed: {leaves_availed} Leave Opening:{leave_opening}, Leave Opening Next Year:{leave_opening+leaves_earned-leaves_availed}')
        print(validated_data)
        return Response({"message": "Successful"}, status=status.HTTP_200_OK)

            
class EmployeeAdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAdvancePaymentSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee_id = self.kwargs.get('employee_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user = user.regular_to_owner.owner
        return user.all_company_employees_advance_payments.filter(company=company_id, employee=employee_id)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data['employee_advance_details'], many=True)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            if user.role != "OWNER":
                user = user = user.regular_to_owner.owner
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        user = request.user
        queryset = self.get_queryset(request)
        serializer = self.get_serializer(queryset, many=True)
        if user.role != 'OWNER':
            print(f"Not owner")
            for row in serializer.data:
                emi_repayments = EmployeeAdvanceEmiRepayment.objects.filter(employee_advance_payment=row['id'], user=user)
                total_repaid_amount = 0
                if emi_repayments.exists():
                    total_repaid_amount = emi_repayments.aggregate(total_amount=Sum('amount')).get('total_amount', 0)
                row['repaid_amount'] = total_repaid_amount
        return Response(serializer.data, status=status.HTTP_200_OK)

class EmployeeAdvancePaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeAdvancePaymentSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee_id = self.kwargs.get('employee_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user = user.regular_to_owner.owner
        # if user.role == "OWNER":
        return user.all_company_employees_advance_payments.filter(company=company_id, employee=employee_id)

    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            if user.role != "OWNER":
                user = user = user.regular_to_owner.owner
            employee_advance_details = request.data['employee_advance_details']
            for detail in employee_advance_details:
                instance = self.get_queryset().filter(id=detail['id'])
                serializer = self.get_serializer(instance.first(), data=detail)
                serializer.is_valid(raise_exception=True)
                serializer.save(user=user)
            return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Some Error Occured")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, *args, **kwargs):
        try:        
            user = self.request.user
            if user.role != "OWNER":
                user = user = user.regular_to_owner.owner
            ids_to_delete = self.kwargs.get('ids')
            ids_to_delete = ids_to_delete.split(',')
            print(ids_to_delete)
            queryset = self.get_queryset()
            for id in ids_to_delete:
                instance = queryset.filter(id=int(id)).first()
                if instance:
                    # Check if the user has permission to delete this instance
                    if user.role == "OWNER":
                        instance.delete()
                else:
                    return Response({"detail": f"Detail with ID {id} not found"}, status=status.HTTP_404_NOT_FOUND)
            return Response({"detail": "Deleted successfully"}, status=status.HTTP_200_OK)
        
        except Exception as e:
            print("Some Error Occurred")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class AllEmployeeSalaryEarningListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryEarningSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_employees_earnings.filter(company=company_id)
        
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        queryset = self.get_queryset().filter(from_date__year__lte=year, to_date__year__gte=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        
class SalaryOvertimePreviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SalaryOvertimePreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        result = preview_employee_overtime(actor=request.user, **{
            'company_id': serializer.validated_data['company'],
            'employee_id': serializer.validated_data['employee'],
            'year': serializer.validated_data['year'],
            'month': serializer.validated_data['month'],
        })
        return Response(serialize_overtime_result(result, include_diagnostics=True))


class SalaryPreparationPreviewAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = SalaryPreparationPreviewSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inputs = serializer.validated_data
        return Response(preview_employee_salary(
            actor=request.user,
            company_id=inputs['company'],
            employee_id=inputs['employee'],
            year=inputs['year'],
            month=inputs['month'],
            parent_inputs={
                'incentive_amount': inputs['incentive_amount'],
                'advance_deducted': inputs['advance_deducted'],
                'vpf_deducted': inputs['vpf_deducted'],
                'tds_deducted': inputs['tds_deducted'],
                'others_deducted': inputs['others_deducted'],
            },
            arrear_inputs=inputs['arrears'],
        ))


class EmployeeSalaryPreparedCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryPreparationRequestSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        parent = serializer.validated_data['employee_salary_prepared']
        period = parent['date']
        result = prepare_employee_salary(
            actor=request.user,
            company_id=parent['company'],
            employee_id=parent['employee'],
            year=period.year,
            month=period.month,
            parent_inputs=parent,
            earned_inputs=serializer.validated_data['all_earned_amounts'],
        )
        return Response({
            'salary': EmployeeSalaryPreparedWithEarnedAmountSerializer(result.salary).data,
            'overtime': serialize_overtime_result(result.overtime_result),
        }, status=status.HTTP_200_OK)
        
class EmployeeSalaryPreparedListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryPreparedSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        return user.all_company_employees_salaries_prepared.filter(company=company_id)
        
    def list(self, request, *args, **kwargs):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        date_obj = date(year, month, 1)
        queryset = self.get_queryset().filter(date=date_obj)
        serializer = self.get_serializer(queryset, many=True)
        print(f'RUnning slaary prepared: {queryset}')
        return Response(serializer.data)


class EmployeeSalaryPreparedRetrieveAPIView(generics.RetrieveAPIView): #Add entry in urls.py for this
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryPreparedWithEarnedAmountSerializer

    def get_queryset(self):
        """Base queryset filtered by company and user permissions"""
        company_id = self.kwargs['company_id']
        return self.request.user.all_company_employees_salaries_prepared.filter(company_id=company_id)

    def get_object(self):
        """Retrieve specific salary record using URL parameters"""
        queryset = self.get_queryset()
        
        try:
            employee_id = self.kwargs['employee_id']
            month = self.kwargs['month']
            year = self.kwargs['year']
            date_filter = date(year, month, 1)
        except (ValueError, KeyError) as e:
            raise NotFound("Invalid URL parameters") from e

        obj = queryset.filter(
            employee_id=employee_id,
            date__month=month,
            date__year=year
        ).first()

        if not obj:
            raise NotFound("No salary record found for the given parameters")
            
        return obj
        
class BulkPrepareSalariesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = BulkPrepareSalariesSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        results = bulk_prepare_salaries(
            actor=request.user,
            company_id=validated_data['company'],
            month=validated_data['month'],
            year=validated_data['year'],
            employee_ids=validated_data.get('employee_ids'),
        )
        salary_ids = [result.salary.pk for result in results]
        salary_by_id = {
            salary.pk: salary
            for salary in EmployeeSalaryPrepared.objects.filter(pk__in=salary_ids).prefetch_related(
                'overtime_breakdown',
                'current_salary_earned_amounts__earnings_head',
            )
        }
        salaries = [salary_by_id[salary_id] for salary_id in salary_ids]
        return Response({
            'message': 'Bulk Prepare Salaries successful',
            'prepared_count': len(results),
            'salaries': [
                EmployeeSalaryPreparedWithEarnedAmountSerializer(salary).data
                for salary in salaries
            ],
        }, status=status.HTTP_200_OK)

class SalaryOvertimeSheetCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalaryOvertimeSheetSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        # if user.role != "OWNER":
        #     user = OwnerToRegular.objects.get(user=user).owner

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        print(validated_data)
        employee_ids = validated_data["employee_ids"]

        if validated_data['report_type'] == 'salary_sheet':
            salary_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)
            employee_salaries = EmployeeSalaryPrepared.objects.filter(user=user, employee__id__in=employee_ids, date=salary_date)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode" and validated_data['filters']['group_by'] == 'none':
                employee_salaries = sorted(employee_salaries, key=lambda x: (re.sub(r'[^A-Za-z]', '', x.employee.paycode), int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employee_salaries = employee_salaries.order_by(*order_by)

            if len(employee_salaries) != 0:
                response = StreamingHttpResponse(generate_salary_sheet(request.user, serializer.validated_data, employee_salaries), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Salary Prepared for the given month"}, status=status.HTTP_404_NOT_FOUND)
        
        if validated_data['report_type'] == 'payment_sheet':
            print(f"Validated Data: {validated_data['filters']['format']}")
            salary_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)
            employee_salaries = EmployeeSalaryPrepared.objects.filter(user=request.user, employee__id__in=employee_ids, date=salary_date)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employee_salaries = sorted(employee_salaries, key=lambda x: (
                    (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.employee.paycode), int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employee_salaries = employee_salaries.order_by(*order_by)

            if len(employee_salaries) != 0 and validated_data['filters']['format']=='pdf':
                response = StreamingHttpResponse(generate_payment_sheet(request.user, serializer.validated_data, employee_salaries), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            elif len(employee_salaries) != 0 and validated_data['filters']['format']=='xlsx':
                response = StreamingHttpResponse(generate_payment_sheet_xlsx(request.user, serializer.validated_data, employee_salaries), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
                return response
            else:
                return Response({"detail": "No Salary Prepared for the given month"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'payment_sheet_as_per_compliance':
            if request.user.role != 'OWNER':
                return Response({"detail": "Not Allowed"}, status=status.HTTP_403_FORBIDDEN)
            print(f"Validated Data: {validated_data['filters']['format']}")
            salary_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee_professional_detail__department',)


            """
            Query below filters the employee who have owner_salary (mandatory) and also retrieves their regular account salary
            """
            employees = EmployeePersonalDetail.objects.annotate(
                has_owner_salary=Exists(
                    EmployeeSalaryPrepared.objects.filter(
                        employee=OuterRef('pk'),
                        date=salary_date,
                        user=request.user
                    )
                )
            ).filter(
                has_owner_salary=True,  # Only include employees with owner salary
                id__in=employee_ids
            ).prefetch_related(
                Prefetch(
                    'salaries_prepared',  # Related name from EmployeePersonalDetail to EmployeeSalaryPrepared
                    queryset=EmployeeSalaryPrepared.objects.filter(
                        date=salary_date, user=request.user  # Owner's salaries
                    ),
                    to_attr='owner_salary'  # Custom attribute for owner's salaries
                ),
                Prefetch(
                    'salaries_prepared',  # Related name from EmployeePersonalDetail to EmployeeSalaryPrepared
                    queryset=EmployeeSalaryPrepared.objects.filter(
                        date=salary_date
                    ).exclude(user=request.user),  # Regular account salaries
                    to_attr='regular_account_salary'  # Custom attribute for regular account salaries
                )
            )

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (
                    (getattr(x.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.paycode), 
                    int(re.sub(r'[^0-9]', '', x.paycode))))
            else:
                employees = employees.order_by(*order_by)

            if len(employees) != 0: #Add this later "and validated_data['filters']['format']=='pdf'" when creating xlsx format too
                response = StreamingHttpResponse(generate_payment_sheet_as_per_compliance(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            # elif len(employee_salaries) != 0 and validated_data['filters']['format']=='xlsx':
            #     response = StreamingHttpResponse(generate_payment_sheet_xlsx(request.user, serializer.validated_data, employee_salaries), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
            #     response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
            #     return response
            else:
                return Response({"detail": "Employee Selected does NOT have Salary Prepared."}, status=status.HTTP_404_NOT_FOUND)



        if validated_data['report_type'] == 'payslip':
            payslip_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            employee_salaries = EmployeeSalaryPrepared.objects.filter(user=request.user, employee__id__in=employee_ids, date=payslip_date)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employee_salaries = sorted(employee_salaries, key=lambda x: (re.sub(r'[^A-Za-z]', '', x.employee.paycode), int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employee_salaries = employee_salaries.order_by(*order_by)

            if len(employee_salaries) != 0:
                response = StreamingHttpResponse(generate_payslip(request.user, serializer.validated_data, employee_salaries), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Salary Prepared for the given month"}, status=status.HTTP_404_NOT_FOUND)

        
        if validated_data['report_type'] == 'overtime_sheet':
            overtime_sheet_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            employee_salaries = EmployeeSalaryPrepared.objects.filter(user=request.user, employee__id__in=employee_ids, date=overtime_sheet_date, net_ot_amount_monthly__gt=0)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employee_salaries = sorted(employee_salaries, key=lambda x: (re.sub(r'[^A-Za-z]', '', x.employee.paycode), int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employee_salaries = employee_salaries.order_by(*order_by)

            if len(employee_salaries) != 0:
                response = StreamingHttpResponse(generate_overtime_sheet(request.user, serializer.validated_data, employee_salaries), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Overtime for any Employee in the given month"}, status=status.HTTP_404_NOT_FOUND)
            
        if validated_data['report_type'] == 'advance_report':
            advance_report_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            employee_salaries = EmployeeSalaryPrepared.objects.filter(user=request.user, employee__id__in=employee_ids, date=advance_report_date, advance_deducted__gt=0)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employee_salaries = sorted(employee_salaries, key=lambda x: (
                    (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                    int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employee_salaries = employee_salaries.order_by(*order_by)

            if len(employee_salaries) != 0:
                response = StreamingHttpResponse(generate_advance_report(request.user, serializer.validated_data, employee_salaries), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No advance was deducted for any Employee in the given month"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'yearly_advance_report':
            advance_report_date = date(validated_data["year"], validated_data["month"], 1)
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)
            # if validated_data['filters']['group_by'] != 'none':
            #     if order_by != None:
            #         order_by = ('employee__employee_professional_detail__department', *order_by)
            #     else:
            #         order_by = ('employee__employee_professional_detail__department',)
            #
            #employee_salaries = EmployeeSalaryPrepared.objects.filter(user=request.user, employee__id__in=employee_ids, date=advance_report_date, advance_deducted__gt=0)
            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (
                    (getattr(x.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.paycode), 
                    int(re.sub(r'[^0-9]', '', x.paycode))))

                sorted_employee_ids = [employee.id for employee in employees]
                print(sorted_employee_ids)
                preserved = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(sorted_employee_ids)])
                employees = EmployeePersonalDetail.objects.filter(id__in=sorted_employee_ids).order_by(preserved)
                print(employees)

            else:
                employees = employees.order_by(*order_by)

            if len(employees) != 0:
                response = StreamingHttpResponse(generate_yearly_advance_report(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No advance was deducted for any Employee in the given month"}, status=status.HTTP_404_NOT_FOUND)




        # return Response({"message": "Payslip successful"}, status=status.HTTP_200_OK)
        print('idk')
        return Response({"detail": "No Report was selected"}, status=status.HTTP_400_BAD_REQUEST)

class PersonnelFileReportsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PersonnelFileReportsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(request.data)
        validated_data = serializer.validated_data
        print(validated_data)

        employee_ids = validated_data["employee_ids"]

        if validated_data['report_type'] == 'personnel_file_reports':
            # if 'biodata' in validated_data['filters']['personnel_file_reports_selected']:
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            # if validated_data['filters']['group_by'] != 'none':
            #     order_by = ('employee__employee_professional_detail__department',)
            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (re.sub(r'[^A-Za-z]', '', x.paycode), int(re.sub(r'[^0-9]', '', x.paycode))))
            else:
                employees = employees.order_by(*order_by)

            if len(employees) != 0:
                response = StreamingHttpResponse(generate_personnel_file_reports(serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Employee Selected or Found"}, status=status.HTTP_404_NOT_FOUND)
                
        if validated_data['report_type'] == 'id_card':
            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids)
            if validated_data["filters"]["orientation"] == "landscape":
                response = StreamingHttpResponse(generate_id_card_landscape(serializer.validated_data, employees), content_type="application/pdf")
            elif validated_data["filters"]["orientation"] == "portrait":
                response = StreamingHttpResponse(generate_id_card_portrait(serializer.validated_data, employees), content_type="application/pdf")
            else:
                Response({"detail": "Wrong Orientation"}, status=status.HTTP_400_BAD_REQUEST)
            response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
            return response

        return Response({"message": "Payslip successful"}, status=status.HTTP_200_OK)

class AttendanceReportsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceReportsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        validated_data = serializer.validated_data
        employee_ids = validated_data["employee_ids"]

        if validated_data['report_type'] == 'attendance_register':
            # date_range_query = Q(date__year=validated_data['year'], date__month=validated_data['month'])
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee_professional_detail__department',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        (getattr(x.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
                sorted_employee_ids = [employee.id for employee in employees]
                # Use the sorted IDs to get the queryset in the correct order
                preserved = Case(*[When(id=pk, then=pos) for pos, pk in enumerate(sorted_employee_ids)])
                employees = EmployeePersonalDetail.objects.filter(id__in=sorted_employee_ids).order_by(preserved)
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0:
                response = StreamingHttpResponse(generate_attendance_register(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Attendances Found for the given month"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'daily_attendance_report':
            num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
            if validated_data['filters']['date']> num_days_in_month:
                return Response({"detail": "Invalid Date"}, status=status.HTTP_400_BAD_REQUEST)

            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            employees_attendances = EmployeeAttendance.objects.filter(
                date=date(validated_data['year'], validated_data['month'], validated_data['filters']['date']),
                company_id=validated_data['company'],
                user=request.user
            )

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees_attendances = sorted(
                    employees_attendances, 
                    key=lambda x: (
                        (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                        int(re.sub(r'[^0-9]', '', x.employee.paycode))
                    )
                )
            else:
                employees_attendances = employees_attendances.order_by(*order_by)

            if len(employees_attendances) !=0:
                response = StreamingHttpResponse(generate_daily_attendance_report(serializer.validated_data, employees_attendances), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Attendace found on this date"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'present_report':
            num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
            if validated_data['filters']['date']> num_days_in_month:
                return Response({"detail": "Invalid Date"}, status=status.HTTP_400_BAD_REQUEST)

            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            present_employees_attendances = EmployeeAttendance.objects.filter(
                (Q(manual_in__isnull=False) |
                Q(manual_out__isnull=False) |
                Q(machine_in__isnull=False) |
                Q(machine_out__isnull=False)),
                date=date(validated_data['year'], validated_data['month'], validated_data['filters']['date']),
                company_id=validated_data['company'],
                user=request.user
            )
            print(len(present_employees_attendances))

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                present_employees_attendances = sorted(
                    present_employees_attendances, 
                    key=lambda x: (
                        (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                        int(re.sub(r'[^0-9]', '', x.employee.paycode))
                    )
                )
            else:
                present_employees_attendances = present_employees_attendances.order_by(*order_by)

            if len(present_employees_attendances) !=0:
                print('inside the if')
                response = StreamingHttpResponse(generate_present_report(serializer.validated_data, present_employees_attendances), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Employee Present on this date"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'absent_report':
            num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
            if validated_data['filters']['date']> num_days_in_month:
                return Response({"detail": "Invalid Date"}, status=status.HTTP_400_BAD_REQUEST)

            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            absent_employees_attendances = EmployeeAttendance.objects.filter(
                first_half__name='A',
                second_half__name='A',
                date=date(validated_data['year'], validated_data['month'], validated_data['filters']['date']),
                company_id=validated_data['company'],
                user=request.user
            )
            print(len(absent_employees_attendances))

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                absent_employees_attendances = sorted(
                    absent_employees_attendances, 
                    key=lambda x: (
                        (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                        int(re.sub(r'[^0-9]', '', x.employee.paycode))
                    )
                )
            else:
                absent_employees_attendances = absent_employees_attendances.order_by(*order_by)

            if len(absent_employees_attendances) !=0:
                print('inside the if')
                response = StreamingHttpResponse(generate_absent_report(serializer.validated_data, absent_employees_attendances), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Employee Absent on this date"}, status=status.HTTP_404_NOT_FOUND)




        if validated_data['report_type'] == 'overtime_sheet_daily':
            if request.user.role != 'OWNER':
                return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
            num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
            if validated_data['filters']['date']> num_days_in_month:
                return Response({"detail": "Invalid Date"}, status=status.HTTP_400_BAD_REQUEST)

            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            employees_attendances_with_ot = EmployeeAttendance.objects.filter(
                Q(employee__id__in=employee_ids) &
                Q(ot_min__isnull=False) & Q(ot_min__gt=0),
                date=date(validated_data['year'], validated_data['month'], validated_data['filters']['date']),
                company_id=validated_data['company'],
                user=user #OWNER
            ).select_related(
                'company',
                'employee__employee_professional_detail__department',
                'employee__employee_salary_detail',
            ).prefetch_related('overtime_details')

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees_attendances_with_ot = sorted(
                    employees_attendances_with_ot, 
                    key=lambda x: (
                        (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                        int(re.sub(r'[^0-9]', '', x.employee.paycode))
                    )
                )
            else:
                employees_attendances_with_ot = employees_attendances_with_ot.order_by(*order_by)

            payable_overtime_rows = []
            for attendance in employees_attendances_with_ot:
                overtime_result = calculate_attendance_overtime(actor=request.user, attendance=attendance)
                if overtime_result.policy_eligible_gross_minutes > 0:
                    payable_overtime_rows.append({
                        'attendance': attendance,
                        'overtime_result': overtime_result,
                    })

            if payable_overtime_rows:
                response = StreamingHttpResponse(generate_overtime_sheet_daily(serializer.validated_data, payable_overtime_rows), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No OT Employees on this date"}, status=status.HTTP_404_NOT_FOUND)
            
        if validated_data['report_type'] == 'form_14':
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)

            employees = EmployeeProfessionalDetail.objects.filter(
                Q(employee__id__in=employee_ids) &
                Q(user=user) &
                Q(company=validated_data['company']) &
                Q(date_of_joining__year__lte=validated_data['year'])
            )

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (re.sub(r'[^A-Za-z]', '', x.employee.paycode), int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employees = employees.order_by(*order_by)

            if len(employees) !=0:
                response = StreamingHttpResponse(generate_form_14(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Employee Present on this date"}, status=status.HTTP_404_NOT_FOUND)
        
        if validated_data['report_type'] == 'bonus_calculation_sheet': #Best implementation for department group by
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)

            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department__name', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department__name',)

            employees = EmployeeSalaryDetail.objects.filter(
                Q(employee__id__in=employee_ids) &
                Q(user=user) &
                Q(company=validated_data['company']) &
                Q(employee__employee_professional_detail__date_of_joining__year__lte=validated_data['year']) &
                Q(bonus_allow=True)
            )
            print(f"Employee Length: {len(employees)}")

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (
                    (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                    int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employees = employees.order_by(*order_by)

            if len(employees) !=0:
                response = StreamingHttpResponse(generate_bonus_calculation_sheet(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Employees For Bonus on this date"}, status=status.HTTP_404_NOT_FOUND)
            
        if validated_data['report_type'] == 'bonus_form_c': #Best implementation for department group by
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)

            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department__name', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department__name',)

            employees = EmployeeSalaryDetail.objects.filter(
                Q(employee__id__in=employee_ids) &
                Q(user=user) &
                Q(company=validated_data['company']) &
                Q(employee__employee_professional_detail__date_of_joining__year__lte=validated_data['year']) &
                Q(bonus_allow=True)
            )
            # print(f"Employee Length: {len(employees)}")

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(employees, key=lambda x: (
                    (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                    re.sub(r'[^A-Za-z]', '', x.employee.paycode),
                    int(re.sub(r'[^0-9]', '', x.employee.paycode))))
            else:
                employees = employees.order_by(*order_by)

            if len(employees) !=0:
                response = StreamingHttpResponse(generate_bonus_form_c(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Employees For Bonus on this date"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'miss_punch':
            print("Miss punch")
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee__employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee__employee_professional_detail__department',)

            miss_punch_attendances = EmployeeAttendance.objects.filter(
                Q(first_half__name="MS") | Q(second_half__name="MS"),
                date__year=validated_data['year'],
                date__month=validated_data['month'],
                employee__id__in=employee_ids,
                company_id=validated_data['company'],
                user=request.user
            ) 
            print(miss_punch_attendances)
            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                miss_punch_attendances = sorted(
                    miss_punch_attendances, 
                    key=lambda x: (
                        (getattr(x.employee.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.employee.paycode), 
                        int(re.sub(r'[^0-9]', '', x.employee.paycode))
                    )
                )
            else:
                miss_punch_attendances = miss_punch_attendances.order_by(*order_by)

            if len(miss_punch_attendances) !=0:
                print('inside the if')
                response = StreamingHttpResponse(generate_miss_punch_report(serializer.validated_data, miss_punch_attendances), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Employee Miss Punches in this month"}, status=status.HTTP_404_NOT_FOUND)


            
            # print(f"EMployees found: {employees}")
            # return Response({"detail": "Yo"}, status=status.HTTP_200_OK)

class PfEsiReportsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PfEsiReportsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        validated_data = serializer.validated_data
        employee_ids = validated_data["employee_ids"]

        if validated_data['report_type'] == 'pf_statement':
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0 and validated_data['filters']['format']=='xlsx':
                response = StreamingHttpResponse(generate_pf_statement(request.user, serializer.validated_data, employees), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
                return response
            
            elif len(employees) != 0 and validated_data['filters']['format']=='txt':
                txt_content = generate_pf_statement_txt(request.user, serializer.validated_data, employees)
                response = HttpResponse(content_type='text/plain')
                response['Content-Disposition'] = 'attachment; filename="employee_data.txt"'
                response.write(txt_content)
                return response

            else:
                return Response({"detail": "No Employee for PF Statement on this Month and Year"}, status=status.HTTP_404_NOT_FOUND)

        if validated_data['report_type'] == 'pf_exempt':
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0:
                response = StreamingHttpResponse(generate_pf_exempt_xlsx(request.user, serializer.validated_data, employees), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
                return response

            else:
                return Response({"detail": "No Employee for ESI Statement on this Month and Year"}, status=status.HTTP_404_NOT_FOUND)


            
        if validated_data['report_type'] == 'esi_statement':
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0:
                response = StreamingHttpResponse(generate_esi_statement_xlsx(request.user, serializer.validated_data, employees), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
                return response

            else:
                return Response({"detail": "No Employee for ESI Statement on this Month and Year"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"detail": "Yo"}, status=status.HTTP_200_OK)

class EmployeeStrengthReportsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeStrengthReportsSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        validated_data = serializer.validated_data
        employee_ids = validated_data["employee_ids"]

        if validated_data['report_type'] == 'strength_report':
            # date_range_query = Q(date__year=validated_data['year'], date__month=validated_data['month'])
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee_professional_detail__department',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            # print(validated_data)
            if validated_data['filters']['resignation_filter'] == "without_resigned":
                employees = employees.filter(employee_professional_detail__resigned=False)

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        (getattr(x.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0:
                response = StreamingHttpResponse(generate_strength_report(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Active Employees in given period"}, status=status.HTTP_404_NOT_FOUND)
            
        if validated_data['report_type'] == 'resign_report':
            # date_range_query = Q(date__year=validated_data['year'], date__month=validated_data['month'])
            order_by = None
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("attendance_card_no",)
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('name',)
            if validated_data['filters']['group_by'] != 'none':
                if order_by != None:
                    order_by = ('employee_professional_detail__department', *order_by)
                else:
                    order_by = ('employee_professional_detail__department',)

            employees = EmployeePersonalDetail.objects.filter(id__in=employee_ids, user=user, company_id=validated_data['company'])

            #Use python regular expression to orderby if the order by is using paycode because it is alpha numeric
            if validated_data['filters']['sort_by'] == "paycode":
                employees = sorted(
                    employees, 
                    key=lambda x: (
                        (getattr(x.employee_professional_detail.department, 'name', 'zzzzzzzz') if hasattr(x.employee_professional_detail, 'department') else 'zzzzzzzz') if validated_data['filters']['group_by'] != 'none' else '',
                        re.sub(r'[^A-Za-z]', '', x.paycode), 
                        int(re.sub(r'[^0-9]', '', x.paycode))
                    )
                )
            else:
                employees = employees.order_by(*order_by)


            if len(employees) != 0:
                response = StreamingHttpResponse(generate_resign_report(request.user, serializer.validated_data, employees), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                print('returnining the report now ')
                return response
            else:
                return Response({"detail": "No Resigned Employees in given period"}, status=status.HTTP_404_NOT_FOUND)


#### 2nd Account Done till above here ###

class MachineAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # parser_classes = (MultiPartParser, FormParser)
    parser_classes = [CamelCaseMultiPartParser, CamelCaseFormParser]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == 'OWNER':
            serializer = MachineAttendanceSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            # print(serializer.validated_data)
            validated_data = serializer.validated_data
            company = get_object_or_404(Company, id=validated_data['company'], user=user)
            num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
            if validated_data['month_to_date']>num_days_in_month:
                validated_data['month_to_date'] = num_days_in_month
            from_date = datetime(validated_data['year'], validated_data['month'], validated_data['month_from_date'])
            to_date = datetime(validated_data['year'], validated_data['month'], validated_data['month_to_date'])

            try:
                operation_result, message = EmployeeAttendance.objects.machine_attendance(from_date=from_date, to_date=to_date, company_id=company.id, user=user, all_employees_machine_attendance=validated_data['all_employees_machine_attendance'], mdb_database=validated_data['mdb_database'], employee=validated_data['employee'])
            except DjangoValidationError as exc:
                raise serializers.ValidationError(getattr(exc, 'message_dict', exc.messages)) from exc
            return Response({"message": "Machine Attendance successful"}, status=status.HTTP_200_OK)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)
        
class DefaultAttendanceAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = self.request.user
        print(request.data)
        serializer = DefaultAttendanceSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        owner = user if user.role == 'OWNER' else user.regular_to_owner.owner
        company = get_object_or_404(Company, id=validated_data['company'], user=owner)
        if user.role == 'REGULAR' and not company.visible:
            raise PermissionDenied('Company is not available to this account.')
        num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
        from_date = date(validated_data['year'], validated_data['month'], 1)
        to_date = date(validated_data['year'], validated_data['month'], num_days_in_month)
        print(from_date)

        try:
            operation_result, message = EmployeeAttendance.objects.mark_default_attendance(from_date=from_date, to_date=to_date, company_id=company.id, user=user)
        except DjangoValidationError as exc:
            raise serializers.ValidationError(getattr(exc, 'message_dict', exc.messages)) from exc
        print(operation_result, message)

        if operation_result == True:
            return Response({"message": "Bulk Default Attendance successful"}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "Bulk Default Attendance Failed"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    

class EmployeeResignationUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeResignationSerializer
    lookup_field = 'employee'

    # def delete_attendance_records_after_resignation(self, employee_id, resignation_date):
    #     # Assuming 'resignation_date' is in datetime format
    #     EmployeeAttendance.objects.filter(
    #         Q(employee_id=employee_id) & Q(date__gt=resignation_date)
    #     ).delete()
    def delete_attendance_records_after_resignation(self, employee_id, resignation_date):
        # Delete daily attendance records after resignation date
        EmployeeAttendance.objects.filter(
            Q(employee_id=employee_id) & Q(date__gt=resignation_date)
        ).delete()
        
        EmployeeMonthlyAttendanceDetails.objects.filter(
            Q(employee_id=employee_id) & Q(date__gt=date(resignation_date.year, resignation_date.month, 1))
        ).delete()


    def delete_salary_after_resignation(self, employee_id, resignation_date):
        # Assuming 'resignation_date' is in datetime format
        EmployeeSalaryPrepared.objects.filter(
            Q(employee_id=employee_id) & Q(date__gte=date(resignation_date.year, resignation_date.month, 1))
        ).delete()

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_companys_employee_professional_details.filter(company_id=company_id)
        # instance = OwnerToRegular.objects.get(user=user)
        # return instance.owner.all_companys_employee_professional_details.filter(company_id=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        employee_id = kwargs.get('employee')
        instance = self.get_queryset().filter(employee_id=employee_id).first()
        company_id = instance.company.id

        if instance:
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            # After saving the resignation details, delete attendance records
            resignation_date = serializer.validated_data.get('resignation_date')  # Change this to match your serializer field
            if resignation_date:
                self.delete_attendance_records_after_resignation(employee_id, resignation_date)
                openings = EmployeeLeaveOpening.objects.filter(employee_id=employee_id, year=(resignation_date + relativedelta(years=1)).year, company_id=company_id)
                if openings.exists():
                    openings.delete()
                EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=user, year=resignation_date.year, month=resignation_date.month, employee_id=employee_id, company_id=company_id)
                instance = OwnerToRegular.objects.filter(owner=user)
                if instance.exists():
                    regular = instance.first().user
                    attendance_records_in_resignation_month = EmployeeAttendance.objects.filter(user=regular, employee_id=employee_id, date__gte=date(resignation_date.year, resignation_date.month, 1))
                    if attendance_records_in_resignation_month.exists:
                        EmployeeGenerativeLeaveRecord.objects.generate_update_monthly_record(user=regular, year=resignation_date.year, month=resignation_date.month, employee_id=employee_id, company_id=company_id)
                self.delete_salary_after_resignation(employee_id, resignation_date)

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Employee not found"}, status=status.HTTP_404_NOT_FOUND)
    
class EmployeeUnresignUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeUnresignSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companys_employee_professional_details.filter(company_id=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_companys_employee_professional_details.filter(company_id=company_id)
    
    def update(self, request, *args, **kwargs):
        # user = self.request.user
        employee_id = kwargs.get('employee')
        instance = self.get_queryset().filter(employee_id=employee_id)
        print(instance)
        to_update = request.data
        to_update['resigned'] = False
        to_update['resignation_date'] = None
        serializer = self.get_serializer(instance.first(), data=to_update, partial=True)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
   
    
class BonusCalculationListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BonusCalculationSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_company_bonus_calculation.filter(company=company_id)
    
    def list(self, request, *args, **kwargs):
        start_date = datetime.strptime(self.kwargs.get('start_date'), "%Y-%m-%d").date()
        end_date = datetime.strptime(self.kwargs.get('end_date'), "%Y-%m-%d").date()
        print(f"{start_date}, {end_date}")
        queryset = self.get_queryset().filter(date__gte=start_date, date__lte=end_date)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    
class BonusPercentageListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BonusPercentageSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_company_bonus_percentage.filter(company=company_id)

class BonusCalculationAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        # print(request.data)
        for category, month_dict in request.data['calculations'].items():
            print(month_dict)
            for date, amount in month_dict.items():
                existing_bonus_calculation = BonusCalculation.objects.filter(user=user,company_id=request.data['company'], category_id=category, date=date)
                if existing_bonus_calculation.exists():
                    calculation = {'company': request.data['company'], 'category': category, 'amount': amount, 'date': date}
                    serializer = BonusCalculationSerializer(existing_bonus_calculation.first(), data=calculation)
                    serializer.is_valid(raise_exception=True)
                    serializer.save(user=user)
                else:
                    calculation = {'company': request.data['company'], 'category': category, 'amount': amount, 'date': date}
                    serializer = BonusCalculationSerializer(data=calculation)
                    serializer.is_valid(raise_exception=True)
                    # print(serializer.validated_data)
                    serializer.save(user=user)
        
        existing_bonus_percentage = BonusPercentage.objects.filter(user=user,company_id=request.data['company'])
        bonus_percentage_data = {
            'company': request.data['company'], 'bonus_percentage': request.data['bonus_percentage']
        }
        if existing_bonus_percentage.exists():
            serializer = BonusPercentageSerializer(existing_bonus_percentage.first(), data=bonus_percentage_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)

        else:
            serializer = BonusPercentageSerializer(data=bonus_percentage_data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
        return Response({"message": "Successful"}, status=status.HTTP_200_OK)
    
class EmployeeShiftsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id, employee=employee)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        queryset = self.get_queryset().filter(from_date__year__lte=year, to_date__year__gte=year)
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        return Response(serializer.data)
    
class EarnedAmountPreparedSalaryListAPIView(generics.ListAPIView): #rename this later
    permission_classes = [IsAuthenticated]
    serializer_class = EarnedAmountSerializerPreparedSalary

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee_id = self.kwargs.get('employee_id')
        user = self.request.user
        # if user.role != "OWNER":
        #     user = user.regular_to_owner.owner
        return user.all_company_employees_salaries_prepared.filter(company=company_id, employee=employee_id)
        # instance = OwnerToRegular.objects.get(user=user)
        # return instance.owner.all_company_employees_salaries_prepared.filter(company=company_id, employee=employee_id)
    

    def list(self, request, *args, **kwargs):
        employee_id = self.kwargs.get('employee_id')
        employee_professional_detail = EmployeeProfessionalDetail.objects.filter(employee_id=employee_id)
        if employee_professional_detail.exists:
            if employee_professional_detail.first().resignation_date != None:
                resignation_date = employee_professional_detail.first().resignation_date.replace(day=1)
                queryset = self.get_queryset().filter(date=resignation_date)
                if queryset.exists():
                    print('Yes Exists')
                    serializer = self.get_serializer(queryset.first().current_salary_earned_amounts, many=True)
                else:
                    serializer = self.get_serializer([], many=True)
                return Response(serializer.data)
            
class FullAndFinalCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    # serializer_class = FullAndFinalSerializer
    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        # if user.role != "OWNER":
            # user = OwnerToRegular.objects.get(user=user).owner
        return user.all_company_employees_full_and_final.filter(company=company_id)

    def post(self, request, *args, **kwargs):
        user = self.request.user
        # employee = request.data.get('employee_id')
        employee_id = self.kwargs.get('employee_id')

        print(employee_id)
        print(request.data)
        # Use select_for_update to ensure atomicity and avoid race conditions
        existing_instance = FullAndFinal.objects.filter(user=user, employee=employee_id)
        print(existing_instance)
        if existing_instance.exists():
            serializer = FullAndFinalSerializer(existing_instance.first(), data=request.data, partial=True)
        else:
            serializer = FullAndFinalSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response({"message": "Successful"}, status=status.HTTP_201_CREATED)
    
    
class FullAndFinalRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FullAndFinalSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        # if user.role != "OWNER":
            # user = OwnerToRegular.objects.get(user=user).owner
        return user.all_company_employees_full_and_final.filter(company=company_id)
    
class FullAndFinalReportCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = FullAndFinalReportSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)        
        validated_data = serializer.validated_data
        employee_id = validated_data["employee"]
        employee = EmployeeProfessionalDetail.objects.filter(employee=employee_id, user=user, company_id=validated_data['company'])

        if len(employee) != 0:
            response = StreamingHttpResponse(generate_full_and_final_report(request.user, serializer.validated_data, employee.first()), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
            print('returnining the report now ')
            return response
        else:
            return Response({"detail": "No Attendances Found for the given month"}, status=status.HTTP_404_NOT_FOUND)
    
class EmployeeELLeftRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeELLeftSerializer
    lookup_field = 'employee_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        # if user.role != "OWNER":
        #     user = user.regular_to_owner.owner
        return user.all_company_employees_monthly_attendance_details.filter(company=company_id)
        
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        employee_id = self.kwargs.get('employee_id')
        employee_professional_detail = EmployeeProfessionalDetail.objects.filter(employee_id=employee_id)
        if employee_professional_detail.exists:
            if employee_professional_detail.first().resignation_date != None:
                resignation_date = employee_professional_detail.first().resignation_date.replace(day=1)
                print(type(resignation_date))
                queryset = self.get_queryset().filter(date__year=resignation_date.year, employee=employee_id)
                print(queryset)
                present_count = 0
                el_taken_count = 0
                generate_frequency = LeaveGrade.objects.filter(company=employee_professional_detail.first().company, user=user, name='EL').first().generate_frequency
                if queryset.exists():
                    for monthly_attendance in queryset:
                        present_count += monthly_attendance.present_count
                else:
                    return Response({"message": "Failed"}, status=status.HTTP_404_NOT_FOUND)
                generative_leave_queryset = EmployeeGenerativeLeaveRecord.objects.filter(user=request.user, employee=employee_id, date__year=resignation_date.year, leave__name='EL')
                print(generative_leave_queryset)
                if generative_leave_queryset.exists():
                    for monthly_leave in generative_leave_queryset:
                        el_taken_count += monthly_leave.leave_count
                print(f"Present Count: {present_count}")
                print(f"EL Count: {el_taken_count}")
                print(f"Generate Frequency: {generate_frequency}")
                el_left = ((present_count//generate_frequency) - el_taken_count)/2
                print(f"EL Left: {el_left}")
                serializer = self.get_serializer({'el_left': el_left})
                print(serializer.data)
                return Response(serializer.data)
            

class EmployeeBonusAmountYearlyRetrieveAPIView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeYearlyBonusAmountSerializer
    lookup_field = 'employee_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.all_companys_employee_professional_details.filter(company=company_id)
        
    def retrieve(self, request, *args, **kwargs):
        user = self.request.user
        employee_id = self.kwargs.get('employee_id')
        year = self.kwargs.get('year')
        employee_professional_detail = self.get_queryset().filter(employee_id=employee_id)
        if employee_professional_detail.exists:
            employee_professional_detail = employee_professional_detail.first()
            if employee_professional_detail.resignation_date != None:
                resignation_date = employee_professional_detail.resignation_date
                company_calculations = employee_professional_detail.company.calculations
                grand_total_employee = {
                    "paid_days": 0,
                    "bonus_wages": 0,
                    "bonus_amount": 0,
                }
                start_month_year = None
                if company_calculations:
                    start_month_year = date(year, company_calculations.bonus_start_month, 1)
                    print(start_month_year)
                for month in range(12):
                    #Paid Days
                    paid_days = None
                    try:
                        monthly_details = employee_professional_detail.employee.monthly_attendance_details.filter(date=start_month_year).first()
                        paid_days = monthly_details.paid_days_count
                        grand_total_employee['paid_days'] += paid_days
                    except: 
                        pass
                    #print(f"Paid Days: {paid_days}, Month and Year: {start_month_year}")
                    
                    #Bonus Wages
                    bonus_wages = None
                    try:
                        bonus_rate = employee_professional_detail.company.bonus_calculation.filter(date=start_month_year).first().amount
                        if company_calculations.bonus_calculation_days == 'month_days':
                            divisor = calendar.monthrange(start_month_year.year, start_month_year.month)[1]
                        else:
                            divisor = int(company_calculations.bonus_calculation_days)
                        bonus_wages = round(bonus_rate/divisor*paid_days/2)
                        grand_total_employee['bonus_wages'] += bonus_wages
                    except:
                        pass

                    #Bonus Amount
                    bonus_amount = None
                    try:
                        bonus_percentage = employee_professional_detail.company.bonus_percentage.bonus_percentage
                        bonus_amount = round(bonus_wages*bonus_percentage/100)
                        grand_total_employee['bonus_amount'] += bonus_amount
                    except:
                        pass

                    #Next Month
                    if start_month_year:
                        start_month_year = start_month_year + relativedelta(months=1)
                print(f"Total Paid Days: {grand_total_employee['paid_days']}")
                if (grand_total_employee['paid_days']/2)<30:
                    grand_total_employee['bonus_amount'] = 0
                    grand_total_employee['paid_days'] = 0
                print(f"Bonus Amount: {grand_total_employee['bonus_amount']}")
                serializer = self.get_serializer({'bonus_amount': grand_total_employee['bonus_amount'], 'employee': employee_id})
                # print(serializer.data)
                return Response(serializer.data)
                # return Response({"message": "Successful"}, status=status.HTTP_200_OK)
            
class SubUserOvertimeSettingsMonthlyCreateUpdateAPIView(APIView):
    def post(self, request, format=None):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        print(request.data)
        company_id = request.data['company']
        day_array = request.data['day_array']
        month = int(request.data['month'])
        year = int(request.data['year'])
        num_days_in_month = calendar.monthrange(year, month)[1]

        for day in range(1, num_days_in_month+1):
            matching_day_array_elements = [element for element in day_array if element['day'] == day]
            if len(matching_day_array_elements) != 0: #Max OT Hrs Exists
                element = matching_day_array_elements[0]
                element_day = element.get('day')
                max_ot_hrs = element.get('max_ot_hrs')
                instance = SubUserOvertimeSettings.objects.filter(user=user, company=company_id, date=date(year, month, element_day))
                if instance.exists():
                    print(f"Element{element}, status: updating")
                    serializer = SubUserOvertimeSettingsSerializer(instance.first(), data={'company': company_id, 'date': date(year, month, element_day), 'max_ot_hrs': max_ot_hrs}, partial=True)
                else:
                    print(f"Element{element}, status: creating")
                    serializer = SubUserOvertimeSettingsSerializer(data={'company': company_id, 'date': date(year, month, element_day), 'max_ot_hrs': max_ot_hrs})

                serializer.is_valid(raise_exception=True)     
                serializer.save(user=user)   
            else: #No max OT Hrs
                SubUserOvertimeSettings.objects.filter(user=user, company=company_id, date=date(year, month, day)).delete()

        # for element in day_array:
        #     day = element.get('day')
        #     max_ot_hrs = element.get('max_ot_hrs')
        #     instance = SubUserOvertimeSettings.objects.filter(user=user, company=company_id, date=date(year, month, day))
        #     print(instance)
        #     if instance.exists():
        #         print(f"Element{element}, status: updating")
        #         serializer = SubUserOvertimeSettingsSerializer(instance.first(), data={'company': company_id, 'date': date(year, month, day), 'max_ot_hrs': max_ot_hrs}, partial=True)
        #     else:
        #         print(f"Element{element}, status: creating")
        #         serializer = SubUserOvertimeSettingsSerializer(data={'company': company_id, 'date': date(year, month, day), 'max_ot_hrs': max_ot_hrs})

        #     serializer.is_valid(raise_exception=True)     
        #     serializer.save(user=user)   
        return Response("Data processed successfully", status=status.HTTP_200_OK)
    
class SubUserOvertimeSettingsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubUserOvertimeSettingsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companies_sub_user_settings.filter(company=company_id)
        # return user.regular_to_owner.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        start_date = date(year, month, 1)
        num_days_in_month = calendar.monthrange(year, month)[1]
        end_date = date(year, month, num_days_in_month)
        queryset = self.get_queryset().filter(Q(date__gte=start_date) & Q(date__lte=end_date))        
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class SubUserMiscSettingsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SubUserMiscSettingsSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    
class SubUserMiscSettingsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = SubUserMiscSettingsSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            return user.sub_user_misc_settings
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data)
            print(request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'error': "Not allowed"}, status=status.HTTP_403_FORBIDDEN)

class EmployeeYearlyMissPunchListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAttendanceSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        misspunch_leave = LeaveGrade.objects.get(company_id=company_id, name='MS')
        return user.all_employees_attendance.filter(
            user=user,
            company=company_id, 
            date__year=year, 
            #date__month=month,
            first_half=misspunch_leave,
            second_half=misspunch_leave
        )       # if user.role == "OWNER":
       # return user.all_employees_attendance.filter(company=company_id, date__year=year, date__month=month)
    #

class DownloadAddEditEmployeeUsingExcelTemplateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        # Call the function to generate the Excel template
        response = StreamingHttpResponse(generate_add_edit_employee_using_excel_template(request.user), content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
        response["Content-Disposition"] = 'attachment; filename="myexcel.xlsx"'
        return response

        return generate_add_edit_employee_using_excel_template()

class EmployeeYearlyAdvanceTakenDeductedAPIView(APIView):
    '''
    This api accepts a company Id and year (as query params) and returns a list of employee_id of the employees who have taken an advance in that year
    or whose advance has been deducted in that year.
    '''
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user

        # Employees who have taken advance in the specified year
        advance_taken = EmployeeAdvancePayment.objects.filter(
            user=user if user.role == "OWNER" else user.regular_to_owner.owner,
            company_id=company_id,
            date__year=year
        ).values_list('employee_id', flat=True)

        # Employees who have paid an advance EMI in the specified year
        emi_paid = EmployeeAdvanceEmiRepayment.objects.filter(
            user=user,
            employee_advance_payment__company_id=company_id,
            employee_advance_payment__user=user,
            salary_prepared__date__year=year
        ).values_list('employee_advance_payment__employee_id', flat=True)

        # Combine both sets of employees
        employee_ids = list(set(list(advance_taken) + list(emi_paid)))

        # Serialize the data
        serializer = EmployeeYearlyAdvanceTakenDeductedSerializer({'employee_ids': employee_ids})

        return Response(serializer.data)

class AttendanceMachineConfigCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AttendanceMachineConfigSerializer 
    def perform_create(self, serializer):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return serializer.save(user=user)
    
class AttendanceMachineConfigRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = AttendanceMachineConfigSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        return user.attendance_machine_configuration

    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = user.regular_to_owner.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)

'''
Sub User Views (Exclusive) start from here.
'''
class CompanyVisibilityPatchAPIView(APIView):
    permission_classes = [IsAuthenticated, isOwnerAndAdmin]
    def patch(self, request):
        user = self.request.user
        all_companies_instances = user.companies.all()
        companies_visible_list = request.data
        company_visible_ids = [item['company_id'] for item in companies_visible_list]
        
        for company_instance in all_companies_instances:
            if company_instance.id in company_visible_ids:
                company_instance.visible = True
                company_instance.save()
            else:
                company_instance.visible = False
                company_instance.save()
        return Response(status=status.HTTP_200_OK)
    
class EmployeeVisibilityPatchAPIView(APIView):
    permission_classes = [IsAuthenticated, isOwnerAndAdmin]
    def patch(self, request):
        user = self.request.user
        print(request.data)
        serializer = EmployeeVisibilitySerializer(data=request.data)
        all_employees = EmployeePersonalDetail.objects.filter(user=user, company=request.data['company'])
        print(f"All Employees: {len(all_employees)}")
        # companies_visible_list = request.data
        # company_visible_ids = [item['company_id'] for item in companies_visible_list]
        
        for employee in all_employees:
            if employee.id in request.data['employees_id']:
                employee.visible = True
                employee.save()
            else:
                employee.visible = False
                employee.save()
        return Response(status=status.HTTP_200_OK)
    
class TransferAttendanceFromOwnerToRegularAPIView(APIView):
    permission_classes = [IsAuthenticated, isOwnerAndAdmin]
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = TransferAttendanceFromOwnerToRegularSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        company = get_object_or_404(Company, id=validated_data['company'], user=user)
        
        # try:
        # Call the model manager method
        try:
            success, message = EmployeeAttendance.objects.transfer_attendance_from_owner_to_regular(
                month=validated_data['month'],
                year=validated_data['year'],
                company_id=company.id,
                user=user
            )
        except DjangoValidationError as exc:
            raise serializers.ValidationError(getattr(exc, 'message_dict', exc.messages)) from exc
        if not success:
            # If the operation fails, raise an APIException with the error message
            raise APIException(message)
            
        # except Exception as e:
        #     # Handle any other exceptions and return an appropriate error response
        #     return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"message": "Attendance Transfer Successful"}, status=status.HTTP_200_OK)

'''
User and Auth Views start from here.
'''

#Viewsets
class UserViewSet(viewsets.ModelViewSet):
    http_method_names = ['get']
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()

    def get_object(self):
        lookup_field_value = self.kwargs[self.lookup_field]

        obj = User.objects.get(lookup_field_value)
        self.check_object_permissions(self.request, obj)

        return obj
    
class RegularRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = RegularRetrieveUpdateSerializer
    permission_classes = [IsAuthenticated, isOwnerAndAdmin]

    def get_object(self):
        user = self.request.user
        try:
            instance = OwnerToRegular.objects.get(owner=user)
            return instance.user
        except OwnerToRegular.DoesNotExist:
            raise NotFound("Regular user not found")
        # instance = OwnerToRegular.objects.get(owner=user)
        
    
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound as exc:
            return Response({
                "detail": "Sub User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()

        # Update password if 'password' is present in request.data
        if 'password' in request.data:
            new_password = request.data['password']
            instance.set_password(new_password)
            instance.save()

            # Remove 'password' from request.data
            del request.data['password']

        # Update other fields if they are present in request.data
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
    
    # def perform_update(self, serializer):
    #     user = self.request.user
    #     if user.role == "OWNER":
    #         serializer.save(user=user, partial=True)
    #     else:
    #         raise PermissionDenied("You don't have permission to perform this update.")

    # def perform_destroy(self, instance):
    #     # delete the instance
    #     instance.delete()

    #     # return a custom response
    #     return Response({"detail": "Sub User deleted successfully."}, status=status.HTTP_200_OK)
    
    
class RegularRegisterListCreateAPIViewView(generics.ListCreateAPIView):
    serializer_class = RegularRegisterSerializer
    permission_classes = [IsAuthenticated, isOwnerAndAdmin]
    
    def create(self, request, *args, **kwargs):
        owner = request.user

         # check if the user already exists
        if OwnerToRegular.objects.filter(owner=owner).exists():
            return Response({
                "detail": "Sub User already exists"
            }, status=status.HTTP_409_CONFLICT)

        # create a new user
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        regular = Regular.objects.create_user(**serializer.validated_data)

        # create a new owner to regular mapping
        OwnerToRegular.objects.create(user=regular, owner=owner)

        # return a custom response
        return Response({
            "detail": "Sub User successfuly created"
        }, status=status.HTTP_201_CREATED)
    
        # refresh = RefreshToken.for_user(regular)
        # res = {
        #     "refresh": str(refresh),
        #     "access": str(refresh.access_token),
        # }

        # return Response({
        #     "user": serializer.data,
        #     "refresh": res["refresh"],
        #     "token": res["access"]
        # }, status=status.HTTP_201_CREATED)
