# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from project.accounts.models import OrganizerProfile
from django.utils.text import slugify
from project.core.functions import *
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink


# Категории
# class Category(MPTTModel):
#     name = models.CharField(verbose_name=u'Name', max_length=50, unique=True)
#     parent = TreeForeignKey('self', verbose_name=u'Родительская категория',
#                             related_name='children', blank=True,
#                             help_text=u'Родительская категория для текущей категоири', null=True)
#
#     def __unicode__(self):
#         return self.name


class CommonActiveManager(models.Manager):
    """Класс менеджер для фильтрации активных объектов"""
    def get_query_set(self):
        return super(CommonActiveManager, self).get_query_set().filter(is_active=True)


class Category(MPTTModel):
    """Класс для категорий товаров"""
    name = models.CharField(_(u'Name'), max_length=50, unique=True)
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
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)
    parent = TreeForeignKey('self', verbose_name=_(u'Parent category'),
                            related_name='children', blank=True,
                            help_text=_(u'Parent-category for current category'), null=True)
    active = CommonActiveManager()

    class Meta:
        # db_table = 'categories'
        ordering = ['-created_at']
        verbose_name_plural = _(u'Категории')

    # It is required to rebuild tree after save, when using order for mptt-tree
    # def save(self, *args, **kwargs):
    #     super(Category, self).save(*args, **kwargs)
    #     Category.objects.rebuild()

    def __unicode__(self):
        # return self.name
        return '%s%s' % ('--' * self.level, self.name)

    @permalink
    def get_absolute_url(self):
         #Генерация постоянных ссылок на категории
        return('category', (), {'category_slug': self.slug})


#  возвращает число на 1 больше чем максимальныое занчение ПриоритетаЗакупки во всех закупках
def get_next_status_priority():
    try:
        max_status_priority = PurchaseStatus.objects.order_by('-status_priority')[0]
        return max_status_priority.status_priority + 1
    except:
        return 0

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
    # purchase_status = models.ForeignKey(PurchaseStatus, verbose_name=u'Статус закупки', default=PurchaseStatus.objects.get(id=6) )
    purchase_status = models.ForeignKey(PurchaseStatus, verbose_name=u'Статус закупки', default=PurchaseStatus.objects.order_by('-status_priority')[0] )

    categories = models.ManyToManyField(Category, verbose_name=_(u'Categories'),
                                        help_text=_(u'Categories for product'))
    def __unicode__(self):
        return self.name

    def get_catalogs(self):
        return Catalog.objects.filter(catalog_purchase=self.id)

    def url(self):
        return '/profile/organizer/purchase-%s' % self.id
    def url_core(self):
        return '/purchase-%s' % self.id


class Catalog(models.Model):
    catalog_name = models.CharField(max_length=100, verbose_name=u'Название каталога')
    catalog_purchase = models.ForeignKey(Purchase)
    created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)

    def __unicode__(self):
        return self.catalog_name

    def url(self):
        return '%s/catalog-%s' % (self.catalog_purchase.url(), self.id)
    def url_core(self):
        return '%s/catalog-%s' % (self.catalog_purchase.url_core(), self.id)

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

    def url(self):
        return '%s/product-%s' % (self.catalog.url(), self.id)

    def url_core(self):
        return '%s/product-%s' % (self.catalog.url_core(), self.id)

    def __unicode__(self):
        return self.product_name

    def get_all_image(self):
        return ProductImages.objects.filter(p_image_product=self.id)


class ProductImages(models.Model):
    image = models.FileField(_(u'Image'), upload_to='product/',
                             help_text=u'Изображение', blank=True)
    p_image_product = models.ForeignKey(Product, verbose_name=u'Выбрать товар')
    # p_image_title = models.CharField(u'Название', blank=True, null=True, max_length=255)
    def url(self):
        if self.image and self.image != '':
            return "/media/%s" % self.image
        else:
            return '/static/images/none_image.png'


class CatalogProductProperties(models.Model):
    cpp_name = models.CharField(max_length=100, verbose_name=u'Свойство товара в каталоге', unique=True)
    cpp_slug = models.CharField(null=True, max_length=255, blank=True)
    cpp_values = models.CharField(max_length=255, verbose_name=u'Возможные значения')
    cpp_catalog = models.ForeignKey(Catalog)
    cpp_purchase = models.ForeignKey(Purchase)  # зачем привязка к закупке если есть привязка к каталогу?..

    def __unicode__(self):
        return self.cpp_name

    def save(self):
        self.cpp_slug = translit(self.cpp_name).lower()
        super(CatalogProductProperties, self).save()


class Properties(models.Model):
    properties_value = models.CharField(max_length=100, verbose_name=u'Значения свойства товара')
    properties_product = models.ForeignKey(Product)
    properties_catalogProductProperties = models.ForeignKey(CatalogProductProperties)

    def __unicode__(self):
        return self.properties_value



