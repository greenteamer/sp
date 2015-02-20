# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response


def index_view(request, template_name="catalog/index.html"):

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
