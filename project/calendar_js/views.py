# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render
from django.template import RequestContext
from django.shortcuts import get_object_or_404, render_to_response, redirect
from django.http.response import HttpResponse
import datetime
import json
# from django.utils import simplejson
from project.core.models import Purchase, PurchaseStatus, PurchaseStatusLinks
from project.accounts.models import OrganizerProfile
from project.cart.models import CartItem, Product


# Create your views here.
def calendarView(request, template_name="catalog/index.html"):
    if request.method == 'POST':
        text = "%s" % request.POST['text']
        purchase = Purchase.objects.get(name=text)
        status_link = PurchaseStatusLinks.objects.filter(purchase=purchase.id).get(active=True)
        status = status_link.status
        html_title = u"Инфо: %s" % text
        html_date = u"<h4>%s</h4> <strong>начало:</strong> %s <br/> <strong>конец:</strong> %s" % (status.status_name, status_link.date_start, status_link.date_end)
        html_href = u"%s" % purchase.url_core()
        html_body = u"<p><strong>Комментарий к статусу:</strong><br/> %s</p>" % status_link.data

        items = set(CartItem.objects.select_related().filter(user=request.user))
        p_set = set()
        list_html = u''
        for item in items:
            current_purchase = item.product.catalog.catalog_purchase
            if current_purchase == purchase:
                p_set.add(item)
                list_html += u"<p>%s, %s шт. - цена: <strong>%s р.</strong></p>" % (item.product.product_name, item.quantity, item.product.price)

        html_items = u""
        data = json.dumps({
            "html_title": html_title,
            "html_date": html_date,
            "html_href": html_href,
            "html_body": html_body,
            "list_html": list_html,
        })
        return HttpResponse(data, mimetype="application/json")
    else:
        items = set(CartItem.objects.filter(user=request.user))
        statuses = set()
        for item in items:
            current_purchase = item.product.catalog.catalog_purchase
            try:
                curr_stat = PurchaseStatusLinks.objects.filter(purchase=current_purchase.id).get(active=True)
                statuses.add(curr_stat)
            except PurchaseStatusLinks.DoesNotExist:
                pass
        statuses_list = []
        for status in statuses:
            # status.eventdate_start = datetime.datetime(status.date_start.year, status.date_start.month, status.date_start.day,
            #                               status.date_start.hour, status.date_start.minute)
            # status.eventdate_end = datetime.datetime(status.date_end.year, status.date_end.month, status.date_end.day,
            #                               status.date_end.hour, status.date_end.minute)
            status.eventdate_start = status.date_start
            status.eventdate_end = status.date_end
            statuses_list.append(
                {
                    'title': "%s" % status.purchase.name,
                    'start': status.eventdate_start.isoformat(),
                    'end': status.eventdate_end.isoformat(),
                    # 'color': "yellow",
                    # 'url': "/purchase-%s" % status.purchase.id,
                }
            )
        statuses_json = json.dumps(statuses_list)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))