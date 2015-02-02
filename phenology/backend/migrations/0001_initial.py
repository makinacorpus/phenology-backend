# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Species'
        db.create_table(u'backend_species', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('description', self.gf('django.db.models.fields.TextField')(max_length=500)),
            ('picture', self.gf('django.db.models.fields.files.ImageField')(default='no-img.jpg', max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Species'])

        # Adding model 'Area'
        db.create_table(u'backend_area', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('codezone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('polygone', self.gf('django.db.models.fields.CharField')(max_length=500)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.TextField')(max_length=100, blank=True)),
            ('commune', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Area'])

        # Adding M2M table for field species on 'Area'
        m2m_table_name = db.shorten_name(u'backend_area_species')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('area', models.ForeignKey(orm[u'backend.area'], null=False)),
            ('species', models.ForeignKey(orm[u'backend.species'], null=False))
        ))
        db.create_unique(m2m_table_name, ['area_id', 'species_id'])

        # Adding model 'Observer'
        db.create_table(u'backend_observer', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('fonction', self.gf('django.db.models.fields.CharField')(max_length=70)),
            ('adresse', self.gf('django.db.models.fields.TextField')(max_length=80)),
            ('codepostal', self.gf('django.db.models.fields.IntegerField')()),
            ('nationality', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('mobile', self.gf('django.db.models.fields.CharField')(max_length=20)),
            ('is_crea', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_active', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('date_inscription', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Observer'])

        # Adding M2M table for field areas on 'Observer'
        m2m_table_name = db.shorten_name(u'backend_observer_areas')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('observer', models.ForeignKey(orm[u'backend.observer'], null=False)),
            ('area', models.ForeignKey(orm[u'backend.area'], null=False))
        ))
        db.create_unique(m2m_table_name, ['observer_id', 'area_id'])

        # Adding model 'Individual'
        db.create_table(u'backend_individual', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Species'])),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Area'])),
            ('is_dead', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('lat', self.gf('django.db.models.fields.FloatField')()),
            ('lon', self.gf('django.db.models.fields.FloatField')()),
            ('altitude', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('circonference', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Individual'])

        # Adding model 'Snowing'
        db.create_table(u'backend_snowing', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('area', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Area'])),
            ('observer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Observer'])),
            ('date', self.gf('django.db.models.fields.DateTimeField')()),
            ('remark', self.gf('django.db.models.fields.CharField')(default='', max_length=100, blank=True)),
            ('height', self.gf('django.db.models.fields.FloatField')()),
            ('temperature', self.gf('django.db.models.fields.FloatField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Snowing'])

        # Adding model 'Stage'
        db.create_table(u'backend_stage', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('species', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Species'])),
            ('date_start', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('month_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day_start', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('date_end', self.gf('django.db.models.fields.DateField')(null=True, blank=True)),
            ('month_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('day_end', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('order', self.gf('django.db.models.fields.IntegerField')()),
            ('picture_before', self.gf('django.db.models.fields.files.ImageField')(default='no-img.jpg', max_length=100)),
            ('picture_current', self.gf('django.db.models.fields.files.ImageField')(default='no-img.jpg', max_length=100)),
            ('picture_after', self.gf('django.db.models.fields.files.ImageField')(default='no-img.jpg', max_length=100)),
        ))
        db.send_create_signal(u'backend', ['Stage'])

        # Adding model 'Survey'
        db.create_table(u'backend_survey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('individual', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Individual'])),
            ('stage', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['backend.Stage'])),
            ('answer', self.gf('django.db.models.fields.CharField')(max_length=300, blank=True)),
            ('date', self.gf('django.db.models.fields.DateField')()),
            ('remark', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
        ))
        db.send_create_signal(u'backend', ['Survey'])


    def backwards(self, orm):
        # Deleting model 'Species'
        db.delete_table(u'backend_species')

        # Deleting model 'Area'
        db.delete_table(u'backend_area')

        # Removing M2M table for field species on 'Area'
        db.delete_table(db.shorten_name(u'backend_area_species'))

        # Deleting model 'Observer'
        db.delete_table(u'backend_observer')

        # Removing M2M table for field areas on 'Observer'
        db.delete_table(db.shorten_name(u'backend_observer_areas'))

        # Deleting model 'Individual'
        db.delete_table(u'backend_individual')

        # Deleting model 'Snowing'
        db.delete_table(u'backend_snowing')

        # Deleting model 'Stage'
        db.delete_table(u'backend_stage')

        # Deleting model 'Survey'
        db.delete_table(u'backend_survey')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'backend.area': {
            'Meta': {'ordering': "['name']", 'object_name': 'Area'},
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'codezone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'commune': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'polygone': ('django.db.models.fields.CharField', [], {'max_length': '500'}),
            'remark': ('django.db.models.fields.TextField', [], {'max_length': '100', 'blank': 'True'}),
            'species': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['backend.Species']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'backend.individual': {
            'Meta': {'ordering': "['species', 'name']", 'object_name': 'Individual'},
            'altitude': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Area']"}),
            'circonference': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_dead': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'lat': ('django.db.models.fields.FloatField', [], {}),
            'lon': ('django.db.models.fields.FloatField', [], {}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Species']"})
        },
        u'backend.observer': {
            'Meta': {'object_name': 'Observer'},
            'adresse': ('django.db.models.fields.TextField', [], {'max_length': '80'}),
            'areas': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['backend.Area']", 'symmetrical': 'False', 'blank': 'True'}),
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'codepostal': ('django.db.models.fields.IntegerField', [], {}),
            'date_inscription': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'fonction': ('django.db.models.fields.CharField', [], {'max_length': '70'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_crea': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mobile': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'nationality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '20'}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        },
        u'backend.snowing': {
            'Meta': {'object_name': 'Snowing'},
            'area': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Area']"}),
            'date': ('django.db.models.fields.DateTimeField', [], {}),
            'height': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'observer': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Observer']"}),
            'remark': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '100', 'blank': 'True'}),
            'temperature': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'})
        },
        u'backend.species': {
            'Meta': {'ordering': "['name']", 'object_name': 'Species'},
            'description': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'picture': ('django.db.models.fields.files.ImageField', [], {'default': "'no-img.jpg'", 'max_length': '100'})
        },
        u'backend.stage': {
            'Meta': {'object_name': 'Stage'},
            'date_end': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'date_start': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'day_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'day_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'month_end': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'month_start': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'order': ('django.db.models.fields.IntegerField', [], {}),
            'picture_after': ('django.db.models.fields.files.ImageField', [], {'default': "'no-img.jpg'", 'max_length': '100'}),
            'picture_before': ('django.db.models.fields.files.ImageField', [], {'default': "'no-img.jpg'", 'max_length': '100'}),
            'picture_current': ('django.db.models.fields.files.ImageField', [], {'default': "'no-img.jpg'", 'max_length': '100'}),
            'species': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Species']"})
        },
        u'backend.survey': {
            'Meta': {'ordering': "['-date']", 'object_name': 'Survey'},
            'answer': ('django.db.models.fields.CharField', [], {'max_length': '300', 'blank': 'True'}),
            'date': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'individual': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Individual']"}),
            'remark': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'stage': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['backend.Stage']"})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['backend']