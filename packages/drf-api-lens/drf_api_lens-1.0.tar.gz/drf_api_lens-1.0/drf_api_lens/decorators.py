from rest_framework.response import Response
from rest_framework import status
from drf_api_lens.validators import RequiredParameterValidator
from drf_api_lens.utils import ErrorAnalysis

def capture_error(validate_api_parameters=[]):
    """
    This decorator capture errors and validates API parameters before allowing access to the decorated view function.
    It can be used by adding @capture_error(validate_api_parameters=["param1", "param2"]) above a view function.
    The decorator takes an optional argument, validate_api_parameters, which is a list of required API parameters.
    """

    def decorator(view_func):
        def wrapper(self, request, *args, **kwargs):
            try:
                if validate_api_parameters:
                    validator = RequiredParameterValidator(
                        request, validate_api_parameters
                    )
                    is_valid, missing_parameters = validator.validate()
                    if not is_valid:
                        return Response(
                            data={
                                "error": True,
                                "data": [],
                                "message": f"Missing parameters: {', '.join(missing_parameters)}",
                            },
                            status=status.HTTP_406_NOT_ACCEPTABLE,
                        )
                return view_func(self, request, *args, **kwargs)

            except Exception as exception:
                error_message = ErrorAnalysis.detect_error(exception)
                return Response(
                    status=status.HTTP_406_NOT_ACCEPTABLE,
                    data={
                        "error": True,
                        "data": [],
                        "message": error_message,
                    },
                )

        return wrapper

    return decorator
