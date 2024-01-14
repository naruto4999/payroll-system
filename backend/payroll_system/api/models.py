from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta, date
import pathlib
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import calendar
import math
from django.db.models import Sum
from django.core.files.storage import FileSystemStorage
from .managers import EmployeeAttendanceManager, ActiveEmployeeManager, EmployeeSalaryPreparedManager






#imports for signals
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

# from django.db.models.signals import post_save
# from django.dispatch import receiver


# Create your models here.
# class UserManager(BaseUserManager):
#     def create_user(self, username, email, phone_no, password=None, **kwargs):
#         """Create and return a `User` with an email, phone number, username and password."""
#         if username is None:
#             raise TypeError('Users must have a username.')
#         if email is None:
#             raise TypeError("Users must have an email")
#         if phone_no is None:
#             raise TypeError('Use must have a phone number.')
#         user = self.model(username=username, email=self.normalize_email(email), phone_no=phone_no)
#         user.set_password(password)
#         user.save(using=self._db)
#         return user
        
#     def create_superuser(self, username, phone_no, email, password):
#         """
#         Create and return a `User` with superuser (admin) permissions.
#         """
#         if password is None:
#             raise TypeError('Superusers must have a password.')
#         if email is None:
#             raise TypeError('Superusers must have an email.')
#         if username is None:
#             raise TypeError('Superusers must have an username.')
#         if phone_no is None:
#             raise TypeError('Superusers must have a phone number.')

#         user = self.create_user(username=username, email=email, password=password, phone_no=phone_no)
#         user.is_superuser = True
#         user.is_staff = True
#         user.save(using=self._db)
PERCENTAGE_VALIDATOR = [MinValueValidator(0), MaxValueValidator(100)]

PAYMENT_MODE_CHOICES = (
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
        ('rtgs', 'RTGS'),
        ('neft', 'NEFT'),
    )

def is_valid_date(date):
    date_str = date.strftime('%Y-%m-%d')
    print(type(date_str))
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        # Check if the day is valid for the month and year
        _, max_day = calendar.monthrange(date.year, date.month)
        return 1 <= date.day <= max_day
    except ValueError:
        return False
    # try:
    #     datetime.strptime(date_str, '%Y-%m-%d')
    #     return True
    # except ValueError:
    #     return False

class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, phone_no=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError("Users must have an email")
        if phone_no is None:
            raise TypeError('Users must have a phone number.')
        user = self.model(username=username, email=self.normalize_email(email), phone_no=phone_no)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, email, password, phone_no):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')
        if phone_no is None:
            raise TypeError('Superusers must have a phone number.')
        print(password)
        user = self.create_user(username, email, password, phone_no)
        # print(user.is_superuser)
        user.is_superuser = True
        user.is_staff = True
        # print(user.is_superuser)
        user.save(using=self._db)
        # return user



class User(AbstractBaseUser, PermissionsMixin):
    class Role(models.TextChoices):
        OWNER = "OWNER", 'Owner'
        REGULAR = "REGULAR", 'Regular'

    base_role = Role.OWNER
    role = models.CharField(max_length=50,choices=Role.choices, default=base_role)
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'phone_no']
    phone_no = models.PositiveBigIntegerField(null=False, unique=True)
    # is_superuser = models.BooleanField(default=False)


    objects = UserManager()
    def __str__(self):
        return f"{self.email}"
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)
        else:
            return super().save(*args, **kwargs)
        
class Regular(User):
    base_role = User.Role.REGULAR
    class Meta:
        proxy=True
    def welcome(self):
        return "Only for Regular"
    

class OTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def is_valid(self):
        return self.expires_at > timezone.now()


class OwnerToRegular(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owners')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='regulars')


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False)
    visible = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.email} -> {self.name}"
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'name'], name='unique_company_for_a_user'),
        ]


class CompanyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_companies_details")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="company_details", primary_key=True)
    address = models.TextField(null=True, blank=True)
    key_person = models.CharField(max_length=64, blank=True, null=True)
    involving_industry = models.CharField(max_length=64, blank=True, null=True)
    phone_no = models.PositiveBigIntegerField(null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    pf_no = models.CharField(max_length=30, null=True, blank=True)
    esi_no = models.PositiveBigIntegerField(null=True, blank=True)
    head_office_address = models.TextField(null=True, blank=True)
    pan_no = models.CharField(max_length=10, unique=True, null=True, blank=True)
    gst_no = models.CharField(max_length=15, blank=True, null=True)
    
class Deparment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="departments")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="deparments")
    name = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"

class Designation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="designations")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="designations")
    name = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return self.name

class SalaryGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="salary_grades")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="salary_grades")
    name = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"

class Category(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    
class Bank(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="banks")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="banks")
    name = models.CharField(max_length=256, null=False, blank=False)
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    
class LeaveGrade(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="leave_grades")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="leave_grades")
    name = models.CharField(max_length=256, null=False, blank=False)
    limit = models.PositiveSmallIntegerField(null=True, blank=True)
    mandatory_leave = models.BooleanField(default=False, null=False, blank=False)
    paid = models.BooleanField(null=False, blank=False)
    generate_frequency = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_leave_grade_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    
    def clean(self):
        if not self.paid:
            if self.limit is not None:
                raise ValidationError("If 'paid' is False, 'limit' must be null.")
            if self.generate_frequency is not None:
                raise ValidationError("If 'paid' is False, 'generate_frequency' must be null.")
            
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)
    
class Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="shifts")
    name = models.CharField(max_length=256, null=False, blank=False)
    beginning_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    lunch_duration = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    lunch_beginning_time = models.TimeField(null=True, blank=True)
    tea_time = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    late_grace = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    ot_begin_after = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes (minimum number of minutes that needs to fulfilled for Over Time to be applied)
    next_shift_delay = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    max_late_allowed_min = models.PositiveSmallIntegerField(null=False, blank=False)
    accidental_punch_buffer = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    half_day_minimum_minutes = models.PositiveSmallIntegerField(null=False, blank=False)
    full_day_minimum_minutes = models.PositiveSmallIntegerField(null=False, blank=False)
    short_leaves = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # Number of Short Leaves allowed per month
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_shift_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    

