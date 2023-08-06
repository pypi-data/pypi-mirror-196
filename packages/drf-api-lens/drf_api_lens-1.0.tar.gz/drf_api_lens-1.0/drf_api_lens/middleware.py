import time
from django.conf import settings
from drf_api_lens.store_capture_error import ErrorCaptureOperation
from drf_api_lens.utils import CleaningData


class ErrorCapturingMiddleware:
    """
    This class defines a middleware component in a Python web application that captures errors that occur
    during the processing of requests and stores them in a database if user is allowed. The middleware is
    called for each incoming request and is responsible for handling the request and generating a response.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.STORE_CAPTURE_ERROR_TO_DATABASE = getattr(settings, 'STORE_CAPTURE_ERROR_TO_DATABASE', False)

    def __call__(self, request):
        if self.STORE_CAPTURE_ERROR_TO_DATABASE:
            start_time = time.time()
            # code to be executed for each request before the view (and later middleware) are called.
            response = self.get_response(request)
            # code to be executed for each request/response after the view is called.
            """
            200: HTTP_200_OK
            201: HTTP_201_CREATED
            202: HTTP_202_ACCEPTED
            203: HTTP_203_NON_AUTHORITATIVE_INFORMATION
            204: HTTP_204_NO_CONTENT
            205: HTTP_205_RESET_CONTENT
            206: HTTP_206_PARTIAL_CONTENT
            207: HTTP_207_MULTI_STATUS
            208: HTTP_208_ALREADY_REPORTED
            226: HTTP_226_IM_USED
            """
            if response.status_code not in [200,201,202,203,204,205,206,207,208,226]:
                data = CleaningData.cleaning_and_build_data_dict(request,response,start_time)
                ErrorCaptureOperation.push(data=data)
        else:
            response = self.get_response(request)
        return response