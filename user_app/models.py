from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_save

# Create your models here.
class AccountManager(BaseUserManager):
    def create_user(self,email,username,phone,password,fullname=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            fullname = fullname,
            phone = phone,
            username = username
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,email,username,phone,password,fullname=None):
        user = self.create_user(
            email = self.normalize_email(email),
            username = username,
            phone=phone,
            password=password,
            fullname=fullname
        )

        user.is_staff = True
        user.is_admin = True
        user.is_super_admin = True

        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    fullname = models.CharField(max_length=30,null=True,blank=True)
    username = models.CharField(max_length=30,unique=True)
    phone = models.CharField(max_length=15,blank=True,null=True)
    email = models.EmailField(max_length=100,blank=True,null=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_super_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = ['phone', 'email']

    objects = AccountManager()

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin
    
    def has_module_perms(self, add_label):
        return True

class Profile(models.Model):
    user=models.OneToOneField(Account,on_delete=models.CASCADE,related_name='profile')
    date_of_birth=models.DateField(blank=True,null=True)
    bio=models.TextField(max_length=500)
    photo=models.ImageField(upload_to='profile_photos/',blank=True)
    
    def __unicode__(self):
        return f'Profile for user {self.user.username}'
