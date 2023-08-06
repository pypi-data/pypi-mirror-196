from drf_api_lens.models import ErrorCapture

class ErrorCaptureOperation:
        """
        The ErrorCaptureOperation class is a Python class that contains a static method called push(). 
        This class is likely used for capturing and logging errors that occur during runtime in an application.
        """
        @staticmethod
        def push(data):
                ErrorCapture.objects.create(**data)