from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status, mixins
from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer, RegularRegisterSerializer, CategorySerializer, BankSerializer, LeaveGradeSerializer, ShiftSerializer, HolidaySerializer, EarningsHeadSerializer, DeductionsHeadSerializer, EmployeePersonalDetailSerializer, EmployeeProfessionalDetailSerializer, EmployeeListSerializer, EmployeeSalaryEarningSerializer, EmployeeSalaryDetailSerializer, EmployeeFamilyNomineeDetialSerializer, EmployeePfEsiDetailSerializer
from .models import Company, CompanyDetails, User, OwnerToRegular, Regular, LeaveGrade, Shift, EmployeeSalaryEarning, EarningsHead
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
from datetime import datetime
from dateutil.relativedelta import relativedelta
import pytz



# Create your views here.

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        if user.role == "OWNER":
            return user.companies.all()
        instance = OwnerToRegular.objects.get(user=user)
        return Company.objects.filter(visible=True, user=instance.owner)
    
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
        instance = OwnerToRegular.objects.get(user=user)
        return Company.objects.filter(visible=True, user=instance.owner)
    
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

        # for company in companies_list:
        #     try:
        #         company_instance = Company.objects.get(id=company["company_id"])
        #         company_instance.visible = company["visible"]
        #         company_instance.save()
        #         print(company_instance)

        #     except:
        #         return Response(
        #             {'error': f'Company with id {company["company_id"]} does not exist'},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )
        # return Response(status=status.HTTP_200_OK)

        # company_ids = request.data.get('company_ids', [])
        # visible_values = request.data.get('visible_values', [])

        # if len(company_ids) != len(visible_values):
        #     return Response(
        #         {'error': 'company_ids and visible_values must have the same length'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        # for i in range(len(company_ids)):
        #     try:
        #         company = Company.objects.get(id=company_ids[i])
        #         company.visible = visible_values[i]
        #         company.save()
        #     except Company.DoesNotExist:
        #         return Response(
        #             {'error': f'Company with id {company_ids[i]} does not exist'},
        #             status=status.HTTP_400_BAD_REQUEST
        #         )

        # return Response(status=status.HTTP_200_OK)

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
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.request.user
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        name = serializer.validated_data.get('name').lower()
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name)
        if clashing_names.exists():
            error_message = "Leave grade with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        
        if clashing_names.exists():
            error_message = "Leave grade with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)
        
        if user.role == "OWNER":
            serializer.save(user=self.request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner)
            return Response(serializer.data, status=status.HTTP_200_OK)

    
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
        

class DeductionsHeadListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = DeductionsHeadSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.deductions_head.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.deductions_head.filter(company=company_id)

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
            error_message = "Deductions Head with this name already exists."
            return Response({"error": error_message}, status=status.HTTP_400_BAD_REQUEST)

        if user.role == "OWNER":
            serializer.save(user=user, company=company)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            instance = OwnerToRegular.objects.get(user=user)
            serializer.save(user=instance.owner, company=company)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

class DeductionsHeadRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DeductionsHeadSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.deductions_head.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.deductions_head.filter(company=company_id)
    
    def update(self, request, *args, **kwargs):
        user = self.request.user
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        name = serializer.validated_data.get('name').lower()

        # Cheking if mandatory Deduction
        if instance.mandatory_deduction:
            return Response({"detail": "Cannot edit a mandatory deduction."}, status=status.HTTP_403_FORBIDDEN)
        
        # Check uniqueness
        clashing_names = self.get_queryset().annotate(lower_name=Lower('name')).filter(lower_name=name).exclude(id=instance.id)
        print(clashing_names)
        if clashing_names.exists():
            print(clashing_names)
            error_message = "Deductions Head with this name already exists."
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
        if instance.mandatory_deduction:
            print("yes")
            return Response({"detail": "Cannot delete a mandatory deduction."}, status=status.HTTP_403_FORBIDDEN)
        # Perform deletion
        self.perform_destroy(instance)
        return Response({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
    

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
        

class EmployeeProfessionalDetailCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeeProfessionalDetailSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        if user.role == "OWNER":
            return user.employee_professional_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_professional_details.filter(company=company_id)


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
            return user.employee_professional_details.filter(company=company_id)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.employee_professional_details.filter(company=company_id)
    
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
                print(len(earning_instances))
                if len(earning_instances) > 0:
                    for earning in earning_instances:
                        print(earning)
                        earning.from_date=validated_data['date_of_joining'].replace(day=1)
                        earning.save()
                        print("saved")
                # print(f'0 -> {earning_instances[0].earnings_head}')
                # print(earning_instances[0].to_date)
                

        print(validated_data)
        serializer.save(user=self.request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)
    
# class EmployeeSalaryEarningListCreateAPIView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = EmployeeSalaryEarningSerializer

#     def get_queryset(self, *args, **kwargs):
#         company_id = self.kwargs.get('company_id')
#         employee = self.kwargs.get('employee')
#         user = self.request.user
#         if user.role == "OWNER":
#             return user.all_employees_earnings.filter(company=company_id, employee=employee)
#         instance = OwnerToRegular.objects.get(user=user)
#         return instance.owner.all_employees_earnings.filter(company=company_id, employee=employee)

#     def create(self, request, *args, **kwargs):
#         print(request.data)
#         serializer = self.get_serializer(data=request.data['employee_earnings'], many=True)
#         serializer.is_valid(raise_exception=True)
#         user = self.request.user

#         if user.role == "OWNER":
#             serializer.save(user=user)
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         else:
#             instance = OwnerToRegular.objects.get(user=user)
#             serializer.save(user=instance.owner)
#             return Response(serializer.data, status=status.HTTP_200_OK)
        
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
                validated_data['to_date'] = '9999-01-01'
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
        print('yayyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy')
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
        # print(serializer.data)
        return Response(serializer.data)
            # serializer = self.get_serializer(instance.first(), data=data, partial=partial)
            # serializer.is_valid(raise_exception=True)
            # user = self.request.user
            # if user.role == "OWNER":
            #     serializer.save(user=user)
            # else:
            #     instance = OwnerToRegular.objects.get(user=user)
            #     serializer.save(user=instance.owner)
        
class EmployeeSalaryEarningListUpdateAPIView(generics.UpdateAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = EmployeeSalaryEarningSerializer
    lookup_field = 'employee'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        employee = self.kwargs.get('employee')
        user = self.request.user
        if user.role == "OWNER":
            return user.all_employees_earnings.filter(company=company_id, employee=employee)
        instance = OwnerToRegular.objects.get(user=user)
        return instance.owner.all_employees_earnings.filter(company=company_id, employee=employee)

    
    # def update(self, request, *args, **kwargs):
    #     print(request.data)
    #     employee_earnings = request.data['employee_earnings']
    #     partial = kwargs.pop('partial', False)

    #     for employee_earning in employee_earnings:
    #         print(employee_earning)
    #         instance = self.get_queryset().filter(earnings_head=employee_earning['earnings_head'])
    #         print(instance)
    #         serializer = self.get_serializer(instance.first(), employee_earning=employee_earning, partial=partial)
    #         serializer.is_valid(raise_exception=True)
    #         user = self.request.user
    #         if user.role == "OWNER":
    #             serializer.save(user=user)
    #         else:
    #             instance = OwnerToRegular.objects.get(user=user)
    #             serializer.save(user=instance.owner)

    #     return Response({"error": "sdfsdf"}, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        indian_timezone = pytz.timezone('Asia/Kolkata')
        current_datetime = datetime.now(indian_timezone)
        current_indian_year = current_datetime.year
        employee_earnings = request.data['employee_earnings']
        partial = kwargs.pop('partial', False)
        user = self.request.user
        if user.role != "OWNER":
            instance = OwnerToRegular.objects.get(user=user)
            user=instance

        for item in employee_earnings:
            existing_earning_to_date_before_saving=None
            earnings_head_id = item['earnings_head']
            earnings_head_instance = EarningsHead.objects.get(pk=earnings_head_id)
            earnings_head_instance_data = EarningsHeadSerializer(earnings_head_instance).data

            # earnings_head_instance['company'] = earnings_head_instance['company_id']

            item['earnings_head'] = earnings_head_instance_data
            serializer = self.get_serializer(data=item)
            serializer.is_valid(raise_exception=True)
            employee_earning = serializer.validated_data
            earnings_head = employee_earning['earnings_head']
            from_date = employee_earning['from_date']
            to_date = employee_earning['to_date']
            value = employee_earning['value']
            print(employee_earning)
            # Get existing employee earnings for the earnings_head
            existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')
            existing_earnings.filter(from_date__gte=from_date, to_date__lte=to_date).delete()
            existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')

            # Find the index of the earning that contains the from_date
            index_to_update = None
            for idx, earning in enumerate(existing_earnings):
                print(idx)
                print(earning.from_date)
                print(earning.to_date)

                print(from_date)
                if from_date >=  earning.from_date and from_date <= earning.to_date:
                    index_to_update = idx
                    break
            print('before iffffffffffff')
            print(index_to_update)
            if index_to_update is not None:
                print('afeter if')
                existing_earning = existing_earnings[index_to_update]
                print(value)
                print(existing_earning.value)
                if value!=existing_earning.value:
                    if from_date==existing_earning.from_date and to_date==existing_earning.to_date:
                        existing_earning.value = value
                        print('here')
                        existing_earning.save()
                    elif from_date==existing_earning.from_date and to_date<existing_earning.to_date:
                        existing_earning_from_date_before_saving = existing_earning.to_date
                        print(existing_earning_from_date_before_saving)
                        existing_earning.from_date = to_date + relativedelta(months=1)
                        existing_earning.save()
                        print(existing_earning.to_date)

                        new_earning = EmployeeSalaryEarning.objects.create(
                        user=user,
                        employee=employee_earning['employee'],
                        company=employee_earning['company'],
                        earnings_head_id=earnings_head_id,
                        value=value,
                        from_date=from_date,
                        to_date=to_date
                        )
                        print(new_earning)


                    else:
                        existing_earning_to_date_before_saving = existing_earning.to_date
                        print(existing_earning_to_date_before_saving)
                        existing_earning.to_date = from_date - relativedelta(months=1)
                        existing_earning.save()
                        print(existing_earning.to_date)
                        if to_date < existing_earning_to_date_before_saving:
                            if to_date.year == current_indian_year and to_date.month==12:
                                print("nowwww innfite it")
                                new_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=employee_earning['employee'],
                                company=employee_earning['company'],
                                earnings_head_id=earnings_head_id,
                                value=value,
                                from_date=from_date,
                                to_date="9999-01-01"
                                )
                                print(new_earning)
                            
                            else:
                                print("not saved yet")
                                # serializer.save(user=user) #save the incoming earning head
                                new_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=employee_earning['employee'],
                                company=employee_earning['company'],
                                earnings_head_id=earnings_head_id,
                                value=value,
                                from_date=from_date,
                                to_date=to_date
                                )
                                print("yayyyyyyyyyyyy saved")
                                auto_created_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=existing_earning.employee,
                                company=existing_earning.company,
                                earnings_head=existing_earning.earnings_head,
                                value=existing_earning.value,
                                from_date=to_date + relativedelta(months=1),
                                to_date=existing_earning_to_date_before_saving
                                )
                                print(auto_created_earning)

                        elif to_date == existing_earning_to_date_before_saving:
                            print("inside elif of you know")
                            # serializer.save(user=user) #save the incoming earning head
                            new_earning = EmployeeSalaryEarning.objects.create(
                            user=user,
                            employee=employee_earning['employee'],
                            company=employee_earning['company'],
                            earnings_head_id=earnings_head_id,
                            value=value,
                            from_date=from_date,
                            to_date=to_date
                            )
                        elif to_date > existing_earning_to_date_before_saving:
                            index_for_to_date = None
                            new_existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')
                            # new_existing_earnings.filter(from_date__gte=from_date, to_date__lte=to_date).delete()
                            # new_existing_earnings = self.get_queryset().filter(earnings_head=earnings_head_id).order_by('from_date')

                            for idx_new, earning_for_to_date in enumerate(new_existing_earnings):
                                print(idx_new)
                                print(earning_for_to_date.from_date)
                                print(earning_for_to_date.to_date)

                                print(to_date, 'of recieved')
                                if to_date >=  earning_for_to_date.from_date and to_date <= earning_for_to_date.to_date:
                                    index_for_to_date = idx_new
                                    break
                            print(index_for_to_date)
                            if index_for_to_date is not None:
                                existing_earning_for_to_date = new_existing_earnings[index_for_to_date]
                                print(existing_earning_for_to_date)
                                existing_earning_for_to_date.from_date = to_date  + relativedelta(months=1)
                                existing_earning_for_to_date.save()
                                print(existing_earning_for_to_date)
                                print("now to create new earning ")
                                new_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=employee_earning['employee'],
                                company=employee_earning['company'],
                                earnings_head_id=earnings_head_id,
                                value=value,
                                from_date=from_date,
                                to_date=to_date
                                )
                            elif index_for_to_date is None:
                                new_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=employee_earning['employee'],
                                company=employee_earning['company'],
                                earnings_head_id=earnings_head_id,
                                value=value,
                                from_date=from_date,
                                to_date=to_date
                                )

                elif value==existing_earning.value:
                    if to_date <= existing_earning.to_date:
                        print('no need to update')
                        pass
                    elif to_date>existing_earning.to_date:
                        existing_earnings.filter(from_date__gt=from_date, to_date__lt=to_date).delete()
                        new_earning = EmployeeSalaryEarning.objects.create(
                                user=user,
                                employee=employee_earning['employee'],
                                company=employee_earning['company'],
                                earnings_head_id=earnings_head_id,
                                value=value,
                                from_date=from_date,
                                to_date=to_date
                                )
                        print(new_earning)
                      

            else:
                # If there is no existing earning to update, create a new one
                print(employee_earning)
                new_earning = EmployeeSalaryEarning.objects.create(
                    user=user,
                    employee=employee_earning['employee'],
                    company=employee_earning['company'],
                    earnings_head_id=earnings_head_id,
                    value=value,
                    from_date=from_date,
                    to_date=to_date
                )
        return Response({"message": "Employee earnings updated successfully"}, status=status.HTTP_200_OK)
    
class EmployeeSalaryDetailCreateAPIView(generics.CreateAPIView):
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
        

class EmployeePfEsiDetailCreateAPIView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = EmployeePfEsiDetailSerializer
    lookup_field = 'company_id'

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

        return Response(serializer.data, status=status.HTTP_200_OK)

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