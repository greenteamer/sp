# -*- coding: utf-8 -*-
from project import settings

def settings_processor(request):
    return {
        'server': settings.SERVER
    }
