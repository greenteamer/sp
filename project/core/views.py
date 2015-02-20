# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect


def homePage(request):
    var1 = 'main.html'
    return render_to_response(var1, {'template_name': var1})