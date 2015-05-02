# encoding=utf-8
from django.conf import settings
from fetipro.master.models import Feti

def ga(request):
    return {
            "GA_TRACKING_CODE":settings.GA_TRACKING_CODE
            }


def unauthorized_feties(request):
    return {
            "unauthorized_feties":Feti.objects.filter(status=Feti.Status.Unauthorided).order_by("parent__ordering", "parent__id", "id")
            }
