from django.contrib import admin
from .models import Module, Images, Spelling, \
RepeatSentence, AcademicVocabulary, Dictation, HighlightWords,FillInBlanks, \
SelectMissingWord, HighlightCorrectSummary, ReadTAloud, RetellLecture, Essay, \
AnswerShortQuestions, ReorderParagraph, MultipleSelection, MultipleSelectionReading, \
FillBlanksReading, SummarizeSpokenText, SummarizeWrittenText, QuestionSection

# add related module field when migrating to new  database
@admin.register(QuestionSection)
class QuestionSectionAdmin(admin.ModelAdmin):
    list_display = ['question_type']
    

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ['module_name','question_type', 'slug', 'description','active']
    prepopulated_fields = {'slug':('module_name',)}

@admin.register(Images)
class ImagesAdmin(admin.ModelAdmin):
    list_display = ['related_module','id','image_question']


@admin.register(Spelling)
class SpellingAdmin(admin.ModelAdmin):
    list_display = ['related_module','item','audio']

@admin.register(RepeatSentence)
class RepeatSentenceAdmin(admin.ModelAdmin):
    list_display = ['related_module','item','audio'] #,'main_section'

@admin.register(Dictation)
class DictationAdmin(admin.ModelAdmin):
    list_display = ['related_module','item','audio'] #,'main_section'

@admin.register(AcademicVocabulary)
class AcademicVocabularyAdmin(admin.ModelAdmin):
    list_display = ['related_module','word','academic_in_sentence']

@admin.register(HighlightWords)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','audio','answers']

@admin.register(SelectMissingWord)
class SelectMissingWordAdmin(admin.ModelAdmin):
    list_display = ['related_module','audio_topic','audio','option_1', 'option_2','option_3','option_4','answer']

@admin.register(HighlightCorrectSummary)
class HighlightCorrectSummaryAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','audio','option_1', 'option_2','option_3','option_4','answer']

@admin.register(ReadTAloud)
class ReadAloudAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','audio']

@admin.register(RetellLecture)
class RetellLectureAdmin(admin.ModelAdmin):
    list_display = ['related_module','lecture','audio','video','image']
    
@admin.register(Essay)
class EssayAdmin(admin.ModelAdmin):
    list_display = ['related_module','topic']

@admin.register(FillInBlanks)
class FillinBlanksAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','audio','answers']

@admin.register(AnswerShortQuestions)
class AnswerShortQuestions(admin.ModelAdmin):
    list_display = ['related_module','audio','item']

@admin.register(ReorderParagraph)
class ReorderParagraphAdmin(admin.ModelAdmin):
    list_display = ['related_module','option_1','option_2','option_3','option_4','option_5','answer']

@admin.register(MultipleSelection)
class MultipleSelectionAdmin(admin.ModelAdmin):
    list_display = ['related_module','audio','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(MultipleSelectionReading)
class MultipleSelectionReadingAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(FillBlanksReading)
class FillBlanksReadingAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','option_1','option_2','option_3','option_4','option_5','option_6','answers']

@admin.register(SummarizeWrittenText)
class SummarizeWrittenTextAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','model_answer']

@admin.register(SummarizeSpokenText)
class SummarizeSpokenTextAdmin(admin.ModelAdmin):
    list_display = ['related_module','paragraph','audio','model_answer']
