from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url
from django.utils import timezone

from board.forms import AnswerForm, QuestionForm
from board.models import Answer, Question


@login_required(login_url='common:login')
def answer_create(request, question_id):
    """
    답변 작성
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "POST":
        answer_form = AnswerForm(request.POST)
        if answer_form.is_valid():
            answer = Answer(question=question, **answer_form.cleaned_data)
            answer.create_date = timezone.now()
            answer.author = request.user
            answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', question_id=question.id), answer.id))
    else:
        answer_form = AnswerForm()
    context = {'question': question, 'form': answer_form}
    return render(request, 'board/question_detail.html', context)


@login_required(login_url='common:login')
def answer_modify(request, answer_id):
    """
    게시판 답변수정
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '수정 권한이 없습니다')
        return redirect('{}#answer_{}'.format(
            resolve_url('board:detail', question_id=answer.question.id), answer.id))

    if request.method == 'POST':
        form = AnswerForm(request.POST, instance=answer)

        if form.is_valid():
            modified_answer = form.save(commit=False)
            modified_answer.author = request.user
            modified_answer.modify_date = timezone.now()
            modified_answer.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', question_id=answer.question.id), answer.id))

    else:
        form = QuestionForm(instance=answer)
    context = {'form': form}
    return render(request, 'board/answer_form.html', context)


@login_required(login_url='common:login')
def answer_delete(request, answer_id):
    """
    게시판 답변삭제
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user != answer.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('{}#answer_{}'.format(
            resolve_url('board:detail', question_id=answer.question.id), answer.id))
    answer.delete()
    return redirect('{}#answer_{}'.format(
        resolve_url('board:detail', question_id=answer.question.id), answer.id))
