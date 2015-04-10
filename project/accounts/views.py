# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm, purchaseForm, catalogForm, \
                                    catalogProductPropertiesForm, ProductForm, MemberProfileForm, UserLoginForm, ProductImagesForm
from project.core.forms import ImportXLSForm
from project.core.models import Purchase, Catalog, Product, CatalogProductProperties, Properties, ProductImages, ImportFiles
from django.shortcuts import render, render_to_response, redirect
from project.accounts.models import OrganizerProfile, getProfile, repopulateProfile
from django.contrib import auth
from django.contrib import messages
import xlrd
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.settings import ADMIN_EMAIL, IMPORT_XLS
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from project.cart.purchases import get_purchases_dict, get_all_purchases_dict


def check_organizer(func):
    """декоратор проверки профиля пользователя
    принимает пользователя , проверяет и возвращает вьюху
    purchase-id - необходимо присутствие именованной переменной во views для проверки владельца закупки"""
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated():
            profile = getProfile(request.user)
            try:
                purchase_id = kwargs['purchase_id']
            except:
                purchase_id = None
            if profile is None:
                messages.info(request, "Пожалуйста заполните Ваш профиль")
                return redirect('/profile/populate-profile/')
            elif not profile.is_checked():
                messages.info(request, "Ваш профиль еще не проверен")
                return redirect('/profile/')
            elif not isinstance(profile, OrganizerProfile):
                messages.info(request, "Вы не являетесь организаотором закупок")
                return redirect('/profile/')
            elif purchase_id:  # проверка является ли профайл владельцем закупки
                try:
                    purchase_test = Purchase.objects.get(id=kwargs['purchase_id'])
                    purchase_set = profile.purchase_set.all()
                    if purchase_test in purchase_set:
                        return func(request, *args, **kwargs)
                    else:
                        messages.info(request, "Вы не являетесь вледельцем закупки")
                        return redirect('/profile/')
                except:
                    messages.info(request, "Вы не являетесь вледельцем закупки")
                    return redirect('/profile/')
            else:
                # возвращаем наконец функцию
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/profile/registration/')
    return wrapper


def profileView(request, template_name):
    user = request.user
    if user.is_authenticated():
        """проверка есть ли профиль у пользователя и получение его файл accounts.models"""
        profile = getProfile(user)
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def populateProfileView(request, template_name):
    user = request.user
    form = OrganizerProfileForm()
    if user.is_authenticated():
        profile = getProfile(user)
        form = OrganizerProfileForm(instance=profile)
        if request.method == "POST":
            postdata = request.POST.copy()
            terms = postdata.get('terms', '')
            is_organizer = postdata.get('is_organizer', '')
            form = OrganizerProfileForm(request.POST, request.FILES)

            if form.is_valid() and getProfile(user): #если профиль уже существует то только обновляем (не возвращает None)
                # current_profile = getProfile(user)
                profile = repopulateProfile(profile, request)
                profile.save()
                return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))

            elif form.is_valid() and terms == 'on' and is_organizer == 'on':
                form.save(request.user)
                return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
            elif form.is_valid() and terms == 'on' and is_organizer == '':
                form = MemberProfileForm(request.POST, request.FILES)
                form.save(request.user)
                return HttpResponseRedirect(urlresolvers.reverse('populateProfileView'))
            else:  # TODO: должна быть обработка ошибок
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
    profile = getProfile(user)
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
@check_organizer
def purchases(request, template_name):
    # purchases_dict = get_purchases_dict(request)  # получаем словарь словарей ... описание в cart.purchases.py
    purchases_dict = get_all_purchases_dict(request)  # словарь словарей всех закупок пользователя
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Добавление закупки
@check_organizer
def purchaseAdd(request, template_name):
    user = request.user
    message = ''
    if request.POST:
        form = purchaseForm(request.POST)
        if form.is_valid():
            new_purchase = form.save(user)
            message = u"Новая закупка «%s» успешно добавлена" % request.POST['name']
        else:
            message = u"Ошибка при добавлении закупки"
    purchase_form = purchaseForm()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
@check_organizer
def purchase(request, template_name, purchase_id, edit=False):
    message = ''
    if edit is True:  # если передан парамерт edit равный True, то редактируем закупку
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
            return render_to_response(template_name, locals(), context_instance=RequestContext(request))
        except ObjectDoesNotExist:
            raise Http404
    else:
        try:
            purchase = Purchase.objects.get(id=purchase_id)  # получаем экземпляр Закупки по id
            purchase_cat = purchase.categories.all()
        except ObjectDoesNotExist:
            raise Http404
        return render_to_response(template_name, locals(), context_instance=RequestContext(request))


# __ // Закупки __

# __ Каталоги __

# Просмотр всех каталогов для текущей закупки
@check_organizer
def catalogs(request, purchase_id, template_name):
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalogs = Catalog.objects.filter(catalog_purchase=purchase_id)
        # catalogs = Catalog.objects.all()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404



