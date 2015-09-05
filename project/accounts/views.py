# -*- coding: utf-8 -*-
#!/usr/bin/env python
from project.accounts.forms import OrganizerProfileForm, UserRegistrationForm,\
    purchaseForm, catalogForm, catalogProductPropertiesForm, ProductForm,\
    MemberProfileForm, UserLoginForm, ProductImagesForm

from project.core.forms import ImportXLSForm
from project.core.models import Purchase, PurchaseStatus, Catalog, Product,\
    CatalogProductProperties, ProductImages, ImportFiles, PurchaseStatusLinks

from project.documentation.models import Page
from django.shortcuts import render, render_to_response, redirect
from project.accounts.models import OrganizerProfile, getProfile,\
    repopulateProfile

from django.contrib import auth
from django.contrib import messages
import xlrd
from excel_response import ExcelResponse
from django.template import RequestContext
from django.core import urlresolvers
from django.http import HttpResponseRedirect
from project.settings import ADMIN_EMAIL, IMPORT_XLS
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.http.response import Http404, HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from project.cart.purchases import get_all_purchases_dict
import datetime


def check_organizer(func):
    """декоратор проверки профиля пользователя
    принимает пользователя , проверяет и возвращает вьюху
    purchase-id - необходимо присутствие именованной переменной во views для
    проверки владельца закупки"""
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
            # try:
                purchase_test = Purchase.objects.get(id=kwargs['purchase_id'])
                purchase_set = profile.get_purchases()
                if purchase_test in purchase_set:
                    return func(request, *args, **kwargs)
                else:
                    messages.info(request, "Вы не являетесь вледельцем закупки")
                    return redirect('/profile/')
            # except:
            #     messages.info(request, "Вы не являетесь вледельцем закупки")
            #     return redirect('/profile/')
            else:
                # возвращаем наконец функцию
                return func(request, *args, **kwargs)
        else:
            return HttpResponseRedirect('/profile/registration/')
    return wrapper


def profileView(request, template_name):
    user = request.user
    if user.is_authenticated():
        """проверка есть ли профиль у пользователя и получение его
        файл accounts.models"""
        profile = getProfile(user)
        try:
            page = Page.objects.get(is_main=True)
        except:
            pass
    else:
        return HttpResponseRedirect(urlresolvers.reverse('registrationView'))
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


def populateProfileView(request, template_name):
    user = request.user
    # profile = getProfile(user)
    form = OrganizerProfileForm()
    if user.is_authenticated():
        profile = getProfile(user)
        form = OrganizerProfileForm(instance=profile)
        if request.method == "POST":
            postdata = request.POST.copy()
            terms = postdata.get('terms', '')
            is_organizer = postdata.get('is_organizer', '')
            form = OrganizerProfileForm(request.POST, request.FILES)

            if form.is_valid() and getProfile(user):
            # если профиль уже существует то только
            # обновляем(не возвращает None)"""

                profile = repopulateProfile(profile, request)
                profile.save()
                return HttpResponseRedirect(
                    urlresolvers.reverse('populateProfileView'))

            elif form.is_valid() and terms == 'on' and is_organizer == 'on':
                form.save(request.user)
                return HttpResponseRedirect(
                    urlresolvers.reverse('populateProfileView'))

            elif form.is_valid() and terms == 'on' and is_organizer == '':
                form = MemberProfileForm(request.POST, request.FILES)
                form.save(request.user)
                messages.text(
                    request,
                    "Спасибо, вы успешно создали профиль, ожидайте его\
                    подтверждения от администратора")

                return HttpResponseRedirect(
                    urlresolvers.reverse('populateProfileView'))

            elif form.is_valid() and terms == '':
                messages.text(
                    request, "Вы должны согласиться с условиями")

            else:  # TODO: должна быть обработка ошибок
                form = OrganizerProfileForm(request.POST, request.FILES)
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
                message = u'Зарегистрирован новый пользователь\
                %s / пароль: %s' % (new_user.username, pw)

                send_mail(
                    subject, message, 'teamer777@gmail.com', [ADMIN_EMAIL],
                    fail_silently=False)

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
    statuses = PurchaseStatus.objects.all()

    if 'ajax' in request.POST:
        PurchaseStatusLinks.objects.filter(
            purchase_id=request.POST['purchase_id'],
            status_id=request.POST['status_id']).update(active=0)

        PurchaseStatusLinks.objects.filter(
            purchase_id=request.POST['purchase_id'],
            status_id=request.POST['new_status_id']).update(active=1)

        return HttpResponse('{"status":"ok"}')

    # словарь словарей всех закупок пользователя
    purchases_dict = get_all_purchases_dict(request)

    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Добавление закупки
