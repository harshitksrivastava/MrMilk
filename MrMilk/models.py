from enum import unique

from django.contrib.auth.models import PermissionsMixin
from django.db import models

# Create your models here.
from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
import datetime
from django.utils import timezone


# Create your models here.
class Order(models.Model):
    cod_choices = [('0', 'NO'), ('1', 'YES')]
    order_status_choices = [('PL', 'PLACED'), ('SH', 'SHIPPED'), ('DL', 'DELIVERED')]
    order_id = models.AutoField(primary_key=True, editable=False)
    customer_id = models.ForeignKey('Profile', on_delete=models.DO_NOTHING)
    order_status = models.CharField(max_length=2, choices=order_status_choices, default='PL')
    order_date = models.DateTimeField(default=timezone.now())
    delivery_date = models.DateField(default=timezone.now() + datetime.timedelta(1))
    order_address = models.CharField(max_length=500, blank=True)
    total = models.DecimalField(max_digits=5, decimal_places=2)
    transaction_id = models.CharField(max_length=50, null=True)
    cod = models.CharField(max_length=2, choices=cod_choices, default='0')

    def __str__(self):
        return str(self.order_id)


class OrderDetail(models.Model):
    order = models.ForeignKey('Order', related_name='orders', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])

    class Meta:
        unique_together = ['order_id', 'product_id']

    def __str__(self):
        return str(self.order_id)


class ProfileManager(BaseUserManager):

    def create_user(self, phone, name, email, password, address, is_staff=False, is_active=True, is_superuser=False):
        if not phone or not email or not name:
            raise ValueError('Mandatory fields can not be null')
        normal_email = self.normalize_email(email)
        user = self.model(phone=phone, name=name, email=normal_email, address=address)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, phone, name, email, password, address):
        user = self.create_user(phone=phone, name=name, email=email, password=password, address=address,
                                is_superuser=True,
                                is_staff=True)
        return user


class Profile(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^[0][1-9]\d{9}$|^[1-9]\d{9}$',
                                 message="if phone number start with zero then 11 digits, else it checks 10 digits.")
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=12)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    address = models.CharField(max_length=500, blank=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = ProfileManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=50, primary_key=True, unique=True)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=50, primary_key=True, unique=True)

    class Meta:
        verbose_name = 'Sub Category'
        verbose_name_plural = 'Sub Categories'

    def __str__(self):
        return self.sub_category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=50, primary_key=True, unique=True)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', to_field='category_name', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', related_name='products', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=5)
    quantity = models.IntegerField(validators=[MinValueValidator(0)])
    image = models.ImageField(upload_to='main_products/', blank=True, null=True)

    def __str__(self):
        return self.product_name


class Subscription(models.Model):
    OPTION_TYPE = (
        ("1", "Yes"),
        ("0", "No")
    )
    id = models.IntegerField(primary_key=True, auto_created=True)
    subscriber = models.ForeignKey('Profile', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    start_date = models.DateField(default=timezone.now)
    no_of_days_left = models.IntegerField(validators=[MinValueValidator(1)], default=0)
    sunday = models.CharField(max_length=100, choices=OPTION_TYPE)
    monday = models.CharField(max_length=100, choices=OPTION_TYPE)
    tuesday = models.CharField(max_length=100, choices=OPTION_TYPE)
    wednesday = models.CharField(max_length=100, choices=OPTION_TYPE)
    thursday = models.CharField(max_length=100, choices=OPTION_TYPE)
    friday = models.CharField(max_length=100, choices=OPTION_TYPE)
    saturday = models.CharField(max_length=100, choices=OPTION_TYPE)

    def __str__(self):
        return self.subscription_id
