# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django import template
from project.core.models import Category, Slide
register = template.Library()

def client_slider(context, request):
    return  {
		'slides': Slide.objects.all()
	}
register.inclusion_tag('client/tags/client_slider.html', takes_context=True)(client_slider)
