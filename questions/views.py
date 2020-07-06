from django.shortcuts import render, redirect, reverse,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import UpdateView, DeleteView, CreateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from questions.models import Question
from accounts.models import User
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponseBadRequest, JsonResponse, HttpResponse
from django.urls import reverse
from .forms import QuestionForm
from questions.models import (Question, Answer, AnswerForm,
                         QuestionSerializer, AnswerSerializer)

def homeFeedView(request):
    current_user = request.user
    
    questions = Question.objects.filter(points__gt=-2, hidden=False).order_by('-created')
    paginator = Paginator(questions, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    questions_exist = len(questions) > 0
    context = {
        'current_user': current_user,
        'page_obj': page_obj,
        'questions_exist': questions_exist
    }
    return render(request, 'home.html', context)

def leaderboardView(request):
    current_user = request.user

    leaders = User.objects.filter(points__gt=0, is_superuser=False).order_by('-points')[:25]
    context = {'current_user': current_user, 'leaders': leaders}
    return render(request, 'leaderboard.html', context)

def testView(request):
    current_user = request.user
    context = {'username': current_user.username,
               'current_user': current_user}
    return render(request, 'test.html', context)

def updateVote(user, target, vote_type, question_or_answer):
    if question_or_answer == 'question':
        upvoted_targets = user.upvoted_questions
        downvoted_targets = user.downvoted_questions
    else:
        upvoted_targets = user.upvoted_answers
        downvoted_targets = user.downvoted_answers

    upvoted_targets.remove(target)
    downvoted_targets.remove(target)

    # if this is an upvote, add an upvote. otherwise, add a downvote.
    if vote_type == 'upvote':
        upvoted_targets.add(target)
    elif vote_type == 'downvote':
        downvoted_targets.add(target)

    target.update_points()
    return target.points

def answerVoteView(request, id):
    return voteView(request, id, 'answer')

def questionVoteView(request, id):
    return voteView(request, id, 'question')

def voteView(request, id, question_or_answer):
    current_user = request.user
    if question_or_answer == 'question':
        target = Question.objects.get(pk=id)
    else:
        target = Answer.objects.get(pk=id)
    
    if not current_user.is_authenticated:
        return HttpResponse('Not logged in', status=401)
    if current_user.id == target.user_id:
        return HttpResponseBadRequest('Same user')
    if request.method != 'POST':
        return HttpResponseBadRequest('The request is not POST')
    vote_type = request.POST.get('vote_type')
    points = updateVote(current_user, target, vote_type, question_or_answer)
    if question_or_answer == 'answer':
        target.user.update_points()
    return JsonResponse({'vote_type': vote_type, 'points': points})


def questionView(request, id):
    current_user = request.user
    question = Question.objects.get(pk=id)
    answers = Answer.objects.filter(question_id=id).order_by('created')
    answers_serialized = AnswerSerializer(answers, many=True).data
    for answer in answers_serialized:
        answer['upvoted'] = False
        answer['downvoted'] = False
        if not current_user.is_authenticated:
            pass
        elif current_user.upvoted_answers.filter(id=answer['id']).count() > 0:
            answer['upvoted'] = True
        elif current_user.downvoted_answers.filter(id=answer['id']).count() > 0:
            answer['downvoted'] = True
    
    # For the question
    upvoted = False
    downvoted = False
    asked_by_user = False

    if not current_user.is_authenticated:
        pass
    elif current_user.upvoted_questions.filter(id=question.id).count() > 0:
        upvoted = True
    elif current_user.downvoted_questions.filter(id=question.id).count() > 0:
        downvoted = True
    elif current_user.id == question.user_id:
        asked_by_user = True
        
    context = {'question': question, 'answers': answers,
               'current_user': current_user, 'points': question.points,
               'upvoted': upvoted, 'downvoted': downvoted,
               'asked_by_user': asked_by_user,
               'upvoted': upvoted, 'downvoted': downvoted,
               'answers_serialized': answers_serialized}
    return render(request, 'questions/question.html', context)


@login_required
def newView(request):
    current_user = request.user
    form = QuestionForm()
    if request.method == "POST":
        form = QuestionForm(request.POST)
        form.instance.user = request.user
        form.save()
        return redirect('/')
    context = {
        'current_user':current_user,
        'form':form
    }
    return render(request, 'questions/new.html', context)


def answerView(request, id):
    current_user = request.user

    if not current_user.is_authenticated:
        return HttpResponseRedirect('/accounts/login')
    if not request.method == 'POST':
        return HttpResponseRedirect(f'/question/{id}')
    form = AnswerForm(request.POST)
    if not form.is_valid():
        return HttpResponseRedirect(f'/question/{id}')
    a = Answer(
        user_id = current_user.id,
        question_id = id,
        text = form.cleaned_data['text']
    )
    a.save()
    return HttpResponseRedirect(f'/question/{id}')

def myAnswersView(request):
    current_user = request.user
    answers = Answer.objects.filter(user_id = current_user.id).order_by('-created')
    answers_exist = len(answers) > 0
    paginator = Paginator(answers, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'my_answers.html',
                    {'current_user': current_user,
                    'answers_exist': answers_exist,
                    'page_obj': page_obj})

def myQuestionsView(request):
    current_user = request.user
    questions = Question.objects.filter(user_id = current_user.id).order_by('-created')
    questions_exist = len(questions) > 0
    return render(request, 'questions/my_questions.html',
                  {'current_user': current_user, 'questions': questions,
                   'questions_exist': questions_exist})



@login_required
def questionUpdate(request, id):
    obj = get_object_or_404(Question, id=id)
    if obj.user == request.user:
        form = QuestionForm(instance=obj)
        if request.method == "POST":
            form = QuestionForm(request.POST, instance=obj)
            if form.is_valid:
                form.save()
                messages.success(request, "successfully updated")
                return redirect(obj.get_absolute_url())
        return render(request, 'questions/question_form.html', {'form':form})
    else:
        messages.info(request, "you have no permision for the action")
        return redirect(obj.get_absolute_url())
    
    
    



@login_required
def questionDelete(request, id):
    obj = get_object_or_404(Question, id=id)
    if obj.user == request.user or request.user.is_superuser:
        if request.method == "POST":
            obj.delete()
            messages.success(request, "successfully delete your question")
            return redirect('/')
    else:
        messages.info(request, "you have no permision for the action")
        return redirect(obj.get_absolute_url())
    return render(request, 'questions/question_delete.html', {'obj':obj})



@login_required
def answerDelete(request, id):
    obj = get_object_or_404(Answer, id=id)
    if obj.user == request.user or request.user.is_superuser:
        if request.method == "POST":
            obj.delete()
            messages.success(request, "successfully delete your question")
            return redirect('/')
    else:
        messages.info(request, "you have no permision for the action")
        return redirect(obj.question.get_absolute_url())
    
class AnswerDelete(DeleteView):
    model       =   Answer