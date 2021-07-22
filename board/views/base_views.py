from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

from board.forms import AnswerForm
from board.models import Question


def index(request):
    """
    게시판 목록 출력
    """
    # 게시판 목록 조회(내림차순)
    question_list = Question.objects.order_by('-create_date')

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
