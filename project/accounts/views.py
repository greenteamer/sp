# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm, purchaseForm, catalogForm, \
                                    catalogProductPropertiesForm, ProductForm, propertyForm
from project.core.models import Purchase, Catalog, Product, CatalogProductProperties, Properties, ProductImages
from django.shortcuts import render, render_to_response
from project.accounts.profiles import retrieve
from project.accounts.models import OrganizerProfile, getOrganizerProfile, repopulateOrganizerProfile
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm, purchaseForm, UserLoginForm, ProductImagesForm
from django.contrib import auth
from django.contrib.auth import login, authenticate
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.settings import ADMIN_EMAIL
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse


def profileView(request, template_name):
    user = request.user
    if user.is_authenticated():
        """проверка есть ли профиль у пользователя и получение его файл accounts.models"""
        profile = getOrganizerProfile(user)

    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def populateProfileView(request, template_name):
    user = request.user
    form = OrganizerProfileForm()
    if user.is_authenticated():
        """проверка есть ли профиль у пользователя и получение его файл accounts.models"""
        profile = getOrganizerProfile(user)
        form = OrganizerProfileForm(instance=profile)
        if request.method == "POST":
            form = OrganizerProfileForm(request.POST, request.FILES)
            if form.is_valid() and getOrganizerProfile(user): #если профиль уже существует то только обновляем (не возвращает None)
                current_profile = getOrganizerProfile(user)
                current_profile = repopulateOrganizerProfile(current_profile, request)
                current_profile.save()
                return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
            elif form.is_valid():
                form.save(request.user)
                return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
            else: #должна быть обработка ошибок
                form = UserRegistrationForm(request.POST, request.FILES)
                return render(request, 'accounts/populate_profile.html', {
                    'form': form,
                    'error': form.errors,
                })
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

#регистрация пользователя
def registrationView(request, template_name):
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserRegistrationForm(postdata)
        terms = postdata.get('terms', '')
        if form.is_valid() and terms == 'on':

            form.save()
            un = postdata.get('username', '')
            # name="password1" т.к. два поля с подтверждением
            pw = postdata.get('password1', '')
            new_user = auth.authenticate(username=un, password=pw)
            if new_user and new_user.is_active:

                # отправляем e-mail о регистрации нового пользователя
                subject = u'sp.ru регистрация %s' % new_user.username
                message = u' Зарегистрирован новый пользователь %s / пароль: %s' % (new_user.username, pw)
                send_mail(subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL], fail_silently=False)

                auth.login(request, new_user)
                # Редирект на url с именем my_account
                url = urlresolvers.reverse('profileView')
                return HttpResponseRedirect(url)
        elif terms == '':
            form = UserRegistrationForm(postdata)
            terms_error = 'пожалуйста подтвердите условия пользования сайтом'
            return render(request, 'accounts/registration.html', {
                'terms_error': terms_error,
                'form': form,
            })
        else:
            form = UserRegistrationForm(postdata)
            return render(request, 'accounts/registration.html', {
                'form': form,
                'error': form.errors,
            })
    else:
        form = UserRegistrationForm()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

#страница входа для зарегистрированного пользователя
def loginView(request, template_name):
    form = UserLoginForm()
    if request.method == 'POST':
        postdata = request.POST.copy()
        form = UserLoginForm(postdata)
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
            auth.login(request, user)
        # Перенаправление на "правильную" страницу
            return HttpResponseRedirect("/profile/")
        else:
            form = UserLoginForm(postdata)
            error = 'Логин или пароль введены не верно'
            return render(request, 'accounts/login.html', {
                'form': form,
                'error': error,
            })
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

def logoutView(request, template_name):
    user = request.user
    profile = getOrganizerProfile(user)
    if user.is_authenticated:
        auth.logout(request)
    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = auth.authenticate(username=username, password=password)
        if user is not None and user.is_active:
        # Правильный пароль и пользователь "активен"
            auth.login(request, user)
        # Перенаправление на "правильную" страницу
            return HttpResponseRedirect("/profile/")
        else:
            HttpResponseRedirect(urlresolvers.reverse('loginView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# __ Закупки __

# Просмотр всех закупок
def purchases(request, template_name):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    purchases = Purchase.objects.filter(organizerProfile=profile)
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))

