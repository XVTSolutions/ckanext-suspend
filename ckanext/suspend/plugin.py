import ckan
import ckan.logic.auth as logic_auth
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk
from ckan.logic import auth_sysadmins_check
from model import create_table, get_package_suspend

@auth_sysadmins_check
def _package_update(context, data_dict=None):
    package = logic_auth.get_package_object(context, data_dict)
    no_type_check = context['no_type_check'] if 'no_type_check' in context else False
    if (no_type_check) or ('suspended' not in package.state):
        return logic_auth.update.package_update(context, data_dict)
    else:
        return {'success': False, 'msg': 'Not allowed to update suspended packages'}

class SuspendPlugin(plugins.SingletonPlugin):
    """
    Setup plugin
    """
    print "loading ckanext-suspend"
    
    create_table()
    
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IPackageController, inherit=True)
    plugins.implements(plugins.IAuthFunctions)
    
    """
    IRoutes
    """
    def before_map(self, map):

        map.connect('suspend', '/suspend',
            controller='ckanext.suspend.controller:SuspendController',
            action='bad_url')

        map.connect('suspend', '/suspend/{id}',
            controller='ckanext.suspend.controller:SuspendController',
            action='index')
        
        map.connect('suspend', '/unsuspend/{id}',
            controller='ckanext.suspend.controller:SuspendController',
            action='unsuspend')

        return map
    
    """
    IConfigurer
    """
    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        
    """
    IPackageController
    """       
    def after_show(self, context, pkg_dict):
        model = get_package_suspend(ckan.model.Session, pkg_dict['id'])
        pkg_dict['suspend_reason'] = model.reason if model else ''
        
    def before_search(self, search_params):
        
        if not '+state:' in search_params['fq']:
            search_params['fq'] = "{fq}  +state:(active OR suspended)".format(fq=search_params['fq'])
        
        return search_params
        
    """   
    IAuthFunctions
    """ 
    def get_auth_functions(self):
        return {'package_update': _package_update, 'package_unsuspend': logic_auth.update.package_update}