@check_organizer
def purchaseAdd(request, template_name):
    user = request.user
    message = ''
    statuses = PurchaseStatus.objects.all()  # все статусы
    if request.POST:

        form = purchaseForm(request.POST)
        if form.is_valid():
            new_purchase = form.save(user)
            form.save_m2m()

            dates_start = request.POST.getlist('date_start')
            dates_end = request.POST.getlist('date_end')
            data = request.POST.getlist('data')

            #  TODO: переписать с оптимизацией сохранения.\
            #  чтобы был один запрос (insert) к бд.
            i = 0
            for status in statuses:
                #        A if условие else B - Краткая форма.
                try:
                    date_start = datetime.datetime.strptime(
                        dates_start[i], '%Y-%m-%d')

                except:
                    date_start = None
                try:
                    date_end = datetime.datetime.strptime(
                        dates_end[i], '%Y-%m-%d')

                except:
                    date_end = None
                obj = PurchaseStatusLinks()
                obj.status = status
                obj.purchase = new_purchase
                obj.date_end = date_end
                obj.data = data[i]
                if i == 0:
                    obj.date_start = datetime.datetime.now()
                    obj.active = 1
                else:
                    obj.date_start = date_start
                    obj.active = 0
                obj.save()
                i += 1

            message = u"Новая закупка «%s» успешно\
                добавлена" % request.POST['name']

        else:
            message = u"Ошибка при добавлении закупки"
    purchase_form = purchaseForm()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))


