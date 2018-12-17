from django.db import models


class Membership(models.Model):

    MEMBERSHIP_TYPES = (
                        ('Basic','Basic'),
                        ('Silver','Silver'),
                        ('Gold','Gold'),
                        ('Diamond','Diamond'),
                        )
    member_type = models.CharField(primary_key=True,max_length=100, unique=True, choices=MEMBERSHIP_TYPES,default='Basic')
    presedence = models.IntegerField(default=0)
    #slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    is_active = models.CharField(max_length=100, default=True)
    duration = models.IntegerField(default=3)
    image=models.ImageField(upload_to='ptebooster/media/membership',default='ptebooster/media/images/module_default.png')
    total_listening_question = models.IntegerField(default=50)
    total_reading_question = models.IntegerField(default=50)
    total_speaking_question = models.IntegerField(default=50)
    total_writing_question = models.IntegerField(default=50)

    objects = models.Manager()
    
    class Meta:
        ordering = ('price',)
        indexes = [
            models.Index(fields=['presedence'],name='membership_presendence_idx'),
        ]

    def __str__(self):
        return self.member_type