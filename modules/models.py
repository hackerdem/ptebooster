from django.db import models
from django.urls import reverse
from membership.models import Membership



class QuestionSection(models.Model):
    SECTIONS = (('Listening', 'Listening'),
                ('Reading', 'Reading'),
                ('Speaking', 'Speaking'),
                ('Writing', 'Writing'),
                )

    question_type = models.CharField(primary_key=True, choices=SECTIONS ,max_length=15)
    module_image = models.ImageField(upload_to='ptebooster/media/section/images',default='ptebooster/media/images/module_default.png')
    description = models.TextField(max_length=300,blank=True,null=True)
    objects = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=['question_type'],name='section_type_idx')
        ]
class Module(models.Model):
    active = models.BooleanField(default=True)
    module_name = models.CharField(max_length=80)
    question_type = models.ForeignKey(QuestionSection, on_delete=models.PROTECT,null=True,blank=True,related_name='modules')
    module_image=models.ImageField(upload_to='ptebooster/media/icons',default='ptebooster/media/icons/module_default.png')
    slug = models.SlugField(max_length=80, unique=True) 
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def get_absolute_url(self):
        url= str(self.slug)
        return reverse(url)

    class Meta:
        ordering = ["-module_name",]
        indexes = [
            models.Index(fields=['active','question_type'], name='module_idx')
        ]

    def __str__(self):
        return self.module_name

class StatusAbstract(models.Model):
    QUESTION_TYPES = (('Basic', 'Basic'),
                ('Silver', 'Silver'),
                ('Gold', 'Gold'),
                ('Diamond', 'Diamond'),
                )
    related_module = models.ForeignKey(Module,null=True,blank=True,on_delete=models.PROTECT)
    active = models.BooleanField(default=False)
    question_group = models.ForeignKey(Membership, blank=True,null=True, on_delete=models.PROTECT)
    class Meta:
        abstract = True


class Images(StatusAbstract):
    image = models.ImageField(upload_to='ptebooster/media/images',verbose_name='Image')
    model_answer_text = models.CharField(max_length=400,blank=True, null=True)
    model_answer_audio = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
    class Meta:
        ordering = ['-id']
        indexes = [
            models.Index(fields=['id','related_module','active','question_group'], name='images_idx')
        ]

class Spelling(StatusAbstract):
    item = models.CharField(max_length=100, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/spelling-audio')
    class Meta:
        indexes = [
            models.Index(fields=['item','audio'], name='spelling_idx')
        ]
class RepeatSentence(StatusAbstract):
    item = models.CharField(max_length=300, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/sentences')

class Dictation(StatusAbstract):   
    item = models.CharField(max_length=300, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/dictation')
    class Meta:
        indexes = [
            models.Index(fields=['item','audio'], name='dictation_idx')
        ]
class AcademicVocabulary(StatusAbstract):
    component_1 = models.CharField(max_length=150, blank=False)
    component_2 = models.CharField(max_length=150, blank=False)
    addition_1 = models.CharField(max_length=80, null=True, blank=True)
    addition_2 = models.CharField(max_length=80, null=True, blank=True)
    pos_1 = models.CharField(max_length=80, null=True, blank=True)
    pos_2 = models.CharField(max_length=80, null=True, blank=True)
    academic_in_sentence = models.CharField(max_length=300, null=True, blank=True)
    class Meta:
        ordering = ['component_1']
        unique_together = ('component_1', 'component_2',)
class HighlightWords(StatusAbstract):
    paragraph = models.TextField(max_length=800,blank=False, help_text='In the paragrapgh write incorrect words and correct spelling side by side, incorrect first coreect second.')
    audio = models.FileField(upload_to='ptebooster/media/highlight-incorrect-words')
    answers = models.CharField(max_length=300, blank=False, help_text='Make sure incorrect word has only one instance in the paragraph. Add all answers comma seperated in this field.')
    correct_words = models.CharField(max_length=300, blank=True, help_text='Make sure correct word has only one instance in the paragraph.Add all correct words comma seperated in this field.')

class AbstractChoices(StatusAbstract):
    option_1 = models.TextField(max_length=500, blank=False)
    option_2 = models.TextField(max_length=500, blank=False)
    option_3 = models.TextField(max_length=500, blank=False)
    option_4 = models.TextField(max_length=500, blank=False)
    answer = models.TextField(max_length=500, blank=False,help_text="Enter answers with numbers separated with comman such as 1,2,3")

    class Meta:
        abstract = True

class SelectMissingWord(AbstractChoices):
    audio_topic = models.CharField(max_length=100, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/select-missing-word')
    

class HighlightCorrectSummary(AbstractChoices):
    paragraph = models.TextField(max_length=1000,blank=False)
    audio = models.FileField(upload_to='ptebooster/media/highlight-correct-summary')
    

class  ReadTAloud(StatusAbstract):
    paragraph = models.TextField(max_length=1000,blank=False)
    audio = models.FileField(upload_to='ptebooster/media/read-aloud',blank=True)
    
class RetellLecture(StatusAbstract):
    lecture = models.TextField(max_length=1000,blank=True)
    audio = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=False, null=False)
    video = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
    image = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
    model_answer = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
class Essay(StatusAbstract):
    topic = models.TextField(max_length=250,blank=False)
    model_answer = models.TextField(max_length=2000,blank=False)
    
class FillInBlanks(StatusAbstract):
    paragraph = models.TextField(max_length=1000,blank=False, help_text='Copy and paste full paragraph.')
    audio = models.FileField(upload_to='ptebooster/media/fill-in-blanks',blank=False)
    answers = models.CharField(max_length=300,blank=False, help_text='Enter answers comma seperated.')

class AnswerShortQuestions(StatusAbstract):
    audio = models.FileField(upload_to='ptebooster/media/answer-short-question',blank=False)
    question = models.CharField(max_length=90, unique=True, blank=False)
    answer = models.CharField(max_length=90)

class ReorderParagraph(AbstractChoices):
    option_5 = models.TextField(max_length=500,blank=False)
    

class AbstractSelection(StatusAbstract):
    paragraph = models.TextField(max_length=600,blank=True)
    option_1 = models.CharField(max_length=150,blank=False)
    option_2 = models.CharField(max_length=150,blank=False)
    option_3 = models.CharField(max_length=150,blank=False)
    option_4 = models.CharField(max_length=150,blank=False)
    option_5 = models.CharField(max_length=150,blank=True)
    option_6 = models.CharField(max_length=150,blank=True)
    answers = models.CharField(max_length=150,blank=False)

    class Meta:
        abstract = True

class MultipleSelection(AbstractSelection):
    audio = models.FileField(upload_to='ptebooster/media/multiple-selection-listening',blank=False)
    question = models.CharField(max_length=300, blank=True, null=True)

class MultipleSelectionReading(AbstractSelection):
    paragraph = models.TextField(max_length=1000,blank=False)
    

class FillBlanksReading(AbstractSelection):
    paragraph = models.TextField(max_length=1000,blank=False)

class SummarizeSpokenText(StatusAbstract):
    paragraph = models.TextField(max_length=1000,blank=False)
    audio = models.FileField(upload_to='ptebooster/media/summarize-spoken-text',blank=False)
    model_answer = models.TextField(max_length=1000,blank=True)


class SummarizeWrittenText(StatusAbstract):
    paragraph = models.TextField(max_length=1000,blank=False)
    model_answer = models.TextField(max_length=1000,blank=True)



