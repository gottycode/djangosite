import time
import logging

from django.utils.deprecation import MiddlewareMixin


application_logger = logging.getLogger('application-logger')
error_logger = logging.getLogger('error-logger')
performance_logger = logging.getLogger('performance-logger')
access_logger = logging.getLogger('access-logger')


class MyMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):

        # パスをログに出力
        application_logger.info(request.get_full_path())

        # アクセスログ
        ip_add = request.META.get('REMOTE_ADDR')
        browser = request.META.get('HTTP_USER_AGENT')
        access_logger.info(f'{ip_add}_{browser}')

    def process_exception(self, request, exception):
        error_logger.error(exception, exc_info=True)


class PerformanceMiddleware(MiddlewareMixin):

    def process_view(self, request, view_func, view_args, view_kwargs):
        start_time = time.time()
        request.start_time = start_time

    def process_template_response(self, request, response):
        response_time = time.time() - request.start_time
        performance_logger.info(f'{request.get_full_path()}: {response_time}s')
        return response
