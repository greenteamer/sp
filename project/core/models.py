# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from project.accounts.models import OrganizerProfile
from django.utils.text import slugify
from project.core.functions import translit
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from image_cropping import ImageRatioField
# from datetime import datetime


class CommonActiveManager(models.Manager):
    """Класс менеджер для фильтрации активных объектов"""
    def get_query_set(self):
        return super(CommonActiveManager, self).get_query_set().filter(is_active=True)


class Category(MPTTModel):
    """Класс для категорий товаров"""
    name = models.CharField(_(u'Name'), max_length=50, unique=False)
    slug = models.SlugField(_(u'Slug'), max_length=50, unique=True,
                            help_text=_(u'Slug for product url created from name.'))
    # "Чистые" ссылки для продуктов формирующиеся из названия

    description = models.TextField(_(u'Description'), blank=True)
    is_active = models.BooleanField(_(u'Active'), default=True)
    meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255,
                                     help_text=_(u'Comma-delimited set of SEO keywords for meta tag'),blank=True)
    # Разделенные запятыми теги для SEO оптимизации

    meta_description = models.CharField(_(u'Meta description'), max_length=255,
                                        help_text=_(u'Content for description meta tags'), blank=True)
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True) #default=datetime.utcfromtimestamp(0),
    updated_at = models.DateTimeField(_(u'Updated at'), default='', null=True, auto_now=True)
    parent = TreeForeignKey('self', verbose_name=_(u'Родительская категория'),
                            related_name='children', blank=True,
                            help_text=_(u'Родительская категория для текущей категоири'), null=True)
    active = CommonActiveManager()

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = _(u'Категории')

    # It is required to rebuild tree after save, when using order for mptt-tree
    # def save(self, *args, **kwargs):
    #     super(Category, self).save(*args, **kwargs)
    #     Category.objects.rebuild()

    def __unicode__(self):
        # return self.name
        try:
            return "%s-%s" % ('--' * self.level, self.parent.name, self.name)
        except:
            return '%s%s' % ('--' * self.level, self.name)
            # return self.name

    @permalink
    def get_absolute_url(self):
         #Генерация постоянных ссылок на категории
        return('category', (), {'category_slug': self.slug})


#  возвращает число на 1 больше чем максимальныое занчение ПриоритетаЗакупки во всех закупках,
#  если закупок нет, то возвращает 0
def get_next_status_priority():
    try:
        max_status_priority = PurchaseStatus.objects.order_by('-status_priority')[0]
        return max_status_priority.status_priority + 1
    except:
        return 0


# Статусы закупок
class PurchaseStatus(models.Model):
    status_name = models.CharField(max_length=50, verbose_name=u'Статус закупки')
    status_description = models.TextField(verbose_name=u'Описание статуса закупки', blank=True, null=True)
    status_priority = models.IntegerField(verbose_name=u'Приоритет статуса', default=(get_next_status_priority), unique=True)
    status_icon = models.FileField(_(u'Иконка'), upload_to='purchase_status/',
                             help_text=u'Иконка статуса', blank=True)
    class Meta:
        ordering = ['status_priority']
        verbose_name_plural = _(u'Статусы закупок')

    def __unicode__(self):
        return self.status_name


class Purchase(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название закупки')
    description = models.TextField(verbose_name=u'Описание закупки', null=True)
    organizerProfile = models.ForeignKey('accounts.OrganizerProfile', verbose_name=u'Профиль организатора')
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)
    # purchase_status = models.ForeignKey(PurchaseStatus, verbose_name=u'Статус закупки', default=PurchaseStatus.objects.order_by('-status_priority')[0] )
    # purchase_status = models.ForeignKey(PurchaseStatus, verbose_name=u'Статус закупки', null=True, blank=True)
    prepay = models.IntegerField(verbose_name=u'Предоплата', help_text=u'Отмечается в процентах', default=100)
    percentage = models.IntegerField(verbose_name=u'Процент организатора', help_text=u'Отмечается в процентах', default=15)
    paymethods = models.TextField(u'Способы оплаты', default=u'Не указано')
    categories = models.ManyToManyField(Category, verbose_name=_(u'Categories'),
                                        help_text=_(u'Категории для этой закупки'))

    class Meta:
        verbose_name_plural = _(u'Закупки')

    def __unicode__(self):
        return self.name

    # def get_categories:
    #     return Category.objects.filter()

    def get_current_status(self):
        status = PurchaseStatusLinks.objects.get(purchase=self.id, active=True)
        return status.status

    def get_catalogs(self):
        return Catalog.objects.filter(catalog_purchase=self.id)

    def counts(self):
        c = {"catalogs": Catalog.objects.filter(catalog_purchase=self.id).count(),
             "orders": 0,       # TODO: Настроить подсчет!
             "member": 0        # Настроить подсчет
             }
        return c

    def url(self):
        return '/profile/organizer/purchase-%s' % self.id

    def url_core(self):
        return '/purchase-%s' % self.id


