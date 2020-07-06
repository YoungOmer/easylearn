from django.urls import path
from questions.views import *


urlpatterns = [
    path('', homeFeedView, name ='home'),
    path('test/', testView),
    path('leaderboard/', leaderboardView),
    path('question/<int:id>/', questionView, name="q_detail"),
    path('question/<int:id>/vote', questionVoteView),
    path('answer/<int:id>/vote', answerVoteView),
    path('question/<int:id>/answer', answerView),
    path('question/new/', newView, name ='question_create' ),
    path('question/my_answers/', myAnswersView, name='my-answers'),
    path('question/my_questions/', myQuestionsView, name='my-questions'),

    path('qustiion/<int:id>/delete/', questionDelete, name="q_delete"),
    path('qustiion/<int:id>/update/', questionUpdate, name="q_update"),
    
    path('answer/<int:pk>/delete/', AnswerDelete.as_view(), name="a_delete"),
]
