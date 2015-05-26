# -*- coding: utf-8 -*-
from tastypie.resources import ModelResource
from tastypie.authentication import Authentication
from tastypie.authorization import Authorization
from project.notifications.models import Notification


class NotificationResource(ModelResource):
    class Meta:
        queryset = Notification.objects.all()
        resource_name = 'notice'
        allowed_methods = ['post', 'get', 'patch', 'delete']
        # authentication = Authentication()
        # authorization = Authorization()
        always_return_data = True