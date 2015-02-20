# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey

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

    def __unicode__(self):
        return self.name

class Catalog(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название каталога')
    purchase = models.ForeignKey(Purchase)

    def __unicode__(self):
        return self.name

# Товары
class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Название товара')
    description = models.TextField(verbose_name=u'Описание товара')
    price = models.FloatField(verbose_name=u'Цена')
    catalog = models.ForeignKey(Catalog, verbose_name=u'Выбрать каталог')

    def __unicode__(self):
        return self.name

class CatalogProductProperties(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Свойства товара в каталоге')
    values = models.CharField(max_length=255, verbose_name=u'Возможные значения')
    catalog = models.ForeignKey(Catalog)
    purchase = models.ForeignKey(Purchase)

    def __unicode__(self):
        return self.name

class Properties(models.Model):
    name = models.CharField(max_length=100, verbose_name=u'Свойства товара')
    product = models.ForeignKey(Product)
    catalogProductProperties = models.ForeignKey(CatalogProductProperties)


    def __unicode__(self):
        return self.name







