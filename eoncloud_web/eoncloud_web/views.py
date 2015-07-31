#-*-coding=utf-8-*-
from django.conf import settings
from django.shortcuts import render_to_response, render, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout

from biz.account.models import Notification
from django.http import HttpResponseRedirect, JsonResponse
from django.core.urlresolvers import reverse
from biz.idc.models import DataCenter, UserDataCenter as UDC
from biz.account.models import UserProfile
from cloud.tasks import link_user_to_dc_task

from eoncloud_web.decorators import superuser_required


def index(request, template_name="index.html"):
    return render_to_response(template_name, RequestContext(request, {}))


@login_required
def cloud(request, template_name="cloud.html"):
    return render_to_response(template_name, RequestContext(request, {}))


@superuser_required
def management(request):
    return render(request, 'management.html', {'inited': DataCenter.objects.exists()})


def login(request, template_name="login.html"):

    if request.method == "GET":
        authenticationForm = AuthenticationForm()
    elif request.method == "POST":
        # try:
        #     old_user = User.objects.get(username=request.POST.get("username", ''))
        # except User.DoesNotExist:
        #     old_user = None

        authenticationForm = AuthenticationForm(data=request.POST)
        if authenticationForm.is_valid():
            user = authenticationForm.get_user()
            # if backend is LDAPBackend and local no exist user create localuser data_center
            # if 'LDAPBackend' in user.backend and not old_user:
            #     ldap_auth_local_user_create(user)

            auth_login(request, user)

            if user.is_superuser:
                return redirect('management')

            ucc = UDC.objects.filter(user=user)
            if ucc:
                request.session["UDC_ID"] = ucc[0].id
            else:
                raise Exception("User has not register to any SDDC")

            Notification.pull_announcements(user)

            return HttpResponseRedirect(reverse("cloud"))

    return render_to_response(template_name, RequestContext(request, {
        "authenticationForm": authenticationForm,
        "error": authenticationForm.errors.get('__all__', None),
        "BRAND": settings.BRAND,
        "ICP_NUMBER": settings.ICP_NUMBER,
        "LDAP_AUTH_ENABLED": settings.LDAP_AUTH_ENABLED
    }))


def logout(request):
    auth_logout(request) 
    return HttpResponseRedirect(reverse("index"))


def current_user(request):
    if request.user.is_authenticated():

        if request.user.is_superuser:
            return JsonResponse({'result': {'logged': True}, 'user': request.user.username})

        udc_id = request.session["UDC_ID"]
        data_center_names = DataCenter.objects.filter(userdatacenter__pk=udc_id)
        cc_name = data_center_names[0].name if data_center_names else u'N/A'

        return JsonResponse({'result': {'logged': True},
                            'user': request.user.username,
                            'datacenter': cc_name})
    else:
        return JsonResponse({'result': {'logged': False}})


def ldap_auth_local_user_create(ldap_user):
    if ldap_user:
        UserProfile.objects.create(user=ldap_user,
                                   user_type=2)

        link_user_to_dc_task(ldap_user, DataCenter.get_default())
        return ldap_user
    else:
        return None
