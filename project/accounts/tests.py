# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
import sys
import re
from django.core import mail
from django_webtest import WebTest
from django.contrib.auth.models import User, Group
from  models import OrganizerProfile, MemberProfile, getProfile


# Create your tests here.

class OrganizerTest(TestCase):
    fixtures = ['accounts.xml', 'core.xml']
    client = Client()
    csrf_client = Client(enforce_csrf_checks=True)
    user = User()

    def def_createOrganizerProfile(self):
        self.user = User.objects.create(username="userOrganizer",)
        self.user.set_password("balabas")
        profile = OrganizerProfile.objects.create(
            user=self.user,
            email="organizer@mail.ru",
            phone="89138886899",
            firstName="Орган",
            lastName="Изатор",
            address="Ленина 42-56",
            city="Северск",
            zipCode="636070",
            organizer_checked=False,
            icon="accounts/images/maksimov.jpg",
            )
        self.user.save()
        return self.user

    def def_createMemberProfile(self):
        self.user = User.objects.create(username="userMember")
        self.user.set_password("balabas")
        profile = MemberProfile.objects.create(
            user=self.user,
            email="member@mail.ru",
            phone="89138886899",
            firstName="Уча",
            lastName="Стник",
            address="Ленина 42-56",
            city="Северск",
            zipCode="636070",
            icon="accounts/images/maksimov.jpg",
            )
        self.user.save()
        return self.user

    def def_getAllUsers(self):
        return User.objects.all()

    def def_AccountUrls(self):
        return ['profileView', 'registrationView', 'loginView', 'logoutView','populateProfileView', ]

    def def_OrganizerUrls(self):
        return [
            '/profile/organizer/purchases/',
            '/profile/organizer/purchase-add/',
            '/profile/organizer/purchase-1/',
            '/profile/organizer/purchase-1-edit/',
            '/profile/organizer/purchase-1/catalogs/',
            '/profile/organizer/purchase-1/catalog-add/',
            '/profile/organizer/purchase-1/catalog-1/',
            '/profile/organizer/purchase-1/catalog-1/products/',
            '/profile/organizer/purchase-1/catalog-1/product-1/',
            '/profile/organizer/purchase-1/catalog-1/product-1-edit/',
        ]


    """тест создание users через функции выше определенные,
    получение profile Organizer и profile Member через метод getProfile(user) в accounts/models"""
    def test_getProfile(self):
        userO = self.def_createOrganizerProfile()
        userO.is_staff = True
        userO.save()
        userM = self.def_createMemberProfile()
        profileO = getProfile(userO)
        purshuasesO = profileO.getOrganizerPurchases()
        profileM = getProfile(userM)

        print '---*---*---*---'
        print u'Получен profile: %s через getProfile, его закупки: %s' % (profileO.firstName, purshuasesO)
        print u'Получен profile: %s через getProfile' % profileM.firstName
        print '---*---*---*---'


    def test_populateProfile(self):
        client = Client()
        print '---*---*---*--- тестирование ЛК организатора'
        response = client.get(reverse('profileView'))
        print "get запрос пользователя на стр /profile/ - %s" % response.status_code

        is_login = client.login(username='admin', password='balabas')
        response = client.get(reverse('profileView'))
        print "get запрос пользователя admin на стр /profile/ - %s" % (response.status_code)
        # assert  (is_login==True)

        is_login = client.login(username='userOrganizer', password='balabas')
        # assert (is_login==True)
        response = client.post('/profile/login/', {'username': 'userOrganizer', 'password': 'balabas'})
        print "post запрос пользователя (userOrganizer balabas) на стр /profile/login/ - %s" % response.status_code
        # assert (response.status_code==302)

        response = client.post('/profile/login/', {'username': 'admin', 'password': 'balabas'})
        print "post запрос пользователя (admin balabas редирект - значит залогинился)  на стр /profile/login/ - %s" % response.status_code

        client.login(username='userOrganizer', password='balabas')
        response = client.get('/profile/populate-profile/')
        print "get запрос пользователя на стр /profile/populate-profile/ - %s" % response.status_code

        response = client.get('/profile/organizer/purchase-add/')
        print "get запрос пользователя на стр /profile/organizer/purchase-add/ - %s" % response.status_code

        response = client.get('/profile/registration/')
        print "get запрос пользователя на стр /profile/registration/ - %s" % response.status_code
        print '---*---*---*---'


    def test_allUsers(self):
        userO = self.def_createOrganizerProfile()
        userM = self.def_createMemberProfile()
        users = self.def_getAllUsers()
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
                if urls.index(url)+1 == len(urls):
                    print u"Accounts Urls проверены для пользователя %s" % user.username

            for url in self.def_OrganizerUrls():
                response = client.get(url)
                profile = getProfile(user)
                if hasattr(profile, 'organizer_checked') and profile.is_checked():
                    print u"%s - %s (тип профиля организатор проверен)" % (user.username, response.status_code)
                    # assert (response.status_code==200)
                elif hasattr(profile, 'organizer_checked') and not profile.is_checked():
                    print u"%s - %s (тип профиля организатор не проверен)" % (user.username, response.status_code)
                    assert (response.status_code==302)
                elif hasattr(profile, 'member_checked'):
                    assert (response.status_code==302)
                    print u"Пользователь в профиле участников %s - %s" % (user.username, response.status_code)
                else:
                    assert (response.status_code==302)
                    print u"Пользователь без профиля %s - %s" % (user.username, response.status_code)
                # print u"user %s have (%s)" % (user.username, user.groups)

                # assert (response.status_code==302)
                # print u"ананим на стр %s - %s" % (url, response.status_code)
            # print u"Пользователь %s  успешно"


            response = self.client.post(reverse('loginView'), {'username': user.username, 'password': 'balabas'})
            assert (response.status_code==302)

        print "все пользователи залогинились"

        client = Client()
        for url in self.def_OrganizerUrls():
            # крэш по ссылкам организатора для незалогиненного пользователя
            # каждая страница должна вывести 302 редирект на регистрацию
            response = client.get(url)
            assert (response.status_code==302)
            # print u"ананим на стр %s - %s" % (url, response.status_code)
        print u"Аноним Пользователь редиректится по ссылкам организатора успешно"

        response = self.client.post(reverse('registrationView'), {'username': "testReg", 'email': 'aksdhf@sdfsd.ru', 'password1': 'balabas', 'terms': 'on'})
        assert (response.status_code==302)




