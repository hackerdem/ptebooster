from django.db import models


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