# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from project.core.models import Category

register = template.Library()

@register.inclusion_tag("core/tags/category_list.html")
def categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.filter(is_active=True) }



