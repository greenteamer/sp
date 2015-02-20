# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Category'
        db.create_table(u'core_category', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=50)),
            ('parent', self.gf('mptt.fields.TreeForeignKey')(blank=True, related_name='children', null=True, to=orm['core.Category'])),
            (u'lft', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'rght', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'tree_id', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
            (u'level', self.gf('django.db.models.fields.PositiveIntegerField')(db_index=True)),
        ))
        db.send_create_signal(u'core', ['Category'])

        # Adding model 'Purchase'
        db.create_table(u'core_purchase', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'core', ['Purchase'])

        # Adding model 'Catalog'
        db.create_table(u'core_catalog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Purchase'])),
        ))
        db.send_create_signal(u'core', ['Catalog'])

        # Adding model 'Product'
        db.create_table(u'core_product', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('catalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Catalog'])),
        ))
        db.send_create_signal(u'core', ['Product'])

        # Adding model 'CatalogProductProperties'
        db.create_table(u'core_catalogproductproperties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('values', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('catalog', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Catalog'])),
            ('purchase', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Purchase'])),
        ))
        db.send_create_signal(u'core', ['CatalogProductProperties'])

        # Adding model 'Properties'
        db.create_table(u'core_properties', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('product', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Product'])),
            ('catalogProductProperties', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.CatalogProductProperties'])),
        ))
        db.send_create_signal(u'core', ['Properties'])


    def backwards(self, orm):
        # Deleting model 'Category'
        db.delete_table(u'core_category')

        # Deleting model 'Purchase'
        db.delete_table(u'core_purchase')

        # Deleting model 'Catalog'
        db.delete_table(u'core_catalog')

        # Deleting model 'Product'
        db.delete_table(u'core_product')

        # Deleting model 'CatalogProductProperties'
        db.delete_table(u'core_catalogproductproperties')

        # Deleting model 'Properties'
        db.delete_table(u'core_properties')


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
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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