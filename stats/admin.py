from django.contrib import admin
from .models import QuestionStatistics
@admin.register(QuestionStatistics)
class QuestionStatisticsAdmin(admin.ModelAdmin):
    list_display = ['question_id', 'related_module','membership_type','question_section','is_active']
