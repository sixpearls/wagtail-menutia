# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import modelcluster.fields


class Migration(migrations.Migration):

    dependencies = [
        ('wagtailcore', '0013_update_golive_expire_help_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text=b'The title as it will be called from templates', unique=True, max_length=255)),
                ('html_ul_id', models.CharField(max_length=255, blank=True)),
                ('html_ul_class', models.CharField(max_length=255, blank=True)),
                ('html_li_selected_class', models.CharField(default=b'selected', max_length=255, blank=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sort_order', models.IntegerField(null=True, editable=False, blank=True)),
                ('text', models.CharField(max_length=255, blank=True)),
                ('html_li_id', models.CharField(max_length=255, blank=True)),
                ('html_li_class', models.CharField(max_length=255, blank=True)),
                ('exact_match', models.BooleanField(default=True)),
                ('menu', modelcluster.fields.ParentalKey(related_name='items', to='menutia.Menu')),
                ('page', models.ForeignKey(to='wagtailcore.Page')),
            ],
            options={
                'ordering': ['sort_order'],
                'abstract': False,
            },
            bases=(models.Model,),
        ),
    ]
