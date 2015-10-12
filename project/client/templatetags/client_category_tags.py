# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from project.core.models import Category
from project.core import mobile
from project.accounts.models import OrganizerProfile
register = template.Library()


@register.inclusion_tag("client/tags/client_category_list.html")
def client_categories_tree(request):
	"""Возвращает дерево категорий"""
	device = check_device(request)
	return {
		'nodes': Category.objects.filter(is_active=True),
		'device': device
	 }


@register.inclusion_tag("client/tags/client_sidebar.html")
def client_sidebar(request):
	"""Возвращает дерево категорий"""
	return {'organizers': OrganizerProfile.objects.filter(organizer_checked=True) }

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
    return device
