# django-board-project

Django로 구현한 간단한 게시판 📋

🔗 [https://board.leeyongjoo.site](https://board.leeyongjoo.site/)

![screenshot](https://user-images.githubusercontent.com/46367323/137743169-b241f154-c5f3-4297-9b88-47179e806d1b.png)

## 📚 Stacks

- Bootstrap 5, Javascript
- Django
- Nginx, Gunicorn
- AWS Lightsail

## 🎨 Features

`/common` : 공통 기능

- 로그인
    - 로그인 상태 유지
- 회원가입

`/board` : 질문 리스트 페이지

- 질문 페이징
- 질문 정렬
    - 최신순, 조회순, 추천순, 답변순
- 질문 검색

`/board/<quesiton_id>` : 질문 상세 페이지

- 질문 CRUD
- 답변, 답변 댓글 CRUD
- 질문 추천
- 질문 조회수
    - 중복 방지

## 💬 Descriptions

- FRONT (HTML, CSS, JS, Bootstrap 5)
    - 기존 jQuery 코드 Javascript 코드로 변경
    - 로그아웃 상태에서 글 작성 불가 (disabled)
    - 답변 추천이나 수정을 하면 앵커 엘리먼트를 이용하여 추천한 글로 스크롤 이동
    - 웹 폰트 추가
- BACK (Django)
    - 로그인 없이 질문 또는 답변 작성 시 로그인 요청
        - 로그인이 필요한 함수에 `@login_require` 어노테이션 적용
        - 로그인 성공 후 `next` 파라미터에 담긴 이전 페이지로 이동
    - 본인이 작성한 질문을 추천하면 오류 출력
    - `markdown` 모듈을 이용하여 마크다운으로 작성한 내용 HTML로 변환하여 출력
    - 템플릿 상속을 이용하여 섹션별로 분리
    - 추천 기능 - 본인글 추천 불가
    - 조회수 기능 - 비로그인, 로그인 상태 구분하여 중복 조회 방지 
    
- NETWORK
    - HTTPS 적용 및 리디렉션
