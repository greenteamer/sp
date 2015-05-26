from django.shortcuts import render_to_response
from django.template import RequestContext
from project.notifications.forms import NoticeForm


def noticeFormView(request, template_name):
    JobForm = NoticeForm()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def noticeAllView(request, template_name):
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