class Holiday(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="holidays")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="holidays")
    name = models.CharField(max_length=256, null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    mandatory_holiday = models.BooleanField(default=False, null=False, blank=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_hodiday_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    
class EarningsHead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="earnings_heads")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="earnings_heads")
    name = models.CharField(max_length=256, null=False, blank=False)
    mandatory_earning = models.BooleanField(default=False, null=False, blank=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_earnings_head_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    
class DeductionsHead(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="deductions_head")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="deductions_head")
    name = models.CharField(max_length=256, null=False, blank=False)
    mandatory_deduction = models.BooleanField(default=False, null=False, blank=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_deductions_head_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    

# Employee related models
class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        # If a file with the same name exists, replace it
        if self.exists(name):
            self.delete(name)
        return name
    
def employee_photo_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_image_name = f"{instance.user.username}/{instance.user.id}_{instance.company.id}_{instance.paycode}{fpath.suffix}"
    return new_image_name

#Employee personal details
class EmployeePersonalDetail(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Others'),
    )
    MARITAL_STATUS_CHOICES = (
        ('S', 'Single'),
        ('M', 'Married'),
        ('D', 'Divorced'),
        ('W', 'Widowed'),
    )
    BLOOD_GROUP_CHOICES = (
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    )
    EDUCATION_CHOICES = [
        ('0', 'No Qualification'),
        ('1', '1st class'),
        ('2', '2nd class'),
        ('3', '3rd class'),
        ('4', '4th class'),
        ('5', '5th class'),
        ('6', '6th class'),
        ('7', '7th class'),
        ('8', '8th class'),
        ('9', '9th class'),
        ('10', '10th class'),
        ('11', '11th class'),
        ('12', '12th class'),
        ('G', 'Graduate'),
        ('PG', ' Post Graduate')
    ]
    STATE_AND_UT_CHOICES = [
        #States
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UK', 'Uttarakhand'),
        ('WB', 'West Bengal'),

        #Union
        ('JK', 'Jammu and Kashmir'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli'),
        ('DD', 'Daman and Diu'),
        ('DL', 'Delhi'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_personal_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee_personal_details")
    name = models.CharField(max_length=100, null=False, blank=False)
    paycode = models.CharField(max_length=32, null=False, blank=False)
    attendance_card_no = models.PositiveSmallIntegerField(null=False, blank=False)
    photo = models.ImageField(upload_to=employee_photo_handler ,null=True, blank=True, storage=OverwriteStorage())
    father_or_husband_name = models.CharField(max_length=100, null=True, blank=True)
    mother_name = models.CharField(max_length=100, null=True, blank=True)
    wife_name = models.CharField(max_length=100, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    alternate_phone_number = models.CharField(max_length=10, null=True, blank=True)
    email = models.EmailField(max_length=150, null=True, blank=True)
    pan_number = models.CharField(max_length=10, null=True, blank=True)
    driving_licence = models.CharField(max_length=20, null=True, blank=True) #cross check the number of digits
    passport = models.CharField(max_length=8, null=True, blank=True)
    aadhaar = models.CharField(max_length=12, null=True, blank=True)
    handicapped = models.BooleanField(null=False, blank=False, default=False)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, null=True, blank=True)
    marital_status = models.CharField(max_length=1, choices=MARITAL_STATUS_CHOICES, null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES, null=True, blank=True)
    religion = models.CharField(max_length=50, null=True, blank=True)
    nationality = models.CharField(max_length=50, null=False, blank=False, default='Indian')
    education_qualification = models.CharField(max_length=2, choices=EDUCATION_CHOICES, null=True, blank=True)
    technical_qualification = models.CharField(max_length=50, null=True, blank=True)
    local_address = models.CharField(max_length=256, null=True, blank=True)
    local_district = models.CharField(max_length=30, null=True, blank=True)
    local_state_or_union_territory = models.CharField(max_length=2, choices=STATE_AND_UT_CHOICES, null=True, blank=True)
    local_pincode = models.CharField(max_length=6, null=True, blank=True)
    permanent_address = models.CharField(max_length=256, null=True, blank=True)
    permanent_district = models.CharField(max_length=30, null=True, blank=True)
    permanent_state_or_union_territory = models.CharField(max_length=2, choices=STATE_AND_UT_CHOICES, null=True, blank=True)
    permanent_pincode = models.CharField(max_length=6, null=True, blank=True)
    isActive = models.BooleanField(default=True, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'paycode'], name='unique_paycode_per_employee_within_each_company_and_user'),
            models.UniqueConstraint(fields=['user', 'company', 'attendance_card_no'], name='unique_attendance_card_no_per_employee_within_each_company_and_user')
        ]
    def _str_(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    

class EmployeeProfessionalDetail(models.Model):
    WEEKDAY_CHOICES = [
        ('no_off', 'No Off'),
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    ]

    EXTRA_OFF_CHOICES = [
        ('no_off', 'No Off'),
        ('mon1', 'First Monday'),
        ('mon2', 'Second Monday'),
        ('mon3', 'Third Monday'),
        ('mon4', 'Fourth Monday'),
        ('tue1', 'First Tuesday'),
        ('tue2', 'Second Tuesday'),
        ('tue3', 'Third Tuesday'),
        ('tue4', 'Fourth Tuesday'),
        ('wed1', 'First Wednesday'),
        ('wed2', 'Second Wednesday'),
        ('wed3', 'Third Wednesday'),
        ('wed4', 'Fourth Wednesday'),
        ('thu1', 'First Thursday'),
        ('thu2', 'Second Thursday'),
        ('thu3', 'Third Thursday'),
        ('thu4', 'Fourth Thursday'),
        ('fri1', 'First Friday'),
        ('fri2', 'Second Friday'),
        ('fri3', 'Third Friday'),
        ('fri4', 'Fourth Friday'),
        ('sat1', 'First Saturday'),
        ('sat2', 'Second Saturday'),
        ('sat3', 'Third Saturday'),
        ('sat4', 'Fourth Saturday'),
        ('sun1', 'First Sunday'),
        ('sun2', 'Second Sunday'),
        ('sun3', 'Third Sunday'),
        ('sun4', 'Fourth Sunday'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_companys_employee_professional_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employee_professional_details")
    employee = models.OneToOneField(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="employee_professional_detail", primary_key=True)
    date_of_joining = models.DateField(null=False, blank=False)
    date_of_confirm = models.DateField(null=False, blank=False)
    department = models.ForeignKey(Deparment, on_delete=models.CASCADE, related_name="same_department_employees", null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="same_designation_employees", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="same_category_employees", null=True, blank=True)
    salary_grade = models.ForeignKey(SalaryGrade, on_delete=models.CASCADE, related_name="same_salary_grade_employees", null=True, blank=True)
    # shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    weekly_off = models.CharField(max_length=6, choices=WEEKDAY_CHOICES, null=False, blank=False, default='sun')    
    extra_off = models.CharField(max_length=10, choices=EXTRA_OFF_CHOICES, default='no_off', null=False, blank=False)
    resigned = models.BooleanField(default=False, null=False, blank=False)
    resignation_date = models.DateField(null=True, blank=True, default=None)
    ##Previous Experience
    #Row 1
    first_previous_experience_company_name = models.CharField(max_length=64, null=True, blank=True)
    first_previous_experience_from_date = models.DateField(null=True, blank=True)
    first_previous_experience_to_date = models.DateField(null=True, blank=True)
    first_previous_experience_designation = models.CharField(max_length=64, null=True, blank=True)
    first_previous_experience_reason_for_leaving = models.CharField(max_length=64, null=True, blank=True)
    first_previous_experience_salary = models.IntegerField(null=True, blank=True)
    #Row 2
    second_previous_experience_company_name = models.CharField(max_length=64, null=True, blank=True)
    second_previous_experience_from_date = models.DateField(null=True, blank=True)
    second_previous_experience_to_date = models.DateField(null=True, blank=True)
    second_previous_experience_designation = models.CharField(max_length=64, null=True, blank=True)
    second_previous_experience_reason_for_leaving = models.CharField(max_length=64, null=True, blank=True)
    second_previous_experience_salary = models.IntegerField(null=True, blank=True)
    #Row 3
    third_previous_experience_company_name = models.CharField(max_length=64, null=True, blank=True)
    third_previous_experience_from_date = models.DateField(null=True, blank=True)
    third_previous_experience_to_date = models.DateField(null=True, blank=True)
    third_previous_experience_designation = models.CharField(max_length=64, null=True, blank=True)
    third_previous_experience_reason_for_leaving = models.CharField(max_length=64, null=True, blank=True)
    third_previous_experience_salary = models.IntegerField(null=True, blank=True)
    ##References
    #Row 1
    first_reference_name = models.CharField(max_length=64, null=True, blank=True)
    first_reference_address = models.CharField(max_length=128, null=True, blank=True)
    first_reference_relation = models.CharField(max_length=64, null=True, blank=True)
    first_reference_phone = models.CharField(max_length=10, null=True, blank=True)
    #Row 2
    second_reference_name = models.CharField(max_length=64, null=True, blank=True)
    second_reference_address = models.CharField(max_length=128, null=True, blank=True)
    second_reference_relation = models.CharField(max_length=64, null=True, blank=True)
    second_reference_phone = models.CharField(max_length=10, null=True, blank=True)
    #Custom Manager
    objects = ActiveEmployeeManager()



    def save(self, *args, **kwargs):
        if self.department and (self.department.company != self.company or self.department.user != self.user):
            raise ValidationError("Invalid department selected.")
        elif self.designation and (self.designation.company != self.company or self.designation.user != self.user):
            raise ValidationError("Invalid designation selected.")
        elif self.category and (self.category.company != self.company or self.category.user != self.user):
            raise ValidationError("Invalid category selected.")
        elif self.salary_grade and (self.salary_grade.company != self.company or self.salary_grade.user != self.user):
            raise ValidationError("Invalid salary grade selected.")
        elif not self.resigned and self.resignation_date is not None:
            raise ValidationError("Non-resigned employees must not have a resignation date.")
        elif self.resigned and self.resignation_date is None:
            raise ValidationError("Resigned employees must have a resignation date.")
        # elif self.shift and (self.shift.company != self.company or self.shift.user != self.user):
        #     raise ValidationError("Invalid shift selected.")
        super().save(*args, **kwargs)


# class CompanyEmployeeStatistics(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_employees_statistics")
#     company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="employee_statistics")
#     earliest_employee_date_of_joining = models.DateField(null=True, blank=True)

#     def update_earliest_employee_date(self):
#         earliest_employee = EmployeeProfessionalDetail.objects.filter(company=self.company).order_by('date_of_joining').first()
#         if earliest_employee:
#             self.earliest_employee_date_of_joining = earliest_employee.date_of_joining
#             self.save()
#         else:
#             self.earliest_employee_date_of_joining = None
#             self.save()


class EmployeeSalaryEarning(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_employees_earnings")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="earnings")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_company_employees_earnings")
    earnings_head = models.ForeignKey(EarningsHead, on_delete=models.CASCADE, related_name="employees_earnings")
    value = models.IntegerField(default=0, null=False, blank=False)
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'earnings_head', 'from_date'], name='unique_employee_earnings_head_with_from_date'),

            #Covers the fact that a particuar earning head for an employee can have to_date set to "9999-01-01" for only one record
            models.UniqueConstraint( fields=['earnings_head', 'employee', 'to_date'], name='unique_employee_earnings_head_with_to_date')
        ]

    def clean(self):
        if isinstance(self.from_date, str):
            # Parse the string into a datetime object
            print('in istance')
            self.from_date = datetime.strptime(self.from_date, "%Y-%m-%d").date()
        if isinstance(self.to_date, str):
            # Parse the string into a datetime object
            self.to_date = datetime.strptime(self.to_date, "%Y-%m-%d").date()
        if isinstance(self.from_date, datetime):
            self.from_date = self.from_date.date()
        if isinstance(self.to_date, datetime):
            self.to_date = self.to_date.date()
        # Now both from_date and to_date are datetime objects
        print(f'from_date type : {type(self.from_date)} value: {self.from_date} and to_date type: {type(self.to_date)} and value {self.to_date}')

        # Now both from_date and to_date are datetime objects

        if self.from_date.day != 1:
            self.from_date = self.from_date.replace(day=1)

        if self.to_date.day != 1:
            self.to_date = self.to_date.replace(day=1)

        if self.from_date > self.to_date:
            raise ValidationError("'from_date' must be before 'to_date'")

        if self.from_date.year < 1950 or self.from_date.year > 2100:
            raise ValidationError("Invalid From Date value")
        
    def save(self, *args, **kwargs):
        self.clean()
        if self.earnings_head.company != self.company or self.earnings_head.user != self.user:
            raise ValidationError("Invalid Earning Head selected.")
        super().save(*args, **kwargs)
    

class EmployeeSalaryDetail(models.Model):
    OVERTIME_TYPE_CHOICES = (
        ('no_overtime', 'No Overtime'),
        ('all_days', 'All Days'),
        ('holiday_weekly_off', 'Holiday/Weekly Off'),
    )

    OVERTIME_RATE_CHOICES = (
        ('S', 'Single'),
        ('D', 'Double'),
    )

    SALARY_MODE_CHOICES = (
        ('monthly', 'Monthly'),
        ('daily', 'Daily'),
        ('piece_rate', 'Piece Rate'),
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_salary_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee_salary_details")
    employee = models.OneToOneField(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="employee_salary_detail", primary_key=True)
    overtime_type = models.CharField(max_length=20, choices=OVERTIME_TYPE_CHOICES, default='no_overtime', null=False, blank=False)
    overtime_rate = models.CharField(max_length=1, choices=OVERTIME_RATE_CHOICES, null=True, blank=True)
    salary_mode = models.CharField(max_length=20, choices=SALARY_MODE_CHOICES, default='monthly', null=False, blank=False)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, default='bank_transfer', null=False, blank=False)
    bank_name = models.CharField(max_length=75, null=True, blank=True)
    account_number = models.CharField(max_length=50, null=True, blank=True)
    ifcs = models.CharField(max_length=25, null=True, blank=True)
    labour_wellfare_fund = models.BooleanField(default=False, null=False, blank=False)
    late_deduction = models.BooleanField(default=False, null=False, blank=False)
    bonus_allow = models.BooleanField(default=False, null=False, blank=False)
    bonus_exg = models.BooleanField(default=False, null=False, blank=False)

    def get_payment_mode_display(self):
        return dict(PAYMENT_MODE_CHOICES).get(self.payment_mode, self.payment_mode)

    def clean(self):
        if self.overtime_type in ['holiday_weekly_off', 'all_days'] and not self.overtime_rate:
            raise ValidationError({
                'overtime_rate': "Overtime rate cannot be null or blank for 'Holiday/Weekly Off' or 'All Days' overtime type."
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

class EmployeePfEsiDetail(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_pf_esi_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee_pf_esi_details")
    employee = models.OneToOneField(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="employee_pf_esi_detail", primary_key=True)
    pf_allow = models.BooleanField(null=False, blank=False, default=False)
    pf_number = models.CharField(max_length=50, null=True, blank=True)
    pf_limit_ignore_employee = models.BooleanField(null=False, blank=False, default=False)
    pf_limit_ignore_employee_value = models.PositiveIntegerField(null=True, blank=True)
    pf_limit_ignore_employer = models.BooleanField(null=False, blank=False, default=False)
    pf_limit_ignore_employer_value = models.PositiveIntegerField(null=True, blank=True)
    # pf_percent_ignore_employee = models.BooleanField(null=False, blank=False, default=False)
    # pf_percent_ignore_employee_value = models.DecimalField(max_digits=4, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    # pf_percent_ignore_employer = models.BooleanField(null=False, blank=False, default=False)
    # pf_percent_ignore_employer_value = models.DecimalField(max_digits=4, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    vpf_amount = models.PositiveIntegerField(null=False, blank=False, default=0)
    tds_amount = models.PositiveIntegerField(null=False, blank=False, default=0)
    uan_number = models.CharField(max_length=30, null=True, blank=True)
    esi_allow = models.BooleanField(null=False, blank=False, default=False)
    esi_number = models.CharField(max_length=30, null=True, blank=True)
    esi_dispensary = models.CharField(max_length=100, null=True, blank=True)
    esi_on_ot = models.BooleanField(null=False, blank=False, default=False)

    def check_family_nominee_rules(self):
        family_nominees = EmployeeFamilyNomineeDetial.objects.filter(employee=self.employee)

        for nominee in family_nominees:
            if not self.pf_allow:
                nominee.pf_benefits = False
                nominee.is_pf_nominee = False
                nominee.pf_nominee_share = None
            if not self.esi_allow:
                nominee.esi_benefit = False
                nominee.is_esi_nominee = False
                nominee.esi_nominee_share = None

            if not nominee.pf_benefits:
                nominee.is_pf_nominee = False
                nominee.pf_nominee_share = None
            if not nominee.esi_benefit:
                nominee.is_esi_nominee = False
                nominee.esi_nominee_share = None
            if not nominee.is_fa_nominee:
                nominee.fa_nominee_share = None
            if not nominee.is_gratuity_nominee:
                nominee.gratuity_nominee_share = None

            nominee.save()
    
    def save(self, *args, **kwargs):
        if self.pk:  # Check if it's an update, not a new instance
            super().save(*args, **kwargs)
            self.check_family_nominee_rules()
        else:
            super().save(*args, **kwargs)


class EmployeeFamilyNomineeDetial(models.Model):

    RELATION_CHOICES = [
    ('Father', 'Father'),
    ('Mother', 'Mother'),
    ('Wife', 'Wife'),
    ('Son', 'Son'),
    ('Brother', 'Brother'),
    ('Sister', 'Sister'),
    ('Daughter', 'Daughter'),
    ('Husband', 'Husband'),
]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_family_nominee_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee_family_nominee_details")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="employee_family_nominee_detail")
    name = models.CharField(max_length=256, null=False, blank=False)
    address = models.CharField(max_length=256, null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    relation = models.CharField(max_length=10, choices=RELATION_CHOICES, null=False, blank=False)
    residing = models.BooleanField(null=False, blank=False, default=True)
    esi_benefit = models.BooleanField(null=False, blank=False, default=True)
    pf_benefits = models.BooleanField(null=False, blank=False, default=True)
    is_esi_nominee = models.BooleanField(null=False, blank=False, default=False)
    esi_nominee_share = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    is_pf_nominee = models.BooleanField(null=False, blank=False, default=False)
    pf_nominee_share = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    is_fa_nominee = models.BooleanField(null=False, blank=False, default=False)
    fa_nominee_share = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    is_gratuity_nominee = models.BooleanField(null=False, blank=False, default=False)
    gratuity_nominee_share = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)

    def calculate_age(self):
        if self.dob:
            today = date.today()
            birth_date = self.dob
            age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            return age
        else:
            return None

    def save(self, *args, **kwargs):
        if not hasattr(self.employee, 'employee_pf_esi_detail'):
            raise ValidationError("Employee has no PF and ESI detail")
        else:
            pf_esi_detail = self.employee.employee_pf_esi_detail
            if not pf_esi_detail.pf_allow:
                self.pf_benefits = False
                self.is_pf_nominee = False
                self.pf_nominee_share = None
            if not pf_esi_detail.esi_allow:
                self.esi_benefit = False
                self.is_esi_nominee = False
                self.esi_nominee_share = None
        if not self.esi_benefit:
            self.is_esi_nominee = False
        if not self.pf_benefits:
            self.is_pf_nominee = False
        if not self.is_esi_nominee:
            self.esi_nominee_share = None
        if not self.is_pf_nominee:
            self.pf_nominee_share = None
        if not self.is_fa_nominee:
            self.fa_nominee_share = None
        if not self.is_gratuity_nominee:
            self.gratuity_nominee_share = None
        
            # self.save(update_fields=['pf_benefits', 'is_pf_nominee'])
        super().save(*args, **kwargs)

class WeeklyOffHolidayOff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="weekly_off_holiday_off_entries")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="weekly_off_holiday_off_entry", primary_key=True)
    min_days_for_weekly_off = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    min_days_for_holiday_off = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    def __str__(self):
        return f"{self.user.username} ({self.company.name}) - Weekly Off: {self.min_days_for_weekly_off} days, Holiday Off: {self.min_days_for_holiday_off} days"
    
class PfEsiSetup(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_companies_pf_esi_setup_details")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="pf_esi_setup_details", primary_key=True)
    ac_1_epf_employee_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=12)
    ac_1_epf_employee_limit = models.PositiveIntegerField(null=False, blank=False, default=15000)
    ac_1_epf_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=3.67)
    ac_1_epf_employer_limit = models.PositiveIntegerField(null=False, blank=False, default=15000)
    ac_10_eps_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=8.33)
    ac_10_eps_employer_limit = models.PositiveIntegerField(null=False, blank=False, default=15000)
    ac_2_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=0.5)
    ac_21_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=0.5)
    ac_22_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=0)
    employer_pf_code = models.CharField(max_length=100, null=True, blank=True)
    esi_employee_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=0.75)
    esi_employee_limit = models.PositiveIntegerField(null=False, blank=False, default=21000)
    esi_employer_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=3.25)
    esi_employer_limit = models.PositiveIntegerField(null=False, blank=False, default=21000)
    employer_esi_code = models.CharField(max_length=100, null=True, blank=True)
    enable_labour_welfare_fund = models.BooleanField(null=False, blank=False, default=False)
    labour_wellfare_fund_employer_code = models.CharField(max_length=100, null=True, blank=True)
    labour_welfare_fund_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=0.2)
    labour_welfare_fund_limit = models.PositiveIntegerField(null=False, blank=False, default=31)

