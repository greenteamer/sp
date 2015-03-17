# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from django.db.models import Model
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink


# Категории товаров
class Category(Model):
    category_name = models.CharField(_(u'Name'), max_length=50, unique=True)
    category_slug = models.SlugField(_(u'Slug'), max_length=50, unique=True,
                            help_text=_(u'Slug for product url created from name.'))
    category_description = models.TextField(_(u'Description'), blank=True)
    category_is_active = models.BooleanField(_(u'Active'), default=True)
    category_meta_keywords = models.CharField(_(u'Meta keywords'), max_length=255,
                                     help_text=_(u'Comma-delimited set of SEO keywords for meta tag'), blank=True)
    category_meta_description = models.CharField(_(u'Meta description'), max_length=255,
                                        help_text=_(u'Content for description meta tags'), blank=True)
    category_created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    category_updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)

    class Meta:
        ordering = ['-category_created_at']
        verbose_name_plural = _(u'Категории')

    def __unicode__(self):
        return self.category_name
        # return '%s%s' % ('--' * self.level, self.name)

    @permalink
    def url(self):
        return('pristroy_category', (), {'category_slug': self.category_slug})     #Генерация постоянных ссылок на категории


# Товары
class Product(Model):
    product_name = models.CharField(max_length=100, verbose_name=u'Название товара')
    product_description = models.TextField(verbose_name=u'Описание товара')
    product_price = models.FloatField(verbose_name=u'Цена')
    product_catalog = models.ForeignKey(Category, verbose_name=u'Выбрать категорию')
    product_created_at = models.DateTimeField(_(u'Created at'), null=True, auto_now_add=True)
    product_updated_at = models.DateTimeField(_(u'Updated at'), null=True, auto_now=True)
    class Meta:
        verbose_name_plural = _(u'Товары')
    def url(self):
        return '%s/product-%s' % (self.product_catalog.url(), self.id)

    def __unicode__(self):
        return self.product_name

    def get_all_image(self):
        return ProductImages.objects.filter(p_image_product=self.id)


class ProductImages(models.Model):
    image = models.FileField(_(u'Image'), upload_to='product/',
                             help_text=u'Изображение', blank=True)
    p_image_product = models.ForeignKey(Product, verbose_name=u'Выбрать товар')
    p_image_title = models.CharField(u'Название', blank=True, null=True, max_length=255)
    class Meta:
        verbose_name_plural = _(u'Изображения для товаров')
    def url(self):
        if self.image and self.image != '':
            return "/media/%s" % self.image
        else:
            return '/static/images/none_image.png'
