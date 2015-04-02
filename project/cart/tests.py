# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from models import CartItem
from django.contrib.auth.models import User
from project.core.views import getProfile

class CartTest(TestCase):
    # fixtures = ['auth.xml', 'accounts.xml', 'core.xml']
    # fixtures = ['fixtures.xml']
    fixtures = ['accounts/fixtures/data.json']

    def def_pushToCart(self):
        users = User.objects.all()
        for user in users:
            client = Client()
            client.login(username=user.username, password='balabas')
            # response = client.get('/purchase-1/catalog-1/product-1/')
            response = client.post('/purchase-1/catalog-1/product-1/', {'quantity': 1, 'product':1,})
            profile = getProfile(user)
            if hasattr(profile, 'member_checked') and profile.is_checked():
                assert (response.status_code==200)
        print u'Проверенный участник может добавлять товар'

            # product = Product.objects.get(id=1)
            # cart_item = CartItem.objects.create(
            #     cart_id=_cart_id(request),
            #     date_added = datetime.datetime.now(),
            #     quantity = random.randrange(1,10,1),
            #     product = product,
            # )
            # cart_item.save()

    def test_getCartItems(self):
        self.def_pushToCart()
        cart_items = CartItem.objects.all()
        for item in cart_items:
            # print u"%s (%s), %s, %s кол-во:%s" % (item.id, item.product.product_name, item.cart_id, item.date_added, item.quantity)
            print u'продукт %s в корзине' % item.name()
    # def def_createOrganizerProfile(self, username, checked=False):
    #     self.user = User.objects.create(username=username,)
    #     self.user.set_password("balabas")
    #     profile = OrganizerProfile.objects.create(
    #         user=self.user,
    #         email="%s@mail.ru" % self.user.username,
    #         phone="8913888689%s" % self.user.id,
    #         firstName="Орган%s" % self.user.id,
    #         lastName="Изатор%s" % self.user.id,
    #         address="Ленина %s" % self.user.id,
    #         city="Северск%s" % self.user.id,
    #         zipCode="63607%s" % self.user.id,
    #         organizer_checked = checked,
    #         icon="accounts/images/maksimov.jpg",
    #         )
    #     self.user.save()
    #     return self.user



    # def test_allUsers(self):
    #     users = User.objects.all()
    #     for user in users:
    #         client = Client()
    #
    #         urls = self.def_AccountUrls()
    #         for url in urls:
    #             # крэш для незалогиненного пользователя
    #             response = client.get(reverse(url))
    #             if url=='profileView' or url=='populateProfileView':
    #                 assert (response.status_code==302)
    #             else:
    #                 assert (response.status_code==200)
    #             # крэш для залогиненного пользователя
    #             is_login = client.login(username=user.username, password="balabas")
    #             response = client.get(reverse(url))
    #             assert (response.status_code == 200 and is_login)
    #             if urls.index(url)+1 == len(urls):
    #                 print u"Accounts Urls проверены для пользователя %s" % user.username
    #
    #         """проверка что организатор может просматривать и добавлять закупки
    #         проверка что все кроме проверенных организаторов редиректятся """
    #         for url in self.def_OrganizerUrls():
    #             response = client.get(url)
    #             profile = getProfile(user)
    #             if hasattr(profile, 'organizer_checked') and profile.is_checked():
    #                 assert (response.status_code==200)
    #             elif hasattr(profile, 'organizer_checked') and not profile.is_checked():
    #                 assert (response.status_code==302)
    #             elif hasattr(profile, 'member_checked'):
    #                 assert (response.status_code==302)
    #             else:
    #                 assert (response.status_code==302)
    #
    #         """проверка что только владелец может глядеть
    #         на свои закупки и редактировать их"""
    #         for url in self.def_OwnerUrls():
    #             response = client.get(url)
    #             profile = getProfile(user)
    #             if hasattr(profile, 'organizer_checked') and profile.is_checked():
    #                 if Purchase.objects.get(id=url[28]) in profile.purchase_set.all():
    #                     assert (response.status_code==200)
    #                 else:
    #                     # print u"%s, url %s, status: %s" % (user.username, url, response.status_code)
    #                     assert (response.status_code==302)
    #             elif hasattr(profile, 'organizer_checked') and not profile.is_checked():
    #                 assert (response.status_code==302)
    #             elif hasattr(profile, 'member_checked'):
    #                 assert (response.status_code==302)
    #             else:
    #                 assert (response.status_code==302)
    #
    #         """проверка что только проверенный пользователь
    #          может гулять по core ссылкам"""
    #         for url in self.def_CoreUrls():
    #             response = client.get(url)
    #             profile = getProfile(user)
    #             if profile.is_checked():
    #                 assert (response.status_code==200)
    #             elif not profile.is_checked():
    #                 assert (response.status_code==302)
    #             else:
    #                 assert (response.status_code==302)
    #
    #         response = self.client.post(reverse('loginView'), {'username': user.username, 'password': 'balabas'})
    #         assert (response.status_code==302)
    #
    #     print "все пользователи залогинились"
    #
    #     client = Client()
    #     list_urls = self.def_OrganizerUrls()
    #     list_urls.extend(self.def_OwnerUrls())
    #     for url in list_urls:
    #         # крэш по ссылкам организатора для незалогиненного пользователя
    #         # каждая страница должна вывести 302 редирект на регистрацию
    #         response = client.get(url)
    #         assert (response.status_code==302)
    #     print u"Аноним Пользователь редиректится по ссылкам организатора успешно"
    #
    #     response = self.client.post(reverse('registrationView'), {'username': "testReg", 'email': 'aksdhf@sdfsd.ru', 'password1': 'balabas', 'terms': 'on'})
    #     assert (response.status_code==302)  #успешная регистрация




