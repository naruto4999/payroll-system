import calendar
from dataclasses import field
from datetime import date

from django.db.models import Sum

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular, Category, Bank, LeaveGrade, Shift, Holiday, EarningsHead, OvertimePolicy, OvertimePolicyDayRule, OvertimePolicyEarningsHead, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeeSalaryEarning, EmployeeSalaryDetail, EmployeeFamilyNomineeDetial, EmployeePfEsiDetail, WeeklyOffHolidayOff, PfEsiSetup, Calculations, EmployeeShifts, EmployeeAttendance, EmployeeAttendanceOvertimeDetail, EmployeeGenerativeLeaveRecord, EmployeeLeaveOpening, EmployeeMonthlyAttendanceDetails, EmployeeAdvancePayment, EmployeeSalaryPrepared, EmployeeSalaryPreparedOvertimeDetail, EarnedAmount, BonusCalculation, BonusPercentage, FullAndFinal, SubUserOvertimeSettings, SubUserMiscSettings, AttendanceMachineConfig
from rest_framework import serializers

from .services.overtime_policy import create_overtime_policy, update_overtime_policy


ATTENDANCE_HISTORY_MIN_DATE = date(2009, 1, 1)


def validate_attendance_period_not_before_cutoff(attrs):
    from_date = date(attrs['year'], attrs['month'], attrs.get('month_from_date', 1))
    if from_date < ATTENDANCE_HISTORY_MIN_DATE:
        raise serializers.ValidationError({'date': 'Attendance cannot be created before 2009-01-01.'})
    return attrs

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
    company = serializers.PrimaryKeyRelatedField(queryset=Company.objects.all(), validators=[])
    #comp = serializers.StringRelatedField(many=False, read_only=True)
    # user = UserSerializer(read_only=True)
    class Meta:
        model = CompanyDetails
        #fields = ('company', 'address', 'key_person', 'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no', 'registration_no', 'registration_date')
        fields = ('company', 'address', 'key_person' ,'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no', 'payroll_timezone')

    def validate_company(self, company):
        request_user = self.context['request'].user
        owner = request_user if request_user.role == 'OWNER' else request_user.regular_to_owner.owner
        if company.user_id != owner.id or (request_user.role == 'REGULAR' and not company.visible):
            raise serializers.ValidationError('Company does not belong to the authenticated account scope.')
        return company

    def create(self, validated_data):
        company = validated_data.pop('company')
        user = validated_data.pop('user')
        instance, created = CompanyDetails.objects.get_or_create(
            company=company,
            defaults={'user': user, **validated_data},
        )
        if not created:
            instance.user = user
            for field_name, value in validated_data.items():
                setattr(instance, field_name, value)
            instance.full_clean()
            instance.save()
        return instance

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

class RegularRetrieveUpdateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128, min_length=8, write_only=True)
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
        fields = ('id', 'user', 'company', 'name' ,'beginning_time', 'end_time', 'lunch_duration', 'lunch_beginning_time', 'tea_time', 'late_grace', 'ot_begin_after', 'half_day_minimum_minutes', 'full_day_minimum_minutes', "max_late_allowed_min", 'short_leaves', 'next_shift_delay', 'accidental_punch_buffer')

class HolidaySerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Holiday
        fields = ('id', 'user', 'company', 'name' ,'date', 'mandatory_holiday')
        read_only_fields = ('mandatory_holiday',)

class EarningsHeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EarningsHead
        fields = ('id', 'company', 'name', 'mandatory_earning')
        read_only_fields = ('mandatory_earning',)


class OvertimePolicyDayRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = OvertimePolicyDayRule
        fields = ('id', 'day_type', 'multiplier', 'late_deduction_priority')


