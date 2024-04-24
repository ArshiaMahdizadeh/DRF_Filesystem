from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.timezone import now
import os

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email='', name='', family='', active_code=None, gender=None, password=None):
        if not mobile_number:
            raise ValueError('must enter the mobile number')
        user = self.model(
            mobile_number=mobile_number,
            email=self.normalize_email(email),
            name=name,
            family=family,
            active_code=active_code,
            gender=gender
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, email='', name='', family='', password=None, active_code=None, gender=None):
        user = self.create_user(
            mobile_number=mobile_number,
            email=email,
            name=name,
            family=family,
            active_code=active_code,
            gender=gender,
            password=password,
        )
        user.is_active = True
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class CustomUser(AbstractBaseUser, PermissionsMixin):
    mobile_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    email = models.EmailField(max_length=200, blank=True)
    name = models.CharField(max_length=50, blank=True)
    family = models.CharField(max_length=50, blank=True)
    GENDER_CHOICES = (('True', 'مرد'), ('False', 'زن'))
    gender = models.CharField(max_length=50, blank=True, choices=GENDER_CHOICES, default='True', null=True)
    register_data = models.DateField(default=now)
    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    active_code = models.CharField(max_length=100, null=True, blank=True)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = ['email', 'name', 'family']

    objects = CustomUserManager()

    def __str__(self):
        return self.name + '' + self.family

    def has_perms(self, perm_list, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
    
    
TEXT_EXTENSIONS = ['txt', 'csv', 'json', 'xml', 'pdf']
IMAGE_EXTENSIONS = ['jpg', 'png', 'gif', 'bmp', 'tiff']

def custom_upload_to(instance, filename):
    extension = filename.split('.')[-1].lower()
    if extension in TEXT_EXTENSIONS:
        return os.path.join('text_files', filename)
    elif extension in IMAGE_EXTENSIONS:
        return os.path.join('image_files', filename)
    else:
        raise ValueError(f'Unsupported file extension: .{extension}')    
    
class FileUpload(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="fileuploader")
    file = models.FileField(upload_to=custom_upload_to, storage=FileSystemStorage(location='media/files'))
    upload_date = models.DateTimeField(auto_now_add=True)
    metadata = models.JSONField(blank=True, null=True)
   
    def __str__(self):
        return f'{self.user.name} - {self.file.name}'
    
 