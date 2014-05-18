#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as site_settings
from django.utils.translation import ugettext, ugettext_lazy as _

from modelcluster.models import ClusterableModel
from modelcluster.fields import ParentalKey

from wagtail.wagtailcore.models import Page, Orderable
from wagtail.wagtailadmin.edit_handlers import FieldPanel, MultiFieldPanel, InlinePanel, PageChooserPanel, ObjectList

from wagtail.wagtailsnippets.edit_handlers import SnippetChooserPanel
from wagtail.wagtailsnippets.models import register_snippet

from menutia import settings


class MenuItem(Orderable):
    menu = ParentalKey('menutia.Menu', related_name="items")

    text = models.CharField(max_length=255, blank=True)
    page = models.ForeignKey(Page)

    html_li_id = models.CharField(max_length=255, blank=True)
    match_exact = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s > %s" % (self.menu.__unicode__(), self.text)

    def get_match_test_function(self):
        if self.exact_match:
            return operator.__eq__
        else:
            return unicode.startswith

    def match_url(self,path):
        tester = self.get_match_test_function()
        url = self.get_url
        return tester(request_url,url)

    panels = [
        FieldPanel('text'),
        PageChooserPanel('page'),
        FieldPanel('html_li_id'),
        FieldPanel('match_exact'),
    ]

class Menu(ClusterableModel):
    title = models.CharField(max_length=255, unique=True,
        help_text="The title as it will be called from templates")

    html_ul_id = models.CharField(max_length=255, blank=True)
    html_li_selected_class = models.CharField(max_length=255, blank=True, default="selected")

panels = [
    FieldPanel('title'),
    FieldPanel('html_ul_id'),
    FieldPanel('html_li_selected_class'),
    InlinePanel(Menu,'items')
]

register_snippet(Menu)

