from datetime import datetime, timedelta

from django.core.paginator import Paginator
from django.db.models import Q, Count, F
from django.shortcuts import render, get_object_or_404


from board.forms import AnswerForm
from board.models import Question


import logging
logger = logging.getLogger('board')




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
    elif so == 'view':
        question_list = question_list.annotate(num_answer=Count('answer')).order_by('-hit', '-create_date')
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

        q_id: str = str(question.id)

        # 로그인 한 경우
        if request.user.is_authenticated is True:
            cookie_hits_key = f'hits_{request.user.id}'
        # 비로그인 경우
        else:
            cookie_hits_key = 'hits_0'

        # 쿠키로부터 방문기록 로드
        cookie_hits_value: str = request.COOKIES.get(cookie_hits_key, '')

        # 쿠키에 cookie_hits_key 항목이 있는 경우
        if cookie_hits_value != '':
            q_id_list = cookie_hits_value.split('|')
            # 방문한 경우는 그대로 응답
            if q_id in q_id_list:
                return render(request, 'board/question_detail.html', context)
            # 방문하지 않은 경우
            else:
                new_hits_dict = (cookie_hits_key, cookie_hits_value+f'|{q_id}')
                question.hit = F('hit') + 1
                question.save()
                question.refresh_from_db()
        # hits 가 없는 경우
        else:
            new_hits_dict = (cookie_hits_key, q_id)
            question.hit = F('hit') + 1
            question.save()
            question.refresh_from_db()

        response = render(request, 'board/question_detail.html', context)

        # 만료시간 설정
        midnight_utc = datetime.replace(datetime.utcnow() + timedelta(days=1), hour=0, minute=0, second=0)
        midnight_kst = midnight_utc - timedelta(hours=9)

        response.set_cookie(*new_hits_dict, expires=midnight_kst)
        return response
