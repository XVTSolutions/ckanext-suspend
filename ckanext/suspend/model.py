import ckan
from sqlalchemy import orm, Table, Column, types, ForeignKey
from ckan.model.meta import metadata

package_suspend_table = Table('package_suspend', metadata,
        Column('package_id', types.UnicodeText, ForeignKey('package.id'), primary_key=True),
        Column('reason', types.UnicodeText),
    )

class PackageSuspend(object):
    pass

#orm.mapper(PackageSuspend, package_suspend_table, properties={
#    'package': orm.relationship(ckan.model.Package, uselist=False)
#})
#m = orm.class_mapper(ckan.model.Package)
#m.add_property('package_suspend', orm.relationship(PackageSuspend, uselist=False))

orm.mapper(PackageSuspend, package_suspend_table)

def create_table():
    package_suspend_table.create(checkfirst=True)
        
def get_package_suspend(session, package_id):
    return session.query(PackageSuspend).filter(PackageSuspend.package_id == package_id).first()

def add_package_suspend(session, package_id, reason):
    model = PackageSuspend()
    
    model.package_id = package_id
    model.reason = reason
    
    session.add(model)
    
    session.flush()
    
def delete_package_suspend(session, package_id):
    model = get_package_suspend(session, package_id)
    if model:
        session.delete(model)
        session.flush()
    