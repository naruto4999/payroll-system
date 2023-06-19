from dataclasses import field
from rest_framework import serializers

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular, Category, Bank, LeaveGrade, Shift
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
        fields =  ('id', 'name', 'user', 'visible')

class CompanyVisibilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'visible']
        
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
    email = serializers.EmailField(required=True, write_only=False, max_length=128)
    owner = UserSerializer(read_only=True)


    class Meta:
        model = Regular
        fields = ['id', 'username', 'email', 'password', 'is_active', 'owner', 'phone_no']

    # def create(self, validated_data):
    #     user = Regular.objects.create_user(**validated_data)
    #     return user

class CategorySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Category
        fields = ('id', 'user', 'company', 'name')

class BankSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Bank
        fields = ('id', 'user', 'company', 'name')

class LeaveGradeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = LeaveGrade
        fields = ('id', 'user', 'company', 'name' ,'limit', 'mandatory_leave')
        read_only_fields = ('mandatory_leave',)

class ShiftSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Shift
        fields = ('id', 'user', 'company', 'name' ,'beginning_time', 'end_time', 'lunch_time', 'tea_time', 'late_grace', 'ot_begin_after', 'half_day_minimum_minutes', 'full_day_minimum_minutes', 'short_leaves', 'next_shift_dealy', 'accidental_punch_buffer')