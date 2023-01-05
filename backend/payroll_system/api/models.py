from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **kwargs):
        """Create and return a `User` with an email, phone number, username and password."""
        if username is None:
            raise TypeError('Users must have a username.')
        if email is None:
            raise TypeError("Users must have an email")
        user = self.model(username=username, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, username, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """
        if password is None:
            raise TypeError('Superusers must have a password.')
        if email is None:
            raise TypeError('Superusers must have an email.')
        if username is None:
            raise TypeError('Superusers must have an username.')

        user = self.create_user(username, email, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(db_index=True, max_length=255, unique=True)
    email = models.EmailField(db_index=True, unique=True,  null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()
    def __str__(self):
        return f"{self.email}"


class Company(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="company")
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256, null=False, unique=True)
    def __str__(self):
        return self.name


class CompanyDetails(models.Model):
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
    tin_no = models.CharField(max_length=11, blank=True)
    registration_no = models.CharField(max_length=50, blank=True)
    registration_date = models.DateField()
    

