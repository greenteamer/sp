# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.contrib import admin
from project.core.models import *

admin.site.register(Product)
admin.site.register(Properties)
admin.site.register(Catalog)
admin.site.register(CatalogProductProperties)
admin.site.register(Category)
admin.site.register(Purchase)