class OvertimePolicySerializer(serializers.ModelSerializer):
    day_rules = OvertimePolicyDayRuleSerializer(many=True, required=False)
    selected_earning_head_ids = serializers.PrimaryKeyRelatedField(
        source='selected_earning_heads',
        many=True,
        queryset=EarningsHead.objects.all(),
        required=False,
        write_only=True,
    )
    selected_earning_heads = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = OvertimePolicy
        fields = (
            'id',
            'company',
            'name',
            'code',
            'is_default',
            'is_active',
            'is_system',
            'earnings_basis',
            'rounding_increment_minutes',
            'round_up_from_minutes',
            'day_rules',
            'selected_earning_head_ids',
            'selected_earning_heads',
        )
        read_only_fields = ('company', 'code', 'is_system')

    def get_selected_earning_heads(self, obj):
        return EarningsHeadSerializer([link.earnings_head for link in obj.selected_earning_heads.all()], many=True).data

    def validate(self, attrs):
        company = self.context.get('company') or getattr(self.instance, 'company', None)
        submitted_company = self.initial_data.get('company')
        if submitted_company is not None and company is not None and str(submitted_company) != str(company.pk):
            raise serializers.ValidationError({'company': 'Company is bound by the URL and cannot be changed.'})
        if self.instance is not None and self.instance.is_system:
            if 'code' in self.initial_data and self.initial_data['code'] != self.instance.code:
                raise serializers.ValidationError({'code': 'System policy definitions cannot be changed.'})
            if 'is_system' in self.initial_data and bool(self.initial_data['is_system']) != self.instance.is_system:
                raise serializers.ValidationError({'is_system': 'System policy definitions cannot be changed.'})

        day_rules = attrs.get('day_rules')
        if day_rules is not None:
            day_types = [rule['day_type'] for rule in day_rules]
            priorities = [rule['late_deduction_priority'] for rule in day_rules]
            if len(day_types) != len(set(day_types)):
                raise serializers.ValidationError({'day_rules': 'Day types must be unique.'})
            if len(priorities) != len(set(priorities)):
                raise serializers.ValidationError({'day_rules': 'Late-deduction priorities must be unique.'})
            if any(priority < 1 for priority in priorities):
                raise serializers.ValidationError({'day_rules': 'Late-deduction priorities must be at least 1.'})

        selected_heads = attrs.get('selected_earning_heads')
        if selected_heads is not None and len(selected_heads) != len({head.pk for head in selected_heads}):
            raise serializers.ValidationError({'selected_earning_head_ids': 'Selected earning heads must be unique.'})
        selected_heads_for_validation = selected_heads
        if selected_heads_for_validation is None and self.instance is not None:
            selected_heads_for_validation = [link.earnings_head for link in self.instance.selected_earning_heads.all()]
        selected_heads_for_validation = selected_heads_for_validation or []
        for earnings_head in selected_heads_for_validation:
            if earnings_head.company_id != company.id:
                raise serializers.ValidationError({'selected_earning_head_ids': 'All selected earning heads must belong to the policy company.'})

        resulting_basis = attrs.get('earnings_basis', getattr(self.instance, 'earnings_basis', OvertimePolicy.EARNINGS_BASIS_ALL))
        previous_basis = getattr(self.instance, 'earnings_basis', None)
        if resulting_basis == OvertimePolicy.EARNINGS_BASIS_SELECTED:
            if previous_basis != OvertimePolicy.EARNINGS_BASIS_SELECTED and selected_heads is None:
                raise serializers.ValidationError({'selected_earning_head_ids': 'A non-empty list is required when selecting SELECTED_HEADS.'})
            if not selected_heads_for_validation:
                raise serializers.ValidationError({'selected_earning_head_ids': 'At least one earning head is required for SELECTED_HEADS.'})
        elif resulting_basis == OvertimePolicy.EARNINGS_BASIS_ALL:
            attrs['selected_earning_heads'] = []

        resulting_default = attrs.get('is_default', getattr(self.instance, 'is_default', False))
        resulting_active = attrs.get('is_active', getattr(self.instance, 'is_active', True))
        if resulting_default and not resulting_active:
            raise serializers.ValidationError({'is_default': 'An inactive policy cannot be the company default.'})
        if self.instance is not None and self.instance.is_default and not resulting_default:
            raise serializers.ValidationError({'is_default': 'Select another default instead of clearing the active default.'})

        resulting_increment = attrs.get(
            'rounding_increment_minutes', getattr(self.instance, 'rounding_increment_minutes', 30)
        )
        resulting_threshold = attrs.get(
            'round_up_from_minutes', getattr(self.instance, 'round_up_from_minutes', 16)
        )
        if resulting_increment <= 0:
            raise serializers.ValidationError({'rounding_increment_minutes': 'Rounding increment must be greater than zero.'})
        if resulting_threshold < 1:
            raise serializers.ValidationError({'round_up_from_minutes': 'Round-up threshold must be at least 1.'})
        if resulting_threshold > resulting_increment:
            raise serializers.ValidationError({'round_up_from_minutes': 'Round-up threshold cannot exceed the rounding increment.'})

        if self.instance is not None and self.instance.is_system:
            protected = ('name', 'is_active', 'earnings_basis')
            changed = [field for field in protected if field in attrs and attrs[field] != getattr(self.instance, field)]
            if day_rules is not None:
                changed.append('day_rules')
            if selected_heads is not None and [head.pk for head in selected_heads] != list(
                self.instance.selected_earning_heads.values_list('earnings_head_id', flat=True)
            ):
                changed.append('selected_earning_head_ids')
            if changed:
                raise serializers.ValidationError({field: 'System policy definitions cannot be changed.' for field in changed})
        return attrs

    def create(self, validated_data):
        day_rules = validated_data.pop('day_rules', None)
        selected_heads = validated_data.pop('selected_earning_heads', None)
        try:
            return create_overtime_policy(
                actor=self.context['request'].user,
                company=self.context['company'],
                validated_data=validated_data,
                day_rules=day_rules,
                selected_heads=selected_heads,
            )
        except Exception as exc:
            self._raise_service_validation(exc)

    def update(self, instance, validated_data):
        day_rules = validated_data.pop('day_rules', None)
        selected_heads = validated_data.pop('selected_earning_heads', None)
        try:
            return update_overtime_policy(
                actor=self.context['request'].user,
                company=self.context['company'],
                policy=instance,
                validated_data=validated_data,
                day_rules=day_rules,
                selected_heads=selected_heads,
            )
        except Exception as exc:
            self._raise_service_validation(exc)

    @staticmethod
    def _raise_service_validation(exc):
        from django.core.exceptions import ValidationError as DjangoValidationError
        from django.db import IntegrityError

        if isinstance(exc, DjangoValidationError):
            detail = getattr(exc, 'message_dict', None) or getattr(exc, 'messages', None)
            raise serializers.ValidationError(detail) from exc
        if isinstance(exc, IntegrityError):
            raise serializers.ValidationError('The policy conflicts with existing overtime configuration.') from exc
        raise exc

