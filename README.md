# django-board-practice

Django로 게시판 구현하고 이것저것 연습해 보는 repo

🔗 http://leeyongjoo.site


## Stack

- Bootstrap 5, Javascript
- Django
- Nginx, Gunicorn
- AWS Lightsail

## Screenshot

...

## Feature

`/common` : 공통 기능
- 로그인
- 회원가입

`/board` : 질문 리스트 페이지
- 질문 조회
- 질문 리스트 페이징 처리
- 정렬, 검색

`/board/<quesiton_id>` : 질문 상세 페이지
- 질문 수정, 삭제
- 질문 추천
- 질문 조회수
- 답변 조회, 수정, 삭제

## Description

각 스택별로 구현하거나 적용한 사항

### Bootstrap (css)

- 커서 지정이 필요없는 부분을 `user-select-none` 클래스를 사용하여 지정 못하게 설정

### Django

- 질문 또는 답변 작성 시 로그인 필요
- 본인이 작성한 질문을 추천하면 오류 발생

### To-Do

- [ ] 조회수 중복으로 오르지 않게 수정
- [ ] HTTPS 적용
- [ ] ...

### Learned

...
