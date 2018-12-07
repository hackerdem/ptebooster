from django.contrib import admin
from .models import Module, Images, Spelling, \
RepeatSentence, AcademicVocabulary, Dictation, HighlightWords,FillInBlanks, \
SelectMissingWord, HighlightCorrectSummary, ReadTAloud, RetellLecture, Essay, \
AnswerShortQuestions, ReorderParagraph, MultipleSelection, MultipleSelectionReading, \
FillBlanksReading, SummarizeSpokenText, SummarizeWrittenText, QuestionSection
from stats.models import QuestionStatistics
# add related module field when migrating to new  database

class ModelAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change): 
        super(ModelAdmin, self).save_model(request, obj, form, change)
        # temporary solution ,define a unique identifier for every question and modify related question later
        if change:
            QuestionStatistics.objects.get(question_id=obj.id, related_module=obj.related_module).delete()

        QuestionStatistics.objects.create(question_id=obj.id, membership_type=obj.question_group, related_module=obj.related_module, question_section=obj.related_module.question_type, is_active=obj.active)

    def delete_queryset(self, request, queryset):
        """Given a queryset, delete it from the database."""

        for object in queryset:
            try:
                QuestionStatistics.objects.get(question_id=object.id, related_module=object.related_module).delete()
            except:
                pass
        queryset.delete()

@admin.register(QuestionSection)
class QuestionSectionAdmin(admin.ModelAdmin):
    list_display = ['question_type']
    
@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['module_name','question_type', 'slug', 'description','active']
    prepopulated_fields = {'slug':('module_name',)}

@admin.register(Images)
class ImagesAdmin(ModelAdmin):
    list_display = ['related_module','id','image_question']


@admin.register(Spelling)
class SpellingAdmin(ModelAdmin):
    list_display = ['related_module','item','audio']

@admin.register(RepeatSentence)
class RepeatSentenceAdmin(ModelAdmin):
    list_display = ['related_module','item','audio'] #,'main_section'

@admin.register(Dictation)
class DictationAdmin(ModelAdmin):
    list_display = ['related_module','item','audio'] #,'main_section'

@admin.register(AcademicVocabulary)
class AcademicVocabularyAdmin(ModelAdmin):
    list_display = ['related_module','component_1','component_2','addition_1','addition_2','pos_1','pos_2','academic_in_sentence']


@admin.register(HighlightWords)
class HighlightAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','audio','answers']

@admin.register(SelectMissingWord)
class SelectMissingWordAdmin(ModelAdmin):
    list_display = ['related_module','audio_topic','audio','option_1', 'option_2','option_3','option_4','answer']

@admin.register(HighlightCorrectSummary)
class HighlightCorrectSummaryAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','audio','option_1', 'option_2','option_3','option_4','answer']

@admin.register(ReadTAloud)
class ReadAloudAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','audio']

@admin.register(RetellLecture)
class RetellLectureAdmin(ModelAdmin):
    list_display = ['related_module','lecture','audio','video','image']
    
@admin.register(Essay)
class EssayAdmin(ModelAdmin):
    list_display = ['related_module','topic']

@admin.register(FillInBlanks)
class FillinBlanksAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','audio','answers']

@admin.register(AnswerShortQuestions)
class AnswerShortQuestions(ModelAdmin):
    list_display = ['related_module','audio','item']

@admin.register(ReorderParagraph)
class ReorderParagraphAdmin(ModelAdmin):
    list_display = ['related_module','option_1','option_2','option_3','option_4','option_5','answer']

@admin.register(MultipleSelection)
class MultipleSelectionAdmin(ModelAdmin):
    list_display = ['related_module','audio','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(MultipleSelectionReading)
class MultipleSelectionReadingAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(FillBlanksReading)
class FillBlanksReadingAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(SummarizeWrittenText)
class SummarizeWrittenTextAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','model_answer']

@admin.register(SummarizeSpokenText)
class SummarizeSpokenTextAdmin(ModelAdmin):
    list_display = ['related_module','paragraph','audio','model_answer']
