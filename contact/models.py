from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
User = get_user_model()
class ContactDataManager(models.Manager):
    def create_request(self,request_number,is_registered, is_paid_member, name, email, subject, message):
        request = self.create(
                            request_number=request_number,
                            is_registered=is_registered,
                            is_paid_member=is_paid_member,
                            name=name,
                            email=email,
                            subject=subject,
                            message=message
                            )
        return request
class ContactData(models.Model):
    request_number = models.CharField(primary_key=True, max_length=50)
    is_registered = models.BooleanField(default=False)
    is_paid_member = models.BooleanField(default=False)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.CharField(max_length=1250)
    created_on = models.DateTimeField(auto_now_add=True)

    objects = ContactDataManager()

    
    def __str__(self):
        return self.request_number



class Notification(models.Model):
    subject = models.CharField(max_length=100, blank=False, null=False)
    body = models.TextField(max_length=1000, blank=False, null=False)
    receiver_id = models.IntegerField(null=True, default=0,validators=[MinValueValidator(0)],help_text="Enter user ID for a specific user. For bulk notification leave as it is.")
    created_on = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User,on_delete=models.PROTECT ,limit_choices_to={'is_staff':True})

    objects = models.Manager() 
    @classmethod
    def create(cls,subject,body,receiver_id,created_by):
        notification = cls(subject=subject, body=body, receiver_id=receiver_id, created_by=created_by)
        notification.save()
    
    class Meta:
        indexes = [
            models.Index(fields=['receiver_id'], name='receiver_id_idx'),
            models.Index(fields=['created_on'],name='created_on_idx')
        ]