# Просмотр или редактирование одной конкретной закупки (по id)
@check_organizer
def purchase(request, template_name, purchase_id, edit=False):
    message = ''
    # если передан парамерт edit равный True, то редактируем закупку
    if edit is True:
        try:
            # получаем экземпляр Закупки по id
            purchase = Purchase.objects.get(id=purchase_id)
            if request.POST:
                form = purchaseForm(request.POST, instance=purchase)
                if form.is_valid():
                    form.save(request.user)
                    form.save_m2m()
                    dates_start = request.POST.getlist('date_start')
                    dates_end = request.POST.getlist('date_end')
                    data = request.POST.getlist('data')
                    statuses = PurchaseStatus.objects.all()  # все статусы
                    i = 0
                    for status in statuses:
                        try:
                            date_start = datetime.datetime.strptime(
                                dates_start[i], '%Y-%m-%d')

                        except:
                            date_start = None
                        try:
                            date_end = datetime.datetime.strptime(
                                dates_end[i], '%Y-%m-%d')

                        except:
                            date_end = None
                        # Проверяем выставлена ли активность этого статуса
                        if int(request.POST['active']) != status.id:
                            PurchaseStatusLinks.objects.filter(
                                purchase=purchase, status=status).update(
                                    date_start=date_start, date_end=date_end,
                                    data=data[i], active=0)

                        else:
                            PurchaseStatusLinks.objects.filter(
                                purchase=purchase, status=status).update(
                                    date_start=date_start, date_end=date_end,
                                    data=data[i], active=1)

                        i += 1

                    message = u"Закупка «%s» успешно изменена" % request.POST['name']

                else:
                    message = u"Ошибка при изменении закупки"
            # заполненная форма текущей закупки
            purchase_form = purchaseForm(instance=purchase)

            # При создании закупки должны быть созданы все статусы.
            # выдираем их из базы со всеми параметрами
            sql = 'SELECT core_purchasestatus.id, core_purchasestatus.status_name, core_purchasestatuslinks.id as links_id, core_purchasestatuslinks.date_start, core_purchasestatuslinks.date_end, core_purchasestatuslinks.data, core_purchasestatuslinks.active \
            FROM core_purchasestatus \
            LEFT JOIN core_purchasestatuslinks \
            ON core_purchasestatus.id = core_purchasestatuslinks.status_id \
            WHERE core_purchasestatuslinks.purchase_id = %s '
            # ORDER BY core_purchasestatus.status_priority DESC'  # сортировка по приоритету статуса

            statuses = PurchaseStatus.objects.raw(sql, [purchase_id])

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
            catalog_form.save_m2m()

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
    # try:
    # 3 запроса к базе
    # purchase = Purchase.objects.get(id=purchase_id)
    # catalog = Catalog.objects.get(id=catalog_id)
    # catalog_product_properties = CatalogProductProperties.objects.filter(cpp_catalog=catalog_id)

    # 1 запрос к базе
    catalog_product_properties = CatalogProductProperties.objects.select_related().filter(cpp_catalog=catalog_id)
    catalog = catalog_product_properties[0].cpp_catalog
    purchase = catalog.catalog_purchase

    products = catalog.get_products()
    for product in products:
        product.property = product.property.split(';')  # для более читаемого вида
    if request.method == 'POST' and 'import' in request.POST:

        # импорт товаров через xml
        form = ImportXLSForm(request.POST, request.FILES)
        # form = ImportXLSForm(request.POST, request.FILES, initai=instance_form)
        # form = ImportXLSForm(initial=formset)
        if form.is_valid():
            form.save()
            import_file = list(ImportFiles.objects.filter(import_catalog=catalog))[-1].file
            # file_name = '%s/%s' % (IMPORT_XLS, request.FILES['file'].name)
            rb = xlrd.open_workbook(import_file.path, formatting_info=True)
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
                    new_image.image = 'product/no-image.png'
                    new_image.p_image_product = new_product
                    new_image.save()
            return HttpResponseRedirect(catalog.url())
    elif request.method == 'POST' and 'export' in request.POST:
        data = [[u'sku', u'description', u'price', u'product_name', u'catalog', u'property']]
        for product_item in catalog.get_products():
            data.append([product_item.sku, product_item.description, product_item.price,
                         product_item.product_name, product_item.catalog.id, product_item.property])
        return ExcelResponse(data, 'catalog_example')
    elif request.method == 'POST' and 'del_product' in request.POST:  # удаление продукта
        p = Product.objects.get(id=request.POST['product'])
        products = set(products) ^ set([p, ])  # преобразуем в set и делаем симметричкскую разность
        p.delete()
        return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
    else:
        # instance_form = ImportFiles.objects.create(import_catalog=catalog)
        # form = ImportXLSForm(instance=instance_form)
        form = ImportXLSForm(initial={"import_catalog": catalog.id})
        # new_product = Product()
    return render_to_response(template_name, locals(),
                              context_instance=RequestContext(request))
    # except ObjectDoesNotExist:
    #         raise Http404

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

    # если передан парамерт edit равный True, то редактируем товар
    if edit is True:
        # получаем экземпляр товара по id
        product = Product.objects.get(id=product_id)

        if request.POST:
            product_form = ProductForm(request.POST)
            if product_form.is_valid():
                product.product_name = request.POST['product_name']
                properties = request.POST.getlist('properties')
                product.property = ';'.join(properties)            # u'34,green,41;34,green,42;34,green,43;34,blue,41;34,blue,42'
                product.description = request.POST['description']
                product.price = request.POST['price']
                product.sku = request.POST['sku']
                product.save()

                # Удаляем отмеченные файлы
                delete_image_list = properties = request.POST.getlist('delete_image')
                for image_id in delete_image_list:
                    productimages_delete = ProductImages.objects.get(id=image_id).delete()

                # добавляем новые файлы
                if request.FILES:
                    for f in request.FILES.getlist('file', []):
                        productimages = ProductImages(p_image_product=product, image=f)
                        productimages.save()

                message = u"Новый товар %s успешно отредактирован." % request.POST['product_name']
            else:
                message = u"Ошибка при изменении товара"

        product = Product.objects.get(id=product_id)

        images = product.get_all_image()

        product_form = ProductForm(instance=product)                    # заполненная форма текущей товара        
        catalog_product_properties = CatalogProductProperties.objects.select_related().filter(cpp_catalog=catalog_id)
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

            images = product.get_all_image()

            catalog_product_properties = CatalogProductProperties.objects.select_related().filter(cpp_catalog=catalog_id)

            # указанные свойства товара
            product_properties = product.property.split(";")


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

            if product_form.is_valid():
                properties = request.POST.getlist('properties')
                property = ';'.join(properties)          # u'34,green,41;34,green,42;34,green,43;34,blue,41;34,blue,42'
                new_product = product_form.save(catalog_id, property)
                if request.FILES:
                    for f in request.FILES.getlist('file', []):
                        productimages = ProductImages(p_image_product=new_product, image=f)
                        productimages.save()

                        # создаем url обрезанной фотографии после сохранения
                        from easy_thumbnails.files import get_thumbnailer
                        productimages.cropping_url = get_thumbnailer(productimages.image).get_thumbnail({
                            'size': (250, 375),
                            'box': productimages.cropping_250x375,
                            'crop': True,
                            'detail': True,
                        }).url
                        productimages.save()

                message = u"Новый товар %s успешно добавлен." % request.POST['product_name']
            else:
                message = u"Ошибка при добавлении товара"

        product_form = ProductForm
        catalog_product_properties = CatalogProductProperties.objects.select_related().filter(cpp_catalog=catalog_id)
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
