# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from project.documentation.models import Documentation
from project.accounts.models import getProfile
from project.cart.cart import get_cart_items
from project.notifications.functions import get_notifications


def docView(request, template_name):
    docs = Documentation.objects.all()
    user = request.user
    if user.is_authenticated():
        profile = getProfile(user)
        # try:
        #     try:
        #         test_profile = user.memberprofile
        #     except:
        #         test_profile = user.organizerprofile
        # except:
        #     test_profile = None
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))