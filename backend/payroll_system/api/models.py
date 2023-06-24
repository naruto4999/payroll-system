from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, timedelta


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
    email = models.EmailField(max_length=254)
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
        return f"{self.user.email} -> {self.company.name}: {self.name}"

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