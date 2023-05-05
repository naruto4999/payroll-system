from dataclasses import field
from rest_framework import serializers

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular
from rest_framework import serializers



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_active', 'phone_no']
        read_only_field = ['is_active']

class CompanySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Company
        fields =  ('id', 'name', 'user')

        # def to_representation(self, instance):
        #     response = super().to_representation(instance)
        #     response['user'] = UserSerializer(instance.user).data
        #     print(response)
        #     return response

class CreateCompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name',)

class CompanyEntrySerializer(serializers.ModelSerializer):
    #comp = serializers.StringRelatedField(many=False, read_only=True)
    user = UserSerializer(read_only=True)
    class Meta:
        model = CompanyDetails
        #fields = ('company', 'address', 'key_person', 'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no', 'registration_no', 'registration_date')
        fields = ('user', 'company', 'address', 'key_person' ,'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no')

        def to_representation(self, instance):
            print(instance)
            response = super().to_representation(instance)
            response['company'] = CompanySerializer(instance.company).data
            print(response)
            return response

            # self.fields['company'] =  CompanySerializer(read_only=True)
            # return super(CompanyEntrySerializer, self).to_representation(instance)

class DepartmentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Deparment
        fields = ('id', 'user', 'company', 'name')

class DesignationSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Designation
        fields = ('id', 'user', 'company', 'name')

class SalaryGradeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = SalaryGrade
        fields = ('id', 'user', 'company', 'name')

class RegularRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True, required=True)
    email = serializers.EmailField(required=True, write_only=True, max_length=128)
    owner = UserSerializer(read_only=True)


    class Meta:
        model = Regular
        fields = ['id', 'username', 'email', 'password', 'is_active', 'owner']

    def create(self, validated_data):
        user = Regular.objects.create_user(**validated_data)
        print(user)
        return user