from django.db import models

from accounts.managers import UserManager
from oscar.apps.customer.abstract_models import AbstractUser

from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import Permission


# Create your models here.

class User(AbstractUser):
    """
    customized user model
    """

    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='customuser_set',
        blank=True,
    )

    objects = UserManager()

    USERNAME_FIELD = 'email'

    @property
    def full_name(self):
        return self.get_full_name()

    def __str__(self):
        return self.email or self.sys_id

    def get_full_name(self):
        return '{0} {1}'.format(self.first_name, self.last_name)    

    def get_short_name(self):
        return self.first_name
    
    @property
    def sys_id(self):
        return 'USER{}'.format(str(self.pk).zfill(6))    

    @property
    def name(self):
        return self.get_full_name()

    @name.setter
    def name(self, full_name):
        self.first_name, self.last_name = get_first_and_last_name(full_name)

def get_first_and_last_name(name):
    """
    Returns first and last name from a given name
    """
    name = name.strip()
    name_parts = name.split()
    if len(name_parts) > 1:
        first_name = name_parts[0]
        last_name = ' '.join(name_parts[1:])
        return first_name, last_name
    return name, ''   