# Добавление закупки
def purchaseAdd(request, template_name):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if request.POST:
        form = purchaseForm(request.POST)
        if form.is_valid():
            form.save(user)
            message = u"Новая закупка «%s» успешно добавлена" % request.POST['name']
        else:
            message = u"Ошибка при добавлении закупки"

    purchase_form = purchaseForm()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
def purchase(request, purchase_id, template_name, edit=False):
    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if edit == True:  # если передан парамерт edit равный True, то редактируем закупку
        try:
            purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
            if request.POST:
                form = purchaseForm(request.POST)
                if form.is_valid():
                    purchase.name = request.POST['name']
                    purchase.save()
                    message = u"Закупка «%s» успешно изменена" % request.POST['name']
                else:
                    message = u"Ошибка при изменении закупки"

            purchase_form = purchaseForm(instance=purchase) # заполненная форма текущей закупки
            return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            raise Http404

    else:
        try:
            purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
        except ObjectDoesNotExist:
            raise Http404

        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))


# __ // Закупки __

# __ Каталоги __

# Просмотр всех каталогов для текущей закупки
def catalogs(request, purchase_id, template_name):
    try:
        user = request.user

        """ проверяем пользователя и его профайл организатора"""
        if user.is_authenticated():
            profile = getOrganizerProfile(user)
        else:
            return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

        purchase = Purchase.objects.get(id=purchase_id)
        catalogs = Catalog.objects.filter(catalog_purchase=purchase_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404



# Добавление каталога
def catalogAdd(request, purchase_id, template_name):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''
    if request.POST:
        catalog_form = catalogForm(request.POST)
        # catalogProductProperties_form = catalogProductPropertiesForm(request.POST)

        if catalog_form.is_valid():
            new_catalog = catalog_form.save(purchase_id)  # каталог сохраняется для нужной закупки - переопределена ф-я save, возвращает созданный объект каталога

            cpp_names = request.POST.getlist('cpp_name')
            cpp_values = request.POST.getlist('cpp_values')

            cpp_purchase = Purchase.objects.get(id=purchase_id)

            for cpp_name in cpp_names:
                if cpp_name != '' and cpp_name != None:
                    new_catalogProductProperties = CatalogProductProperties()
                    new_catalogProductProperties.cpp_name = cpp_name
                    new_catalogProductProperties.cpp_values = cpp_values[cpp_names.index(cpp_name)]
                    new_catalogProductProperties.cpp_catalog = new_catalog
                    new_catalogProductProperties.cpp_purchase = cpp_purchase
                    new_catalogProductProperties.save()

            message = u"Новый каталог «%s» успешно добавлен. <br/> Добавить еще: " % request.POST['catalog_name']
        else:
            message = u"Ошибка при добавлении каталога"
        #
        # if catalog_form.is_valid() and catalogProductProperties_form.is_valid():
        #     new_catalogProductProperties = catalogProductProperties_form.save(commit=False)
        #     new_catalogProductProperties.cpp_catalog = catalog_form.save(purchase_id)  # каталог сохраняется для нужной закупки - переопределена ф-я save, возвращает созданный объект каталога
        #     new_catalogProductProperties.cpp_purchase = Purchase.objects.get(id=purchase_id)
        #     new_catalogProductProperties.save()
        #     message = u"Новый каталог «%s» успешно добавлен. <br/> Добавить еще: " % request.POST['catalog_name']
        # else:
        #     message = u"Ошибка при добавлении каталога"

    catalog_form = catalogForm()
    catalogProductProperties_form = catalogProductPropertiesForm()

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# страница для ajax запроса получения полей ввода свойств,при добавлении каталога
def getNewCatalogProductPropertiesFormBlock(request):
    content = '<label>Свойство товара в каталоге:</label> \
        <input class="form-control" name="cpp_name" placeholder="Введите свойство для товаров в этом каталоге" type="text"> \
	    <label>Возможные значения:</label> \
	    <input class="form-control" name="cpp_values" placeholder="Введите возможные значения для свойства через символ &quot;;&quot;" type="text"> \
        <hr/>'
    return HttpResponse(content)




# Просмотр каталога
def catalog(request, purchase_id, catalog_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# __ // Каталоги __


# __ Товары __

# Просмотр всех товаров для текущего каталога
def products(request, purchase_id, catalog_id, template_name):
    try:
        user = request.user

        """ проверяем пользователя и его профайл организатора"""
        if user.is_authenticated():
            profile = getOrganizerProfile(user)
        else:
            return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        products = Product.objects.filter(catalog=catalog_id)

        for product in products:
            try:
                product.product_image = ProductImages.objects.get(p_image_product_id=product.id).image
            except:
                continue
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# Просмотр и Редактирование товара
def product(request, purchase_id, catalog_id, product_id, template_name, edit=False):

    user = request.user

    """ проверяем пользователя и его профайл организатора"""
    if user.is_authenticated():
        profile = getOrganizerProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

    message = ''

    if edit == True:  # если передан парамерт edit равный True, то редактируем товар
        try:
            product = Product.objects.get(id=product_id)  # получаем экземпляр товара по id

            if request.POST:
                product_form = ProductForm(request.POST)
                product_image_form = ProductImagesForm(request.POST, request.FILES)
                if product_form.is_valid() and product_image_form.is_valid():

                    product.product_name = request.POST['product_name']
                    product.description = request.POST['description']
                    product.price = request.POST['price']
                    product.sku = request.POST['sku']
                    product.save()

                    if request.FILES:
                        ProductImages.objects.get(p_image_product_id=product_id).delete()
                        product_image_form.save(product_id)


                    Properties.objects.filter(properties_product_id=product_id).delete()

                    properties = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
                    for property in properties:
                        try:
                            if request.POST[property.cpp_slug] is not None:
                                new_properties = Properties()
                                new_properties.properties_value = request.POST[property.cpp_slug]  #request.POST['tsvet']
                                new_properties.properties_product = product
                                new_properties.properties_catalogProductProperties = CatalogProductProperties.objects.get(cpp_slug=property.cpp_slug)
                                new_properties.save()
                        except:
                            continue

                    message = u"Новый товар %s успешно отредактирован." % request.POST['product_name']
                else:
                    message = u"Ошибка при изменении товара"

            product = Product.objects.get(id=product_id)
            product_image_Obj = ProductImages(p_image_product_id=product_id)
            product_image = ProductImages.objects.get(p_image_product_id=product_id).image
            product_image_form = ProductImagesForm(instance=product_image_Obj)
            product_form = ProductForm(instance=product)                    # заполненная форма текущей товара
            property_form = propertyForm(catalog_id, product_id)


            return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            raise Http404

    else:           # если параметр edit равный True не передан, но выводим товар
        try:
            purchase = Purchase.objects.get(id=purchase_id)
            catalog = Catalog.objects.get(id=catalog_id)
            product = Product.objects.get(id=product_id)
            product_image = ProductImages.objects.get(p_image_product_id=product_id).image
            properties = Properties.objects.filter(properties_product=product_id)  # получим все свойства для этого товара
            all_properties = {}
            for property in properties:
                current_catalog_product_properties = CatalogProductProperties.objects.get(id=property.properties_catalogProductProperties_id)
                all_properties.update({current_catalog_product_properties.cpp_name: property.properties_value.split(";")})  # формируется словарь вида {имя_свойства: значения_распарсенные_в_список}

            return render_to_response(template_name, locals(),
                                          context_instance=RequestContext(request))
        except ObjectDoesNotExist:
                raise Http404


# Добавление товара
def productAdd(request, catalog_id, template_name):
    try:
        message = ''
        user = request.user

        """ проверяем пользователя и его профайл организатора"""
        if user.is_authenticated():
            profile = getOrganizerProfile(user)
        else:
            return HttpResponseRedirect(urlresolvers.reverse('registrationView'))

        if request.POST:
            product_form = ProductForm(request.POST)
            product_image_form = ProductImagesForm(request.POST, request.FILES)
            if product_form.is_valid() and product_image_form.is_valid():
                new_product = product_form.save(catalog_id)
                product_image_form.save(new_product.id)

                properties = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
                for property in properties:
                    try:
                        if request.POST[property.cpp_slug] is not None:
                            new_properties = Properties()
                            new_properties.properties_value = request.POST[property.cpp_slug]  #request.POST['tsvet']
                            new_properties.properties_product = new_product
                            new_properties.properties_catalogProductProperties = CatalogProductProperties.objects.get(cpp_slug=property.cpp_slug)
                            new_properties.save()
                    except:
                        continue

                message = u"Новый товар %s успешно добавлен." % request.POST['product_name']
            else:
                message = u"Ошибка при добавлении товара"

        product_form = ProductForm
        property_form = propertyForm(catalog_id)
        product_image_form = ProductImagesForm()

        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