class Calculations(models.Model):
    OT_CALCULATION_CHOICES = [
        ('26', '26'),
        ('30', '30'),
        ('month_days', 'month_days'),
    ]
    CALCULATION_CHOICES = [
        ('26', '26'),
        ('30', '30')
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="calculations")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="calculations", primary_key=True)
    ot_calculation = models.CharField(max_length=10, choices=OT_CALCULATION_CHOICES, default='26', null=False, blank=False)
    el_calculation =  models.CharField(max_length=2, choices=CALCULATION_CHOICES, default='26', null=False, blank=False)
    notice_pay =  models.CharField(max_length=2, choices=CALCULATION_CHOICES, default='30', null=False, blank=False)
    service_calculation =  models.CharField(max_length=2, choices=CALCULATION_CHOICES, default='30', null=False, blank=False)
    gratuity_calculation =  models.CharField(max_length=2, choices=CALCULATION_CHOICES, default='26', null=False, blank=False)
    el_days_calculation = models.PositiveSmallIntegerField(default=20, null=False, blank=False)
    bonus_start_month = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(12)])


class EmployeeShiftsManager(models.Manager):
    def process_employee_shifts(self, employee_shift_data, user):
        # Step 2: Delete overlapping shifts for the month
        from_date = employee_shift_data['from_date']
        to_date = employee_shift_data['to_date']
        shift = employee_shift_data["shift"]
        if is_valid_date(from_date) and is_valid_date(to_date):
            self.filter(from_date__gte=from_date, to_date__lte=to_date, employee=employee_shift_data['employee']).delete()
        else:
            raise ValidationError("Invalid date format for from_date or to_date.")

        parent_shift_queryset = self.filter(from_date__lte=from_date, to_date__gte=to_date, employee=employee_shift_data['employee'])
        if parent_shift_queryset.exists():
            parent_shift_instance = parent_shift_queryset[0]
            print(f'this is parent info from date: {parent_shift_instance.from_date}, to date: {parent_shift_instance.to_date}')
            if parent_shift_instance.shift != shift:
                if parent_shift_instance.from_date == from_date:
                        print(f'Parent shift instance from date is same {parent_shift_instance}')
                        parent_shift_instance.from_date = to_date + relativedelta(days=1)
                        parent_shift_instance.save()
                        print(f'After Saving {parent_shift_instance}')

                elif parent_shift_instance.to_date == to_date:
                    parent_shift_instance.to_date = from_date - relativedelta(days=1)
                    parent_shift_instance.save()
                
                else:
                    #Divide Parent into two
                    parent_original_shift = parent_shift_instance.shift
                    parent_original_from_date = parent_shift_instance.from_date
                    parent_original_to_date = parent_shift_instance.to_date
                    
                    #Creating First Half
                    parent_shift_instance.to_date = from_date - relativedelta(days=1)
                    parent_shift_instance.save()
                    print(f'Saved 1st half of parent info is => from date: {parent_shift_instance.from_date}, to date: {parent_shift_instance.to_date}')

                    #Creating Second Half
                    self.create(user=user, employee=employee_shift_data['employee'], company=employee_shift_data['company'], from_date=employee_shift_data['to_date'] + relativedelta(days=1), to_date=parent_original_to_date, shift=parent_original_shift)
                
                #Creating Employee Shift
                employee_shift_data['user'] = user
                self.create(**employee_shift_data)
        else:
            #Checking if existing shift is overlapping from the front
            front_object_interfering_has_same_value = False
            front_object_interfering_queryset = self.filter(from_date__lt=from_date, to_date__gte=from_date, employee=employee_shift_data['employee'])
            front_object_non_interfering_has_same_value = False
            if front_object_interfering_queryset.exists():
                    front_object_interfering_instance = front_object_interfering_queryset[0]
                    print(f'front object intering info => from date: {front_object_interfering_instance.from_date}, to date: {front_object_interfering_instance.to_date}')
                    print(f'front_object_interfering_instance value: {front_object_interfering_instance.shift} and incomming shift: {employee_shift_data["shift"]}')
                    if front_object_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_interfering_instance.to_date = to_date
                        front_object_interfering_instance.save()
                        front_object_interfering_has_same_value = True
                    else:
                        front_object_interfering_instance.to_date = from_date - relativedelta(days=1)
                        front_object_interfering_instance.save()
            else:
                front_object_non_interfering_queryset = self.filter(to_date=(from_date - relativedelta(days=1)), employee=employee_shift_data['employee'])
                if front_object_non_interfering_queryset.exists():
                    front_object_non_interfering_instance = front_object_non_interfering_queryset[0]
                    if front_object_non_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_non_interfering_instance.to_date = to_date
                        front_object_non_interfering_instance.save()
                        front_object_non_interfering_has_same_value = True
                else:
                    print("something is wrong")

            #Checking if existing shift is overlapping from the back
            end_object_interfering_has_same_value = False
            end_object_non_interfering_has_same_value = False
            end_object_interfering_queryset = self.filter(from_date__lte=to_date, to_date__gt=to_date, employee=employee_shift_data['employee'])
            if end_object_interfering_queryset.exists():
                    end_object_interfering_instance = end_object_interfering_queryset[0]
                    print(f'end object interfering info => from date: {end_object_interfering_instance.from_date}, to date: {end_object_interfering_instance.to_date}')
                    print(f'end_object_interfering_instance shift: {end_object_interfering_instance.shift} and incomming shift: {employee_shift_data["shift"]}')
                    if end_object_interfering_instance.shift == employee_shift_data['shift']:
                        if front_object_interfering_has_same_value:
                            front_object_interfering_instance.to_date = end_object_interfering_instance.to_date
                            end_object_interfering_queryset.delete()
                            front_object_interfering_instance.save()
                        elif front_object_non_interfering_has_same_value:
                            front_object_non_interfering_instance.to_date = end_object_interfering_instance.to_date
                            end_object_interfering_queryset.delete()
                            front_object_non_interfering_instance.save()
                        else:
                            end_object_interfering_instance.from_date = employee_shift_data['from_date']
                            end_object_interfering_instance.save()
                        end_object_interfering_has_same_value = True
                            
                    else:
                        end_object_interfering_instance.from_date = to_date + relativedelta(days=1)
                        end_object_interfering_instance.save()
            else:
                end_object_non_interfering_queryset = self.filter(from_date=(to_date + relativedelta(days=1)), employee=employee_shift_data['employee'])
                if end_object_non_interfering_queryset.exists():
                    end_object_non_interfering_instance = end_object_non_interfering_queryset[0]
                    if end_object_non_interfering_instance.shift == employee_shift_data['shift']:
                        if front_object_interfering_has_same_value:
                            front_object_interfering_instance.to_date = end_object_non_interfering_instance.to_date
                            end_object_non_interfering_queryset.delete()
                            front_object_interfering_instance.save()
                        elif front_object_non_interfering_has_same_value:
                            front_object_non_interfering_instance.to_date = end_object_non_interfering_instance.to_date
                            end_object_non_interfering_queryset.delete()
                            front_object_non_interfering_instance.save()
                        else:
                            end_object_non_interfering_instance.from_date = employee_shift_data['from_date']
                            end_object_non_interfering_instance.save()
                        end_object_non_interfering_has_same_value = True
            if not front_object_interfering_has_same_value and not front_object_non_interfering_has_same_value and not end_object_interfering_has_same_value and not end_object_non_interfering_has_same_value:
                employee_shift_data['user'] = user
                self.create(**employee_shift_data)
                
    def process_employee_permanent_shift(self, employee_shift_data, user):
        from_date = employee_shift_data['from_date']
        to_date = employee_shift_data['to_date']
        shift = employee_shift_data["shift"]
        if is_valid_date(from_date) and is_valid_date(to_date):
            self.filter(from_date__gte=from_date, to_date__lte=to_date, employee=employee_shift_data['employee']).delete()
        else:
            raise ValidationError("Invalid date format for from_date or to_date.")
    
        parent_shift_queryset = self.filter(from_date__lte=from_date, to_date__gte=to_date, employee=employee_shift_data['employee'])
        if parent_shift_queryset.exists():
            parent_shift_instance = parent_shift_queryset[0]
            print(f'this is parent info from date: {parent_shift_instance.from_date}, to date: {parent_shift_instance.to_date}')
            if parent_shift_instance.shift != shift:

                if parent_shift_instance.to_date == to_date:
                    parent_shift_instance.to_date = from_date - relativedelta(days=1)
                    parent_shift_instance.save()
                
                else:
                   print('something is wrong a lorger parent on both sides exist')
                #Creating Employee Shift
                employee_shift_data['user'] = user
                self.create(**employee_shift_data)
        else:
            front_object_interfering_has_same_value = False
            front_object_interfering_queryset = self.filter(from_date__lt=from_date, to_date__gte=from_date, employee=employee_shift_data['employee'])
            front_object_non_interfering_has_same_value = False
            if front_object_interfering_queryset.exists():
                    front_object_interfering_instance = front_object_interfering_queryset[0]
                    if front_object_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_interfering_instance.to_date = to_date
                        front_object_interfering_instance.save()
                        front_object_interfering_has_same_value = True
                    else:
                        front_object_interfering_instance.to_date = from_date - relativedelta(days=1)
                        front_object_interfering_instance.save()
            else:
                front_object_non_interfering_queryset = self.filter(to_date=(from_date - relativedelta(days=1)), employee=employee_shift_data['employee'])
                if front_object_non_interfering_queryset.exists():
                    front_object_non_interfering_instance = front_object_non_interfering_queryset[0]
                    if front_object_non_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_non_interfering_instance.to_date = to_date
                        front_object_non_interfering_instance.save()
                        front_object_non_interfering_has_same_value = True
                else:
                    print("something is wrong")
            if not front_object_interfering_has_same_value and not front_object_non_interfering_has_same_value:
                employee_shift_data['user'] = user
                self.create(**employee_shift_data)

        
