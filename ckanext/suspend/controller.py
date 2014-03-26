import ckan
import ckan.lib.helpers as h
import ckan.plugins as plugins
from ckan.lib.base import BaseController
from ckan.lib.helpers import flash_error, flash_success, flash_notice
from model import add_package_suspend, delete_package_suspend

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
            
            #validate
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
            
            #update necessary fields
            #pkg_dict['state'] += 'suspended'
            pkg_dict['state'] = 'suspended'
        
            #add package suspend
            add_package_suspend(ckan.model.Session, pkg_dict['id'], reason)
                                    
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
        
    def unsuspend(self, id):
        
        context = {
                   'user': plugins.toolkit.c.user or plugins.toolkit.c.author,
                   'auth_user_obj': plugins.toolkit.c.userobj,
                   'no_type_check': True
                   }
        data_dict = {'id': id}
        
        if ckan.plugins.toolkit.request.method == 'POST':
            try:
                plugins.toolkit.check_access('package_update', context, data_dict)
            except plugins.toolkit.NotAuthorized:
                plugins.toolkit.abort(401, plugins.toolkit._('Unauthorized to update a package'))
                
            #get current package...
            pkg_dict = plugins.toolkit.get_action('package_show')(None, data_dict)
            
            #update necessary fields
            #pkg_dict['state'] =  pkg_dict['state'].replace('suspended', '')  
            pkg_dict['state'] = 'active'
            delete_package_suspend(ckan.model.Session, pkg_dict['id'])
                        
            #update...
            plugins.toolkit.get_action('package_update')(context, pkg_dict)

            ckan.plugins.toolkit.redirect_to(controller="package", action="read", id=pkg_dict['name'])
        else :
    
            ckan.plugins.toolkit.redirect_to(controller="package", action="read", id=id)
