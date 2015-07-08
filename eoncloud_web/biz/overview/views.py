#-*-coding-utf-8-*-

from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from biz.account.models import Contract
from biz.idc.models import DataCenter
from biz.instance.models import Instance, Flavor
from biz.image.models import Image


@api_view(["GET"])
def summary(request):
    return Response({"user_num": User.objects.filter(is_superuser=False).count(),
                     "instance_num": Instance.objects.filter(deleted=False).count(),
                     "flavor_num": Flavor.objects.count(),
                     "data_center_num": DataCenter.objects.count(),
                     "contract_num": Contract.objects.filter(deleted=False).count(),
                     "image_num": Image.objects.count()})


@api_view(["POST"])
def init(request):
    data_center_params = _extract_fields(request.data, 'data_center_name', 'host', 'project',
                                         'user', 'password', 'auth_url', 'ext_net')
    flavor_params = _extract_fields(request.data, 'flavor_name', 'cpu', 'memory', 'price')
    image_params = _extract_fields(request.data, 'image_name', 'os_type', 'login_name')

    data_center = DataCenter.objects.create(**data_center_params)

    Flavor.objects.create(**flavor_params)

    image_params['data_center'] = data_center
    Image.objects.create(**image_params)

    return Response({'success': True,
                     "msg": _('Cloud has been initialized!')},
                    status=status.HTTP_201_CREATED)


def _extract_fields(data, name_field, *keys):

    result = {'name': data[name_field]}

    for key in keys:
        result[key] = data[key]

    return result