from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings
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
            raise TypeError('Use must have a phone number.')
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
    
class OwnerToRegular(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='regulars')
    owner = models.OneToOneField(User, on_delete=models.CASCADE, related_name='owners')


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="companies")
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, unique=True)
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
