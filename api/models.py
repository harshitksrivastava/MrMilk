from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.core.validators import MinValueValidator, RegexValidator
from django.db import models
import datetime
from django.utils import timezone


# Create your models here.


class Order(models.Model):
    order_id = models.IntegerField(primary_key=True, auto_created=True)
    customer_id = models.ForeignKey('User', on_delete=models.DO_NOTHING)
    product_id = models.ForeignKey('Product', on_delete=models.DO_NOTHING)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    date = models.DateField(default=timezone.now)
    total = models.DecimalField(max_digits=5, decimal_places=2)


class UserManager(BaseUserManager):

    def create_user(self, phone, name, email, password, is_staff=False, is_active=True, is_superuser=False):
        if not phone or not email or not name:
            raise ValueError('Mandatory fields can not be null')
        normal_email = self.normalize_email(email)
        user = self.model(phone=phone, name=name, email=normal_email)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_superuser(self, phone, name, email, password):
        user = self.create_user(phone=phone, name=name, email=email, password=password, is_superuser=True,
                                is_staff=True)
        return user


class User(AbstractBaseUser):
    phone_regex = RegexValidator(regex=r'^[0][1-9]\d{9}$|^[1-9]\d{9}$',
                                 message="if phone number start with zero then 11 digits, else it checks 10 digits.")
    phone = models.CharField(validators=[phone_regex], unique=True, max_length=12)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['name', 'email']

    def __str__(self):
        return self.name


class Category(models.Model):
    category_name = models.CharField(max_length=50)
    image = models.ImageField(upload_to='category/', blank=True, null=True)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.category_name


class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=50)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.sub_category_name


class Brand(models.Model):
    brand_name = models.CharField(max_length=50)

    def __str__(self):
        return self.brand_name


class Product(models.Model):
    product_name = models.CharField(max_length=50)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    sub_category = models.ForeignKey('SubCategory', on_delete=models.CASCADE)
    brand = models.ForeignKey('Brand', on_delete=models.CASCADE)
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
    subscription = models.ForeignKey('User', on_delete=models.CASCADE)
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
