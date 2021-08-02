from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render, resolve_url

from board.forms import CommentForm
from board.models import Comment, Question, Answer


@login_required(login_url='common:login')
def comment_create_question(request, question_id):
    """
    게시판 질문댓글등록
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.question = question
            comment.save()
            return redirect('board:detail', question_id=question.id)
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='common:login')
def comment_modify_question(request, comment_id):
    """
    게시판 질문댓글수정
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글수정권한이 없습니다')
        return redirect('board:detail', question_id=comment.question.id)

    if request.method == "POST":
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.save()
            return redirect('board:detail', question_id=comment.question.id)
    else:
        form = CommentForm(instance=comment)
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_question(request, comment_id):
    """
    게시판 질문댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다')
        return redirect('board:detail', question_id=comment.question.id)
    else:
        comment.delete()
    return redirect('board:detail', question_id=comment.question.id)

#########################################################################

@login_required(login_url='common:login')
def comment_create_answer(request, answer_id):
    """
    게시판 답변댓글등록
    """
    answer = get_object_or_404(Answer, pk=answer_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.answer = answer
            comment.save()
            return redirect('{}#answer_{}'.format(
                resolve_url('board:detail', question_id=comment.answer.question.id), answer.id))
    else:
        form = CommentForm()
    context = {'form': form}
    return render(request, 'board/comment_form.html', context)


@login_required(login_url='common:login')
def comment_delete_answer(request, comment_id):
    """
    게시판 답변댓글삭제
    """
    comment = get_object_or_404(Comment, pk=comment_id)
    if request.user != comment.author:
        messages.error(request, '댓글삭제 권한이 없습니다')
        return redirect('{}#answer_{}'.format(
            resolve_url('board:detail', question_id=comment.answer.question.id), comment.answer.id))
    else:
        comment.delete()
    return redirect('{}#answer_{}'.format(
        resolve_url('board:detail', question_id=comment.answer.question.id), comment.answer.id))