# class DeductionsHeadSerializer(serializers.ModelSerializer):
#     user = UserSerializer(read_only=True)
#     class Meta:
#         model = DeductionsHead
#         fields = ('id', 'user', 'company', 'name', 'mandatory_deduction')
#         read_only_fields = ('mandatory_deduction',)

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
                  'isActive', 'created_at', 'nationality']
        
    #Just return the absolute path of the photo without the domain so that domain can be added on client side
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        if instance.photo:
            representation['photo'] = instance.photo.url
        return representation


class EmployeeListSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    paycode = serializers.CharField(read_only=True)
    attendance_card_no = serializers.IntegerField(read_only=True)
    date_of_joining = serializers.DateField(source='employee_professional_detail.date_of_joining', read_only=True)
    designation = serializers.CharField(source='employee_professional_detail.designation', read_only=True)
    resignation_date = serializers.DateField(source='employee_professional_detail.resignation_date', read_only=True)
    pf_allow = serializers.BooleanField(source='employee_pf_esi_detail.pf_allow', read_only=True)
    esi_allow = serializers.BooleanField(source='employee_pf_esi_detail.esi_allow', read_only=True)
    visible = serializers.BooleanField(read_only=True, default=False)
    class Meta:
        fields = ['id', 'name', 'paycode', 'attendance_card_no', 'date_of_joining', 'designation', 'resignation_date', 'pf_allow', 'esi_allow', 'visible']


class EmployeeProfessionalDetailSerializer(serializers.ModelSerializer):
    weekly_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.WEEKDAY_CHOICES, allow_blank=False)
    extra_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.EXTRA_OFF_CHOICES, allow_blank=False)

    class Meta:
        model = EmployeeProfessionalDetail
        fields = ['company', 'employee', 'date_of_joining', 'date_of_confirm', 'department', 'designation', 'category', 'salary_grade', 'weekly_off', 'extra_off', 'resigned', 'resignation_date', 'first_previous_experience_company_name', 'first_previous_experience_from_date', 'first_previous_experience_to_date', 'first_previous_experience_designation', 'first_previous_experience_reason_for_leaving', 'first_previous_experience_salary', 'second_previous_experience_company_name', 'second_previous_experience_from_date', 'second_previous_experience_to_date', 'second_previous_experience_designation', 'second_previous_experience_reason_for_leaving', 'second_previous_experience_salary', 'third_previous_experience_company_name', 'third_previous_experience_from_date', 'third_previous_experience_to_date', 'third_previous_experience_designation', 'third_previous_experience_reason_for_leaving', 'third_previous_experience_salary', 'first_reference_name', 'first_reference_address', 'first_reference_relation', 'first_reference_phone', 'second_reference_name', 'second_reference_address', 'second_reference_relation', 'second_reference_phone'
]
        
class EmployeeProfessionalDetailRetrieveSerializer(serializers.ModelSerializer):
    weekly_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.WEEKDAY_CHOICES, allow_blank=False)
    extra_off = serializers.ChoiceField(choices=EmployeeProfessionalDetail.EXTRA_OFF_CHOICES, allow_blank=False)
    department = DepartmentSerializer()
    designation = DesignationSerializer()

    class Meta:
        model = EmployeeProfessionalDetail
        fields = ['company', 'employee', 'date_of_joining', 'date_of_confirm', 'department', 'designation', 'category', 'salary_grade', 'weekly_off', 'extra_off', 'resigned', 'resignation_date', 'first_previous_experience_company_name', 'first_previous_experience_from_date', 'first_previous_experience_to_date', 'first_previous_experience_designation', 'first_previous_experience_reason_for_leaving', 'first_previous_experience_salary', 'second_previous_experience_company_name', 'second_previous_experience_from_date', 'second_previous_experience_to_date', 'second_previous_experience_designation', 'second_previous_experience_reason_for_leaving', 'second_previous_experience_salary', 'third_previous_experience_company_name', 'third_previous_experience_from_date', 'third_previous_experience_to_date', 'third_previous_experience_designation', 'third_previous_experience_reason_for_leaving', 'third_previous_experience_salary', 'first_reference_name', 'first_reference_address', 'first_reference_relation', 'first_reference_phone', 'second_reference_name', 'second_reference_address', 'second_reference_relation', 'second_reference_phone'
]


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
    resolved_overtime_policy = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = EmployeeSalaryDetail
        fields = ['company', 'employee', 'overtime_policy', 'resolved_overtime_policy', 'overtime_type', 'overtime_rate', 'salary_mode', 'payment_mode', 'bank_name', 'account_number', 'ifcs', 'labour_wellfare_fund', 'late_deduction', 'bonus_allow', 'bonus_exg']

    def get_resolved_overtime_policy(self, obj):
        from .services.overtime_policy import resolve_calculation_overtime_policy, resolve_employee_overtime_policy

        request = self.context.get('request')
        policy = (
            resolve_calculation_overtime_policy(actor=request.user, employee_salary_detail=obj)
            if request and request.user.is_authenticated
            else resolve_employee_overtime_policy(obj)
        )
        return OvertimePolicySerializer(policy).data

    def validate_overtime_policy(self, policy):
        company = self.context.get('company')
        company_id = getattr(company, 'pk', None) or self.initial_data.get('company') or getattr(self.instance, 'company_id', None)
        if policy and company_id and policy.company_id != int(company_id):
            raise serializers.ValidationError('Overtime policy must belong to the employee company.')
        existing_policy_id = getattr(self.instance, 'overtime_policy_id', None)
        if policy and not policy.is_active and policy.id != existing_policy_id:
            raise serializers.ValidationError('Inactive overtime policies cannot be newly assigned.')
        return policy

    def validate(self, attrs):
        company = self.context.get('company') or attrs.get('company') or getattr(self.instance, 'company', None)
        employee = attrs.get('employee') or getattr(self.instance, 'employee', None)
        if self.instance is not None:
            if 'company' in attrs and attrs['company'].pk != self.instance.company_id:
                raise serializers.ValidationError({'company': 'Employee salary details cannot be moved to another company.'})
            if 'employee' in attrs and attrs['employee'].pk != self.instance.employee_id:
                raise serializers.ValidationError({'employee': 'Employee salary details cannot be moved to another employee.'})
        if company and employee and (employee.company_id != company.pk or employee.user_id != company.user_id):
            raise serializers.ValidationError({'employee': 'Employee must belong to the salary-detail company.'})
        policy = attrs.get('overtime_policy', getattr(self.instance, 'overtime_policy', None))
        if policy and company and policy.company_id != company.pk:
            raise serializers.ValidationError({'overtime_policy': 'Overtime policy must belong to the employee company.'})
        return attrs


class EmployeePfEsiDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeePfEsiDetail
        fields = ['company', 'employee', 'pf_allow', 'pf_number', 'pf_limit_ignore_employee', 'pf_limit_ignore_employee_value', 'pf_limit_ignore_employer', 'pf_limit_ignore_employer_value', 'uan_number', 'esi_allow', 'esi_number', 'esi_dispensary', 'esi_on_ot', 'vpf_amount', 'tds_amount']

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
        fields = ('company', 'ac_1_epf_employee_percentage', 'ac_1_epf_employee_limit', 'ac_1_epf_employer_percentage', 'ac_1_epf_employer_limit', 'ac_10_eps_employer_percentage', 'ac_10_eps_employer_limit', 'ac_2_employer_percentage', 'ac_21_employer_percentage', 'ac_22_employer_percentage', 'employer_pf_code', 'esi_employee_percentage', 'esi_employee_limit', 'esi_employer_percentage', 'esi_employer_limit', 'employer_esi_code', 'enable_labour_welfare_fund', 'labour_wellfare_fund_employer_code', 'labour_welfare_fund_percentage', 'labour_welfare_fund_limit')

class CalculationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Calculations
        fields = ('company' ,'ot_calculation', 'el_calculation', 'notice_pay', 'service_calculation', 'gratuity_calculation', 'el_days_calculation', 'bonus_start_month', 'bonus_calculation_days', 'gratuity_salary')

class EmployeeShiftsSerializer(serializers.ModelSerializer):
    shift = ShiftSerializer()
    class Meta:
        model = EmployeeShifts
        fields = ['employee', 'company', 'shift', 'from_date', 'to_date']

class EmployeeShiftsUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeShifts
        fields = ['employee', 'company', 'shift', 'from_date', 'to_date']

