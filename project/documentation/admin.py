# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.documentation.models import Documentation, Page

admin.site.register(Documentation)
admin.site.register(Page)
