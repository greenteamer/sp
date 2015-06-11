# -*- coding: utf-8 -*-
#!/usr/bin/env python
from django.db import models
from ckeditor.fields import RichTextField


class Documentation(models.Model):
    name = models.CharField(
        verbose_name=u'Название раздела документации',
        max_length=240
    )
    description = RichTextField(
        verbose_name=u'Описание раздела документации')

    def __unicode__(self):
        return self.name


class Page(models.Model):
    name = models.CharField(
        verbose_name=u'Название страницы',
        max_length=240
    )
    description = RichTextField(
        verbose_name=u'Текст страницы')

    is_main = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name