class AttendanceOvertimeExclusionInputSerializer(serializers.Serializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    exclusion_reason = serializers.ChoiceField(
        choices=EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES,
    )
    exclusion_note = serializers.CharField(required=False, allow_blank=True, max_length=255)


class AttendanceOvertimeIntervalInputSerializer(serializers.Serializer):
    start_datetime = serializers.DateTimeField()
    end_datetime = serializers.DateTimeField()
    excluded_minutes = serializers.IntegerField(required=False, min_value=0)
    exclusion_reason = serializers.ChoiceField(
        choices=EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES,
        required=False,
    )
    exclusion_note = serializers.CharField(required=False, allow_blank=True, max_length=255)
    exclusions = AttendanceOvertimeExclusionInputSerializer(many=True, required=False)


class AttendanceOvertimeDurationInputSerializer(serializers.Serializer):
    work_date = serializers.DateField()
    gross_minutes = serializers.IntegerField(min_value=1)
    excluded_minutes = serializers.IntegerField(required=False, min_value=0)
    exclusion_reason = serializers.ChoiceField(
        choices=EmployeeAttendanceOvertimeDetail.EXCLUSION_REASON_CHOICES,
        required=False,
    )
    exclusion_note = serializers.CharField(required=False, allow_blank=True, max_length=255)


class EmployeeAttendanceOvertimeDetailSerializer(serializers.ModelSerializer):
    attendance = serializers.SerializerMethodField()
    exclusion_reason_display = serializers.CharField(
        source='get_exclusion_reason_display',
        read_only=True,
    )

    def get_attendance(self, obj):
        return obj.attendance.date

    class Meta:
        model = EmployeeAttendanceOvertimeDetail
        fields = [
            'id', 'attendance', 'work_date', 'day_type', 'source', 'start_datetime', 'end_datetime',
            'gross_minutes', 'excluded_minutes', 'eligible_minutes', 'exclusion_reason',
            'exclusion_reason_display', 'exclusion_note', 'created_at', 'updated_at',
        ]
        read_only_fields = fields


class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    overtime_details = EmployeeAttendanceOvertimeDetailSerializer(many=True, read_only=True)
    overtime_intervals = AttendanceOvertimeIntervalInputSerializer(many=True, write_only=True, required=False)
    overtime_duration_entries = AttendanceOvertimeDurationInputSerializer(many=True, write_only=True, required=False)

    class Meta:
        model = EmployeeAttendance
        fields = [
            'id', 'employee', 'company', 'machine_in', 'machine_out', 'manual_in',
            'manual_out', 'first_half', 'second_half', 'date', 'ot_min', 'late_min',
            'manual_mode', 'overtime_details', 'overtime_intervals',
            'overtime_duration_entries',
        ]
        read_only_fields = ['id', 'employee', 'company', 'ot_min', 'overtime_details']

    def validate_date(self, value):
        if value < ATTENDANCE_HISTORY_MIN_DATE:
            raise serializers.ValidationError('Attendance cannot be created before 2009-01-01.')
        return value

    def create(self, validated_data):
        validated_data.pop('overtime_intervals', None)
        validated_data.pop('overtime_duration_entries', None)
        return super().create(validated_data)

    def update(self, instance, validated_data):
        validated_data.pop('overtime_intervals', None)
        validated_data.pop('overtime_duration_entries', None)
        return super().update(instance, validated_data)

class AllEmployeeCurrentMonthAttendanceSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    employee = serializers.PrimaryKeyRelatedField(read_only=True)
    company = serializers.PrimaryKeyRelatedField(read_only=True)
    machine_in = serializers.DateTimeField(read_only=True)
    machine_out = serializers.DateTimeField(read_only=True)
    manual_in = serializers.DateTimeField(read_only=True)
    manual_out = serializers.DateTimeField(read_only=True)
    first_half = serializers.BooleanField(read_only=True)
    second_half = serializers.BooleanField(read_only=True)
    date = serializers.DateField(read_only=True)
    ot_min = serializers.IntegerField(read_only=True)
    late_min = serializers.IntegerField(read_only=True)
    manual_mode = serializers.BooleanField(read_only=True)

class EmployeeGenerativeLeaveRecordSerializer(serializers.ModelSerializer):
    leave = LeaveGradeSerializer()
    class Meta:
        model = EmployeeGenerativeLeaveRecord
        fields = ['id', 'employee', 'company', 'leave', 'date', 'leave_count']

class EmployeeMonthlyAttendancePresentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMonthlyAttendanceDetails
        fields = ['id', 'employee', 'company', 'date', 'present_count']

class EmployeeMonthlyAttendanceDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeMonthlyAttendanceDetails
        fields = ['id', 'employee', 'company', 'date', 'present_count', 'weekly_off_days_count', 'paid_days_count', 'holiday_days_count', 'not_paid_days_count', 'net_ot_minutes_monthly']

class EmployeeLeaveOpeningSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveOpening
        fields = ['id', 'employee', 'company', 'leave', 'leave_count', 'year']

class LeaveClosingTransferSerializer(serializers.Serializer):
    from_year = serializers.IntegerField(allow_null=False)
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    leave_ids = serializers.ListField(child=serializers.IntegerField())
    company = serializers.IntegerField()


# class FiltersAttendanceReportsSerializer(serializers.Serializer):
#     group_by = serializers.ChoiceField(choices=["none", "department"])
#     month_from_date = serializers.IntegerField(allow_null=True)
#     month_to_date = serializers.IntegerField(allow_null=True)
#     resignation_filter = serializers.ChoiceField(choices=["all", "without_resigned", "only_resigned"])
#     sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
#     date = serializers.IntegerField(allow_null=True)
#
# class AttendanceReportsSerializer(serializers.Serializer):
    # employee_ids = serializers.ListField(child=serializers.IntegerField())
    # filters = FiltersAttendanceReportsSerializer()
    # company = serializers.IntegerField()
    # month = serializers.IntegerField()
    # year = serializers.IntegerField()
    # report_type = serializers.ChoiceField(choices=["present_report", "attendance_register", "form_14", "overtime_sheet_daily", "bonus_calculation_sheet", "bonus_form_c"])
    # class Meta:
    #     fields = ['employee_ids', "filters"]
    #
#
class EmployeeLeaveOpeningElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeLeaveOpening
        fields = ['employee', 'leave', 'leave_count']
    


class EmployeeLeaveOpeningCreateUpdateSerializer(serializers.Serializer):
    leave_openings = serializers.ListField(child=EmployeeLeaveOpeningElementSerializer())
    year = serializers.IntegerField()
    company = serializers.IntegerField()
    class Meta:
        fields = ["leave_openings", "year", "company"]


class EmployeeAdvancePaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAdvancePayment
        fields = ('id', 'employee', 'company', 'principal', 'emi', 'date', 'closed', 'closed_date', 'tenure_months_left', 'repaid_amount')

class EmployeeSalaryPreparedSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = EmployeeSalaryPrepared
        fields = ('id', 'employee', 'company', 'date', 'incentive_amount', 'pf_deducted', 'esi_deducted', 'vpf_deducted', 'advance_deducted', 'tds_deducted', 'labour_welfare_fund_deducted', 'others_deducted', 'net_ot_minutes_monthly', 'net_ot_amount_monthly', 'ot_rounding_increment_minutes', 'ot_round_up_from_minutes', 'payment_mode')
        read_only_fields = ('net_ot_minutes_monthly', 'net_ot_amount_monthly', 'ot_rounding_increment_minutes', 'ot_round_up_from_minutes')


class SalaryOvertimePreviewSerializer(serializers.Serializer):
    company = serializers.IntegerField(min_value=1)
    employee = serializers.IntegerField(min_value=1)
    year = serializers.IntegerField(min_value=1950, max_value=2100)
    month = serializers.IntegerField(min_value=1, max_value=12)


class SalaryArrearInputSerializer(serializers.Serializer):
    earnings_head = serializers.IntegerField(min_value=1)
    arear_amount = serializers.IntegerField(min_value=0, default=0)


class SalaryPreparationPreviewSerializer(SalaryOvertimePreviewSerializer):
    incentive_amount = serializers.IntegerField(min_value=0, default=0)
    advance_deducted = serializers.IntegerField(min_value=0, allow_null=True, default=None)
    vpf_deducted = serializers.IntegerField(min_value=0, allow_null=True, default=None)
    tds_deducted = serializers.IntegerField(min_value=0, allow_null=True, default=None)
    others_deducted = serializers.IntegerField(min_value=0, default=0)
    arrears = SalaryArrearInputSerializer(many=True, required=False, default=list)


class SalaryPreparationParentInputSerializer(serializers.Serializer):
    employee = serializers.IntegerField(min_value=1)
    company = serializers.IntegerField(min_value=1)
    date = serializers.DateField()
    incentive_amount = serializers.IntegerField(min_value=0, default=0)
    advance_deducted = serializers.IntegerField(min_value=0, default=0)
    others_deducted = serializers.IntegerField(min_value=0, default=0)
    pf_deducted = serializers.IntegerField(min_value=0, required=False)
    esi_deducted = serializers.IntegerField(min_value=0, required=False)
    vpf_deducted = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    tds_deducted = serializers.IntegerField(min_value=0, allow_null=True, required=False)
    labour_welfare_fund_deducted = serializers.IntegerField(min_value=0, required=False)
    payment_mode = serializers.CharField(required=False)

    def to_internal_value(self, data):
        prohibited = sorted({
            'pf_deducted',
            'esi_deducted',
            'labour_welfare_fund_deducted',
            'payment_mode',
            'net_ot_minutes_monthly',
            'net_ot_amount_monthly',
            'ot_rounding_increment_minutes',
            'ot_round_up_from_minutes',
            'overtime_breakdown',
        } & set(data))
        if prohibited:
            raise serializers.ValidationError({
                field: 'This overtime field is server-owned.' for field in prohibited
            })
        return super().to_internal_value(data)

    def validate_date(self, value):
        if value.day != 1:
            raise serializers.ValidationError('Salary periods must start on the first day of a month.')
        return value


class EmployeeSalaryPreparationRequestSerializer(serializers.Serializer):
    employee_salary_prepared = SalaryPreparationParentInputSerializer()
    all_earned_amounts = serializers.ListField(child=serializers.DictField(), allow_empty=False)


class EmployeeSalaryPreparedOvertimeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeSalaryPreparedOvertimeDetail
        fields = ('day_type', 'gross_minutes', 'deducted_late_minutes', 'net_minutes', 'multiplier', 'eligible_salary_rate', 'divisor', 'amount')

class EmployeeSalaryPreparedWithEarnedAmountSerializer(serializers.ModelSerializer):
    earned_amounts = serializers.SerializerMethodField()
    overtime_breakdown = EmployeeSalaryPreparedOvertimeDetailSerializer(many=True, read_only=True)
    net_salary = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = EmployeeSalaryPrepared
        fields = ('id', 'employee', 'company', 'date', 'incentive_amount', 'pf_deducted', 'esi_deducted', 'vpf_deducted', 'advance_deducted', 'tds_deducted', 'labour_welfare_fund_deducted', 'others_deducted', 'net_ot_minutes_monthly', 'net_ot_amount_monthly', 'ot_rounding_increment_minutes', 'ot_round_up_from_minutes', 'payment_mode', 'net_salary', 'earned_amounts', 'overtime_breakdown')
        read_only_fields = ('ot_rounding_increment_minutes', 'ot_round_up_from_minutes')
    def get_earned_amounts(self, obj):
        # Get all related EarnedAmount records through the reverse relation
        earned_amounts = obj.current_salary_earned_amounts.all()
        return EarnedAmountWithEarningsHeadSerializer(earned_amounts, many=True).data

    def get_net_salary(self, obj):
        total_earned = obj.current_salary_earned_amounts.aggregate(total=Sum('earned_amount'))['total'] or 0
        total_deductions = sum(getattr(obj, field) or 0 for field in (
            'pf_deducted',
            'esi_deducted',
            'vpf_deducted',
            'advance_deducted',
            'tds_deducted',
            'labour_welfare_fund_deducted',
            'others_deducted',
        ))
        return total_earned + obj.net_ot_amount_monthly + obj.incentive_amount - total_deductions

class EarnedAmountWithEarningsHeadSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    earnings_head = EarningsHeadSerializer()
    class Meta:
        model = EarnedAmount
        fields = (
            'earnings_head',
            'salary_prepared',
            'rate',
            'earned_amount',
            'arear_amount',
        )


class EarnedAmountSerializer(serializers.ModelSerializer):
    # id = serializers.IntegerField(read_only=True)
    class Meta:
        model = EarnedAmount
        fields = (
            'earnings_head',
            'salary_prepared',
            'rate',
            'earned_amount',
            'arear_amount',
        )

class FiltersSalaryOvertimeSheet(serializers.Serializer):
    group_by = serializers.ChoiceField(choices=["none", "department"])
    resignation_filter = serializers.ChoiceField(choices=["all", "without_resigned", "only_resigned"])
    sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
    language = serializers.ChoiceField(choices=["hindi", "english"])
    format = serializers.ChoiceField(choices=["xlsx", "pdf"])
    overtime = serializers.ChoiceField(choices=["with_ot", "without_ot"])

class SalaryOvertimeSheetSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    filters = FiltersSalaryOvertimeSheet()
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    report_type = serializers.ChoiceField(choices=["salary_sheet", "payslip", "overtime_sheet", "payment_sheet", "payment_sheet_as_per_compliance" , "advance_report", "yearly_advance_report"])

    class Meta:
        fields = ['employee_ids', "filters"]
        
class FiltersPersonnelFileReports(serializers.Serializer):
    resignation_filter = serializers.ChoiceField(choices=["all", "without_resigned", "only_resigned"])
    sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
    language = serializers.ChoiceField(choices=["hindi", "english"])
    personnel_file_reports_selected = serializers.ListField(allow_empty=True)
    orientation = serializers.ChoiceField(choices =["portrait", "landscape"])

class PersonnelFileReportsSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    filters = FiltersPersonnelFileReports()
    company = serializers.IntegerField()
    # month = serializers.IntegerField()
    # year = serializers.IntegerField()
    report_type = serializers.ChoiceField(choices=["personnel_file_reports", "id_card"])

    class Meta:
        fields = ['employee_ids', "filters"]


class FiltersAttendanceReportsSerializer(serializers.Serializer):
    group_by = serializers.ChoiceField(choices=["none", "department"])
    month_from_date = serializers.IntegerField(allow_null=True)
    month_to_date = serializers.IntegerField(allow_null=True)
    resignation_filter = serializers.ChoiceField(choices=["all", "without_resigned", "only_resigned"])
    sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
    date = serializers.IntegerField(allow_null=True)

class AttendanceReportsSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    filters = FiltersAttendanceReportsSerializer()
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    report_type = serializers.ChoiceField(choices=["present_report", "absent_report", "attendance_register", "form_14", "overtime_sheet_daily", "bonus_calculation_sheet", "bonus_form_c", "miss_punch", "daily_attendance_report"])
    class Meta:
        fields = ['employee_ids', "filters"]

class FiltersPfEsiReportsSerializer(serializers.Serializer):
    sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
    format = serializers.ChoiceField(choices=["xlsx", "txt"])

class PfEsiReportsSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    filters = FiltersPfEsiReportsSerializer()
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    report_type = serializers.ChoiceField(choices=["pf_statement", "esi_statement", "pf_exempt"])
    class Meta:
        fields = ['employee_ids', "filters"]

class EmployeeAttendanceBulkAutofillSerializer(serializers.Serializer):
    month_from_date = serializers.IntegerField(min_value=1, max_value=31)
    month_to_date = serializers.IntegerField(min_value=1, max_value=31)
    company = serializers.IntegerField()
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=1)
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), required=False, default=list,
    )

    def validate(self, attrs):
        validate_attendance_period_not_before_cutoff(attrs)
        if attrs['month_from_date'] > attrs['month_to_date']:
            raise serializers.ValidationError({'month_to_date': 'End day must not precede start day.'})
        last_day = calendar.monthrange(attrs['year'], attrs['month'])[1]
        if attrs['month_from_date'] > last_day:
            raise serializers.ValidationError({'month_from_date': 'Start day is outside the requested month.'})
        return attrs

