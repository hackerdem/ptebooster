from django.db import models
from membership.models import Membership
from modules.models import QuestionSection,Module

class QuestionStatistics(models.Model):
    question_id = models.IntegerField(null=False, blank=False)
    membership_type = models.ForeignKey(Membership,on_delete=models.CASCADE)
    question_section = models.ForeignKey(QuestionSection,on_delete=models.CASCADE)
    related_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    objects = models.Manager()
    class Meta:
        unique_together = ("question_id","related_module","question_section")
        indexes = [
            models.Index(fields=['membership_type','question_section','is_active'], name='statistics_idx'),
            
        ]