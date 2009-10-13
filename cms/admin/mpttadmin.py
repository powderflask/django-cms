from cms import settings
from django.conf import settings as django_settings
from mptt.utils import tree_item_iterator
from os.path import join
from django.contrib import admin
from django.utils.encoding import force_unicode
            
def get_mptt_admin(admin_base):
    
    class RealMpttAdmin(admin_base):
        
        actions = None
        change_list_template = 'admin/mptt_change_list.html'
        list_display = ('edit_links', 'target_container')
            
        class Media:
            css = {
                'all': [join(settings.CMS_MEDIA_URL, path) for path in (
                    'css/rte.css',
                    'css/pages.css',
                    'css/change_form.css',
                    'css/jquery.dialog.css',
                )]
            }
            js = [join(settings.CMS_MEDIA_URL, path) for path in (
                'js/lib/jquery.js',
                'js/lib/jquery.query.js',
                'js/lib/ui.core.js',
                'js/lib/ui.dialog.js',
                
            )]
            
        def add_extra_to_results(self, results, request):
            
            if hasattr(super(RealMpttAdmin, self), 'add_extra_to_results'):
                extras = super(RealMpttAdmin, self).add_extra_to_results(results, request)
            else:
                extras = [{} for r in results]
            
            for index, result_structure in enumerate(tree_item_iterator(results)):
                extras[index]['structure'] = result_structure[1]
            
            return extras
        
        def edit_links(self, obj, extra):
            return u"""
            <a href="%i" class="title" title="edit this page">%s</a>	
            <a href="%i" class="changelink" title="edit this page">edit</a>
            """ % (obj.pk, force_unicode(obj), obj.pk)
            
        edit_links.allow_tags = True
        edit_links.takes_extra = True
        
        def target_container(self, obj, extra):
            return u"""
            <span id="move-target-%i" class="move-target-container">
                <a href="#" class="move-target left" title="insert above">
                    <img alt="" src="%s">
                </a>
                <span class="line first"> |
                </span>
                <a href="#" class="move-target right" title="insert below"><img alt="" src="%s"></a>
                <span class="line second"> |</span>
                    <a href="#" class="move-target last-child" title="insert inside"></a>
            </span>
            """ % (obj.pk, join(django_settings.ADMIN_MEDIA_PREFIX, 'img/admin/arrow-up.gif'), join(django_settings.ADMIN_MEDIA_PREFIX, 'img/admin/arrow-down.gif'))
            
        target_container.allow_tags = True      
        target_container.takes_extra = True
        
    return RealMpttAdmin
        
from cms.admin.pluginadmin import PluginAdmin
from cms.admin.translationadmin import TranslationAdmin, TranslationPluginAdmin

MpttAdmin = get_mptt_admin(admin.ModelAdmin)

MpttPluginAdmin = get_mptt_admin(PluginAdmin)

MpttTranslationAdmin = get_mptt_admin(TranslationPluginAdmin)

MpttTranslationPluginAdmin = get_mptt_admin(TranslationPluginAdmin)

if 'reversion' in settings.INSTALLED_APPS:
    
    from reversion.admin import VersionAdmin
    from cms.admin.pluginadmin import PluginVersionAdmin
    from cms.admin.translationadmin import TranslationVersionAdmin, TranslationPluginVersionAdmin

    MpttVersionAdmin = get_mptt_admin(VersionAdmin)
    
    MpttTranslationVersionAdmin = get_mptt_admin(TranslationVersionAdmin)
    
    MpttPluginVersionAdmin = get_mptt_admin(PluginVersionAdmin)
    
    MpttTranslationPluginVersionAdmin = get_mptt_admin(TranslationPluginVersionAdmin)