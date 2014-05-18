#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from menutia.models import Menu, MenuItem

register = template.Library()

def do_menu(parser, token):
    bits = token.split_contents()[1:]
    if len(bits) != 3 or bits[1] != 'as':
        raise template.TemplateSyntaxError('Invalid syntax. Usage: {%% %s <title> as varname %%}')
    nodelist = parser.parse(('endmenu',))
    parser.delete_first_token()

    this_menu = Menu.objects.get(title=bits[0])

    extra_context = {bits[2]: [ ]}
    return MenuNode(this_menu,bits[2],nodelist)

class MenuNode(template.Node):
    def __init__(self,menu,varname,nodelist):
        self.nodelist = nodelist
        self.varname = varname
        self.menu = menu

    def __repr__(self):
        return "<MenuNode>"

    def render(self,context):
        lis = []
        for menu_item in self.menu.items.all():
            menu_item.selected = menu_item.match_url(context)
            lis.append(mark_safe( render_to_string("menutia/li.html", {"self": menu_item, "request": context['request']} ) ) )

        context.update({self.varname: lis})
        output = self.nodelist.render(context)

        return mark_safe(render_to_string("menutia/ul.html", {"self": self.menu, "content": output}))

register.tag('menu', do_menu)