# Добавление каталога
@check_organizer
def catalogAdd(request, purchase_id, template_name):
    user = request.user
    profile = checkOrganizerProfile(request.user)
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
def getNewCatalogProductPropertiesFormBlock(request, template_name):
    # content = '<label>Свойство товара в каталоге:</label> \
    #     <input class="form-control" name="cpp_name" placeholder="Введите свойство для товаров в этом каталоге" type="text"> \
	 #    <label>Возможные значения:</label> \
	 #    <input class="form-control" name="cpp_values" placeholder="Введите возможные значения для свойства через символ &quot;;&quot;" type="text"> \
    #     <hr/>'
    catalogProductProperties_form = catalogProductPropertiesForm()
    # return HttpResponse()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))




# Просмотр каталога
@check_organizer
def catalog(request, purchase_id, catalog_id, template_name):
    """ проверяем пользователя и его профайл организатора"""
    profile = checkOrganizerProfile(request.user)
    try:
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)
        products = catalog.get_products()
        for product in products:
            product.property = product.property.split(';')  # для более читаемого вида
        if request.method == 'POST':
            # импорт товаров через xml
            form = ImportXLSForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                file_name = '%s/%s' % (IMPORT_XLS, request.FILES['file'].name)
                rb = xlrd.open_workbook(file_name, formatting_info=True)
                sheet = rb.sheet_by_index(0)
                objects_dict = {}
                for colnum in range(sheet.ncols):
                    col = sheet.col_values(colnum)
                    """ с помощью метода pop() извлекаем 1 эллемент колонки и используем его как ключ, удаляя его
                    из последовательности значения при этом - список всех элементов колонки кроме первого """
                    objects_dict.update({col.pop(0): col})
                for rownum in range(sheet.nrows):
                    row = sheet.row_values(rownum)
                    if rownum != 0:
                        new_product = Product()
                        try:
                            test_sku = int(objects_dict['sku'][rownum-1])
                            if Product.objects.filter(catalog=catalog, sku=test_sku):
                                continue
                            # for test_prod in exist_products:
                                # if test_prod in Product.objects.filter(catalog=catalog):
                                #     continue  # прерываем итерацию и создание товара если нашелся SKU в каталоге
                        except:
                            pass
                        new_product.sku = objects_dict['sku'][rownum-1]
                        new_product.catalog = catalog
                        new_product.description = objects_dict['description'][rownum-1]
                        new_product.product_name = objects_dict['product_name'][rownum-1]
                        new_product.property = objects_dict['property'][rownum-1]
                        new_product.price = objects_dict['price'][rownum-1]
                        new_product.save()
                        new_image = ProductImages()
                        new_image.image = 'product/04_small.jpg'
                        new_image.p_image_product = new_product
                        new_image.save()
                return HttpResponseRedirect(catalog.url())
        else:
            instance_form = ImportFiles.objects.create(import_catalog=catalog)
            form = ImportXLSForm(instance=instance_form)
            new_product = Product()
        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# __ // Каталоги __


# __ Товары __

# Просмотр всех товаров для текущего каталога
@check_organizer
def products(request, purchase_id, catalog_id, template_name):
    """ проверяем пользователя и его профайл организатора"""
    profile = checkOrganizerProfile(request.user)
    # if not Purchase.objects.get(id=purchase_id) in profile.purchase_set.all():
    #     messages.info(request, "Вы не являетесь владельцем закупки")
    #     return HttpResponseRedirect(urlresolvers.reverse('profileView'))
    try:
        user = request.user
        purchase = Purchase.objects.get(id=purchase_id)
        catalog = Catalog.objects.get(id=catalog_id)
        products = Product.objects.filter(catalog=catalog_id)

        for product in products:
            try:
                product.product_image = ProductImages.objects.get(p_image_product_id=product.id).image
            except:
                continue

        paginator = Paginator(products, 3)
        page = request.GET.get('page')

        try:
            page_products = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            page_products = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            page_products = paginator.page(paginator.num_pages)

        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404