class BulkPrepareSalariesSerializer(serializers.Serializer):
    company = serializers.IntegerField()
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=1950, max_value=2100)
    employee_ids = serializers.ListField(
        child=serializers.IntegerField(min_value=1), required=False, allow_empty=True,
    )

    def validate_employee_ids(self, value):
        if not value:
            raise serializers.ValidationError('Select at least one employee or omit employee_ids.')
        if len(value) != len(set(value)):
            raise serializers.ValidationError('Employee IDs must be unique.')
        return value

class MachineAttendanceSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    # creator_id = serializers.ReadOnlyField(source='creator.id')
    mdb_database = serializers.FileField(required=True)
    employee = serializers.IntegerField(min_value=1)
    company = serializers.IntegerField()
    all_employees_machine_attendance = serializers.BooleanField()
    month_from_date = serializers.IntegerField(min_value=1, max_value=31)
    month_to_date = serializers.IntegerField(min_value=1, max_value=31)
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        validate_attendance_period_not_before_cutoff(attrs)
        if attrs['month_from_date'] > attrs['month_to_date']:
            raise serializers.ValidationError({'month_to_date': 'End day must not precede start day.'})
        last_day = calendar.monthrange(attrs['year'], attrs['month'])[1]
        if attrs['month_from_date'] > last_day:
            raise serializers.ValidationError({'month_from_date': 'Start day is outside the requested month.'})
        return attrs

class DefaultAttendanceSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    company = serializers.IntegerField()
    month = serializers.IntegerField(min_value=1, max_value=12)
    year = serializers.IntegerField(min_value=1)

    def validate(self, attrs):
        return validate_attendance_period_not_before_cutoff(attrs)

class EmployeeResignationSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfessionalDetail
        fields = ['employee', 'resignation_date', 'resigned']

class EmployeeUnresignSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeProfessionalDetail
        fields = ['employee', 'resigned', 'resignation_date']

class BonusCalculationSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusCalculation
        fields = ('company' ,'date', 'amount', 'category')

class BonusPercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BonusPercentage
        fields = ('company' , 'bonus_percentage')

# class EmployeeSalaryPreparedSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = EmployeeSalaryPrepared
#         fields = ['id', 'employee', 'company', 'date', 'incentive_amount', 'pf_deducted', 'esi_deducted',
#                   'vpf_deducted', 'advance_deducted', 'tds_deducted', 'labour_welfare_fund_deducted',
#                   'others_deducted', 'net_ot_minutes_monthly', 'net_ot_amount_monthly', 'payment_mode']
        
class EarnedAmountSerializerPreparedSalary(serializers.ModelSerializer):
    earnings_head = EarningsHeadSerializer()
    salary_prepared = EmployeeSalaryPreparedSerializer()
    class Meta:
        model = EarnedAmount
        fields = ['id', 'earnings_head', 'salary_prepared', 'rate', 'earned_amount', 'arear_amount']

