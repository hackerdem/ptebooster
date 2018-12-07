from django.urls import path, re_path
from modules.views import ModuleListView,ImagesListView,SpellingListView, \
RepeatListView, AcademicVocabularyListView, DictationListView, \
HighlightListView, SelectMissingWordView, HighlightCorrectSummaryView, ReadAloudView, \
RetellLectureView, EssayView, FillInBlanksView, AnswerShortQuestionsView, ReorderParagraphView, \
MultipleSelectionView, MultipleSelectionReadingView, FillBlanksReadingView, SummarizeSpokenTextView,\
SummarizeWrittenTextView,QuestionSectionView, HomePageListView

urlpatterns = [
    
    path('',HomePageListView.as_view(),name='home'),
    path('speaking-describe-image/', ImagesListView.as_view(),name='describe-image'),
    path('writing-spelling/', SpellingListView.as_view(),name='common-spelling-mistakes'),
    path('speaking-repeat-sentence/', RepeatListView.as_view(),name='repeat-sentence'),
    path('writing-academic-vocabulary-builder/', AcademicVocabularyListView.as_view(),name='academic-vocabulary'),
    path('listening-write-from-dictation/', DictationListView.as_view(),name='write-dictation'),
    path('highlight-incorrect-words/', HighlightListView.as_view(),name='highlight-incorrect-words'),
    path('highlight-correct-summary/', HighlightCorrectSummaryView.as_view(),name='highlight-correct-summary'),
    path('listening-select-missing-word/', SelectMissingWordView.as_view(),name='select-missing-word'),
    path('speaking-read-aloud/', ReadAloudView.as_view(),name='read-aloud'),
    path('speaking-retell-lecture/', RetellLectureView.as_view(),name='re-tell-lecture'),
    path('writing-write-essay/',EssayView.as_view(),name='essay'),
    path('listening-fill-in-blanks/',FillInBlanksView.as_view(),name='fill-blanks'),
    path('speaking-answer-short-question/',AnswerShortQuestionsView.as_view(),name='answer-short-questions'),
    path('reading-reorder-paragraphs/',ReorderParagraphView.as_view(),name='re-order-paragraphs'),
    path('listening-multiple-selection/',MultipleSelectionView.as_view(),name='multiple-choice-questions'),
    path('reading-multiple-selection/',MultipleSelectionReadingView.as_view(),name='multiple-choice-questions-reading'),
    path('listening-fill-blanks/',FillBlanksReadingView.as_view(),name='fill-blanks-reading'),
    path('speaking-summarize-spoken-text/',SummarizeSpokenTextView.as_view(),name='summarize-spoken-text'),
    path('writing-summarize-written-text/',SummarizeWrittenTextView.as_view(),name='summarize-written-text'),
    
]