class EmployeeShifts(models.Model):
    objects = EmployeeShiftsManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_employees_shifts")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="shifts")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_company_employees_shifts")
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="employees_shifts")
    from_date = models.DateField(null=False, blank=False)
    to_date = models.DateField(null=False, blank=False)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'shift', 'from_date'], name='unique_employee_shift_from_date'),

            #Covers the fact that a particuar earning head for an employee can have to_date set to "9999-01-01" for only one record
            models.UniqueConstraint( fields=['shift', 'employee', 'to_date'], name='unique_employee_shift_to_date')
        ]

    def clean(self):
        if isinstance(self.from_date, str):
            # Parse the string into a datetime object
            print('in istance')
            self.from_date = datetime.strptime(self.from_date, "%Y-%m-%d").date()
        if isinstance(self.to_date, str):
            # Parse the string into a datetime object
            self.to_date = datetime.strptime(self.to_date, "%Y-%m-%d").date()
        if isinstance(self.from_date, datetime):
            self.from_date = self.from_date.date()
        if isinstance(self.to_date, datetime):
            self.to_date = self.to_date.date()
        # Now both from_date and to_date are datetime objects
        print(f'from_date type : {type(self.from_date)} value: {self.from_date} and to_date type: {type(self.to_date)} and value {self.to_date}')
        if self.from_date > self.to_date:
            raise ValidationError("'from_date' must be before 'to_date'")
        # if self.from_date.year < 1950 or self.from_date.year > 2100:
        #     raise ValidationError("Invalid From Date value")
        
    def save(self, *args, **kwargs):
        self.clean()
        if self.shift.company != self.company or self.shift.user != self.user:
            raise ValidationError("Invalid Shift selected.")
        super().save(*args, **kwargs)


