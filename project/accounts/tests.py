# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
import sys
import re
import random
from django.core import mail
from django_webtest import WebTest
from django.contrib.auth.models import User, Group
from models import OrganizerProfile, MemberProfile, getProfile, Purchase
from project.core.models import PurchaseStatus, Category, Product, Catalog


# Create your tests here.

class OrganizerTest(TestCase):
    # fixtures = ['auth.xml', 'accounts.xml', 'core.xml']
    # fixtures = ['fixtures.xml']
    fixtures = ['data.json']
    client = Client()
    csrf_client = Client(enforce_csrf_checks=True)
    user = User()

    def def_createOrganizerProfile(self, username, checked=False):
        self.user = User.objects.create(username=username,)
        self.user.set_password("balabas")
        profile = OrganizerProfile.objects.create(
            user=self.user,
            email="%s@mail.ru" % self.user.username,
            phone="8913888689%s" % self.user.id,
            firstName="Орган%s" % self.user.id,
            lastName="Изатор%s" % self.user.id,
            address="Ленина %s" % self.user.id,
            city="Северск%s" % self.user.id,
            zipCode="63607%s" % self.user.id,
            organizer_checked = checked,
            icon="accounts/images/maksimov.jpg",
            )
        self.user.save()
        return self.user

    """Создание тестовой закупки"""
    def def_createCategory(self):
        # category = Category.objects.create(
        #     name="Category",
        #     slug="category",
        #     # active=True,
        #     # status_icon="accounts/images/maksimov.jpg",
        #     )
        # category.save()
        status = PurchaseStatus.objects.create(
            status_name="OK",
            status_priority=1,
            # status_icon="accounts/images/maksimov.jpg",
            )
        status.save()
    def def_createPurchase(self, user):
        purchase = Purchase.objects.create(
            name="purchase_%s" % user.username,
            organizerProfile=getProfile(user),
            purchase_status=PurchaseStatus.objects.get(id=1),
            prepay=100,
            percentage=15,
            paymethods="налик",
            )
        purchase.save()
        print u"Закупка url: %s" % Purchase.objects.get(id=1).url()
        catalog = Catalog.objects.create(
            catalog_name="catalog_%s" % user.username,
            catalog_purchase = purchase,
            )
        catalog.save()
        print u"Каталог url: %s" % Catalog.objects.get(id=1).url()
        product = Product.objects.create(
            product_name="product_%s" % user.username,
            description="description",
            price=100.00,
            sku=random.randrange(20,100000,1),
            catalog=catalog,
            )
        product.save()
        print u"Продукт url: %s" % Product.objects.get(id=1).url()

    def def_createMemberProfile(self, username):
        self.user = User.objects.create(username=username)
        self.user.set_password("balabas")
        profile = MemberProfile.objects.create(
            user=self.user,
            email="%s@mail.ru" % self.user.username,
            phone="8913888689%s" % self.user.id,
            firstName="Уча%s" % self.user.id,
            lastName="Стник%s" % self.user.id,
            address="Ленина %s" % self.user.id,
            city="Северск%s" % self.user.id,
            zipCode="63607%s" % self.user.id,
            icon="accounts/images/maksimov.jpg",
            )
        self.user.save()
        return self.user

    def def_AccountUrls(self):
        return ['profileView', 'registrationView', 'loginView', 'logoutView','populateProfileView', ]

    def def_OrganizerUrls(self):
        return [
            '/profile/organizer/purchases/',
            '/profile/organizer/purchase-add/',
        ]

    def def_OwnerUrls(self):
        return [
            '/profile/organizer/purchase-1/',
            '/profile/organizer/purchase-1-edit/',
            '/profile/organizer/purchase-1/catalogs/',
            '/profile/organizer/purchase-1/catalog-add/',
            '/profile/organizer/purchase-1/catalog-1/',
            '/profile/organizer/purchase-1/catalog-1/products/',
            '/profile/organizer/purchase-1/catalog-1/product-1/',
            '/profile/organizer/purchase-1/catalog-1/product-1-edit/',
        ]

    def def_CoreUrls(self):
        return [
            '/',
            '/categories/',
            '/category-kategoriya-1/',
            '/purchase-1/',
            '/purchase-1/catalog-1/',

        ]


    """тест создание users через функции выше определенные,
    получение profile Organizer и profile Member через метод getProfile(user) в accounts/models"""
    # def test_getProfile(self):
    #     userO = self.def_createOrganizerProfile(username="organ1", checked=False)
    #     userO.is_staff = True
    #     userO.save()
    #     userM = self.def_createMemberProfile(username="member1")
    #     profileO = getProfile(userO)
    #     assert (profileO)
    #     purshuasesO = profileO.getOrganizerPurchases()  #надо проверить
    #     profileM = getProfile(userM)
    #     assert (profileM)

    # def test_getData(self):
    #     users = User.objects.all()
    #     print "%s" % users
    #     profiles = OrganizerProfile.objects.all()
    #     print "%s" % profiles



    # def test_populateProfile(self):
    #     client = Client()
    #     print '---*---*---*--- тестирование ЛК организатора'
    #     response = client.get(reverse('profileView'))
    #     print "get запрос пользователя на стр /profile/ - %s" % response.status_code
    #
    #     is_login = client.login(username='admin', password='balabas')
    #     response = client.get(reverse('profileView'))
    #     print "get запрос пользователя admin на стр /profile/ - %s" % (response.status_code)
    #     # assert  (is_login==True)
    #
    #     is_login = client.login(username='userOrganizer', password='balabas')
    #     # assert (is_login==True)
    #     response = client.post('/profile/login/', {'username': 'userOrganizer', 'password': 'balabas'})
    #     print "post запрос пользователя (userOrganizer balabas) на стр /profile/login/ - %s" % response.status_code
    #     # assert (response.status_code==302)
    #
    #     response = client.post('/profile/login/', {'username': 'admin', 'password': 'balabas'})
    #     print "post запрос пользователя (admin balabas редирект - значит залогинился)  на стр /profile/login/ - %s" % response.status_code
    #
    #     client.login(username='userOrganizer', password='balabas')
    #     response = client.get('/profile/populate-profile/')
    #     print "get запрос пользователя на стр /profile/populate-profile/ - %s" % response.status_code
    #
    #     response = client.get('/profile/organizer/purchase-add/')
    #     print "get запрос пользователя на стр /profile/organizer/purchase-add/ - %s" % response.status_code
    #
    #     response = client.get('/profile/registration/')
    #     print "get запрос пользователя на стр /profile/registration/ - %s" % response.status_code
    #     print '---*---*---*---'


    def test_allUsers(self):
        # self.def_createCategory()  #создаем статус закупки
        # userO = self.def_createOrganizerProfile(username="organ1", checked=False)
        # userO2 = self.def_createOrganizerProfile(username="organ2", checked=True)
        # self.def_createPurchase(userO2)  #создаем закупку и продукт со всеми вытекающими
        # userM = self.def_createMemberProfile(username="member1")
        users = User.objects.all()
        for user in users:
            client = Client()

            urls = self.def_AccountUrls()
            for url in urls:
                # крэш для незалогиненного пользователя
                response = client.get(reverse(url))
                if url=='profileView' or url=='populateProfileView':
                    assert (response.status_code==302)
                else:
                    assert (response.status_code==200)
                # крэш для залогиненного пользователя
                is_login = client.login(username=user.username, password="balabas")
                response = client.get(reverse(url))
                assert (response.status_code == 200 and is_login)
                # if urls.index(url)+1 == len(urls):
                #     print u"Accounts Urls проверены для пользователя %s" % user.username

            """проверка что организатор может просматривать и добавлять закупки
            проверка что все кроме проверенных организаторов редиректятся """
            for url in self.def_OrganizerUrls():
                response = client.get(url)
                profile = getProfile(user)
                if hasattr(profile, 'organizer_checked') and profile.is_checked():
                    assert (response.status_code==200)
                elif hasattr(profile, 'organizer_checked') and not profile.is_checked():
                    assert (response.status_code==302)
                elif hasattr(profile, 'member_checked'):
                    assert (response.status_code==302)
                else:
                    assert (response.status_code==302)

            """проверка что только владелец может глядеть
            на свои закупки и редактировать их"""
            for url in self.def_OwnerUrls():
                response = client.get(url)
                profile = getProfile(user)
                if hasattr(profile, 'organizer_checked') and profile.is_checked():
                    if Purchase.objects.get(id=url[28]) in profile.purchase_set.all():
                        assert (response.status_code==200)
                    else:
                        # print u"%s, url %s, status: %s" % (user.username, url, response.status_code)
                        assert (response.status_code==302)
                elif hasattr(profile, 'organizer_checked') and not profile.is_checked():
                    assert (response.status_code==302)
                elif hasattr(profile, 'member_checked'):
                    assert (response.status_code==302)
                else:
                    assert (response.status_code==302)

            """проверка что только проверенный пользователь
             может гулять по core ссылкам"""
            for url in self.def_CoreUrls():
                response = client.get(url)
                profile = getProfile(user)
                if profile.is_checked():
                    assert (response.status_code==200)
                elif not profile.is_checked():
                    assert (response.status_code==302)
                else:
                    assert (response.status_code==302)

            response = self.client.post(reverse('loginView'), {'username': user.username, 'password': 'balabas'})
            assert (response.status_code==302)

            print u"пользователь %s успешно проверен" % user.username

        print "все пользователи залогинились"

        client = Client()
        list_urls = self.def_OrganizerUrls()
        list_urls.extend(self.def_OwnerUrls())
        for url in list_urls:
            # крэш по ссылкам организатора для незалогиненного пользователя
            # каждая страница должна вывести 302 редирект на регистрацию
            response = client.get(url)
            assert (response.status_code==302)
        print u"Аноним Пользователь редиректится успешно"

        response = self.client.post(reverse('registrationView'), {'username': "testReg", 'email': 'aksdhf@sdfsd.ru', 'password1': 'balabas', 'terms': 'on'})
        assert (response.status_code==302)  #успешная регистрация
        print u"Успешная регистрация нового пользователя"




