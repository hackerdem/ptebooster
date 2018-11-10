from django.db import models


class Membership(models.Model):

    MEMBERSHIP_TYPES = (
                        ('Basic','Basic'),
                        ('Silver','Silver'),
                        ('Gold','Gold'),
                        ('Diamond','Diamond'),
                        )
    member_type = models.CharField(primary_key=True,max_length=100, unique=True, choices=MEMBERSHIP_TYPES,default='Basic')
    #slug = models.SlugField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2, default=0.0)
    is_active = models.CharField(max_length=100, default=True)
    duration = models.IntegerField(default=3)
    total_listening_question = models.IntegerField(default=50)
    total_reading_question = models.IntegerField(default=50)
    total_speaking_question = models.IntegerField(default=50)
    total_writing_question = models.IntegerField(default=50)

    
    class Meta:
        ordering = ('price',)

    def __str__(self):
        return self.member_type