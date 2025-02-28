from dataclasses import field

from .models import Company, CompanyDetails, User, Deparment, Designation, SalaryGrade, Regular, Category, Bank, LeaveGrade, Shift, Holiday, EarningsHead, EmployeePersonalDetail, EmployeeProfessionalDetail, EmployeeSalaryEarning, EmployeeSalaryDetail, EmployeeFamilyNomineeDetial, EmployeePfEsiDetail, WeeklyOffHolidayOff, PfEsiSetup, Calculations, EmployeeShifts, EmployeeAttendance, EmployeeGenerativeLeaveRecord, EmployeeLeaveOpening, EmployeeMonthlyAttendanceDetails, EmployeeAdvancePayment, EmployeeSalaryPrepared, EarnedAmount, BonusCalculation, BonusPercentage, FullAndFinal, SubUserOvertimeSettings, SubUserMiscSettings, AttendanceMachineConfig, ExtraFeaturesConfig
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
    # user = UserSerializer(read_only=True)
    class Meta:
        model = CompanyDetails
        #fields = ('company', 'address', 'key_person', 'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no', 'registration_no', 'registration_date')
        fields = ('company', 'address', 'key_person' ,'involving_industry', 'phone_no', 'email', 'pf_no', 'esi_no', 'head_office_address', 'pan_no', 'gst_no')

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
    class Meta:
        model = EmployeeSalaryDetail
        fields = ['company', 'employee', 'overtime_type', 'overtime_rate', 'salary_mode', 'payment_mode', 'bank_name', 'account_number', 'ifcs', 'labour_wellfare_fund', 'late_deduction', 'bonus_allow', 'bonus_exg']


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

class EmployeeAttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAttendance
        fields = ['id', 'employee', 'company', 'machine_in', 'machine_out', 'manual_in', 'manual_out', 'first_half', 'second_half', 'date', 'ot_min', 'late_min', 'manual_mode']

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
        fields = ('id', 'employee', 'company', 'date', 'incentive_amount', 'pf_deducted', 'esi_deducted', 'vpf_deducted', 'advance_deducted', 'tds_deducted', 'labour_welfare_fund_deducted', 'others_deducted', 'net_ot_minutes_monthly', 'net_ot_amount_monthly', 'payment_mode')

class EmployeeSalaryPreparedWithEarnedAmountSerializer(serializers.ModelSerializer):
    earned_amounts = serializers.SerializerMethodField()
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = EmployeeSalaryPrepared
        fields = ('id', 'employee', 'company', 'date', 'incentive_amount', 'pf_deducted', 'esi_deducted', 'vpf_deducted', 'advance_deducted', 'tds_deducted', 'labour_welfare_fund_deducted', 'others_deducted', 'net_ot_minutes_monthly', 'net_ot_amount_monthly', 'payment_mode', 'earned_amounts')
    def get_earned_amounts(self, obj):
        # Get all related EarnedAmount records through the reverse relation
        earned_amounts = obj.current_salary_earned_amounts.all()
        return EarnedAmountWithEarningsHeadSerializer(earned_amounts, many=True).data

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
    report_type = serializers.ChoiceField(choices=["present_report", "absent_report", "attendance_register", "form_14", "overtime_sheet_daily", "bonus_calculation_sheet", "bonus_form_c", "miss_punch"])
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
    month_from_date = serializers.IntegerField()
    month_to_date = serializers.IntegerField()
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

class BulkPrepareSalariesSerializer(serializers.Serializer):
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

class MachineAttendanceSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    # creator_id = serializers.ReadOnlyField(source='creator.id')
    mdb_database = serializers.FileField(required=True)
    employee = serializers.IntegerField()
    company = serializers.IntegerField()
    all_employees_machine_attendance = serializers.BooleanField()
    month_from_date = serializers.IntegerField()
    month_to_date = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

class DefaultAttendanceSerializer(serializers.Serializer):
    user = UserSerializer(read_only=True)
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()

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

class ExtraFeaturesConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraFeaturesConfig
        fields = ['company', 'enable_calculate_ot_attendance_using_earned_salary']

class TransferAttendanceFromOwnerToRegularSerializer(serializers.Serializer):
    month = serializers.IntegerField()
    company = serializers.IntegerField()
    year = serializers.IntegerField()

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

class CalculateOtAttendanceUsingTotalEarnedSerializer(serializers.Serializer):
    employee_ids = serializers.ListField(child=serializers.IntegerField())
    company = serializers.IntegerField()
    month = serializers.IntegerField()
    year = serializers.IntegerField()
    manually_inserted_total_earned = serializers.IntegerField()
    mark_attendance = serializers.BooleanField()






# class CompanyEmployeeStatisticsSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CompanyEmployeeStatistics
#         fields = ('company', 'earliest_employee_date_of_joining')
