from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta
import pathlib
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from decimal import Decimal
from django.db.models import Q
from dateutil.relativedelta import relativedelta
import calendar




#imports for signals
from django.db.models.signals import post_save
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
    name = models.CharField(max_length=256, null=False, unique=True)
    visible = models.BooleanField(default=False)
    def __str__(self):
        return f"{self.user.email} -> {self.name}"


class CompanyDetails(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="all_companies_details")
    company = models.OneToOneField(Company, on_delete=models.CASCADE, related_name="company_details", primary_key=True)
    address = models.TextField()
    key_person = models.CharField(max_length=64, blank=True)
    involving_industry = models.CharField(max_length=64, blank=True)
    phone_no = models.PositiveBigIntegerField()
    email = models.EmailField(max_length=150)
    pf_no = models.CharField(max_length=30)
    esi_no = models.PositiveBigIntegerField()
    head_office_address = models.TextField()
    pan_no = models.CharField(max_length=10, unique=True)
    gst_no = models.CharField(max_length=15, blank=True)
    
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
    limit = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
    mandatory_leave = models.BooleanField(default=False, null=False, blank=False)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'company', 'name'], name='unique_leave_grade_name_per_user')
        ]
    def __str__(self):
        return f"{self.user.email} -> {self.company.name}: {self.name}"
    # def clean(self):
    #     # Check if the unique constraint is violated
    #     if LeaveGrade.objects.filter(user=self.user, company=self.company, name=self.name).exists():
    #         raise ValidationError("Leave grade with this name already exists for the user and company.")
    
