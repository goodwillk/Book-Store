from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from .managers import CustomUserManager

class BaseModel(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        abstract = True


class Address(BaseModel):
    class TypeChoices(models.TextChoices):
        Work = 'Work address'
        Home = 'Home address'
    
    type = models.CharField(choices=TypeChoices.choices, max_length=150)
    house_no = models.CharField(max_length=150)
    street_no = models.CharField(max_length=150)
    locality = models.CharField(max_length=150)
    city = models.CharField(max_length=150)
    state = models.CharField(max_length=150)
    country = models.CharField(max_length=150)
    pincode = models.PositiveIntegerField(
        validators=[MinValueValidator(100000), MaxValueValidator(999999)]
    )
    
    class Meta:
        unique_together = ('house_no', 'pincode')


class CustomUser(AbstractUser, BaseModel):
    username = None
    email = models.EmailField('email address', unique=True)
    mobile_no = models.BigIntegerField(unique=True)
    address = models.ManyToManyField(Address)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'mobile_no', 'password']
    
    objects = CustomUserManager()           #This is required to override --> username is a required field
    
    def __str__(self):
        return self.email


