from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status, mixins
from django.db import transaction
from rest_framework import serializers

from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer, RegularRegisterSerializer, CategorySerializer, BankSerializer, LeaveGradeSerializer, ShiftSerializer, HolidaySerializer, EarningsHeadSerializer, EmployeePersonalDetailSerializer, EmployeeProfessionalDetailSerializer, EmployeeListSerializer, EmployeeSalaryEarningSerializer, EmployeeSalaryDetailSerializer, EmployeeFamilyNomineeDetialSerializer, EmployeePfEsiDetailSerializer, WeeklyOffHolidayOffSerializer, PfEsiSetupSerializer, CalculationsSerializer, EmployeeSalaryEarningUpdateSerializer, EmployeeShiftsSerializer, EmployeeShiftsUpdateSerializer, EmployeeAttendanceSerializer, EmployeeGenerativeLeaveRecordSerializer, EmployeeLeaveOpeningSerializer, EmployeeMonthlyAttendancePresentDetailsSerializer, EmployeeAdvancePaymentSerializer, EmployeeMonthlyAttendanceDetailsSerializer, EmployeeSalaryPreparedSerializer, EarnedAmountSerializer, SalaryOvertimeSheetSerializer, AttendanceReportsSerializer, EmployeeAttendanceBulkAutofillSerializer
from .models import Company, CompanyDetails, User, OwnerToRegular, Regular, LeaveGrade, Shift, EmployeeSalaryEarning, EarningsHead, EmployeeShifts, EmployeeGenerativeLeaveRecord, EmployeeSalaryPrepared, EarnedAmount, EmployeeAdvanceEmiRepayment, EmployeeAdvancePayment, EmployeeAttendance
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from .auth.views import MyTokenObtainPairView
from django.db.models.functions import Lower
from rest_framework.parsers import MultiPartParser, FormParser
from djangorestframework_camel_case.parser import CamelCaseFormParser, CamelCaseMultiPartParser
from django.db import IntegrityError
from django.db.models import Q
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
import pytz
import calendar
from django.db.models import Sum
from decimal import Decimal
import math
from fpdf import FPDF
from django.http import HttpResponse, StreamingHttpResponse
from .reports.generate_salary_sheet import generate_salary_sheet
from .reports.generate_attendance_register import generate_attendance_register
from itertools import groupby
from operator import attrgetter









# Create your views here.

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.companies.all()
        return Company.objects.filter(visible=True, user__in=OwnerToRegular.objects.filter(owner=user).values('user'))

    
    def perform_create(self, serializer):
        # print(self.request.user)
        user = self.request.user
        if user.role == "OWNER":
            serializer.save(user=user)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, visible=True)


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.companies.all()
        return Company.objects.filter(visible=True, user__in=OwnerToRegular.objects.filter(owner=user).values('user'))

    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            serializer.save(user=user)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)

class CompanyVisibilityPatchAPIView(APIView):
    def patch(self, request):
        print(Company.objects.all())
        all_companies_instances = Company.objects.all()
        companies_visible_list = request.data
        company_visible_ids = [item['company_id'] for item in companies_visible_list]
        
        for company_instance in all_companies_instances:
            if company_instance.id in company_visible_ids:
                company_instance.visible = True
                print(company_instance)
                company_instance.save()
            else:
                company_instance.visible = False
                company_instance.save()
        return Response(status=status.HTTP_200_OK)


class CompanyDetailsMixinView(generics.GenericAPIView,
mixins.CreateModelMixin,
mixins.RetrieveModelMixin,
mixins.ListModelMixin,
mixins.UpdateModelMixin):
    permission_classes = [IsAuthenticated]
    # queryset = CompanyDetails.objects.all()
    serializer_class = CompanyEntrySerializer
    lookup_field = 'company_id'

    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companies_details.all()
        instance = OwnerToRegular.objects.get(user=user)
        return CompanyDetails.objects.filter(user=instance.owner)
        

    def get(self, request, *args, **kwargs):
        #print(kwargs)
        # print(request)
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request,  *args, **kwargs)
    
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)
        
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.departments.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.departments.filter(company=company_id)
        
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner, company=company)
        


class DepartmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.departments.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.departments.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)


class DesignationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = DesignationSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.designations.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.designations.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner, company=company)
        

class DesignationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DesignationSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.designations.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.designations.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)

class SalaryGradeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = SalaryGradeSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.salary_grades.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.salary_grades.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner, company=company)

class SalaryGradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = SalaryGradeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.salary_grades.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.salary_grades.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)

class CategoryListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.categories.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.categories.filter(company=company_id)
    
    def perform_create(self, serializer):
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        if user.role == "OWNER":
            return serializer.save(user=user, company=company)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner, company=company)

class CategoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = CategorySerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.categories.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.categories.filter(company=company_id)
    
    def perform_update(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)
        
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
    # queryset = Company.objects.all()
    serializer_class = LeaveGradeSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.leave_grades.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.leave_grades.filter(company=company_id)
    
    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        try:
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Leave Grade with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)

class LeaveGradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = LeaveGradeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.leave_grades.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.leave_grades.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            print(str(e))
            return Response({"name" : "Leave Grade with this name already exists"}, status=status.HTTP_400_BAD_REQUEST)\

    
    def perform_destroy(self, instance):
        if instance.mandatory_leave:
            return Response({"detail": "Cannot delete a mandatory leave grade."}, status=status.HTTP_403_FORBIDDEN)
        instance.delete()

class ShiftListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ShiftSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.shifts.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.shifts.filter(company=company_id)
    
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
            error_message = "Shift grade with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class ShiftRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = ShiftSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.shifts.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.shifts.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        if clashing_names.exists():
            error_message = "Shift with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.role == "OWNER":
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
    
class HolidayListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = HolidaySerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.holidays.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.holidays.filter(company=company_id)
    
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
            error_message = "Holiday with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
    
class HolidayRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = HolidaySerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.holidays.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.holidays.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Cheking if mandatory Holiday
        if instance.mandatory_holiday:
            return Response({"detail": "Cannot edit a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        if clashing_names.exists():
            error_message = "Holiday with this name already exists."
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
        if instance.mandatory_holiday:
            print("yes")
            return Response({"detail": "Cannot delete a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
        # Perform deletion
        self.perform_destroy(instance)
        return Response({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        
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
        # elif self.request.method == 'POST':
        #     return EmployeePersonalDetailCreateSerializer
        return EmployeePersonalDetailSerializer  # Use the default serializer for other methods

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            personal_details_list = user.employee_personal_details.filter(company=company_id)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            personal_details_list = instance.owner.employee_personal_details.filter(company=company_id)
        combined_queryset = personal_details_list.prefetch_related('employee_professional_detail')
        # print(combined_queryset)
        return combined_queryset


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        try:
            if user.role == "OWNER":
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)
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
        if user.role == "OWNER":
            return user.employee_personal_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_personal_details.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        try:
            if user.role == "OWNER":
                serializer.save(user=self.request.user)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)
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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_companys_employee_professional_details.filter(company=company_id)


    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        # try:
        if user.role == "OWNER":
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # except IntegrityError as e:
        #     error_string = str(e)
        #     print(error_string)
        #     if "user_id" in error_string and "company_id" in error_string and "paycode" in error_string:
        #         error_message = {"paycode": "This Paycode already exists"}
        #     elif "user_id" in error_string and "company_id" in error_string and "attendance_card_no" in error_string:
        #         error_message = {"attendance_card_no": "This Paycode already exists"}
        #     else:
        #         error_message = {"error": "Some error occurred"}
        #     return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
            

class EmployeeProfessionalDetailRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeProfessionalDetailSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_companys_employee_professional_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_companys_employee_professional_details.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        if user.role == "OWNER":
            pass
        else:
            instance = OwnerToRegular.objects.get(user=user)
            user = instance.owner
        if 'date_of_joining' in validated_data:
            print('hahah')
            instance = self.get_queryset().filter(employee=validated_data['employee'])
            print(instance[0].date_of_joining)
            print(type(instance[0].date_of_joining))
            print(type(validated_data['date_of_joining']))
            if instance[0].date_of_joining != validated_data['date_of_joining']:
                earning_instances = EmployeeSalaryEarning.objects.filter(user=user, employee=validated_data['employee'], from_date=instance[0].date_of_joining.replace(day=1))
                shift_instances = EmployeeShifts.objects.filter(user=user, employee=validated_data['employee'], from_date=instance[0].date_of_joining)
                print(earning_instances)
                print("shift length" ,len(shift_instances))
                if len(shift_instances)>0:
                    shift = shift_instances[0]
                    shift.from_date=validated_data['date_of_joining']
                    shift.save()
                if len(earning_instances) > 0:
                    for earning in earning_instances:
                        # print(earning)
                        earning.from_date=validated_data['date_of_joining'].replace(day=1)
                        earning.save()

        print(validated_data)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
        
class EmployeeSalaryEarningListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryEarningSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_earnings.filter(company=company_id, employee=employee)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_earnings.filter(company=company_id, employee=employee)

    def create(self, request, *args, **kwargs):
        print(request.data)
        employee_earnings = request.data['employee_earnings']
        for data in employee_earnings:
            earnings_head_id = data['earnings_head']
            earnings_head_instance = EarningsHead.objects.get(pk=earnings_head_id)
            earnings_head_instance_data = EarningsHeadSerializer(earnings_head_instance).data
            data["earnings_head"] = earnings_head_instance_data
            user = self.request.user
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            validated_data = serializer.validated_data
            instance = self.get_queryset().filter(earnings_head=earnings_head_id)
            if instance.exists():
                print("nuuuuu")
            else:
                print("yayyy")
                validated_data['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
                # print(validated_data)
            if user.role == "OWNER":
                pass
            else:
                instance = OwnerToRegular.objects.get(user=user)
                user=instance.owner
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
        print(year)
        if user.role == "OWNER":
            queryset = user.all_employees_earnings.filter(
                company=company_id,
                employee=employee,
                from_date__year__lte=year,
                to_date__year__gte=year
            )
        else:
            instance = OwnerToRegular.objects.get(user=user)
            queryset = instance.owner.all_employees_earnings.filter(
                company=company_id,
                employee=employee,
                from_date__year__lte=year,
                to_date__year__gte=year
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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_earnings.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(indian_timezone)
        current_indian_year = current_datetime.year
        employee_earnings = request.data['employee_earnings']
        # print(employee_earnings)
        partial = kwargs.pop('partial', False)
        user = self.request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
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

            print(f"Earnings for earnings_head {earnings_head_id}:")
            # print(sorted_earning_records)
            first_object = sorted_earning_records[0]
            last_object = sorted_earning_records[-1]
            print(f'first object: {first_object}, last object: {last_object}')
            # print(first_object['from_date'])
            # print(first_object['earnings_head'])

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

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_salary_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_salary_details.filter(company=company_id)


    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            # try:
            if user.role == "OWNER":
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        except ValidationError as e:
            error_string = str(e)
            return Response({'overtimeRate': "Overtime Rate cannot be blank if overtime is allowed"}, status=status.HTTP_400_BAD_REQUEST)

        
class EmployeeSalaryDetailRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeSalaryDetailSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_salary_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_salary_details.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        try:
            user = self.request.user
            instance = self.get_object()
            serializer = self.get_serializer(instance, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)

            if user.role == "OWNER":
                serializer.save(user=self.request.user)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)

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
        print(f"Pf Esi Detail: ")
        user = self.request.user
        if user.role == "OWNER":
            print(f"Pf Esi Detail: ")
            return user.employee_pf_esi_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_pf_esi_details.filter(company=company_id)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            # try:
            if user.role == "OWNER":
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)
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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_pf_esi_details.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        if user.role == "OWNER":
            serializer.save(user=self.request.user)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)

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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_family_nominee_details.filter(company=company_id, employee=employee)

    def create(self, request, *args, **kwargs):
        print(request.data)
        try:
            serializer = self.get_serializer(data=request.data['family_nominee_detail'], many=True)
            serializer.is_valid(raise_exception=True)
            user = self.request.user

            if user.role == "OWNER":
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)
                return Response(serializer.data, status=status.HTTP_200_OK)
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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_family_nominee_details.filter(company=company_id, employee=employee)

    
    def update(self, request, *args, **kwargs):
        family_nominee_detail = request.data['family_nominee_detail']
        # partial = kwargs.pop('partial', False)

        for data in family_nominee_detail:
            instance = self.get_queryset().filter(id=data['id'])
            serializer = self.get_serializer(instance.first(), data=data)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            if user.role == "OWNER":
                serializer.save(user=user)
            else:
                instance = OwnerToRegular.objects.get(user=user)
                serializer.save(user=instance.owner)

        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
    
class WeeklyOffHolidayOffCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = WeeklyOffHolidayOffSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)
    
class WeeklyOffHolidayOffRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = WeeklyOffHolidayOffSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        # company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.weekly_off_holiday_off_entries
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.weekly_off_holiday_off_entries
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            pass
        else:
            instance = OwnerToRegular.objects.get(user=user)
            user = instance.owner
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
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)
    
class PfEsiSetupRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = PfEsiSetupSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            return user.pf_esi_setup_details
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.pf_esi_setup_details
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            pass
        else:
            instance = OwnerToRegular.objects.get(user=user)
            user = instance.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        print(request.data)
        
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    

class CalculationsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CalculationsSerializer
    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)
    
class CalculationsRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = CalculationsSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            return user.calculations
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.calculations
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role == "OWNER":
            pass
        else:
            instance = OwnerToRegular.objects.get(user=user)
            user = instance.owner
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        print(request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
    
class AllEmployeeMonthyShiftsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        # employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_shifts.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_shifts.filter(company=company_id)
    
    def list(self, request, *args, **kwargs):

        # year = self.kwargs.get('year')
        # month = self.kwargs.get('month')
        # from_date = datetime(year, month, 1).date() - relativedelta(days=6)
        # last_day = calendar.monthrange(year, month)[1]
        # to_date = datetime(year, month, last_day).date()


        # print(type(from_date))
        # print(from_date)
        # print(to_date)
        # # print(month)
        # queryset = self.get_queryset().filter(date__range=[from_date, to_date])
        # serializer = self.get_serializer(queryset, many=True)
        # return Response(serializer.data)
        # # return Response(status.HTTP_200_OK)

        year = self.kwargs.get('year')
        print(year)
        month = self.kwargs.get('month')
        start_date = datetime(year, month, 1).date()
        print(f'Star Date: {start_date}')
        end_date = (start_date + relativedelta(months=1)) - relativedelta(days=1)
        print(end_date)
        print(len(self.get_queryset()))

        queryset = self.get_queryset().filter(
            from_date__lte=end_date,  # Shifts that start before or in the specified year
            to_date__gte=start_date,    # Shifts that end in the specified year or later
        )
        serializer = self.get_serializer(queryset, many=True)
        # print(serializer.data)
        # print(len(serializer.data))
        return Response(serializer.data)
        # return Response(status.HTTP_200_OK)
    
    
class EmployeeShiftsCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeShiftsUpdateSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.role == "OWNER":
            return serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        return serializer.save(user=instance.owner)

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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        employee_shifts = request.data['employee_shifts']
        # print(employee_shifts)
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
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        employee_shift = request.data
        employee_shift['to_date'] = datetime.strptime('9999-01-01', "%Y-%m-%d").date()
        # print(employee_shift)
        serializer = self.get_serializer(data=employee_shift)
        serializer.is_valid(raise_exception=True)
        validated_shift = serializer.validated_data
        EmployeeShifts.objects.process_employee_permanent_shift(user=user, employee_shift_data=validated_shift)
        return Response({"message": "Employee earnings updated successfully"}, status=status.HTTP_200_OK)
    

# class EmployeeShiftsListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EmployeeShiftsSerializer

#     def get_queryset(self, *args, **kwargs):
#         company_id = self.kwargs.get('company_id')
#         employee = self.kwargs.get('employee')
#         user = self.request.user
#         if user.role == "OWNER":
#             return user.all_employees_shifts.filter(company=company_id, employee=employee)
#         instance = OwnerToRegular.objects.get(user=user)
#         return instance.owner.all_employees_shifts.filter(company=company_id, employee=employee)
    
#     def list(self, request, *args, **kwargs):
#         year = self.kwargs.get('year')
#         queryset = self.get_queryset().filter(from_date__year__lte=year, to_date__year__gte=year)
#         serializer = self.get_serializer(queryset, many=True)
#         print(serializer.data)
#         return Response(serializer.data)
    
class EmployeeAttendanceListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAttendanceSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        # employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_attendance.filter(company=company_id)
        # instance = OwnerToRegular.objects.get(user=user)
        # return instance.owner.employee_family_nominee_details.filter(company=company_id, employee=employee)

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data['employee_attendance'], many=True)
            serializer.is_valid(raise_exception=True)
            user = self.request.user
            total_expected_instances= len(serializer.validated_data)
            date_for_one_instance = serializer.validated_data[0]['date']
            employee = serializer.validated_data[0]['employee']
            company = serializer.validated_data[0]['company']
            print(date_for_one_instance.month)
            print(date_for_one_instance.year)

            if user.role == "OWNER":
                serializer.save(user=user)
                EmployeeGenerativeLeaveRecord.objects.generate_monthly_record(total_expected_instances=total_expected_instances, user=user, year=date_for_one_instance.year, month=date_for_one_instance.month, employee=employee, company=company)
                return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response({"msg": "try"}, status=status.HTTP_200_OK)
            # else:
            #     instance = OwnerToRegular.objects.get(user=user)
            #     serializer.save(user=instance.owner)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        from_date = datetime(year, month, 1).date() - relativedelta(days=6)
        last_day = calendar.monthrange(year, month)[1]
        to_date = datetime(year, month, last_day).date()
        queryset = self.get_queryset().filter(date__range=[from_date, to_date])
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
        # return Response(status.HTTP_200_OK)
    
class EmployeeAttendanceUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeAttendanceSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_attendance.filter(company=company_id, employee=employee)
    
    def update(self, request, *args, **kwargs):
        # print(request.data)
        # print(request.data['employee_attendance'])
        try:
            user = self.request.user
            employee_attendance = request.data['employee_attendance']
            total_expected_instances= len(employee_attendance)
            date_for_one_instance = datetime.strptime(employee_attendance[0]['date'], "%Y-%m-%d").date()
            print(f"Date: {date_for_one_instance} Type: {type(date_for_one_instance)}")
            employee_id = employee_attendance[0]['employee']
            company_id = employee_attendance[0]['company']
            print(f"Employee: {employee_id} Company: {company_id}")
            print(total_expected_instances)
            for day in employee_attendance:
                instance = self.get_queryset().filter(id=day['id'])
                serializer = self.get_serializer(instance.first(), data=day)
                serializer.is_valid(raise_exception=True)
                if user.role == "OWNER":
                    serializer.save(user=user)

            if user.role == "OWNER":
                EmployeeGenerativeLeaveRecord.objects.update_monthly_record(total_expected_instances=total_expected_instances, user=user, year=date_for_one_instance.year, month=date_for_one_instance.month, employee_id=employee_id, company_id=company_id)

            return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Some Error Occured")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class EmployeeAttendanceBulkAutoFillView(APIView):
    def post(self, request, *args, **kwargs):
        user = self.request.user
        serializer = EmployeeAttendanceBulkAutofillSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        print(serializer.validated_data)
        validated_data = serializer.validated_data
        num_days_in_month = calendar.monthrange(validated_data['year'], validated_data['month'])[1]
        if validated_data['month_to_date']>num_days_in_month:
            validated_data['month_to_date'] = num_days_in_month
        from_date = date(validated_data['year'], validated_data['month'], validated_data['month_from_date'])
        to_date = date(validated_data['year'], validated_data['month'], validated_data['month_to_date'])

        # try:
        EmployeeAttendance.objects.bulk_autofill(from_date=from_date, to_date=to_date, company_id=validated_data['company'], user=user)
        return Response({"message": "Bulk autofill successful"}, status=status.HTTP_200_OK)
        # except Exception as e:
        #     return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        # return Response({"message": "Bulk autofill successful"}, status=status.HTTP_200_OK)
        

class EmployeeGenerativeLeaveRecordListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeGenerativeLeaveRecordSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_generative_leave_record.filter(company=company_id, date__year=year)
        
class EmployeeMonthlyAttendancePresentDetailsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeMonthlyAttendancePresentDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_monthly_attendance_details.filter(company=company_id, date__year=year)
        
class EmployeeMonthlyAttendanceDetailsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeMonthlyAttendanceDetailsSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_monthly_attendance_details.filter(company=company_id, date__year=year)

class EmployeeLeaveOpeningListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeLeaveOpeningSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        year = self.kwargs.get('year')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_leave_openings.filter(company=company_id, year=year)
        
class EmployeeAdvancePaymentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeAdvancePaymentSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee_id = self.kwargs.get('employee_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_advance_payments.filter(company=company_id, employee=employee_id)
    
    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data['employee_advance_details'], many=True)
            serializer.is_valid(raise_exception=True)
            user = self.request.user

            if user.role == "OWNER":
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_200_OK)
                # return Response({"msg": "try"}, status=status.HTTP_200_OK)
            # else:
            #     instance = OwnerToRegular.objects.get(user=user)
            #     serializer.save(user=instance.owner)
            #     return Response(serializer.data, status=status.HTTP_200_OK)
        except ValidationError as e:
            print(e)
            return Response({'error': e}, status=status.HTTP_400_BAD_REQUEST)
        

class EmployeeAdvancePaymentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeAdvancePaymentSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee_id = self.kwargs.get('employee_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_company_employees_advance_payments.filter(company=company_id, employee=employee_id)
    
    def update(self, request, *args, **kwargs):
        print(request.data)
        # print(request.data['employee_advance_details'])
        # return Response({"detail": "Sub User deleted successfully."}, status=status.HTTP_200_OK)

        try:
            user = self.request.user
            employee_advance_details = request.data['employee_advance_details']
            for detail in employee_advance_details:
                instance = self.get_queryset().filter(id=detail['id'])
                serializer = self.get_serializer(instance.first(), data=detail)
                serializer.is_valid(raise_exception=True)
                if user.role == "OWNER":
                    serializer.save(user=user)
            return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
        except Exception as e:
            print("Some Error Occured")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    def destroy(self, request, *args, **kwargs):
        try:        
            user = self.request.user
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
            user = OwnerToRegular.objects.get(user=user).owner
        return user.all_employees_earnings.filter(company=company_id)
        
    def list(self, request, *args, **kwargs):
        year = self.kwargs.get('year')
        queryset = self.get_queryset().filter(from_date__year__lte=year, to_date__year__gte=year)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
    

class EmployeeSalaryPreparedCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryPreparedSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner
        all_earned_amounts_data = request.data.get('all_earned_amounts', [])
        serializer = self.get_serializer(data=request.data['employee_salary_prepared'])
        serializer.is_valid(raise_exception=True)
        employee_salary_prepared = EmployeeSalaryPrepared.objects.filter(employee=request.data['employee_salary_prepared']['employee'], date=request.data['employee_salary_prepared']['date'])
        
        if employee_salary_prepared.exists():
            existing_instance = employee_salary_prepared.first()
            serializer.update(existing_instance, serializer.validated_data)
        else:
            serializer.save(user=user)
        #Retrieve Saved salary instance
        employee_salary_after_saved = EmployeeSalaryPrepared.objects.filter(employee=serializer.data['employee'], date=serializer.data['date'])
        
        if employee_salary_after_saved.exists():
            employee_salary_after_saved_instance = employee_salary_after_saved.first()
            EarnedAmount.objects.filter(salary_prepared=employee_salary_after_saved_instance.id).delete()

            #Iterating through all the earned amounts and saving it
            for earned_amount_data in all_earned_amounts_data:
                earned_amount_data['salary_prepared'] = employee_salary_after_saved_instance.id
                earned_amount_data['earnings_head'] = earned_amount_data['earnings_head']['id']
                earned_amount_serializer = EarnedAmountSerializer(data=earned_amount_data)
                if earned_amount_serializer.is_valid():
                    earned_amount_serializer.save(user=user)
                else:
                    print("Not valid")
                    print(earned_amount_serializer.errors)

            #First delete all the objects of EmployeeAdvanceEmiRepayment for this salary (which was just saved) then retrieve the advances
            EmployeeAdvanceEmiRepayment.objects.filter(salary_prepared=employee_salary_after_saved_instance.id).delete()
            employee_advances = EmployeeAdvancePayment.objects.filter(user=employee_salary_after_saved_instance.user, employee=employee_salary_after_saved_instance.employee, company=employee_salary_after_saved_instance.company, date__lt=(employee_salary_after_saved_instance.date + relativedelta(months=1))).order_by('date')
            if employee_advances.exists():
                
                monthly_advance_repayment = 0
                max_advance_repayment_left = 0
                for advance in employee_advances:
                    max_advance_repayment_left += advance.principal-advance.repaid_amount
                    if advance.emi <= (advance.principal-advance.repaid_amount):
                        monthly_advance_repayment += advance.emi
                    elif (advance.principal-advance.repaid_amount) > 0:
                        monthly_advance_repayment += (advance.principal-advance.repaid_amount)
                print(f"Advance to be paid: {monthly_advance_repayment}")
                if employee_salary_after_saved_instance.advance_deducted > max_advance_repayment_left:
                    return Response({"detail": "Too Much Advance Emi Repayment"}, status=status.HTTP_400_BAD_REQUEST)
                
                surplus_repayment = employee_salary_after_saved_instance.advance_deducted - monthly_advance_repayment #0
                advance_deducted_left = employee_salary_after_saved_instance.advance_deducted
                for advance in employee_advances:
                    add_to_repaid = min(advance.principal-advance.repaid_amount, advance.emi)
                    if surplus_repayment>0:
                        add_to_repaid = min(advance.principal-advance.repaid_amount, advance.emi+surplus_repayment)
                        if add_to_repaid != advance.emi+surplus_repayment:
                            surplus_repayment -= add_to_repaid - min(advance.principal-advance.repaid_amount, advance.emi)
                        else:
                            surplus_repayment -= surplus_repayment
                    
                    EmployeeAdvanceEmiRepayment.objects.create(user=user, amount=min(add_to_repaid, advance_deducted_left), employee_advance_payment_id=advance.id, salary_prepared_id=employee_salary_after_saved_instance.id)
                    advance_deducted_left -= min(add_to_repaid, advance_deducted_left)

                # if advance_deducted_left !=0:
                #     print(f"Advance is not 0 something is wrong: {advance_deducted_left}")
                #     return Response({"detail": "Too Much Advance Emi Repayment"}, status=status.HTTP_400_BAD_REQUEST)
                if surplus_repayment != 0:
                    print(f"Surplus is left: {surplus_repayment}")

        return Response({"detail": "Successful"}, status=status.HTTP_200_OK)
    
class EmployeeSalaryPreparedListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeSalaryPreparedSerializer

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role != "OWNER":
            # user = OwnerToRegular.objects.get(user=user).owner
            return Response({"detail": "User is regular"}, status=status.HTTP_404_NOT_FOUND)
        return user.all_company_employees_salaries_prepared.filter(company=company_id)
        
    def list(self, request, *args, **kwargs):
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')
        date_obj = date(year, month, 1)
        queryset = self.get_queryset().filter(date=date_obj)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    
# class CompanyEmployeeStatisticsListAPIView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = CompanyEmployeeStatisticsSerializer

#     def get_queryset(self, *args, **kwargs):
#         company_id = self.kwargs.get('company_id')
#         user = self.request.user
#         if user.role == "OWNER":
#             return user.all_employees_statistics.filter(company=company_id)
#         instance = OwnerToRegular.objects.get(user=user)
#         return instance.owner.all_employees_statistics.filter(company=company_id)

class SalaryOvertimeSheetCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SalaryOvertimeSheetSerializer

    def create(self, request, *args, **kwargs):
        user = request.user
        if user.role != "OWNER":
            user = OwnerToRegular.objects.get(user=user).owner

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        validated_data = serializer.validated_data
        employee_ids = validated_data["employee_ids"]
        salary_date = date(validated_data["year"], validated_data["month"], 1)
        # print(validated_data)
        order_by = 'employee__paycode'
        if validated_data['filters']['sort_by'] == "attendance_card_no":
            order_by = "employee__attendance_card_no"
        elif validated_data['filters']['sort_by'] == "employee_name":
            order_by = 'employee__name'
        if validated_data['filters']['group_by'] != 'none':
            order_by = 'employee__employee_professional_detail__department'
            
        employee_salaries = EmployeeSalaryPrepared.objects.filter(employee__id__in=employee_ids, date=salary_date).order_by(order_by)

        print(validated_data)
        if employee_salaries.exists():
            response = StreamingHttpResponse(generate_salary_sheet(serializer.validated_data, employee_salaries), content_type="application/pdf")
            response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
            return response
        else:
            return Response({"detail": "No Salary Prepared for the given month"}, status=status.HTTP_404_NOT_FOUND)

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
            date_range_query = Q(date__year=validated_data['year'], date__month=validated_data['month'])
            # resignation_filter_query = Q()  # You might need to adjust this based on your logic

            order_by = ('employee__paycode', 'date')
            if validated_data['filters']['sort_by'] == "attendance_card_no":
                order_by = ("employee__attendance_card_no",'date')
            elif validated_data['filters']['sort_by'] == "employee_name":
                order_by = ('employee__name','employee__paycode', 'date')
            
            if validated_data['filters']['group_by'] != 'none':
                order_by = ('employee__employee_professional_detail__department',)+order_by
            print(*order_by)

            attendance_objects = EmployeeAttendance.objects.filter(
                Q(employee__id__in=employee_ids) &
                Q(company_id=validated_data['company']) &
                date_range_query
                # resignation_filter_query
            ).order_by(*order_by)
            print(len(attendance_objects))

            # Group by employee using itertools.groupby
            grouped_attendance = groupby(attendance_objects, key=attrgetter('employee_id'))

            # Convert the result to a dictionary where keys are employee_ids and values are lists of attendance objects
            attendance_dict = {key: list(group) for key, group in grouped_attendance}
                
            if attendance_objects.exists():
                response = StreamingHttpResponse(generate_attendance_register(serializer.validated_data, attendance_dict), content_type="application/pdf")
                response["Content-Disposition"] = 'attachment; filename="mypdf.pdf"'
                return response
            else:
                return Response({"detail": "No Attendances Found for the given month"}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Yo"}, status=status.HTTP_200_OK)

        
        



            




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
    
class RegularRetrieveDestroyAPIView(generics.RetrieveDestroyAPIView):
    serializer_class = RegularRegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_object(self):
        # Get the primary key from the URL kwargs
        user = self.request.user
        # Retrieve the instance using a custom lookup field
        try:
            instance = OwnerToRegular.objects.get(owner=user)
        except OwnerToRegular.DoesNotExist:
            raise NotFound("Regular user not found")
        instance = OwnerToRegular.objects.get(owner=user)
        # Return the instance
        return instance.user
    
    def get(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
        except NotFound as exc:
            return Response({
                "detail": "Sub User Not Found"
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_destroy(self, instance):
        # delete the instance
        instance.delete()

        # return a custom response
        return Response({"detail": "Sub User deleted successfully."}, status=status.HTTP_200_OK)
    
    
class RegularRegisterListCreateAPIViewView(generics.ListCreateAPIView):
    serializer_class = RegularRegisterSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    
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