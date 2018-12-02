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

class Module(models.Model):
    active = models.BooleanField(default=False)
    module_name = models.CharField(max_length=80)
    question_type = models.ForeignKey(QuestionSection, on_delete=models.PROTECT,null=True,blank=True,related_name='modules')
    module_image=models.ImageField(upload_to='ptebooster/media/images',default='ptebooster/media/images/module_default.png')
    slug = models.SlugField(max_length=80, unique=True) 
    description = models.CharField(max_length=200)
    created = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        url= str(self.slug)
        return reverse(url)

    class Meta:
        ordering = ["-created",]

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
    image_question=models.ImageField(upload_to='ptebooster/media/images',verbose_name='Image')

    class Meta:
        ordering = ['-id']

class Spelling(StatusAbstract):
    item = models.CharField(max_length=100, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/spelling-audio')

class RepeatSentence(StatusAbstract):
    item = models.CharField(max_length=300, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/sentences')

class Dictation(StatusAbstract):   
    item = models.CharField(max_length=300, blank=False)
    audio = models.FileField(upload_to='ptebooster/media/dictation')

class AcademicVocabulary(StatusAbstract):
    word = models.CharField(max_length=150, blank=False)
    academic_in_sentence = models.CharField(max_length=300, blank=False)

class HighlightWords(StatusAbstract):
    paragraph = models.TextField(max_length=800,blank=False)
    audio = models.FileField(upload_to='ptebooster/media/highlight-incorrect-words')
    answers = models.CharField(max_length=300, blank=False)
    correct_words = models.CharField(max_length=300, blank=True)

class AbstractChoices(StatusAbstract):
    option_1 = models.TextField(max_length=500, blank=False)
    option_2 = models.TextField(max_length=500, blank=False)
    option_3 = models.TextField(max_length=500, blank=False)
    option_4 = models.TextField(max_length=500, blank=False)
    answer = models.TextField(max_length=500, blank=False)

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
    audio = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
    video = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)
    image = models.FileField(upload_to='ptebooster/media/retell-lecture',blank=True)

class Essay(StatusAbstract):
    topic = models.TextField(max_length=1000,blank=False)
    
class FillInBlanks(StatusAbstract):
    paragraph = models.TextField(max_length=1000,blank=False)
    audio = models.FileField(upload_to='ptebooster/media/fill-in-blanks',blank=False)
    answers = models.CharField(max_length=300,blank=False)

class AnswerShortQuestions(StatusAbstract):
    audio = models.FileField(upload_to='ptebooster/media/answer-short-question',blank=False)
    item = models.CharField(max_length=90,blank=False)

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



class QuestionStatistics(models.Model):
    question_id = models.IntegerField(null=False, blank=False)
    membership_type = models.ForeignKey(Membership,on_delete=models.CASCADE)
    question_section = models.ForeignKey(QuestionSection,on_delete=models.CASCADE)
    related_module = models.ForeignKey(Module, on_delete=models.CASCADE)
    is_active = models.BooleanField()

    class Meta:
        unique_together = ("question_id","question_section")