# связи между закупками и статусами закупок
class PurchaseStatusLinks(models.Model):
    status = models.ForeignKey(PurchaseStatus, verbose_name=_(u'Статус'))
    purchase = models.ForeignKey(Purchase, verbose_name=_(u'Закупка'))
    date_start = models.DateTimeField(verbose_name=u'Дата начала действия статуса', null=True)
    date_end = models.DateTimeField(verbose_name=u'Дата окончания действия статуса', null=True)
    data = models.TextField(verbose_name=u'Описание. Дополнительные данные', null=True, blank=True)
    active = models.BooleanField(verbose_name=u'Текущий статус', default=False)

    class Meta:
        verbose_name_plural = _(u'Закупка -> Статус')

    def __unicode__(self):
        return self.status.status_name


class Catalog(models.Model):
    catalog_name = models.CharField(max_length=100, verbose_name=u'Название каталога', unique=False)
    catalog_purchase = models.ForeignKey(Purchase)
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)

    def __unicode__(self):
        return self.catalog_name

    def url(self):
        return '%s/catalog-%s' % (self.catalog_purchase.url(), self.id)

    def url_core(self):
        return '%s/catalog-%s' % (self.catalog_purchase.url_core(), self.id)

    def get_products_count(self):
        products = Product.objects.filter(catalog=self.id)
        return len(products)

    def get_products(self):
        products = Product.objects.filter(catalog=self.id)
        for product in products:
            try:
                product.image = ProductImages.objects.filter(p_image_product=product.id)[0].url()
            except:
                product.image = '/static/images/none_image.png'
        return products


# Товары
class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name=u'Название товара')
    description = models.TextField(verbose_name=u'Описание товара')
    price = models.FloatField(verbose_name=u'Цена')
    sku = models.IntegerField(verbose_name=u'Артикул',null=True,blank=True)
    catalog = models.ForeignKey(Catalog, verbose_name=u'Выбрать каталог')
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)
    property = models.TextField(default='', verbose_name=u'Свойства товара')

    def url(self):
        return '%s/product-%s' % (self.catalog.url(), self.id)

    def url_core(self):
        return '%s/product-%s' % (self.catalog.url_core(), self.id)

    def __unicode__(self):
        return self.product_name

    def get_image(self):
        return ProductImages.objects.filter(p_image_product=self.id).first()

    def get_all_image(self):
        return ProductImages.objects.filter(p_image_product=self.id)

    # def get_properties(self):
    #     return Properties.objects.get(properties_product=self.id)


class ProductImages(models.Model):
    image = models.ImageField(_(u'Image'), upload_to='product/',
                             help_text=u'Изображение', blank=True)
    cropping = ImageRatioField('image', '500x320', verbose_name=u'Обрезка для продукта')
    p_image_product = models.ForeignKey(Product, verbose_name=u'Выбрать товар')
    p_image_title = models.CharField(u'Название', blank=True, null=True, max_length=255)
    def url(self):
        if self.image and self.image != '':
            return "/media/%s" % self.image
        else:
            return '/static/images/none_image.png'


class CatalogProductProperties(models.Model):
    cpp_name = models.CharField(max_length=100, verbose_name=u'Свойство товара в каталоге', unique=False)
    cpp_slug = models.CharField(null=True, max_length=255, blank=True)
    cpp_values = models.CharField(max_length=255, verbose_name=u'Возможные значения')
    cpp_catalog = models.ForeignKey(Catalog)

    def __unicode__(self):
        return self.cpp_name

    def save(self):
        self.cpp_slug = translit(self.cpp_name).lower() + '-cat-' + str(self.cpp_catalog.id)
        super(CatalogProductProperties, self).save()



# class Properties(models.Model):
#     properties_value = models.CharField(max_length=100, verbose_name=u'Значения свойства товара')
#     properties_product = models.ForeignKey(Product)
#     properties_catalogProductProperties = models.ForeignKey(CatalogProductProperties)
#
#     def __unicode__(self):
#         return self.properties_value
#

class ImportFiles(models.Model):
    file = models.FileField(verbose_name=u'Файл для импорта товаров в каталог', upload_to='import_xls')
    import_catalog = models.ForeignKey(Catalog)

    def __unicode__(self):
        return self.import_catalog.catalog_name