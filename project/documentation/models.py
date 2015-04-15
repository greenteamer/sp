# -*- coding: utf-8 -*-
#!/usr/bin/env python

from django.db import models


class Documentation(models.Model):
    name = models.CharField(verbose_name=u'Название раздела документации', max_length=240)
    description = models.TextField(verbose_name=u'Описание раздела документации')

    def __unicode__(self):
        return self.name