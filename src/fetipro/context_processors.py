# encoding=utf-8
from django.conf import settings

def ga(request):
    return {
            "GA_TRACKING_CODE":settings.GA_TRACKING_CODE
            }