# Просмотр и Редактирование товара
@check_organizer
def product(request, purchase_id, catalog_id, product_id, template_name, edit=False):
    user = request.user
    # profile = checkOrganizerProfile(request.user)
    message = ''

    if edit == True:  # если передан парамерт edit равный True, то редактируем товар
        # try:
        product = Product.objects.get(id=product_id)  # получаем экземпляр товара по id

        if request.POST:
            product_form = ProductForm(request.POST)
            product_image_form = ProductImagesForm(request.POST, request.FILES)
            if product_form.is_valid() and product_image_form.is_valid():
                product.product_name = request.POST['product_name']
                properties = request.POST.getlist('properties')
                product.property = ';'.join(properties)            # u'34,green,41;34,green,42;34,green,43;34,blue,41;34,blue,42'
                product.description = request.POST['description']
                product.price = request.POST['price']
                product.sku = request.POST['sku']
                product.save()

                if request.FILES:
                    try:
                        ProductImages.objects.get(p_image_product_id=product_id).delete()
                        product_image_form.save(product_id)
                    except:
                        product_image_form.save(product_id)

                # Сохранение свойств в старом формате. Удалить если все норм работает.
                # Properties.objects.filter(properties_product_id=product_id).delete()
                #
                # properties = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
                # for property in properties:
                #     try:
                #         if request.POST[property.cpp_slug] is not None:
                #             new_properties = Properties()
                #             new_properties.properties_value = request.POST[property.cpp_slug]  #request.POST['tsvet']
                #             new_properties.properties_product = product
                #             new_properties.properties_catalogProductProperties = CatalogProductProperties.objects.get(cpp_slug=property.cpp_slug)
                #             new_properties.save()
                #     except:
                #         continue

                message = u"Новый товар %s успешно отредактирован." % request.POST['product_name']
            else:
                message = u"Ошибка при изменении товара"

        product = Product.objects.get(id=product_id)
        product_image_Obj = ProductImages(p_image_product_id=product_id)
        try:
            product_image = ProductImages.objects.get(p_image_product_id=product_id).image
        except:
            product_image = False
        product_image_form = ProductImagesForm(instance=product_image_Obj)
        product_form = ProductForm(instance=product)                    # заполненная форма текущей товара
        # property_form = propertyForm(catalog_id, product_id)
        properties = get_propeties(catalog_id, 'list')  # получим все возможные свойства для товаров этой категории
        # указанные свойства товара
        product_properties = product.property.split(";")

        return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
        # except ObjectDoesNotExist:
        #     raise Http404

    else:           # если параметр edit равный True не передан, но выводим просмотр товара
        try:
            purchase = Purchase.objects.get(id=purchase_id)
            catalog = Catalog.objects.get(id=catalog_id)
            product = Product.objects.get(id=product_id)
            product_image = ProductImages.objects.get(p_image_product_id=product_id).image

            # указанные свойства товара
            product_properties = product.property.split(";")

            # properties = get_propeties(catalog_id, 'list')  # получим все возможные свойства для товаров этой категории

            # старый вывод:
            # properties = Properties.objects.filter(properties_product=product_id)  # получим все свойства для этого товара
            # all_properties = {}
            # for property in properties:
            #     current_catalog_product_properties = CatalogProductProperties.objects.get(id=property.properties_catalogProductProperties_id)
            #     all_properties.update({current_catalog_product_properties.cpp_name: property.properties_value.split(";")})  # формируется словарь вида {имя_свойства: значения_распарсенные_в_список}


            return render_to_response(template_name, locals(),
                                          context_instance=RequestContext(request))
        except ObjectDoesNotExist:
                raise Http404


# Добавление товара
@check_organizer
def productAdd(request, purchase_id, catalog_id, template_name):
    try:
        message = ''
        user = request.user
        profile = checkOrganizerProfile(request.user)
        if request.POST:
            product_form = ProductForm(request.POST)
            product_image_form = ProductImagesForm(request.POST, request.FILES)
            if product_form.is_valid() and product_image_form.is_valid():
                properties = request.POST.getlist('properties')
                property = ';'.join(properties)            # u'34,green,41;34,green,42;34,green,43;34,blue,41;34,blue,42'
                new_product = product_form.save(catalog_id, property)
                product_image_form.save(new_product.id)

                # Сохранение свойств в старом формате. Удалить если все норм работает.
                # properties = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
                # for property in properties:
                #     try:
                #         if request.POST[property.cpp_slug] is not None:
                #             new_properties = Properties()
                #             new_properties.properties_value = request.POST[property.cpp_slug]  # request.POST['tsvet']
                #             new_properties.properties_product = new_product
                #             new_properties.properties_catalogProductProperties = CatalogProductProperties.objects.get(cpp_slug=property.cpp_slug)
                #             new_properties.save()
                #     except:
                #         continue

                message = u"Новый товар %s успешно добавлен." % request.POST['product_name']
            else:
                message = u"Ошибка при добавлении товара"

        product_form = ProductForm
        # property_form = propertyForm(catalog_id)      # Старая форма свойств. Удалить
        product_image_form = ProductImagesForm()

        properties = get_propeties(catalog_id, 'list')    # получим все возможные свойства для товаров этой категории

        return render_to_response(template_name, locals(),
                                  context_instance=RequestContext(request))
    except ObjectDoesNotExist:
            raise Http404


#  Примает id закупки, и способ возвращения
#  Возвращает все возможные кобинации свойств закупки
def get_propeties(catalog_id, type='list'):
    cpp_obj = CatalogProductProperties.objects.filter(cpp_catalog_id=catalog_id)
    list = []
    i = 0
    dict = {}
    for cpp_object in cpp_obj:
        values = cpp_object.cpp_values.split(";")
        dict[i] = values
        i += 1

    import itertools
    # dict = {0: ['34', '35'], 1: ['green', 'blue', 'black'], 2: ['41', '42']}
    for items in itertools.product(*dict.values()):
        list.append(','.join(items))

    stroka = ';'.join(list)

    if type == 'list':
        return list
    elif type == 'stroka':
        return stroka
    else:
        return None


def checkOrganizerProfile(user):
    try:
        profile = OrganizerProfile.objects.get(user=user)
        if profile.is_checked():
            return profile
    except:
        return None
