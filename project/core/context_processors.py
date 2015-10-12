# -*- coding: utf-8 -*-
from project import settings
from project.core import mobile


def settings_processor(request):
    return {
        'server': settings.SERVER
    }


def check_device(request):
    # определение устройства
    user_agent = request.META.get("HTTP_USER_AGENT")
    http_accept = request.META.get("HTTP_ACCEPT")
    device = ''
    if user_agent and http_accept:
        agent = mobile.UAgentInfo(userAgent=user_agent, httpAccept=http_accept)
        if agent.detectTierIphone():
            device = 'mobile'
        if agent.detectMobileQuick():
            device = 'mobile'
        if agent.detectTierTablet():
            device = 'tablet'

    return {
        'user_agent': user_agent,
        'http_accept': http_accept,
        'agent': agent,
        'device': device
    }
