# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.shortcuts import render, get_object_or_404, render_to_response, redirect
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from project.accounts.models import getProfile, OrganizerProfile, MemberProfile
from project.core.models import Purchase, Product, Promo, Catalog, Category, PurchaseQuestion, PurchaseAnswer
from project.cart.models import CartItem
from project.cart.forms import CartItemForm
from project.documentation.models import Page
from project.cart import cart
from project.helpers import check_profile
from project.cart.cart import add_to_cart
from project.accounts.forms import propertyForm, clientPropertyForm
import json
from django.contrib.auth.models import User

# rest
from rest_framework import serializers, viewsets, generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import detail_route, list_route
from serializers import PurchaseSerializer, OrganizerSerializer, PromoSerializer, CategorySerializer, ProductSerializer, CatalogSerializer, BenefitsSerializer, QuestionsSerializer, AnswersSerializer, UserSerializer

# переменная сервер нужна для подключения разных js и css файлов в 
# зависимости от сервера (develop или production)
from project.settings import ADMIN_EMAIL, SERVER 
from django.core.mail import send_mail

from django.db import connection, connections



# Просмотр каталога
@check_profile
def clientAddToCartView(request):
    if 'ajax' in request.POST:
        ajax = request.POST['ajax']

        if ajax == 'add_to_cart':
            # Добавление в корзину по аяксу
            product = Product.objects.get(id=request.POST['product'])
            list_properties = product.property.split(';')
            try:
                list_properties.index(request.POST['product_properties'])
                add_to_cart(request)    # Добавление в корзину
                data = json.dumps({
                    'name': product.product_name
                })
                return HttpResponse(data, content_type="application/json")
            except Exception:
                pass


def indexView(request, template_name="client/pages/index.html"):    
    server = SERVER
    big_content_purchase = Purchase.objects.get(id=2)  # TODO: сделать вывод нормальной закупки
    main_content_purchase = big_content_purchase  # TODO: сделать вывод нормальной закупки
    # создание формы свойств товара
    main_content_purchase.catalogs = main_content_purchase.get_catalogs()
    for catalog in main_content_purchase.catalogs.all():
        catalog.products = catalog.get_products()
        for product in catalog.products.all():
            product.form = clientPropertyForm(catalog.id)

    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchase.products = set()
        catalogs = purchase.get_catalogs()
        for catalog in catalogs:
            purchase.products.update(catalog.get_products())
        purchase.products = list(purchase.products)[:3]

    # if request.method == 'POST':
    #     """Добавляем товар в корзину
    #     используем стндартную форму для добавления товара
    #     котору мы дополучаем раньше для каждого товара"""
    #     product = Product.objects.get(id=request.POST['product'])
    #     product_properties = product.property   # все возможные свойства Этого товара
    #     if request.POST['product_properties'] in product_properties and request.POST['product_properties'] != '':
    #         # если выбранные св-ва есть в товаре
    #         cart_item = CartItem(product=product)
    #         form = CartItemForm(request.POST or None, instance=cart_item)
    #         if form.is_valid():
    #             cart_item = add_to_cart(request)    # Добавление в корзину

    if request.method == 'POST' and 'subscribe' in request.POST:
        subject = u'Заявка на подписку baybox.ru'
        message = u'почта: %s' % request.POST['email']
        send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# вьюхи для пустых страниц ract
# шаблоны содержат div куда рендериться react
def clientCategoryView(request, category_slug, template_name="client/pages/category.html"):
    server = SERVER
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def clientProductView(request, id, template_name="client/pages/product.html"):
    server = SERVER
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


def clientPurchaseView(request, id, template_name="client/pages/purchase.html"):
    server = SERVER
    return render_to_response(template_name, locals(), context_instance=RequestContext(request))


@check_profile
def catalogView(request, template_name="client/pages/catalog.html"):
    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchase.products = set()
        catalogs = purchase.get_catalogs()
        for catalog in catalogs:
            purchase.products.update(catalog.get_products())
        purchase.products = list(purchase.products)[:3]

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def getAllPurchases(request):

    purchases_list = []
    purchases = Purchase.objects.all()
    for purchase in purchases:
        purchases_list.append({
            'name': purchase.name,
            'description': purchase.description
        })
    purchases = json.dumps(purchases_list)

    return HttpResponse(purchases, content_type="application/json")


# rest_framework

class PurchasesViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer


class OrganizersViewSet(viewsets.ModelViewSet):
    queryset = OrganizerProfile.objects.all()
    serializer_class = OrganizerSerializer


class PopularPromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.filter(alias='popular-promo')
    serializer_class = PromoSerializer


class NewPromoViewSet(viewsets.ModelViewSet):
    queryset = Promo.objects.filter(alias='new-promo')
    serializer_class = PromoSerializer


class ProductsViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CatalogsViewSet(viewsets.ModelViewSet):
    queryset = Catalog.objects.all()
    serializer_class = CatalogSerializer


class HotPurchasesViewSet(viewsets.ModelViewSet):
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        purchases = []
        for purchase in Purchase.objects.all():
            if purchase.get_current_status().id == 5:
                purchases.append(purchase)

        return purchases


class SearchViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]

    def dictfetchall(self, cursor):
        "Return all rows from a cursor as a dict"
        desc = cursor.description
        return [
            dict(zip([col[0] for col in desc], row))
            for row in cursor.fetchall()
        ]

    @list_route()
    def purchases(self, request, **kwargs):
        result = Purchase.objects.all()
        escape_query = '%'+request.query_params["query"]+'%'
        print escape_query
        cursor = connection.cursor()
        # cursor.execute("SELECT distinct(product_id), purchase_id, catalog_id from megaview where product_name LIKE %s OR LIKE category_name %s OR LIKE purchase_name %s OR LIKE catalog_name %s", [escape_query, escape_query, escape_query, escape_query])
        cursor.execute("SELECT distinct(product_id), purchase_id, catalog_id from megaview where product_name LIKE %s OR category_name LIKE %s OR purchase_name LIKE %s OR catalog_name LIKE %s", [escape_query, escape_query, escape_query, escape_query])
        result_sql = self.dictfetchall(cursor)
        # tree_id =
        # cursor.execute("SELECT distinct(product_id), purchase_id, catalog_id from megaview where ", [tree_id, level])
        data = json.dumps(result_sql)
        # print result_sql
        # получить id закупок
        # list_purchases_id = []
        # for dict in result_sql:
        #     for key, value in dict.items():
        #         if key == 'purchase_id':
        #             list_purchases_id.append(value)
        # list_prod_id = []
        # for dict in result_sql:
        #     for key, value in dict.items():
        #         if key == 'product_id':
        #             list_prod_id.append(value)
        # try:
        #     result = Purchase.objects.filter(id__in=list_purchases_id)
        #     # print result
        # except:
        #     pass
        # self.queryset = result
        # serializer = PurchaseSerializer(instance=self.queryset, many=True)
        # result_data = serializer.data

        # return Response(result_sql)
        return HttpResponse(data, content_type="application/json")


class CategoriesViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    @list_route()
    def first_category(self, request, **kwargs):
        """тестовый метод вызывается через /api/v1/categories/first_category/ ...
        тез каких либо дополнительных записей в urls"""
        self.queryset = Category.objects.filter(id=2)
        serializer = CategorySerializer(instance=self.queryset, many=True)
        return Response(serializer.data)


def getCartItems(request):
    items = []
    cart_items = CartItem.objects.filter(user=request.user.id)
    for item in cart_items:
        items.append({
            'product_id': item.product.id,
            'name': item.product.product_name,
            'image': "/media/%s" % item.product.get_image().image,
            'properties': item.properties,
            'price': item.product.price,
            'quantity': item.quantity
        })
    data = json.dumps(items)
    return HttpResponse(data, content_type="application/json")


class BenefitsViewSet(viewsets.ModelViewSet):
    queryset = Page.objects.filter(is_benefits=True)
    serializer_class = BenefitsSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    queryset = PurchaseQuestion.objects.all()
    serializer_class = QuestionsSerializer


class AnswersViewSet(viewsets.ModelViewSet):
    queryset = PurchaseAnswer.objects.all()
    serializer_class = AnswersSerializer


# добавление вопроса без использования REST (нужно исправить)
def pushQuestion(request):
    question = PurchaseQuestion()
    question.user = User.objects.get(id=request.POST['user'])
    question.purchase = Purchase.objects.get(id=request.POST['purchase'])
    question.text = request.POST['text']
    try:
        question.product = Product.objects.get(id=request.POST['product'])
    except:
        pass
    question.save()

    question_dict = {
        "id": question.id,
        "user": question.user.id,
        "purchase": question.purchase.id,
        "product": None,
        "text": question.text,
        "answers": []
    }
    question_dump = json.dumps(question_dict)
    return HttpResponse(question_dump, content_type="application/json")


def postAnswer(request):
    answer = PurchaseAnswer()
    answer.user = request.user
    answer.question = PurchaseQuestion.objects.get(id=request.POST['id'])
    answer.text = request.POST['text']
    answer.save()

    answer_dict = {
        "id": answer.id,
        "user": answer.user.id,
        "question": answer.question.id,
        "text": answer.text
    }
    answer_dict = json.dumps(answer_dict)
    return HttpResponse(answer_dict, content_type="application/json")


def getOrganizers(request):
    organizers = OrganizerProfile.objects.all()
    organizers_for_dump = []
    for organizer in organizers:
        tmp_user = organizer.user
        organizers_for_dump.append({
            "id": organizer.id,
            "user": organizer.user.id,
            "username": organizer.user.username
        })

    dump = json.dumps(organizers_for_dump)
    return HttpResponse(dump, content_type="application/json")


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @list_route()
    def current_user(self, request, **kwargs):
        """тестовый метод вызывается через /api/v1/users/current_user/ ...
        тез каких либо дополнительных записей в urls"""
        self.queryset = User.objects.filter(id=request.user.id)
        serializer = UserSerializer(instance=self.queryset, many=True)
        return Response(serializer.data)

