# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from project.pristroy.models import Category

register = template.Library()

@register.inclusion_tag("pristroy/tags/pristroy_category_list.html")
def pristroy_categories_tree(request):
	"""Возвращает дерево категорий"""
	return {'nodes': Category.objects.all() }

# filter(category_is_active=True)

