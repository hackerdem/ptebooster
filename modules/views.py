from django.views.generic import ListView,TemplateView, FormView
import re
from modules.models import Module, Images, Spelling, \
RepeatSentence, AcademicVocabulary, Dictation, HighlightWords, \
SelectMissingWord, HighlightCorrectSummary, ReadTAloud, RetellLecture, Essay,\
FillInBlanks, AnswerShortQuestions, ReorderParagraph, MultipleSelection, MultipleSelectionReading,\
FillBlanksReading, SummarizeSpokenText,SummarizeWrittenText, QuestionSection
from django.contrib.auth.mixins import LoginRequiredMixin
from contact.forms import ContactDataForm
from contact.models import ContactData
from membership.models import Membership
from django.http import HttpResponse
from django.utils.crypto import get_random_string
from django.contrib.auth import get_user_model


User = get_user_model()
class HomePageListView(ListView,FormView):
    form_class= ContactDataForm
    template_name='modules/home.html'
    context_object_name = 'question_section_list'
    model = QuestionSection
    def get_context_data(self, **kwargs):
        context = super(HomePageListView, self).get_context_data(**kwargs)
        context.update({
            'membership_list': Membership.objects.all()
        })
        return context
    def get_queryset(self):
        return QuestionSection.objects.all()

    def get(self,request):
        form = ContactDataForm()
       
        return super(HomePageListView, self).get(request, form=form)

    def post(self, request, *args, **kwargs):
        if request.is_ajax():
            try:
                is_registered = False
                is_paid_member = False
                email = request.POST['email']
                
                if User.objects.filter(email=email).exists():
                    user = User.objects.get(email=email)
                else:
                    user = None
                if user:
                    is_registered = True
                    if user.user_type != 'Basic':is_paid_member = True
                request_number = get_random_string(8)
                new_request = ContactData.objects.create_request(
                                                                request_number,
                                                                is_registered,
                                                                is_paid_member,
                                                                request.POST['name'],
                                                                email,
                                                                request.POST['subject'],
                                                                request.POST['message'])
                new_request.save()
            except Exception as e:
                print(e)

            return HttpResponse('ok')
        else:
            return HttpResponse('ko')
        """error = None
        success =None
        form = ContactDataForm(request.POST)
        if form.is_valid():
            a='Form is valid'

        else:
            a='haydeee'"""
        
class AbstractListView(ListView):
    
    def get_queryset(self):    
        qs = super().get_queryset() 
        queryset = qs.filter(active=True)
        return queryset
    class Meta:
        abstract = True

class ModuleListView(AbstractListView):
    model = Module
    template_name='modules/home.html'
    #paginate_by = 6

class QuestionSectionView(ListView):
    model = QuestionSection
    template_name='modules/home.html'
    #paginate_by = 6 

class ImagesListView(LoginRequiredMixin,AbstractListView):
    login_url = 'account_login'
    model = Images
    template_name = 'questions/describe-image.html'
    paginate_by = 1

class SpellingListView(AbstractListView):
    model = Spelling
    template_name = 'questions/spelling.html'
    paginate_by = 10

class RepeatListView(AbstractListView):
    model = RepeatSentence
    template_name = 'questions/repeat-sentence.html'
    paginate_by = 10

class AcademicVocabularyListView(AbstractListView):
    model = AcademicVocabulary
    template_name = 'questions/academic-vocabulary.html'
    paginate_by = 10

class DictationListView(AbstractListView):
    model = Dictation
    template_name = 'questions/write-from-dictation.html'
    paginate_by = 2

class HighlightListView(AbstractListView):
    model = HighlightWords
    template_name = 'questions/highlight-incorrect-words.html'
    paginate_by = 1
    def get_queryset(self):
            queryset = super(HighlightListView,self).get_queryset()
            for item in queryset:
                paragraph = item.paragraph
                item.paragraph = paragraph.split()
                answers = item.answers
                item.answers = [ i.strip() for i in answers.split(',')]
            return queryset
class SelectMissingWordView(AbstractListView):
    model = SelectMissingWord
    template_name = 'questions/select-missing-word.html'
    paginate_by = 1

class HighlightCorrectSummaryView(AbstractListView):
    model = HighlightCorrectSummary
    template_name = 'questions/highlight-correct-summary.html'
    paginate_by = 1

class ReadAloudView(AbstractListView):
    model = ReadTAloud
    template_name = 'questions/read-aloud.html'
    paginate_by = 1

class RetellLectureView(AbstractListView):
    model = RetellLecture
    template_name = 'questions/retell-lecture.html'
    paginate_by = 1

class EssayView(AbstractListView):
    model = Essay
    template_name = 'questions/write-essay.html'
    paginate_by = 1

class FillInBlanksView(AbstractListView):
    model = FillInBlanks
    template_name = 'questions/fill-in-blanks.html'
    paginate_by = 1

    def get_queryset(self):
        queryset = super(FillInBlanksView, self).get_queryset()
        for item in queryset:
            answer_string = item.answers
            answer_list = answer_string.split(",")
            regex_words = re.compile('|'.join(map(re.escape,answer_list)))
            paragraph = regex_words.sub('XXXX',item.paragraph)
            item.paragraph = paragraph.split()
            item.answers = answer_list
            
        return queryset
class AnswerShortQuestionsView(AbstractListView):
    model = AnswerShortQuestions
    template_name = 'questions/spelling.html'
    paginate_by = 10

class ReorderParagraphView(AbstractListView):
    model = ReorderParagraph
    template_name = 'questions/reorder-paragraph.html'
    paginate_by = 1
    def get_queryset(self):
        queryset = super(ReorderParagraphView, self).get_queryset()
        for item in queryset:
            
            item.answer = [item.option_1,item.option_2,item.option_3,item.option_4]
            if item.option_5:(item.answer).append(item.option_5)
       
            
        return queryset
class MultipleSelectionView(AbstractListView):
    model = MultipleSelection
    template_name = 'questions/multiple-selection.html'
    paginate_by = 1

class MultipleSelectionReadingView(AbstractListView):
    model = MultipleSelectionReading
    template_name = 'questions/multiple-selection.html'
    paginate_by = 1

class FillBlanksReadingView(AbstractListView):
    model = FillBlanksReading
    template_name = 'questions/fill-blanks-reading.html'
    paginate_by = 1
    def get_queryset(self):
        queryset = super(FillBlanksReadingView, self).get_queryset()
        for item in queryset:
            pr = (item.paragraph).split()
            item.answers = (item.answers).split(',')
            item.option_1 = (item.option_1).split(',')
            item.option_2 = (item.option_2).split(',')
            item.option_3 = (item.option_3).split(',')
            item.option_4 = (item.option_4).split(',')
            item.option_5 = (item.option_5).split(',')
            for i in pr:
                if i in item.answers:
                    pr[pr.index(i)]=i.upper()
            item.paragraph = pr  
        return queryset

class SummarizeSpokenTextView(AbstractListView):
    model = SummarizeSpokenText
    template_name = 'questions/summarize-spoken-text.html'
    paginate_by = 1

class SummarizeWrittenTextView(AbstractListView):
    model = SummarizeWrittenText
    template_name = 'questions/summarize-written-text.html'
    paginate_by = 1

# this is not working tke care of it later not urgent


class Template404View(TemplateView):
    template_name='modules/404.html'