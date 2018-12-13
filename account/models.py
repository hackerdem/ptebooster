from django.db import models
from django.contrib.auth.models import AbstractUser as _AbstractUser, UserManager as _UserManager
from django.core.exceptions import ValidationError
from membership.models import Membership
from django.urls import reverse
from django.utils.html import format_html

class UserManager(_UserManager):


    def register(self,membership_start_date, first_name, username, password, email,user_type,last_name='',verify_code='xxxx',verify_time_limit='',):
        if self.filter(email__iexact=email).count()>0:
            message = format_html('User with this Email account already exists.Please click <a href="{}">here</a>', reverse('account:account_forgot_password'))
            raise ValidationError(message)

        if self.count()==0:
            user = self.create_superuser(membership_start_date=membership_start_date,
                                        username=username,
                                        first_name=first_name,
                                        email=email,
                                        password=password,
                                        last_name=last_name,
                                        verify_code=verify_code,
                                        verify_time_limit=verify_time_limit,
                                        user_type=user_type)

        else:
            user = self.create_user(membership_start_date=membership_start_date,
                                        username=username,
                                        first_name=first_name,
                                        email=email,
                                        password=password,
                                        last_name=last_name,
                                        verify_code=verify_code,
                                        verify_time_limit=verify_time_limit,
                                        user_type=user_type)

        return user


class AbstractUser(_AbstractUser):
    user_type = models.ForeignKey(Membership,default='Basic',on_delete=models.PROTECT)
    membership_start_date = models.DateTimeField(blank=True, null=True,)
    membership_end_date = models.DateTimeField(blank=True, null=True,)
    is_active = models.BooleanField(default=False)
    verify_code = models.CharField(max_length=512, blank=True, null=True, help_text='Account verification code', editable=False)
    verify_time_limit = models.DateTimeField(blank=True, null=True, editable=False)
    reset_code = models.CharField(max_length=512, blank=True, null=True, help_text='Account verification code', editable=False)
    reset_time_limit = models.DateTimeField(blank=True, null=True, editable=False)
    created_on = models.DateTimeField(auto_now=True)
    updated_on = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    REQUIRED_FIELDS = ['email',]

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['email','user_type','is_active'], name='user_idx')
        ]

    @classmethod
    def get_by_username(cls, username):

        return cls.objects.get(username__iexact=username)
        
class User(AbstractUser):
    """
    Extends Django authentication user model.
    """
