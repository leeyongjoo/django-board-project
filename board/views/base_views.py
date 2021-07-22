from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.shortcuts import render, get_object_or_404

from board.forms import AnswerForm
from board.models import Question


def index(request):
    """
    게시판 목록 출력
    """
    # 입력 파라미터
    page = request.GET.get('page', '1')
    kw = request.GET.get('kw', '')
    so = request.GET.get('so', 'recent')

    # 검색
    if kw:
        question_list = Question.objects.filter(
            Q(subject__icontains=kw) |  # 제목에서 검색
            Q(content__icontains=kw) |  # 내용에서 검색
            Q(author__username__icontains=kw) | #질문 글쓴이에서 검색
            Q(answer__author__username__icontains=kw)   #답변 글쓴이에서 검색
        ).distinct()
    else:
        question_list = Question.objects.all()

    # 정렬
    if so == 'recommend':
        question_list = question_list.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:
        question_list = question_list.order_by('-create_date')

    # 페이징 처리
    # page = request.GET.get('page', 1)
    paginator = Paginator(question_list, 10)  # 한 페이지 당 10개씩
    page_obj = paginator.get_page(page)

    last_page = page_obj.paginator.page_range[-1]

    context = {'question_list': page_obj, 'last_page': last_page,
               'kw': kw, 'page': page, 'so': so
               }
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
