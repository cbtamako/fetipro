# encoding=utf-8

from django import forms
from fetipro.user.models import UserFeti


class UserFetiForm(forms.ModelForm):

    class Meta:
        model = UserFeti
        fields = ("rating",)

    RATING_CHOICES = (
                      (0, "0%"),
                      (25, "25%"),
                      (50, "50%"),
                      (75, "75%"),
                      (100, "100%")
                      )
    rating = forms.TypedChoiceField(RATING_CHOICES, required=True, coerce=int)

    def __init__(self, *args, **kwargs):
        kwargs["prefix"] = "uf_{0}".format(kwargs["instance"].feti.id)
        super(UserFetiForm, self).__init__(*args, **kwargs)
