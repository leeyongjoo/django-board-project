from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from board.forms import QuestionForm
from board.models import Question


@login_required(login_url='common:login')
def question_create(request):
    """
    게시판 질문등록
    """
    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            # question = form.save(commit=False)
            question = Question(**form.cleaned_data)
            question.create_date = timezone.now()
            question.author = request.user
            question.save()
            return redirect('board:index')
    else:
        form = QuestionForm()
    return render(request, 'board/question_form.html', {'form': form})


@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    게시판 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('board:detail', question_id=question.id)

    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)

        if form.is_valid():
            modified_question = form.save(commit=False)
            modified_question.author = request.user
            modified_question.modify_date = timezone.now()
            modified_question.save()
            return redirect('board:detail', question_id=modified_question.id)

    else:
        form = QuestionForm(instance=question)
    context = {'form': form}
    return render(request, 'board/question_form.html', context)


@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
    게시판 질문삭제
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('board:detail', question_id=question.id)
    question.delete()
    return redirect('board:index')
