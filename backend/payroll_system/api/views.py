from django.forms import ValidationError
from django.shortcuts import render
from rest_framework import generics, status, mixins
from .serializers import CompanySerializer, CreateCompanySerializer, CompanyEntrySerializer, UserSerializer, DepartmentSerializer,DesignationSerializer, SalaryGradeSerializer, RegularRegisterSerializer, CategorySerializer
from .models import Company, CompanyDetails, User, OwnerToRegular, Regular
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import NotFound
from .auth.views import MyTokenObtainPairView




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
            serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        serializer.save(user=instance.owner)


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
            serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        serializer.save(user=instance.owner)

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
            serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        serializer.save(user=instance.owner)

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
            serializer.save(user=self.request.user)
        instance = OwnerToRegular.objects.get(user=user)
        serializer.save(user=instance.owner)
        
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