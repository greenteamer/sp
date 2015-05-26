# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.notifications.models import Notification


def get_notifications(user):
    text = str(user.id)+','
    notifications = Notification.objects.filter(users_list__icontains=text)
    return notifications