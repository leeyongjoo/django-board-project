from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from .forms import QuestionForm, AnswerForm
from .models import Question, Answer


# Create your views here.
def index(request):
    """
    게시판 목록 출력
    """
    # 게시판 목록 조회(오름차순)
    question_list = Question.objects.order_by('create_date')

    # 페이징 처리
    page = request.GET.get('page', 1)
    paginator = Paginator(question_list, 10)  # 한 페이지 당 10개씩
    page_obj = paginator.get_page(page)

    last_page = page_obj.paginator.page_range[-1]

    context = {'question_list': page_obj, 'last_page': last_page}
    return render(request, 'board/question_list.html', context)


def detail(request, question_id):
    """
    게시판 내용 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.method == "GET":
        answer_form = AnswerForm()
        context = {'question': question, 'answer_form': answer_form}
        return render(request, 'board/question_detail.html', context)


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
            return redirect('board:detail', question_id=question.id)
    else:
        answer_form = AnswerForm()
    context = {'question': question, 'answer_form': answer_form}
    return render(request, 'board/question_detail.html', context)


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
