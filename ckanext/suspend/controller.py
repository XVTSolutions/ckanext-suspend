import ckan
import ckan.lib.helpers as h
import ckan.plugins as plugins
from ckan.lib.base import BaseController
from ckan.lib.helpers import flash_error, flash_success, flash_notice

class SuspendController(BaseController):
    """
    ckanext-suspend controller
    """

    def bad_url(self):
        flash_notice('please form URL in this format: http://<your_website>/clone/<dataset_name>')
        #return plugins.toolkit.render('bad_url.html')
        return plugins.toolkit.render('suspend/index.html')

    def index(self, id):
        
        context = {
                   'user': plugins.toolkit.c.user or plugins.toolkit.c.author,
                   'auth_user_obj': plugins.toolkit.c.userobj,
                   }
        data_dict = {'id': id}
        
        if ckan.plugins.toolkit.request.method == 'POST':
            #clone dataset and redirect to edit screen
            
            try:
                plugins.toolkit.check_access('package_update', context, data_dict)
            except plugins.toolkit.NotAuthorized:
                plugins.toolkit.abort(401, plugins.toolkit._('Unauthorized to update a package'))
                
            #get current package...
            pkg_dict = plugins.toolkit.get_action('package_show')(None, data_dict)
            
            #update necessary fields
            pkg_dict['type'] = 'dataset-suspended'
#             if 'extras' not in pkg_dict:
#                 pkg_dict['extras'] = []
#             pkg_dict['extras'].append({ 'key' :'suspend_reason', 'value' : ckan.plugins.toolkit.request.params.getone('suspend_reason') })

            reason = ckan.plugins.toolkit.request.params.getone('suspend_reason')
            if reason is None or reason == '':
                vars = {
                    'errors': { 'suspend_reason' : [ plugins.toolkit._('Reason to suspend dataset is required') ] },
                    'data': { 
                             'suspend_reason' : reason
                             }
                    }
    
                plugins.toolkit.c.pkg_dict = pkg_dict
                plugins.toolkit.c.pkg = context['package']
                return plugins.toolkit.render("suspend/index.html", extra_vars = vars)
        
            pkg_dict['suspend_reason'] = reason
                        
            #update...
            plugins.toolkit.get_action('package_update')(context, pkg_dict)

            ckan.plugins.toolkit.redirect_to(controller="package", action="read", id=pkg_dict['name'])
        else :
    
            try:
                plugins.toolkit.check_access('package_update', context, data_dict)
            except plugins.toolkit.ObjectNotFound:
                plugins.toolkit.abort(404, plugins.toolkit._('Dataset not found'))
            except plugins.toolkit.NotAuthorized:
                plugins.toolkit.abort(401, plugins.toolkit._('Unauthorized to update package %s') % id)
    
            try:
                plugins.toolkit.c.pkg_dict = plugins.toolkit.get_action('package_show')(context, data_dict)
                plugins.toolkit.c.pkg = context['package']
                plugins.toolkit.c.resources_json = h.json.dumps(plugins.toolkit.c.pkg_dict.get('resources', []))
            except plugins.toolkit.ObjectNotFound:
                plugins.toolkit.abort(404, plugins.toolkit._('Dataset not found'))
            except plugins.toolkit.NotAuthorized:
                plugins.toolkit.abort(401, plugins.toolkit._('Unauthorized to read package %s') % id)
                
            vars = {
                    'errors': {},
                    'data': { 
                             'suspend_reason' : plugins.toolkit.c.pkg_dict['suspend_reason'] if 'suspend_reason' in plugins.toolkit.c.pkg_dict else ''
                             }
                    }
    
            return plugins.toolkit.render("suspend/index.html", extra_vars = vars)