def validate_pay_multiplier_allowed_values(value):
    allowed_values = [Decimal('1'), Decimal('0.5'), Decimal('0')]
    if value not in allowed_values:
        raise ValidationError(f"{value} is not a valid choice for this field.")

class LimitedFloatField(models.DecimalField):
    def __init__(self, *args, **kwargs):
        kwargs['max_digits'] = 3  # Adjust as needed
        kwargs['decimal_places'] = 1  # One decimal place
        kwargs['validators'] = [validate_pay_multiplier_allowed_values]
        kwargs['editable'] = False
        super().__init__(*args, **kwargs)

class EmployeeAttendance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_employees_attendance")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="attendance")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_company_employees_attendance")
    machine_in = models.TimeField(null=True, blank=True)
    machine_out = models.TimeField(null=True, blank=True)
    manual_in = models.TimeField(null=True, blank=True)
    manual_out = models.TimeField(null=True, blank=True)
    first_half = models.ForeignKey(LeaveGrade, on_delete=models.CASCADE, null=False, blank=False, related_name="employees_first_half_attendances_with_same_leave")
    second_half = models.ForeignKey(LeaveGrade, on_delete=models.CASCADE, null=False, blank=False, related_name="employees_second_half_attendances_with_same_leave")
    date = models.DateField(null=False, blank=False)
    ot_min = models.PositiveSmallIntegerField(null=True, blank=True)
    late_min = models.PositiveSmallIntegerField(null=True, blank=True)
    pay_multiplier = LimitedFloatField()
    manual_mode = models.BooleanField(default=False)
    objects = EmployeeAttendanceManager()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Set default value for 'first_half' based on the specified conditions
        if not self.first_half:
            try:
                self.first_half = LeaveGrade.objects.get(user=self.user, company=self.company, name='A')
            except LeaveGrade.DoesNotExist:
                pass
        if not self.second_half:
            try:
                self.second_half = LeaveGrade.objects.get(user=self.user, company=self.company, name='A')
            except LeaveGrade.DoesNotExist:
                pass

    class Meta:
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['date']),
            models.Index(fields=['company_id']),
            models.Index(fields=['user']),

        ]
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date'], name='unique_employee_attendance_date_wise'),
        ]

    def save(self, *args, **kwargs):
        if self.first_half.paid and self.second_half.paid:
            self.pay_multiplier = 1
        elif self.first_half.paid or self.second_half.paid:
            self.pay_multiplier = 0.5
        else:
            self.pay_multiplier = 0
        super().save(*args, **kwargs)
    

