from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status, mixins
from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer
from .models import Company, CompanyDetails, User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet



# Create your views here.

class CompanyListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = CompanySerializer

    def get_queryset(self):
        user = self.request.user
        return user.companies.all()
    
    def perform_create(self, serializer):
        # print(self.request.user)
        serializer.save(user=self.request.user)


class CompanyRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = CompanySerializer
    lookup_field = 'id'
    def get_queryset(self):
        user = self.request.user
        return user.companies.all()
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

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
        return user.all_companies_details.all()

    def get(self, request, *args, **kwargs):
        #print(kwargs)
        # print(request)
        return self.retrieve(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request,  *args, **kwargs)
    
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)
    
    def perform_update(self, serializer):
        return serializer.save(user=self.request.user)


class DepartmentListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = DepartmentSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        print(user.username)
        departments = user.departments.filter(company=company_id)
        # print(departments)
        return departments
    
    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        serializer.save(user=self.request.user, company=company)


class DepartmentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DepartmentSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        departments = user.departments.filter(company=company_id)
        # print(departments)
        return departments
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class DesignationListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = DesignationSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        designations = user.designations.filter(company=company_id)
        print(designations)
        return designations
    
    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        serializer.save(user=self.request.user, company=company)

class DesignationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = DesignationSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        designations = user.designations.filter(company=company_id)
        print(designations)
        return designations
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)

class SalaryGradeListCreateAPIView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    # queryset = Company.objects.all()
    serializer_class = SalaryGradeSerializer
    lookup_field = 'company_id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        salary_grades = user.salary_grades.filter(company=company_id)
        print(salary_grades)
        return salary_grades
    
    def perform_create(self, serializer):
        company_id = self.kwargs.get('company_id')
        company = Company.objects.get(id=company_id)
        serializer.save(user=self.request.user, company=company)

class SalaryGradeRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes= [IsAuthenticated]
    serializer_class = SalaryGradeSerializer
    lookup_field = 'id'

    def get_queryset(self, *args, **kwargs):
        company_id = self.kwargs.get('company_id')
        user = self.request.user
        salary_grades = user.salary_grades.filter(company=company_id)
        print(salary_grades)
        return salary_grades
    
    def perform_update(self, serializer):
        serializer.save(user=self.request.user)
        
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