# encoding=utf-8

from django import forms
from fetipro.user.models import UserFeti


class UserFetiForm(forms.ModelForm):

    class Meta:
        model = UserFeti
        fields = ("status",)

    STATUS_CHOICES = (
                      (UserFeti.Status.No, "いいえ"),
                      (UserFeti.Status.Yes, "はい"),
                      )
    status = forms.TypedChoiceField(STATUS_CHOICES, required=True, coerce=int)

    def __init__(self, *args, **kwargs):
        kwargs["prefix"] = "uf_{0}".format(kwargs["instance"].feti.id)
        super(UserFetiForm, self).__init__(*args, **kwargs)