class EmployeeGenerativeLeaveRecordManager(models.Manager):
    def generate_update_monthly_record(self, user, year, month, employee_id, company_id):
        leave_grades_queryset = LeaveGrade.objects.filter(user=user, company_id=company_id, paid=True, generate_frequency__isnull=False)
        leave_grade_dict = {leave_grade.id: {'leave_count': 0, 'name': leave_grade.name} for leave_grade in leave_grades_queryset}
        employee_professional_detail = EmployeeProfessionalDetail.objects.get(user=user, employee_id=employee_id, company_id=company_id)

        if year > employee_professional_detail.date_of_joining.year or (month > employee_professional_detail.date_of_joining.month and year == employee_professional_detail.date_of_joining.year):
            from_date = datetime(year, month, 1).date()
            last_day = calendar.monthrange(year, month)[1]
            to_date = datetime(year, month, last_day).date()
        elif month == employee_professional_detail.date_of_joining.month and year == employee_professional_detail.date_of_joining.year:
            day = employee_professional_detail.date_of_joining.day
            from_date = datetime(year, month, day).date()
            # to_date = datetime(year, month, day + total_expected_instances - 1).date()
            last_day = calendar.monthrange(year, month)[1]
            to_date = datetime(year, month, last_day).date()

        present_count = 0
        weekly_off_days_count = 0
        holiday_days_count = 0
        paid_days_count = 0
        not_paid_days_count = 0
        total_ot_minutes_monthly = 0
        total_late_min = 0
        compensation_off_days_count = 0

        employee_attendance_queryset = EmployeeAttendance.objects.filter(user=user, employee_id=employee_id, company_id=company_id, date__gte=from_date, date__lte=to_date)

        for employee_attendance in employee_attendance_queryset:
            # Present Count
            present_count += 1 if employee_attendance.first_half.name == "P" else 0
            present_count += 1 if employee_attendance.second_half.name == "P" else 0

            #Weekly Off Count
            weekly_off_days_count += 1 if employee_attendance.first_half.name == "WO" else 0
            weekly_off_days_count += 1 if employee_attendance.second_half.name == "WO" else 0

            #Holiday Off Count
            holiday_days_count += 1 if employee_attendance.first_half.name == "HD" else 0
            holiday_days_count += 1 if employee_attendance.second_half.name == "HD" else 0

            #Compensation Off Count
            compensation_off_days_count += 1 if employee_attendance.first_half.name == "CO" else 0
            compensation_off_days_count += 1 if employee_attendance.second_half.name == "CO" else 0

            #Paid Days Count
            paid_days_count += 1 if employee_attendance.first_half.paid == True else 0
            paid_days_count += 1 if employee_attendance.second_half.paid == True else 0

            #Not Paid Days Count
            not_paid_days_count += 1 if employee_attendance.first_half.paid == False else 0
            not_paid_days_count += 1 if employee_attendance.second_half.paid == False else 0

            total_ot_minutes_monthly += employee_attendance.ot_min if employee_attendance.ot_min != None else 0
            total_late_min += employee_attendance.late_min if employee_attendance.late_min != None else 0
            # print(f"Total OT: {total_ot_minutes_monthly} Total Late: {total_late_min}")

            for leave_id in (employee_attendance.first_half.id, employee_attendance.second_half.id):
                if leave_id in leave_grade_dict:
                    leave_grade_dict[leave_id]['leave_count'] += 1

        net_ot_minutes_monthly = max(total_ot_minutes_monthly - ((total_late_min // 30) * 30 + (30 if total_late_min % 30 >= 20 else 0)), 0)


        # For updating existing instance
        defaults = {
        "present_count": present_count,
        "weekly_off_days_count": weekly_off_days_count,
        "holiday_days_count": holiday_days_count,
        "paid_days_count": paid_days_count,
        "not_paid_days_count": not_paid_days_count,
        "net_ot_minutes_monthly": net_ot_minutes_monthly,
        "compensation_off_days_count": compensation_off_days_count,
        }

        #For creating new instance
        create_defaults = {
        "user": user, 
        "company_id": company_id, 
        "employee_id": employee_id, 
        "date": from_date.replace(day=1),
        "present_count": present_count,
        "weekly_off_days_count": weekly_off_days_count,
        "holiday_days_count": holiday_days_count,
        "paid_days_count": paid_days_count,
        "not_paid_days_count": not_paid_days_count,
        "net_ot_minutes_monthly": net_ot_minutes_monthly,
        "compensation_off_days_count": compensation_off_days_count,
        }
        # present_count_record = EmployeeMonthlyAttendanceDetails.objects.filter(user=user, employee_id=employee_id, company_id=company_id, date=from_date.replace(day=1)).first()

        EmployeeMonthlyAttendanceDetails.objects.update_or_create(user=user, company_id=company_id, employee_id=employee_id, date=from_date.replace(day=1), defaults=defaults, create_defaults=create_defaults)

        for key, value in leave_grade_dict.items():
            defaults_generative_leave = {
                "leave_count": value['leave_count']
            }
            create_defaults_generative_leave = {
                "user": user,
                "employee_id": employee_id,
                "company_id": company_id,
                "leave_id": key,
                "date": from_date.replace(day=1),
                "leave_count": value['leave_count']
            }
            self.update_or_create(user=user, employee_id=employee_id, company_id=company_id, leave_id=key, date=from_date.replace(day=1), defaults=defaults_generative_leave, create_defaults=create_defaults_generative_leave)


class EmployeeGenerativeLeaveRecord(models.Model):
    objects = EmployeeGenerativeLeaveRecordManager()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_generative_leave_record")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="generative_leave_record")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employees_generative_leave_record")
    leave = models.ForeignKey(LeaveGrade, on_delete=models.CASCADE, related_name="current_generative_leave_record")
    date = models.DateField(null=False, blank=False) #day of date is always 1
    leave_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)


    class Meta:
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['date']),
            models.Index(fields=['company_id']),
        ]
        constraints = [
            models.UniqueConstraint(fields=['employee', 'date', 'company', 'leave'], name='unique_date_per_employee_per_company'),
        ]

class EmployeeMonthlyAttendanceDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_monthly_attendance_details")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="monthly_attendance_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employees_monthly_attendance_details")
    present_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    date = models.DateField(null=False, blank=False) #day of date is always 1
    # working_days = models.PositiveSmallIntegerField(null=False, blank=False, default=0) Same as present count
    weekly_off_days_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    paid_days_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    holiday_days_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    not_paid_days_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    net_ot_minutes_monthly = models.PositiveIntegerField(null=False, blank=False, default=0)
    compensation_off_days_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)

    class Meta:
        indexes = [
            models.Index(fields=['employee']),
            models.Index(fields=['date']),
            models.Index(fields=['company_id']),
        ]


class EmployeeLeaveOpening(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_leave_openings")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="leave_opening")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employees_leave_openings")
    leave = models.ForeignKey(LeaveGrade, on_delete=models.CASCADE, related_name="all_leave_openings")
    leave_count = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    year = models.PositiveSmallIntegerField(null=False, blank=False, validators=[
            MinValueValidator(1900, message="Year cannot be less than 1900."),
            MaxValueValidator(2100, message="Year cannot be more than 2100."),
        ])

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['employee', 'year', 'company'], name='unique_year_per_employee_per_company'),
        ]


class EmployeeAdvancePayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_advance_payments")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="advance_payments")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employees_advance_payments")
    principal = models.PositiveIntegerField(null=False, blank=False)
    emi = models.PositiveIntegerField(null=False, blank=False)
    date = models.DateField(null=False, blank=False)
    closed = models.BooleanField(null=False, blank=False, default=False)
    closed_date = models.DateField(null=True, blank=True)
    tenure_months_left = models.PositiveSmallIntegerField(null=False, blank=False)
    @property
    def repaid_amount(self):
        # Filter the related objects
        emi_repayments = EmployeeAdvanceEmiRepayment.objects.filter(employee_advance_payment=self.id)

        # Check if there are no related objects and set total_amount to 0 in that case
        if emi_repayments.exists():
            total_amount = emi_repayments.aggregate(total_amount=Sum('amount')).get('total_amount', 0)
        else:
            total_amount = 0

        return total_amount


    # repaid_amount = models.PositiveIntegerField(null=False, blank=False, default=0)

    # class Meta:
    #     constraints = [
    #         models.UniqueConstraint(fields=['employee', 'year', 'company'], name='unique_advance_payment_per_employee_per_company'),
    #     ]




class EmployeeSalaryPrepared(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_salaries_prepared")
    employee = models.ForeignKey(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="salaries_prepared")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="all_employees_salaries_prepared")
    date = models.DateField(null=False, blank=False) #date should always be 1
    incentive_amount = models.PositiveIntegerField(null=False, blank=False, default=0)
    pf_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    esi_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    vpf_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    advance_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    tds_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    labour_welfare_fund_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    others_deducted = models.PositiveIntegerField(null=False, blank=False, default=0)
    net_ot_minutes_monthly = models.PositiveSmallIntegerField(null=False, blank=False, default=0)
    net_ot_amount_monthly = models.PositiveIntegerField(null=False, blank=False, default=0)
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, null=False, blank=False, default='bank_transfer')
    objects = EmployeeSalaryPreparedManager()

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['date', 'employee'], name='unique_salary_for_each_month'),
        ]


class EmployeeAdvanceEmiRepayment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_advance_emi_repayments")
    amount = models.PositiveIntegerField(null=False, blank=False)
    employee_advance_payment = models.ForeignKey(EmployeeAdvancePayment, on_delete=models.CASCADE, related_name="all_emis_of_advance")
    salary_prepared = models.ForeignKey(EmployeeSalaryPrepared, on_delete=models.CASCADE, related_name="emis_with_salary_prepared")


class EarnedAmount(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_employees_earned_amounts")
    earnings_head = models.ForeignKey(EarningsHead, on_delete=models.CASCADE, related_name="earning_head_earned_amount")
    salary_prepared = models.ForeignKey(EmployeeSalaryPrepared, on_delete=models.CASCADE, related_name="current_salary_earned_amounts")
    rate = models.PositiveIntegerField(null=False, blank=False, default=0)
    earned_amount = models.PositiveIntegerField(null=False, blank=False, default=0) #inclusive of arrear
    arear_amount = models.PositiveIntegerField(null=False, blank=False, default=0)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['earnings_head', 'salary_prepared'], name='unique_earned_amount_for_each_earnings_head'),
        ]

class BonusCalculation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_bonus_calculation")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="bonus_calculation")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="same_category_bonus_calculation", null=False, blank=False)
    date = models.DateField(null=False, blank=False) #day of date is always 1
    amount = models.IntegerField(default=0, null=False, blank=False)


    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['company', 'date', 'category'], name='unique_bonus_calculation_for_each_month'),
        ]

class BonusPercentage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_company_bonus_percentage")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="bonus_percentage")
    bonus_percentage = models.DecimalField(max_digits=5, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=False, blank=False, default=8.33)


    
