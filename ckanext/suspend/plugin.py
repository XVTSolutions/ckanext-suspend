import ckan.logic.auth as logic_auth
import ckan.plugins as plugins
import ckan.plugins.toolkit as tk


def _package_update(context, data_dict=None):
    package = logic_auth.get_package_object(context, data_dict)
    if (not package.type == 'dataset-suspended'):
        return logic_auth.update.package_update(context, data_dict)
    else:
        return {'success': False, 'msg': 'Not allowed to update suspended packages'}

class SuspendPlugin(plugins.SingletonPlugin, tk.DefaultDatasetForm):
    """
    Setup plugin
    """
    plugins.implements(plugins.IRoutes, inherit=True)
    plugins.implements(plugins.IConfigurer, inherit=True)
    plugins.implements(plugins.IDatasetForm, inherit=False)
    plugins.implements(plugins.IAuthFunctions)
    
    def before_map(self, map):

        map.connect('suspend', '/suspend',
            controller='ckanext.suspend.controller:SuspendController',
            action='bad_url')

        map.connect('suspend', '/suspend/{id}',
            controller='ckanext.suspend.controller:SuspendController',
            action='index')

        return map
    
    def update_config(self, config):
        plugins.toolkit.add_template_directory(config, 'templates')
        
        
        
        
    def is_fallback(self):
        return False
    
    def package_types(self):
        return ['dataset-suspended']
    
    def _modify_package_schema(self, schema):
        schema.update({
                'suspend_reason': [tk.get_validator('ignore_missing'),
                    tk.get_converter('convert_to_extras')]
                })
        return schema
    
    def create_package_schema(self):
        schema = super(SuspendPlugin, self).create_package_schema()
        #schema = self._modify_package_schema(schema)
        return schema

    def update_package_schema(self):
        schema = super(SuspendPlugin, self).update_package_schema()
        schema = self._modify_package_schema(schema)
        return schema

    def show_package_schema(self):
        schema = super(SuspendPlugin, self).show_package_schema()
        
        schema['tags']['__extras'].append(tk.get_converter('free_tags_only'))

        schema.update({
            'suspend_reason': [tk.get_converter('convert_from_extras'),
                tk.get_validator('ignore_missing')]
            })

        return schema

    def setup_template_variables(self, context, data_dict):
        return super(SuspendPlugin, self).setup_template_variables(context, data_dict)

    def new_template(self):
        return super(SuspendPlugin, self).new_template()

    def read_template(self):
        return super(SuspendPlugin, self).read_template()

    def edit_template(self):
        return super(SuspendPlugin, self).edit_template()

    def search_template(self):
        return super(SuspendPlugin, self).search_template()

    def history_template(self):
        return super(SuspendPlugin, self).history_template()

    def package_form(self):
        return super(SuspendPlugin, self).package_form()
        


    def get_auth_functions(self):
        return {'package_update': _package_update}