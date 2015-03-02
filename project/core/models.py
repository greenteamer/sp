# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
# from project.accounts.models import OrganizerProfile
from django.utils.text import slugify
from project.core.functions import *
from autoslug import AutoSlugField
from django.utils.translation import ugettext_lazy as _


# Категории
class Category(MPTTModel):
    name = models.CharField(verbose_name=u'Name', max_length=50, unique=True)
    parent = TreeForeignKey('self', verbose_name=u'Родительская категория',
                            related_name='children', blank=True,
                            help_text=u'Родительская категория для текущей категоири', null=True)

    def __unicode__(self):
        return self.name

class Purchase(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название закупки')
    description = models.TextField(verbose_name=u'Описание закупки')
    organizerProfile = models.ForeignKey('accounts.OrganizerProfile', verbose_name=u'Профиль организатора')
    date = models.DateField(auto_now_add=True)

    def __unicode__(self):
        return self.name

    def get_catalogs(self):
        return Catalog.objects.filter(catalog_purchase=self.id)

    def url(self):
        return '/profile/organizer/purchase-%s' % self.id


class Catalog(models.Model):
    catalog_name = models.CharField(max_length=100, verbose_name=u'Название каталога')
    catalog_purchase = models.ForeignKey(Purchase)

    def __unicode__(self):
        return self.catalog_name



# Товары
class Product(models.Model):
    product_name = models.CharField(max_length=100, verbose_name=u'Название товара')
    description = models.TextField(verbose_name=u'Описание товара')
    price = models.FloatField(verbose_name=u'Цена')
    sku = models.IntegerField(verbose_name=u'Артикул',null=True,blank=True)
    catalog = models.ForeignKey(Catalog, verbose_name=u'Выбрать каталог')

    def __unicode__(self):
        return self.product_name


class ProductImages(models.Model):
    image = models.FileField(_(u'Image'), upload_to='product/',
                             help_text=u'Изображение', blank=True)
    p_image_product = models.ForeignKey(Product, verbose_name=u'Выбрать товар')


class CatalogProductProperties(models.Model):
    cpp_name = models.CharField(max_length=100, verbose_name=u'Свойство товара в каталоге', unique=True)
    # cpp_slug = models.SlugField((u'Slug'), max_length=50, unique=True,
    #                         help_text=(u'Slug for product url created from name.'))
    # cpp_slug = models.SlugField(null=True, blank=True) # Allow blank submission in admin
    # cpp_slug = AutoSlugField(populate_from='cpp_name', unique=True)
    cpp_slug = models.CharField(null=True, max_length=255, blank=True)
    cpp_values = models.CharField(max_length=255, verbose_name=u'Возможные значения')
    cpp_catalog = models.ForeignKey(Catalog)
    cpp_purchase = models.ForeignKey(Purchase)  # зачем привязка к закупке если есть привязка к каталогу?..

    def __unicode__(self):
        return self.cpp_name

    def save(self):
        # if not self.id:
        self.cpp_slug = translit(self.cpp_name).lower()
        super(CatalogProductProperties, self).save()


class Properties(models.Model):
    properties_value = models.CharField(max_length=100, verbose_name=u'Значения свойства товара')
    properties_product = models.ForeignKey(Product)
    properties_catalogProductProperties = models.ForeignKey(CatalogProductProperties)

    def __unicode__(self):
        return self.properties_value



