#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, ObjectList

from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

import operator

class MenuItem(Orderable):
    menu = ParentalKey('menutia.Menu', related_name="items")

    text = models.CharField(max_length=255, blank=True)
    page = models.ForeignKey(Page)

    html_li_id = models.CharField(max_length=255, blank=True)
    html_li_class = models.CharField(max_length=255, blank=True)
    exact_match = models.BooleanField(default=True)

    @python_2_unicode_compatible
    def __unicode__(self):
        return "%s > %s" % (self.menu.__unicode__(), self.text)

    def get_match_test_function(self):
        if self.exact_match:
            return operator.__eq__
        else:
            return str.startswith

    def match_url(self,context):
        path = u''
        try:
            path = context['request'].path
        except:
            return False

        tester = self.get_match_test_function()
        url = self.page.relative_url(context['request'].site)
        return tester(path,url)

    panels = [
        FieldPanel('text'),
        PageChooserPanel('page'),
        FieldPanel('html_li_id'),
        FieldPanel('exact_match'),
    ]

@register_snippet
class Menu(ClusterableModel):
    title = models.CharField(max_length=255, unique=True,
        help_text="The title as it will be called from templates")

    html_ul_id = models.CharField(max_length=255, blank=True)
    html_ul_class = models.CharField(max_length=255, blank=True)
    html_li_selected_class = models.CharField(max_length=255, blank=True, default="selected")

    @python_2_unicode_compatible
    def __str__(self):
        return self.title

    panels = [
        FieldPanel('title'),
        FieldPanel('html_ul_id'),
        FieldPanel('html_li_selected_class'),
        InlinePanel('items',label='Menu items')
    ]