class Shift(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="shifts")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="shifts")
    name = models.CharField(max_length=256, null=False, blank=False)
    beginning_time = models.TimeField(null=False, blank=False)
    end_time = models.TimeField(null=False, blank=False)
    lunch_time = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    tea_time = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    late_grace = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes
    ot_begin_after = models.PositiveSmallIntegerField(default=0, null=False, blank=False) # In minutes (minimum number of minutes that needs to fulfilled for Over Time to be applied)
    next_shift_dealy = models.PositiveSmallIntegerField(default=0, null=False, blank=False)
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
def employee_photo_handler(instance, filename):
    fpath = pathlib.Path(filename)
    new_image_name = f"{instance.user.username}/{instance.user.id}_{instance.company.id}_{instance.id}{fpath.suffix}"
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
    name = models.CharField(max_length=256, null=False, blank=False)
    paycode = models.PositiveSmallIntegerField(null=False, blank=False)
    attendance_card_no = models.PositiveSmallIntegerField(null=False, blank=False)
    photo = models.ImageField(upload_to=employee_photo_handler ,null=True, blank=True)
    father_or_husband_name = models.CharField(max_length=256, null=True, blank=True)
    mother_name = models.CharField(max_length=256, null=True, blank=True)
    wife_name = models.CharField(max_length=256, null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employee_professional_details")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="employee_professional_details")
    employee = models.OneToOneField(EmployeePersonalDetail, on_delete=models.CASCADE, related_name="employee_professional_detail", primary_key=True)
    date_of_joining = models.DateField(null=False, blank=False)
    date_of_confirm = models.DateField(null=False, blank=False)
    department = models.ForeignKey(Deparment, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    designation = models.ForeignKey(Designation, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    salary_grade = models.ForeignKey(SalaryGrade, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    shift = models.ForeignKey(Shift, on_delete=models.CASCADE, related_name="employee_professional_detail", null=True, blank=True)
    weekly_off = models.CharField(max_length=6, choices=WEEKDAY_CHOICES, null=False, blank=False, default='sun')    
    extra_off = models.CharField(max_length=10, choices=EXTRA_OFF_CHOICES, default='no_off', null=False, blank=False)


    def save(self, *args, **kwargs):
        if self.department and (self.department.company != self.company or self.department.user != self.user):
            raise ValidationError("Invalid department selected.")
        elif self.designation and (self.designation.company != self.company or self.designation.user != self.user):
            raise ValidationError("Invalid designation selected.")
        elif self.category and (self.category.company != self.company or self.category.user != self.user):
            raise ValidationError("Invalid category selected.")
        elif self.salary_grade and (self.salary_grade.company != self.company or self.salary_grade.user != self.user):
            raise ValidationError("Invalid salary grade selected.")
        elif self.shift and (self.shift.company != self.company or self.shift.user != self.user):
            raise ValidationError("Invalid shift selected.")
        super().save(*args, **kwargs)


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
    PAYMENT_MODE_CHOICES = (
        ('bank_transfer', 'Bank Transfer'),
        ('cheque', 'Cheque'),
        ('cash', 'Cash'),
        ('rtgs', 'RTGS'),
        ('neft', 'NEFT'),
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
    pf_percent_ignore_employee = models.BooleanField(null=False, blank=False, default=False)
    pf_percent_ignore_employee_value = models.DecimalField(max_digits=4, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
    pf_percent_ignore_employer = models.BooleanField(null=False, blank=False, default=False)
    pf_percent_ignore_employer_value = models.DecimalField(max_digits=4, decimal_places=2, validators=PERCENTAGE_VALIDATOR, null=True, blank=True)
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
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="pf_esi_setup_details")
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


class EmployeeShiftsManager(models.Manager):
    def process_employee_shifts(self, employee_shift_data, user):
        # Step 2: Delete overlapping shifts for the month
        from_date = employee_shift_data['from_date']
        to_date = employee_shift_data['to_date']
        shift = employee_shift_data["shift"]
        if is_valid_date(from_date) and is_valid_date(to_date):
            self.filter(from_date__gte=from_date, to_date__lte=to_date).delete()
        else:
            raise ValidationError("Invalid date format for from_date or to_date.")

        parent_shift_queryset = self.filter(from_date__lte=from_date, to_date__gte=to_date)
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
            front_object_interfering_queryset = self.filter(from_date__lt=from_date, to_date__gte=to_date)
            front_object_non_interfering_has_same_value = False
            if front_object_interfering_queryset.exists():
                    front_object_interfering_instance = front_object_interfering_queryset[0]
                    print(f'front object intering info => from date: {front_object_interfering_instance.from_date}, to date: {front_object_interfering_instance.to_date}')
                    print(f'front_object_interfering_instance value: {front_object_interfering_instance.shift} and incomming shift: {employee_shift_data.shift}')
                    if front_object_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_interfering_instance.to_date = to_date
                        front_object_interfering_instance.save()
                        front_object_interfering_has_same_value = True
                    else:
                        front_object_interfering_instance.to_date = from_date - relativedelta(days=1)
                        front_object_interfering_instance.save()
            else:
                front_object_non_interfering_queryset = self.filter(to_date=(from_date - relativedelta(days=1)))
                if front_object_non_interfering_queryset.exists():
                    front_object_non_interfering_instance = front_object_non_interfering_queryset[0]
                    if front_object_non_interfering_instance.shift == employee_shift_data['shift']:
                        front_object_non_interfering_instance.to_date = to_date
                        front_object_non_interfering_instance.save()
                        front_object_non_interfering_has_same_value
                else:
                    print("something is wrong")

            #Checking if existing shift is overlapping from the back
            end_object_interfering_has_same_value = False
            end_object_non_interfering_has_same_value = False
            end_object_interfering_queryset = self.filter(from_date__lte=to_date, to_date__gt=to_date)
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
                end_object_non_interfering_queryset = self.filter(from_date=(to_date + relativedelta(days=1)))
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










    
@receiver(post_save, sender=Company)
def create_default_leave_grades_for_company(sender, instance, created, **kwargs):
    print("reciever ran")
    print(sender)
    print(instance)
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        print("reciever ran")
        # Create the first row for the new user
        LeaveGrade.objects.create(user=user,company=company, name='CL', limit=7, mandatory_leave=True)
        
        # Create the second row for the new user
        LeaveGrade.objects.create(user=user,company=company, name='EL', limit=15, mandatory_leave=True)
        
        # Create the third row for the new user
        LeaveGrade.objects.create(user=user,company=company, name='SL', limit=7, mandatory_leave=True)

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

@receiver(post_save, sender=Company)
def create_default_deductions_for_company(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        # Create the default deduction on post save for company
        DeductionsHead.objects.create(user=user,company=company, name='PF', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='ESI', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='VPF', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='Loan', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='Advance', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='TDS', mandatory_deduction=True)
        DeductionsHead.objects.create(user=user,company=company, name='Others', mandatory_deduction=True)

@receiver(post_save, sender=Company)
def create_default_earning_for_company(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        # Create the default earning on post save for company
        EarningsHead.objects.create(user=user,company=company, name='Basic', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='HRA', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Conveyance', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Other', mandatory_earning=True)
        EarningsHead.objects.create(user=user,company=company, name='Medical', mandatory_earning=True)

@receiver(post_save, sender=Company)
def create_default_holiday_off_weekly_off(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        # Create the default Weekly Off and Holiday Off on post save for company
        WeeklyOffHolidayOff.objects.create(user=user,company=company, min_days_for_holiday_off=0, min_days_for_weekly_off=0)

@receiver(post_save, sender=Company)
def create_default_pf_esi_setup(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        PfEsiSetup.objects.create( user=user, company=company, ac_1_epf_employee_percentage=12, ac_1_epf_employee_limit=15000, ac_1_epf_employer_percentage=3.67, ac_1_epf_employer_limit=15000, ac_10_eps_employer_percentage=8.33, ac_10_eps_employer_limit=15000, ac_2_employer_percentage=0.5, ac_21_employer_percentage=0.5, ac_22_employer_percentage=0, esi_employee_percentage=0.75, esi_employee_limit=21000, esi_employer_percentage=3.25, esi_employer_limit=21000, employer_pf_code=None, employer_esi_code=None,)
        
@receiver(post_save, sender=Company)
def create_default_calculations(sender, instance, created, **kwargs):
    if created:
        company = instance  # Assign the instance to a variable
        user = company.user
        Calculations.objects.create( user=user, company=company, ot_calculation='26', el_calculation='26', notice_pay='26', service_calculation='26', gratuity_calculation='26', el_days_calculation=20,)