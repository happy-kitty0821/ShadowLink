from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        USER = 'USER', 'User'

    # setting a default role for new users
    role = models.CharField(max_length=15, choices=Role.choices, default=Role.ADMIN)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile-images/', null=True, blank=True)
    emails_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        #automatically assign staff/superuser based on user role
        if self.role == self.Role.ADMIN:
            self.is_staff = True
            self.is_superuser = True
        elif self.role == self.Role.USER:
            self.is_staff = False
            self.is_superuser = False
        # if the user is being created and no role is given then set the role to ADMIN
        if not self.pk:
            self.role = self.role or self.Role.ADMIN  # ensures that a role is set if not provided
        if self.password and not self.password.startswith(
                "pbkdf2_"):  # checks before saving that if a password is a django hash or not
            self.set_password(self.password)
        return super().save(*args, **kwargs)

    def __str__(self):
        return f"username : {self.username} role : {self.role}"


class SystemLogRecord(models.Model):
    date = models.DateField(auto_now_add=True, unique=True)
    log_file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.date} log"