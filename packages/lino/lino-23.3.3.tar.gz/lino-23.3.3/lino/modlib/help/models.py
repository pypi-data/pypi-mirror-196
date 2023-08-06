# Copyright 2021 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from django.conf import settings
from django.utils.translation import get_language
from lino.core.actors import Actor
from lino.api import dd, _


class OpenHelpWindow(dd.Action):

    action_name = 'open_help'
    # icon_name = 'help'
    default_format = 'ajax'
    button_text = '?'
    select_rows = False
    help_text = _('Open Help Window')
    show_in_plain = True

    # def js_handler(self, actor):
    #     parts = ['cache', 'help']
    #     if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
    #         parts.append(get_language())
    #     parts.append(str(actor) + ".html")
    #     url = settings.SITE.build_site_cache_url(*parts)
    #     # return "let _ = window.open('%s');" % url
    #     # return "() => window.open('%s')" % url
    #     return "function (){window.open('%s')}" % url
    #     # return "window.open('%s')" % url

    def run_from_ui(self, ar, **kwargs):
        # print("20210612")
        parts = ['cache', 'help']
        if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
            parts.append(get_language())
        parts.append(str(ar.actor) + ".html")
        # parts.append("index.html")
        url = settings.SITE.build_site_cache_url(*parts)
        ar.set_response(success=True)
        ar.success(open_url=url)

    # def get_a_href_target(self):
    #     parts = ['cache', 'help']
    #     if get_language() != settings.SITE.DEFAULT_LANGUAGE.django_code:
    #         parts.append(get_language())
    #     parts.append("index.html")
    #     return settings.SITE.build_media_url(*parts)


if dd.plugins.help.make_help_pages:
    Actor.open_help = OpenHelpWindow()
