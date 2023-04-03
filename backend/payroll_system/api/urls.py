from django.urls import path, include
from .views import CompanyListCreateAPIView, CompanyDetailsMixinView, CompanyRetrieveUpdateDestroyAPIView, DepartmentListCreateAPIView, DepartmentRetrieveUpdateDestroyAPIView, DesignationListCreateAPIView, DesignationRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('company', CompanyListCreateAPIView.as_view()),
    path('edit-company/<int:id>', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    
    path('company-details', CompanyDetailsMixinView.as_view()),
    path('company-details/<int:company_id>', CompanyDetailsMixinView.as_view()),
    path('', include('api.routers',)),
    path('department/<int:company_id>', DepartmentListCreateAPIView.as_view()),
    path('department/<int:company_id>/<int:id>', DepartmentRetrieveUpdateDestroyAPIView.as_view()),
    path('designation/<int:company_id>', DesignationListCreateAPIView.as_view()),
    path('designation/<int:company_id>/<int:id>', DesignationRetrieveUpdateDestroyAPIView.as_view()),

]

