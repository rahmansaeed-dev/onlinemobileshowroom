from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

# Custom user manager 
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))

        return self.create_user(email, password, **extra_fields)


# Our user model 
class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_staff = models.BooleanField(default=False)  
    is_active = models.BooleanField(default=True) 

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text=_('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions_set',
        help_text=_('Specific permissions for this user.'),
        related_query_name='customuser',
    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

    def __str__(self):
        return self.email



# Company model
class MobileCompany(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    company_image = models.ImageField(upload_to='media/')
    
    def __str__(self):
        return self.name

# Mobile model
class Mobile(models.Model):
    company = models.ForeignKey(MobileCompany, on_delete=models.CASCADE)
    name = models.CharField(max_length=70)
    description = models.TextField()
    mobile_ram = models.CharField(max_length=10)
    color = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    screen_size = models.DecimalField(max_digits=4, decimal_places=2)
    image = models.ImageField(upload_to='media/', default='media/4.png')
    image1 = models.ImageField(upload_to='media/',default='media/4.png')
    image2 = models.ImageField(upload_to='media/',default='media/4.png')
    image3 = models.ImageField(upload_to='media/',default='media/4.png')

    def __str__(self):
        return f'{self.company.name} {self.name}'
    

# cart model 
class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    product = models.ForeignKey(Mobile, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_cast(self):
        return self.quantity * self.product.price