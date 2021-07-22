from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, resolve_url

from board.models import Question, Answer


@login_required(login_url='common:login')
def vote_question(request, question_id):
    """
    게시판 질문추천등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user == question.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    # 이미 추천한 경우
    elif len(request.user.voter_question.filter(pk=question_id)) > 0:
        question.voter.remove(request.user)
    else:
        question.voter.add(request.user)
    return redirect('board:detail', question_id=question_id)


@login_required(login_url='common:login')
def vote_answer(request, answer_id):
    """
    게시판 답변추천등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.user == answer.author:
        messages.error(request, '본인이 작성한 글은 추천할 수 없습니다')
    # 이미 추천한 경우
    elif len(request.user.voter_answer.filter(pk=answer_id)) > 0:
        answer.voter.remove(request.user)
    else:
        answer.voter.add(request.user)
    return redirect('{}#answer_{}'.format(
        resolve_url('board:detail', question_id=answer.question.id), answer.id))
