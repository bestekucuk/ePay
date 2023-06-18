
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(email=username)
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        print(password)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30,null=True)
    last_name = models.CharField(max_length=30,null=True)
    para_birimi_secimi = models.CharField(max_length=10)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0,editable=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if self.pk is None:  # Yeni kullanıcı oluşturuluyorsa
            self.balance = 1000  # Yeni kullanıcının başlangıç bakiyesi 0 olarak ayarlanır
        super().save(*args, **kwargs)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name','para_birimi_secimi']
    def __str__(self) :
        return self.email
    
    objects = CustomUserManager()
