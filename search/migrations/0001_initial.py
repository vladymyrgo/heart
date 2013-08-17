# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Cities'
        db.create_table(u'search_cities', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('city', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20L)),
        ))
        db.send_create_signal(u'search', ['Cities'])

        # Adding model 'Names'
        db.create_table(u'search_names', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=20L)),
        ))
        db.send_create_signal(u'search', ['Names'])

        # Adding model 'Terms'
        db.create_table(u'search_terms', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(max_length=20L)),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=100L)),
        ))
        db.send_create_signal(u'search', ['Terms'])

        # Adding model 'Units'
        db.create_table(u'search_units', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('unit', self.gf('django.db.models.fields.CharField')(max_length=5L)),
        ))
        db.send_create_signal(u'search', ['Units'])

        # Adding model 'Links'
        db.create_table(u'search_links', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('link', self.gf('django.db.models.fields.CharField')(unique=True, max_length=2000L)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=2000L)),
            ('sum_words', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_unique_words', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_terms', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_names', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_units', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_cities', self.gf('django.db.models.fields.IntegerField')()),
            ('sum_percent', self.gf('django.db.models.fields.IntegerField')()),
            ('add_time', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'search', ['Links'])


    def backwards(self, orm):
        # Deleting model 'Cities'
        db.delete_table(u'search_cities')

        # Deleting model 'Names'
        db.delete_table(u'search_names')

        # Deleting model 'Terms'
        db.delete_table(u'search_terms')

        # Deleting model 'Units'
        db.delete_table(u'search_units')

        # Deleting model 'Links'
        db.delete_table(u'search_links')


    models = {
        u'search.cities': {
            'Meta': {'object_name': 'Cities'},
            'city': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        },
        u'search.links': {
            'Meta': {'object_name': 'Links'},
            'add_time': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'link': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2000L'}),
            'sum_cities': ('django.db.models.fields.IntegerField', [], {}),
            'sum_names': ('django.db.models.fields.IntegerField', [], {}),
            'sum_percent': ('django.db.models.fields.IntegerField', [], {}),
            'sum_terms': ('django.db.models.fields.IntegerField', [], {}),
            'sum_unique_words': ('django.db.models.fields.IntegerField', [], {}),
            'sum_units': ('django.db.models.fields.IntegerField', [], {}),
            'sum_words': ('django.db.models.fields.IntegerField', [], {}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '2000L'})
        },
        u'search.names': {
            'Meta': {'object_name': 'Names'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '20L'})
        },
        u'search.terms': {
            'Meta': {'object_name': 'Terms'},
            'category': ('django.db.models.fields.CharField', [], {'max_length': '20L'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '100L'})
        },
        u'search.units': {
            'Meta': {'object_name': 'Units'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'unit': ('django.db.models.fields.CharField', [], {'max_length': '5L'})
        }
    }

    complete_apps = ['search']