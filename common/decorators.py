from functools import wraps

KEEP_LOGIN_AGE = 60 * 60 * 24 * 365  # 1 year


def keep_login(view_func):
    @wraps(view_func)
    def _wrapped_view_func(request, *args, **kwargs):
        response = view_func(request, *args, **kwargs)

        # 로그인 성공 시 세션 만료 시간 설정
        if request.user.is_authenticated:
            if request.POST.get('keepLogin', '') != '':
                request.session.set_expiry(KEEP_LOGIN_AGE)
                request.session.modified = True
        return response
    return _wrapped_view_func
