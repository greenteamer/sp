# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.notifications.models import Notification

admin.site.register(Notification)
