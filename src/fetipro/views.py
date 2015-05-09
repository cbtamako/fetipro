# encoding=utf-8
import itertools
from django.shortcuts import render, redirect, get_object_or_404
from fetipro.master.models import Feti
from fetipro.user.models import UserFeti, User
from django.contrib.auth.decorators import login_required
from collections import OrderedDict
from fetipro.user.forms import UserFetiForm
from django.contrib import messages
from django.contrib.auth import logout as django_logout
from django.http.response import Http404, HttpResponseRedirect
from fetipro.master.forms import FetiForm


def index(request):
    if request.user.is_authenticated():
        return redirect("feties")

    return render(request, "index.html")

def logout(request):
    if request.user.is_authenticated():
        django_logout(request)
        messages.success(request, "ログアウトしました")

    return redirect("index")


@login_required
def mypage(request):
    return render(request, "mypage.html")

def feties(request, username=None, is_edit=False):

    if not username:
        if request.user.is_authenticated():
            return redirect("user_feties", username=request.user.username)
        raise Http404

    if is_edit and username != request.user.username:
        raise Http404

    user = get_object_or_404(User, username=username)

    feties = OrderedDict()
    user_feties = dict(map(lambda uf:(uf.feti, uf), UserFeti.objects.filter(user=user).select_related("feti")))

    def get_user_feti_form(feti):
        if feti in user_feties:
            user_feti = user_feties[feti]
        else:
            user_feti = UserFeti(user=user, feti=feti)

        if request.method == "POST" and str(feti.id) in request.POST.getlist("feties"):
            return UserFetiForm(request.POST, instance=user_feti)

        return UserFetiForm(instance=user_feti)

    posted_forms = []

    for feti in Feti.objects.filter(parent__isnull=True, status=Feti.Status.Authorized).prefetch_related("children"):
        children = list(filter(lambda f: f.status == Feti.Status.Authorized, feti.children.all()))
        children.insert(0, feti)

        for child in children:
            child.form = get_user_feti_form(child)
            if child.form.is_bound:
                posted_forms.append(child.form)

        feties[feti] = children


    if request.method == "POST":
        if all([f.is_valid() for f in posted_forms]):

            for f in posted_forms:
                if f.changed_data:
                    f.save()
            messages.success(request, "保存しました")
            return redirect("feties")
        else:
            messages.warning(request, "エラーが発生しました")

    context = {
               "current_user":user,
               "is_edit":is_edit,
               "feties":feties,
               }

    return render(request, "feties.html", context)


@login_required
def edit_feties(request):
    return feties(request, username=request.user.username, is_edit=True)

@login_required
def add_feti(request):
    form = FetiForm()

    if request.method == "POST":
        form = FetiForm(request.POST, request.FILES)
        print(request.FILES)
        if form.is_valid():
            form.save(user=request.user)
            messages.success(request, "申請ありがとうございます")
            return HttpResponseRedirect("")

    context = {
               "form":form
               }
    return render(request, "feti_form.html", context)

@login_required
def authorize_feti(request):
    if not request.user.can_authorize:
        messages.warning(request, "権限がありません")
        return redirect("add_feti")

    feties = Feti.objects.filter(status=Feti.Status.Unauthorided).order_by("parent__ordering", "parent__id", "id")

    if request.method == "POST":
        feti_id = request.POST.get("feti")
        action = request.POST.get("action")

        try:
            feti = feties.get(id=feti_id)
            if action == "authorize":
                feti.status = Feti.Status.Authorized
                feti.authorized_by = request.user
                feti.save()
                messages.success(request, "{0} を承認しました".format(feti.name))
            elif action == "ignore":
                feti.status = Feti.Status.Ignored
                feti.authorized_by = request.user
                feti.save()
                messages.success(request, "{0} を却下しました".format(feti.name))
            else:
                raise ValueError("Invalid action")

            return HttpResponseRedirect("")

        except Feti.DoesNotExist:
            messages.error(request, "エラーが発生しました")

    context = {
               "feties":feties,
               }
    return render(request, "feti_authorize.html", context)