@receiver(post_save, sender=Company)
def create_default_leave_grades_for_company(sender, instance, created, **kwargs):
    print("reciever ran")
    print(sender)
    print(instance)
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        print("reciever ran")
        LeaveGrade.objects.create(user=user,company=company, name='CL', limit=7, mandatory_leave=True, paid=True, generate_frequency=40)        
        LeaveGrade.objects.create(user=user,company=company, name='EL', limit=15, mandatory_leave=True, paid=True, generate_frequency=20)
        LeaveGrade.objects.create(user=user,company=company, name='SL', limit=7, mandatory_leave=True, paid=True, generate_frequency=40)
        LeaveGrade.objects.create(user=user,company=company, name='A', mandatory_leave=True, paid=False)
        LeaveGrade.objects.create(user=user,company=company, name='P', mandatory_leave=True, paid=True)
        LeaveGrade.objects.create(user=user,company=company, name='HD*', mandatory_leave=True, paid=False)
        LeaveGrade.objects.create(user=user,company=company, name='HD', mandatory_leave=True, paid=True)
        LeaveGrade.objects.create(user=user,company=company, name='MS', mandatory_leave=True, paid=False)
        LeaveGrade.objects.create(user=user,company=company, name='WO', mandatory_leave=True, paid=True)
        LeaveGrade.objects.create(user=user,company=company, name='WO*', mandatory_leave=True, paid=False)
        LeaveGrade.objects.create(user=user,company=company, name='OD', mandatory_leave=True, paid=True)
        LeaveGrade.objects.create(user=user,company=company, name='CO', mandatory_leave=True, paid=True)
        #Salary Sheet attendances WD, WO, HD, A (Non generative mandatory ones)
        #Attendance EL, CL, SL, CO


@receiver(post_save, sender=Company)
def create_default_holidays_for_company(sender, instance, created, **kwargs):
    print("reciever ran")
    print(sender)
    print(instance)
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        print("reciever ran")
        current_year = datetime.now().year
        gandhi_jayanti = datetime(current_year, 10, 2)
        republic_day = datetime(current_year, 1, 26)
        independence_day = datetime(current_year, 8, 15)
        # Create the first row for the new user
        Holiday.objects.create(user=user,company=company, name='Gandhi Jayanti', date=gandhi_jayanti, mandatory_holiday=True)
        
        # Create the second row for the new user
        Holiday.objects.create(user=user,company=company, name='Republic Day', date=republic_day, mandatory_holiday=True)
        
        # Create the third row for the new user
        Holiday.objects.create(user=user,company=company, name='Independence Day', date=independence_day, mandatory_holiday=True)

# @receiver(post_save, sender=Company)
# def create_default_deductions_for_company(sender, instance, created, **kwargs):
#     if created:
#         company = instance  # Assign the instance to a variable
#         user = company.user
#         # Create the default deduction on post save for company
#         DeductionsHead.objects.create(user=user,company=company, name='PF', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='ESI', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='VPF', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='Loan', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='Advance', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='TDS', mandatory_deduction=True)
#         DeductionsHead.objects.create(user=user,company=company, name='Others', mandatory_deduction=True)

@receiver(post_save, sender=Company)
def create_default_earning_for_company(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        # Create the default earning on post save for company
        EarningsHead.objects.create(user=user,company=company, name='Basic', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='HRA', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Conveyance', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Medical', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Other', mandatory_earning=True)

@receiver(post_save, sender=Company)
def create_default_holiday_off_weekly_off(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        # Create the default Weekly Off and Holiday Off on post save for company
        WeeklyOffHolidayOff.objects.create(user=user,company=company, min_days_for_holiday_off=3, min_days_for_weekly_off=3)

@receiver(post_save, sender=Company)
def create_default_pf_esi_setup(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        PfEsiSetup.objects.create( user=user, company=company, ac_1_epf_employee_percentage=12, ac_1_epf_employee_limit=15000, ac_1_epf_employer_percentage=3.67, ac_1_epf_employer_limit=15000, ac_10_eps_employer_percentage=8.33, ac_10_eps_employer_limit=15000, ac_2_employer_percentage=0.5, ac_21_employer_percentage=0.5, ac_22_employer_percentage=0, esi_employee_percentage=0.75, esi_employee_limit=21000, esi_employer_percentage=3.25, esi_employer_limit=21000, employer_pf_code=None, employer_esi_code=None, enable_labour_welfare_fund=False, labour_welfare_fund_percentage=0.2, labour_welfare_fund_limit=31)
        
@receiver(post_save, sender=Company)
def create_default_calculations(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        Calculations.objects.create( user=user, company=company, ot_calculation='26', el_calculation='26', notice_pay='26', service_calculation='26', gratuity_calculation='26', el_days_calculation=20, bonus_start_month=1)

@receiver(post_save, sender=EmployeeAttendance)
def create_generative_leave_record(sender, instance, created, **kwargs):
    if created:
        employee_attendance = instance  # Assign the instance to a variable
        user = employee_attendance.user
        print(employee_attendance)
        # Calculations.objects.create( user=user, company=company, ot_calculation='26', el_calculation='26', notice_pay='26', service_calculation='26', gratuity_calculation='26', el_days_calculation=20,)

# @receiver(post_save, sender=EmployeeProfessionalDetail)
# @receiver(post_delete, sender=EmployeeProfessionalDetail)

# def update_earliest_employee_date(sender, instance, **kwargs):
#     if instance.company:
#         user = instance.user
#         if user.role != "OWNER":
#             user = OwnerToRegular.objects.get(user=user).owner
#         company_stats, created = CompanyEmployeeStatistics.objects.get_or_create(company=instance.company, user=user)
#     else:
#         return
#     company_stats.update_earliest_employee_date()

# @receiver(post_save, sender=EmployeeSalaryPrepared)
# def calculate_repaid_amount(sender, instance, created, **kwargs):
#     """
#     This function is called when an EmployeeSalaryPrepared instance is saved.
#     """
#     if created:
#         print(f"Created: {instance}")
#         print(f"Advance Paid: {instance.advance_deducted}")
#     else:
#         #employee_advances = contains all the advances that employee took
#         employee_advances = EmployeeAdvancePayment.objects.filter(user=instance.user, employee=instance.employee, company=instance.company)
#         if employee_advances.exists():
#                 advance_to_be_paid = 0
#                 for advance in employee_advances:
#                     if advance.emi <= (advance.principal-advance.repaid_amount):
#                         advance_to_be_paid += advance.emi
#                     elif (advance.principal-advance.repaid_amount) > 0:
#                         advance_to_be_paid += (advance.principal-advance.repaid_amount)

#                 print(f"Advance to be paid: {advance_to_be_paid}")

                # if advance_to_be_paid != instance.advance_deducted:
                # discrepancy_advance_amount = Decimal(instance.advance_deducted-advance_to_be_paid)
                # advance_to_be_paid = Decimal(advance_to_be_paid)
                # discrepency_advance_percentage = (discrepancy_advance_amount*Decimal(100))/advance_to_be_paid
                # advance_deducted_left = instance.advance_deducted
                # for advance in employee_advances:
                #     if advance.emi <= (advance.principal-advance.repaid_amount):
                #         add_to_repaid = int(math.ceil((discrepency_advance_percentage/Decimal(100)*Decimal(advance.emi)) + Decimal(advance.emi)))
                #     else:
                #         add_to_repaid = int(math.ceil((discrepency_advance_percentage/Decimal(100)*Decimal(advance.principal-advance.repaid_amount)) + Decimal(advance.principal-advance.repaid_amount)))

                        
                #     if add_to_repaid <= advance_deducted_left:
                #         advance.repaid_amount += add_to_repaid
                #         advance_deducted_left -= add_to_repaid
                #         advance.save()
                #     elif advance_deducted_left > 0:
                #         advance.repaid_amount += advance_deducted_left
                #         advance_deducted_left -= advance_deducted_left
                #         advance.save()

                # elif advance_to_be_paid==instance.advance_deducted:
                #     advance_deducted_left = instance.advance_deducted
                #     for advance in employee_advances:
                #         if advance.emi <= (advance.principal-advance.repaid_amount):


        # print(f"First instance: {employee_advances[0].emi}")
        # print(f"Updated: {instance}")
        # print(f"Advance Paid: {instance.advance_deducted}")