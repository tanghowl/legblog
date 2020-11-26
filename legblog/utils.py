from flask import request, redirect, url_for
from urllib.parse import urlparse, urljoin
from datetime import datetime


def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


def redirect_back(default='blog.index', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))


def get_current_theme() -> str:
    now_hour = get_current_time()
    if now_hour < 12:
        return 'perfect_blue'
    else:
        return 'black_swan'


def get_current_time() -> int:
    now_hour = datetime.now().hour
    return now_hour