class FullAndFinalSerializer(serializers.ModelSerializer):
    class Meta:
        model = FullAndFinal
        fields = ['employee', 'company', 'full_and_final_date', 'el_encashment_days', 'el_encashment_amount', 'bonus_prev_year', 'bonus_current_year', 'gratuity', 'service_compensation_days', 'service_compensation_amount', 'earnings_notice_period_days', 'earnings_notice_period_amount', 'ot_min', 'ot_amount', 'earnings_others', 'deductions_notice_period_days', 'deductions_notice_period_amount', 'deductions_others',]


class EmployeeELLeftSerializer(serializers.Serializer):
    el_left = serializers.DecimalField(max_digits=4, decimal_places=1)

class EmployeeYearlyBonusAmountSerializer(serializers.Serializer):
    bonus_amount = serializers.IntegerField()
    employee = serializers.IntegerField()

class FullAndFinalReportSerializer(serializers.Serializer):
    employee = serializers.IntegerField()
    company = serializers.IntegerField()
    class Meta:
        fields = ['employee', "company"]

class EmployeeVisibilitySerializer(serializers.Serializer):
    employees_id = serializers.ListField()
    company = serializers.IntegerField()
    class Meta:
        fields = ["employees_id", "company"]

class SubUserOvertimeSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUserOvertimeSettings
        fields = ['company', 'date', 'max_ot_hrs']

class SubUserMiscSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SubUserMiscSettings
        fields = ['company', 'enable_female_max_punch_out', 'max_female_punch_out']

class AttendanceMachineConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceMachineConfig
        fields = ['company', 'machine_ip']

class TransferAttendanceFromOwnerToRegularSerializer(serializers.Serializer):
    month = serializers.IntegerField(min_value=1, max_value=12)
    company = serializers.IntegerField()
    year = serializers.IntegerField(min_value=1)

class FiltersEmployeeStrengthReportsSerializer(serializers.Serializer):
    group_by = serializers.ChoiceField(choices=["none", "department"])
    resignation_filter = serializers.ChoiceField(choices=["with_resigned", "without_resigned"])
    sort_by = serializers.ChoiceField(choices=["paycode", "attendance_card_no", "employee_name"])
    salary_rate = serializers.ChoiceField(choices=["with_salary_rate", "without_salary_rate"])

class EmployeeStrengthReportsSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    filters = FiltersEmployeeStrengthReportsSerializer()
    company = serializers.IntegerField()
    from_date = serializers.DateField()
    to_date = serializers.DateField()
    report_type = serializers.ChoiceField(choices=["strength_report", "resign_report"])
    class Meta:
        fields = ['employee_ids', "filters"]

class EmployeeMonthlyMissPunchSerializer(serializers.Serializer):
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

class EmployeeYearlyAdvanceTakenDeductedSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())

# class CompanyEmployeeStatisticsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyEmployeeStatistics
#         fields = ('company', 'earliest_employee_date_of_joining')
