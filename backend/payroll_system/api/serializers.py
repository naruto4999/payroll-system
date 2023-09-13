from dataclasses import field
from rest_framework import serializers

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular, Category, Bank, LeaveGrade, Shift, Holiday, EarningsHead, DeductionsHead, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeeSalaryEarning, EmployeeSalaryDetail, EmployeeFamilyNomineeDetial, EmployeePfEsiDetail, WeeklyOffHolidayOff, PfEsiSetup, Calculations, EmployeeShifts, EmployeeAttendance, EmployeeGenerativeLeaveRecord, EmployeeLeaveOpening, EmployeePresentCount, EmployeeAdvancePayment
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
    class Meta:
        model = LeaveGrade
        fields = ('id', 'company', 'name' ,'limit', 'paid', 'generate_frequency', 'mandatory_leave')
        read_only_fields = ('mandatory_leave',)

class ShiftSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Shift
        fields = ('id', 'user', 'company', 'name' ,'beginning_time', 'end_time', 'lunch_time', 'tea_time', 'late_grace', 'ot_begin_after', 'half_day_minimum_minutes', 'full_day_minimum_minutes', "max_late_allowed_min", 'short_leaves', 'next_shift_delay', 'accidental_punch_buffer')

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
        

class EmployeeListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    paycode = serializers.IntegerField(read_only=True)
    attendance_card_no = serializers.IntegerField(read_only=True)
    date_of_joining = serializers.DateField(source='employee_professional_detail.date_of_joining', read_only=True)
    designation = serializers.CharField(source='employee_professional_detail.designation', read_only=True)
    resignation_date = serializers.DateField(source='employee_professional_detail.resignation_date', read_only=True)
    class Meta:
        fields = ['id', 'name', 'paycode', 'attendance_card_no', 'date_of_joining', 'designation', 'resignation_date']


class EmployeeProfessionalDetailSerializer(serializers.ModelSerializer):
    weekly_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.WEEKDAY_CHOICES, allow_blank=False)
    extra_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.EXTRA_OFF_CHOICES, allow_blank=False)

    class Meta:
        model = EmployeeProfessionalDetail
        fields = ['company', 'employee', 'date_of_joining', 'date_of_confirm', 'department', 'designation', 'category', 'salary_grade', 'weekly_off', 'extra_off', 'resigned', 'resignation_date']


class EmployeeSalaryEarningSerializer(serializers.ModelSerializer):
    earnings_head = EarningsHeadSerializer()
    class Meta:
        model = EmployeeSalaryEarning
        fields = ['employee', 'company', 'earnings_head', 'value', 'from_date', 'to_date']

class EmployeeSalaryEarningUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalaryEarning
        fields = ['employee', 'company', 'earnings_head', 'value', 'from_date', 'to_date']
    
class EmployeeSalaryDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalaryDetail
        fields = ['company', 'employee', 'overtime_type', 'overtime_rate', 'salary_mode', 'payment_mode', 'bank_name', 'account_number', 'ifcs', 'labour_wellfare_fund', 'late_deduction', 'bonus_allow', 'bonus_exg']


class EmployeePfEsiDetailSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = EmployeePfEsiDetail
        fields = ['user', 'company', 'employee', 'pf_allow', 'pf_number', 'pf_limit_ignore_employee', 'pf_limit_ignore_employee_value', 'pf_limit_ignore_employer', 'pf_limit_ignore_employer_value', 'pf_percent_ignore_employee', 'pf_percent_ignore_employee_value', 'pf_percent_ignore_employer', 'pf_percent_ignore_employer_value', 'uan_number', 'esi_allow', 'esi_number', 'esi_dispensary', 'esi_on_ot',
        ]

class EmployeeFamilyNomineeDetialSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeFamilyNomineeDetial
        fields = ['id', 'company', 'employee', 'name', 'address', 'dob', 'relation', 'residing', 'esi_benefit', 'pf_benefits', 'is_esi_nominee', 'esi_nominee_share', 'is_pf_nominee', 'pf_nominee_share', 'is_fa_nominee', 'fa_nominee_share', 'is_gratuity_nominee', 'gratuity_nominee_share',]

class WeeklyOffHolidayOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = WeeklyOffHolidayOff
        fields = ('company', 'min_days_for_weekly_off', 'min_days_for_holiday_off')
    
class PfEsiSetupSerializer(serializers.ModelSerializer):
    class Meta:
        model = PfEsiSetup
        fields = ('company', 'ac_1_epf_employee_percentage', 'ac_1_epf_employee_limit', 'ac_1_epf_employer_percentage', 'ac_1_epf_employer_limit', 'ac_10_eps_employer_percentage', 'ac_10_eps_employer_limit', 'ac_2_employer_percentage', 'ac_21_employer_percentage', 'ac_22_employer_percentage', 'employer_pf_code', 'esi_employee_percentage', 'esi_employee_limit', 'esi_employer_percentage', 'esi_employer_limit', 'employer_esi_code',)


class CalculationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculations
        fields = ('company' ,'ot_calculation', 'el_calculation', 'notice_pay', 'service_calculation', 'gratuity_calculation', 'el_days_calculation',)

class EmployeeShiftsSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer()
    class Meta:
        model = EmployeeShifts
        fields = ['employee', 'company', 'shift', 'from_date', 'to_date']

class EmployeeShiftsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShifts
        fields = ['employee', 'company', 'shift', 'from_date', 'to_date']

class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = ['id', 'employee', 'company', 'machine_in', 'machine_out', 'manual_in', 'manual_out', 'first_half', 'second_half', 'date', 'ot_min', 'late_min', 'manual_mode']

class EmployeeGenerativeLeaveRecordSerializer(serializers.ModelSerializer):
    leave = LeaveGradeSerializer()
    class Meta:
        model = EmployeeGenerativeLeaveRecord
        fields = ['id', 'employee', 'company', 'leave', 'date', 'leave_count']

class EmployeePresentCountSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePresentCount
        fields = ['id', 'employee', 'company', 'date', 'present_count']

class EmployeeLeaveOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveOpening
        fields = ['id', 'employee', 'company', 'leave', 'leave_count', 'year']

class EmployeeAdvancePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAdvancePayment
        fields = ('id', 'employee', 'company', 'principal', 'emi', 'date', 'closed', 'closed_date', 'tenure_months', 'repaid_amount')