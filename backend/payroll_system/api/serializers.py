from dataclasses import field
from rest_framework import serializers

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular, Category, Bank, LeaveGrade, Shift, Holiday, EarningsHead, DeductionsHead, EmployeePersonalDetail
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

class HolidaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Holiday
        fields = ('id', 'user', 'company', 'name' ,'date', 'mandatory_holiday')
        read_only_fields = ('mandatory_holiday',)

class EarningsHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EarningsHead
        fields = ('id', 'user', 'company', 'name', 'mandatory_earning')
        read_only_fields = ('mandatory_earning',)

class DeductionsHeadSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = DeductionsHead
        fields = ('id', 'user', 'company', 'name', 'mandatory_deduction')
        read_only_fields = ('mandatory_deduction',)

class EmployeePersonalDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # creator_id = serializers.ReadOnlyField(source='creator.id')
    photo = serializers.ImageField(required=False)
    education_qualification = serializers.ChoiceField(choices=EmployeePersonalDetail.EDUCATION_CHOICES, allow_blank=True)
    local_state_or_union_territory = serializers.ChoiceField(choices=EmployeePersonalDetail.STATE_AND_UT_CHOICES, allow_blank=True)
    permanent_state_or_union_territory = serializers.ChoiceField(choices=EmployeePersonalDetail.STATE_AND_UT_CHOICES, allow_blank=True)
    gender = serializers.ChoiceField(choices=EmployeePersonalDetail.GENDER_CHOICES, allow_blank=True)
    marital_status = serializers.ChoiceField(choices=EmployeePersonalDetail.MARITAL_STATUS_CHOICES, allow_blank=True)
    blood_group = serializers.ChoiceField(choices=EmployeePersonalDetail.BLOOD_GROUP_CHOICES, allow_blank=True)
    isActive = serializers.ReadOnlyField()
    created_at = serializers.ReadOnlyField()

    class Meta:
        model = EmployeePersonalDetail
        fields = ['id', 'user', 'company', 'name', 'paycode', 'attendance_card_no', 'photo',
                  'father_or_husband_name', 'mother_name', 'wife_name', 'dob', 'phone_number', 'alternate_phone_number',
                  'email', 'pan_number', 'driving_licence', 'passport', 'aadhaar', 'handicapped', 'gender',
                  'marital_status', 'blood_group', 'religion', 'education_qualification', 'technical_qualification',
                  'local_address', 'local_district', 'local_state_or_union_territory', 'local_pincode',
                  'permanent_address', 'permanent_district', 'permanent_state_or_union_territory', 'permanent_pincode',
                  'isActive', 'created_at']
