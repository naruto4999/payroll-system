from django.urls import path, include
from .views import CompanyListCreateAPIView, CompanyDetailsMixinView, CompanyRetrieveUpdateDestroyAPIView

urlpatterns = [
    path('company', CompanyListCreateAPIView.as_view()),
    path('edit-company/<int:id>', CompanyRetrieveUpdateDestroyAPIView.as_view()),
    
    path('company-details', CompanyDetailsMixinView.as_view()),
    path('company-details/<int:company_id>', CompanyDetailsMixinView.as_view()),
    path('', include('api.routers',)),

]

