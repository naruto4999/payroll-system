from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status, mixins
from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer, RegularRegisterSerializer, CategorySerializer, BankSerializer, LeaveGradeSerializer, ShiftSerializer, HolidaySerializer
from .models import Company, CompanyDetails, User, OwnerToRegular, Regular, LeaveGrade, Shift
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from .auth.views import MyTokenObtainPairView
from django.db.models.functions import Lower




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
    
    # def perform_create(self, serializer):
    #     user = self.request.user
    #     company_id = self.kwargs.get('company_id')
    #     company = Company.objects.get(id=company_id)
    #     if user.role == "OWNER":
    #         return serializer.save(user=user, company=company)
    #     instance = OwnerToRegular.objects.get(user=user)
    #     return serializer.save(user=instance.owner, company=company)

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
    
    # def perform_update(self, serializer):
    #     user = self.request.user
    #     if user.role == "OWNER":
    #         return serializer.save(user=self.request.user)
    #     instance = OwnerToRegular.objects.get(user=user)
    #     return serializer.save(user=instance.owner)
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
        
    # def perform_destroy(self, instance):
    #     if instance.mandatory_holiday:
    #         print("yes")
    #         return Response({"detail": "Cannot delete a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
    #     instance.delete()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.mandatory_holiday:
            print("yes")
            return Response({"detail": "Cannot delete a mandatory holiday."}, status=status.HTTP_403_FORBIDDEN)
        # Perform deletion
        self.perform_destroy(instance)
        return Response({"detail": "Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)
        

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