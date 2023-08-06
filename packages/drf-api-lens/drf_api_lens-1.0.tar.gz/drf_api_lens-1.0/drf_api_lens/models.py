from django.db import models

# Create your models here.
class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class ErrorCapture(TimeStampModel):
        user = models.CharField(max_length=256,null=True,blank=True)
        url_requested = models.CharField(max_length=1024,null=True,blank=True)
        request_headers = models.TextField(null=True,blank=True)
        request_body = models.TextField(null=True,blank=True)
        query_params = models.TextField(null=True,blank=True)
        request_method = models.CharField(max_length=8,null=True,blank=True)
        ip_address = models.CharField(max_length=50,null=True,blank=True)
        response_body = models.TextField(null=True,blank=True)
        response_status_code = models.PositiveSmallIntegerField(null=True,blank=True)
        execution_time = models.DecimalField(decimal_places=5, max_digits=8,null=True,blank=True)

        class Meta:
                db_table = 'error_capture'