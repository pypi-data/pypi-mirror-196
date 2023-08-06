import re
from django.conf import settings
import json
import time

class RequestAnalysis:
    """
    The class RequestAnalysis contains a collection of static methods that can be used
    to analyze a request object in a web application. Each method is responsible for retrieving
    a specific aspect of the request object, such as headers, URL, parameters, data, method, user, 
    and client IP address.
    """
    
    @staticmethod
    def get_headers(request=None):
        """
        This method retrieves the HTTP headers from the request 
        object and returns them in a dictionary format.
        """
        regex = re.compile('^HTTP_')
        return dict((regex.sub('', header), value) for (header, value)
                in request.META.items() if header.startswith('HTTP_'))

    @staticmethod
    def get_request_url(request=None):
        """
        This method retrieves the full URL of the request object.
        """
        return request.build_absolute_uri()

    @staticmethod
    def get_request_params(request=None):
        """
        This method retrieves the query parameters from the 
        request object and returns them in a dictionary format.
        """
        return dict(request.GET)

    @staticmethod
    def get_request_data(request=None):
        """
        This method retrieves the request data from the request object. 
        It first attempts to parse the data as JSON, but if that fails,
        it will fall back to a combination of the FILES and POST dictionaries.
        """
        try:
            request_data = json.loads(request.body) if request.body else ''
        except Exception:
            request_data = {**dict(request.FILES),**dict(request.POST)}

        return request_data

    @staticmethod
    def get_request_method(request=None):
        """
        This method retrieves the HTTP method (e.g., GET, POST, PUT, DELETE)
        from the request object.
        """
        return request.method

    @staticmethod
    def get_requested_user(request=None):
        """
        This method retrieves the user object associated with the request object, if any.
        """
        return request.user

    @staticmethod
    def get_request_client_ip(request):
        """
        This method retrieves the client IP address associated with the
        request object. It first checks for the HTTP_X_FORWARDED_FOR header 
        and uses that if available. Otherwise, it falls back to the REMOTE_ADDR header. 
        If all else fails, it returns an empty string.
        """
        try:
            if x_forwarded_for := request.META.get('HTTP_X_FORWARDED_FOR'):
                remote_ip = x_forwarded_for.split(',')[0]
            else:
                remote_ip = request.META.get('REMOTE_ADDR')
            return remote_ip
        except Exception:
            return ''

class ResponseAnalysis:
    def __init__(self,response) -> None:
        """
        This is the constructor of the class, which takes in a response parameter
        that represents the response received from a web request. The constructor 
        initializes the response attribute of the class with this parameter.
        """
        self.response=response

    def get_response_data(self):
        """
        This method analyzes the response attribute and returns the body of the response
        in a format that is suitable for further processing. It does this by checking the 
        content-type header of the response and using it to determine how to parse the 
        response body. If the content-type is JSON, the method parses the response body 
        using the json.loads() function and returns the resulting JSON object. If the 
        content-type is any other type, the method returns the content-type string itself.
        """
        CONTENT_TYPES = (
            'application/json',    
            'application/xml',
            'application/xhtml+xml',
            'application/pdf',
            'application/zip',
            'application/x-www-form-urlencoded',
            'application/javascript',
            'application/octet-stream',
            'application/vnd.ms-excel',
            'application/vnd.ms-powerpoint',
            'application/vnd.ms-word',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.api+json',
            'audio/mpeg',
            'audio/wav',
            'image/gif',
            'image/jpeg',
            'image/png',
            'image/svg+xml',
            'multipart/form-data',
            'text/html',
            'text/plain',
            'text/xml',
            'text/csv'
        )

        content_type = self.response.get('content-type')
        if content_type in CONTENT_TYPES:
            if content_type != 'application/json':
                response_body = content_type
            else:
                response_body = json.loads(self.response.content).get("message")
        else:
            response_body = []
        return response_body


    def get_response_status_code(self):
        """
        This method returns the HTTP status code of the response. 
        It does this by calling the status_code attribute of the response object.
        """
        return self.response.status_code


class ErrorAnalysis:
    """
    This class seems to be designed to help with error handling and
    debugging by providing useful information about where an error occurred.
    """

    @staticmethod
    def detect_error(exception):
        """
        The detect_error method takes an exception as input, and
        uses the get_error_info method to extract the file path,
        line number, and function name where the error occurred.
        It then formats these values and the exception message 
        into a string, which it returns as the error message.
        """
        error_file_path, error_line_number, function_name = ErrorAnalysis.get_error_info()
        error_message = "An error occurred in file '{}' at line {}: '{}' in function '{}'".format(
            error_file_path, error_line_number,str(exception) ,function_name)
        return error_message
        

    @staticmethod
    def get_error_info() -> None:
        """
        The get_error_info method uses the traceback module to extract 
        information about the current exception, such as the file path,
        line number, and function name. It then returns these values.
        """
        import sys
        import traceback
        tb = traceback.extract_tb(sys.exc_info()[2])
        error_file, error_line, function_name, text = tb[-1]
        return error_file, error_line, function_name


class CleaningData:
    """
    This is a class definition for a Python class called "CleaningData".The 
    class contains a single static method called "cleaning_and_build_data_dict" 
    that takes three parameters: "request", "response", and "start_time".

    Within the method, an instance of a class called "ResponseAnalysis" is created
    using the "response" parameter, which is used to analyze the response and extract
    information such as the response data and status code. The method also uses another 
    class called "RequestAnalysis" to extract information about the request such as the 
    requested user, URL, headers, body, parameters, and method. The method then returns 
    a dictionary that contains all of this information, as well as the execution time of the method.
    """

    @staticmethod
    def cleaning_and_build_data_dict(request,response,start_time):
        response_analysis = ResponseAnalysis(response=response)
        data = dict(
            user=RequestAnalysis.get_requested_user(request=request),
            url_requested=RequestAnalysis.get_request_url(request=request),
            request_headers=RequestAnalysis.get_headers(request=request),
            request_body=RequestAnalysis.get_request_data(request=request),
            query_params=RequestAnalysis.get_request_params(request=request),
            request_method=RequestAnalysis.get_request_method(request=request),
            ip_address=RequestAnalysis.get_request_client_ip(request=request),
            response_body=response_analysis.get_response_data(),
            response_status_code=response_analysis.get_response_status_code(),
            execution_time=(time.time() - start_time)*1000,
        )
        return data