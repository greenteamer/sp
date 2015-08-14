# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from project.core.models import Category
from project.accounts.models import OrganizerProfile
register = template.Library()


@register.inclusion_tag("client/tags/client_category_list.html")
def client_categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.filter(is_active=True) }


@register.inclusion_tag("client/tags/client_sidebar.html")
def client_sidebar(request):
	"""Возвращает дерево категорий"""
	return {'organizers': OrganizerProfile.objects.filter(organizer_checked=True) }
