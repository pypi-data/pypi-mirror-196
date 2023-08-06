# DRF API LENS
DRF API Lens is a comprehensive Python package designed to help developers capture errors in their Django REST framework (DRF) APIs.The package offers a range of reusable tools to simplify the process of error handling in DRF.At the core of the package is the ErrorCapturingMiddleware, which intercepts any error that occurs during the execution of an API request. The middleware logs the error to the console and optionally stores it in a database when configured to do so via the STORE_CAPTURE_ERROR_TO_DATABASE setting.In addition, the package provides the capture_error decorator to handle exceptions that occur during view function execution. This powerful decorator takes care of catching any errors that arise during the execution of an API request, saving developers time and effort.The validate_api_parameters parameter is another valuable feature of DRF API Lens. This parameter checks if the required parameters are present in the API request data, and returns an error response if any of the parameters are missing. This functionality is highly customizable, as developers can specify the parameters they want to validate using a list of strings.Overall, DRF API Lens is an end-to-end solution that makes error handling in DRF APIs a breeze. It provides developers with a range of reusable tools that are easy to implement and highly customizable, saving them time and effort while ensuring their APIs are robust and reliable.

## Installation
To install drf_api_lens, run the following command:
```
pip install drf_api_lens
```

## Setup Configuration
1. Add 'drf_api_lens' to your INSTALLED_APPS in your settings.py file.
```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ...
    'drf_api_lens',
]
```

2. Add the following lines to your MIDDLEWARE setting:
```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    ...
    'drf_api_lens.middleware.ErrorCapturingMiddleware',
]
```
This will enable the ErrorCapturingMiddleware to capture errors that occur during API request execution.

3. Run following command ```python manage.py migrate```

4. Add setting.py ```STORE_CAPTURE_ERROR_TO_DATABASE: If set to True, captured errors will be stored in the database. The default value is False.```



## Usage

#### ErrorCapture model is used to capture and store error-related information for analysis and debugging purposes.
> **user**: CharField with a maximum length of 256 characters. This field is optional and may be left blank. It is used to store the username or email or identifier of the user who triggered the error.

> **url_requested**: CharField with a maximum length of 1024 characters. This field is optional and may be left blank. It is used to store the URL that was requested when the error occurred.

> **request_headers**: TextField. This field is optional and may be left blank. It is used to store the HTTP headers that were sent with the request.

> **request_body**: TextField. This field is optional and may be left blank. It is used to store the request body that was sent with the request.

> **query_params**: TextField. This field is optional and may be left blank. It is used to store the query parameters that were sent with the request.

> **request_method**: CharField with a maximum length of 8 characters. This field is optional and may be left blank. It is used to store the HTTP method that was used for the request (e.g. GET, POST, etc.).

> **ip_address**: CharField with a maximum length of 50 characters. This field is optional and may be left blank. It is used to store the IP address of the client that made the request.

> **response_body**: TextField. This field is optional and may be left blank. It is used to store the response body that was sent back by the server.

> **response_status_code**: PositiveSmallIntegerField. This field is optional and may be left blank. It is used to store the HTTP status code that was returned by the server.

> **execution_time**: DecimalField with 5 decimal places and a maximum of 8 digits. This field is optional and may be left blank. It is used to store the time (in seconds) that it took for the server to process the request and generate a response.

Additionally, you can mention any other relevant details about the model, such as the fact that it inherits from TimeStampModel and includes the **created_at** and **updated_at** fields. You could also provide information about the Meta class and the db_table attribute, which specifies the name of the database table that will be used to store instances of the model.

**NOTE**: The ErrorCapture model only stores information for requests that return HTTP status codes other than HTTP_200_OK, HTTP_201_CREATED, HTTP_202_ACCEPTED, HTTP_203_NON_AUTHORITATIVE_INFORMATION, HTTP_204_NO_CONTENT, HTTP_205_RESET_CONTENT, HTTP_206_PARTIAL_CONTENT, HTTP_207_MULTI_STATUS, HTTP_208_ALREADY_REPORTED, or HTTP_226_IM_USED. Requests that return any of these status codes are considered successful and are not captured by this model.


## ErrorCapturingMiddleware
The ErrorCapturingMiddleware is a middleware that captures any error that occurs during API request execution. If an error occurs, it will be logged to the console and optionally saved to the database if the STORE_CAPTURE_ERROR_TO_DATABASE setting is True.


## @capture_error decorator
The drf_api_lens package provides the capture_error decorator to handle exceptions that occur during view function execution.


Here is an example usage of the capture_error decorator in a class-based view:
```
from drf_api_lens.decorators import capture_error

class MyAPIView(APIView):
    @capture_error()
    def post(self, request, *args, **kwargs):
        # Your code here
```

The decorator is a tool that helps handle errors that occur during the post method's execution. If an error occurs, it will provide a response that includes a message with the name of the file and line number where the error occurred. The message will also include the name of the function in which the error occurred, along with the error message itself.

Here is an example of what the response might look like:
```
{
    "error": true,
    "data": [],
    "message": "An error occurred in file '/home/../../../api_v1/views.py' at line 47: 'name 'test' is not defined' in function 'testing'"
}
```

## validate_api_parameters parameter
The validate_api_parameters parameter is an optional parameter for the capture_error decorator that checks if the required parameters are present in the API request data. If the parameters are not present, the package returns an error response.

Here's an example of how to use the validate_api_parameters parameter:
```
from drf_api_lens.decorators import capture_error

class MyAPIView(APIView):
    @capture_error(validate_api_parameters=['name', 'email'])
    def post(self, request, *args, **kwargs):
        # Your code here
```

If the name and email parameters are not present in the API request data, the capture_error decorator will return an error response with the message "Missing parameters: name, email".
like this:
If the required parameters are not present in the API request data, the package will return an error response:
```
{
    "error": True,
    "data": [],
    "message": "Missing parameters: name, email"
}
```

## Conclusion
The drf_api_lens package provides a middleware, decorator, and optional settings to capture errors in Django REST framework (DRF) APIs. The package provides the ErrorCapturingMiddleware to catch any error that occurs during the execution of an API request, and the capture_error decorator to handle exceptions that occur during view function execution. The package also provides a validate_api_parameters parameter that checks if the required parameters are present in the API request data. If the parameters are not present, the package returns an error response.


