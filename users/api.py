# -*- coding: utf-8 -*-
#


from rest_framework.pagination import LimitOffsetPagination
from rest_framework_bulk import BulkModelViewSet

from users.serializers import UserSerializer, UserGroupSerializer

from users.models import User, UserGroup
from users.permissions import IsSuperUser
from users.mixins import IDInFilterMixin


class UserViewSet(IDInFilterMixin, BulkModelViewSet):
    '''
    用户的操作接口
    '''
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperUser,)
    filter_fields = ('username', 'email', 'name', 'phone', 'date_expired')
    search_fields = filter_fields


class UserGroupViewSet(IDInFilterMixin, BulkModelViewSet):
    '''
    用户组的操作接口
    '''
    queryset = UserGroup.objects.all()
    serializer_class = UserGroupSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsSuperUser,)
    search_fields = ('name', 'comment')
