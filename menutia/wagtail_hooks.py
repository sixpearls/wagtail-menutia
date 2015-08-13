from wagtail.wagtailadmin.menu import MenuItem
from wagtail.wagtailcore import hooks
from django.core import urlresolvers
from django.utils.translation import ugettext_lazy as _

@hooks.register('register_admin_menu_item')
def register_menutia_admin_item():
    return MenuItem(_('Menutia'), 
        urlresolvers.reverse('wagtailsnippets_list', 
            args=['menutia', 'menu',]),
        classnames='icon icon-list-ul', order=900)
