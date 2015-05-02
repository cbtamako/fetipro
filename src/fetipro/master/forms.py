# encoding=utf-8

from django import forms
from fetipro.master.models import Feti

class FetiForm(forms.ModelForm):

    class Meta:
        model = Feti
        fields = ("parent", "name", "slug", "icon")


    def __init__(self, *args, **kwargs):
        super(FetiForm, self).__init__(*args, **kwargs)
        self.fields['parent'].queryset = Feti.objects.filter(parent__isnull=True, status=Feti.Status.Authorized)
        self.fields['parent'].required = True
        self.fields['parent'].widget.attrs["class"] = "form-control"
        self.fields['name'].widget.attrs["class"] = "form-control"
        self.fields['name'].widget.attrs["placeholder"] = "くすぐり"
        self.fields['slug'].widget.attrs["class"] = "form-control"
        self.fields['slug'].widget.attrs["placeholder"] = "tickle"
        self.fields['icon'].widget.attrs["class"] = "form-control"


    def save(self, commit=True, user=None):
        instance = super(FetiForm, self).save(commit=False)

        if user:
            instance.created_by = user

        if commit:
            instance.save()
            self.save_m2m()

        return instance

