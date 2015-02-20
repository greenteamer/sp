# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Product.description'
        db.add_column(u'core_product', 'description',
                      self.gf('django.db.models.fields.TextField')(default=''),
                      keep_default=False)

        # Adding field 'Product.price'
        db.add_column(u'core_product', 'price',
                      self.gf('django.db.models.fields.FloatField')(default=0.0),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Product.description'
        db.delete_column(u'core_product', 'description')

        # Deleting field 'Product.price'
        db.delete_column(u'core_product', 'price')


    models = {
        u'core.catalog': {
            'Meta': {'object_name': 'Catalog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Purchase']"})
        },
        u'core.catalogproductproperties': {
            'Meta': {'object_name': 'CatalogProductProperties'},
            'catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Catalog']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'purchase': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Purchase']"}),
            'values': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        u'core.category': {
            'Meta': {'object_name': 'Category'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            u'level': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'lft': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'parent': ('mptt.fields.TreeForeignKey', [], {'blank': 'True', 'related_name': "'children'", 'null': 'True', 'to': u"orm['core.Category']"}),
            u'rght': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'}),
            u'tree_id': ('django.db.models.fields.PositiveIntegerField', [], {'db_index': 'True'})
        },
        u'core.product': {
            'Meta': {'object_name': 'Product'},
            'catalog': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Catalog']"}),
            'description': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'price': ('django.db.models.fields.FloatField', [], {})
        },
        u'core.properties': {
            'Meta': {'object_name': 'Properties'},
            'catalogProductProperties': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.CatalogProductProperties']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'product': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Product']"})
        },
        u'core.purchase': {
            'Meta': {'object_name': 'Purchase'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['core']