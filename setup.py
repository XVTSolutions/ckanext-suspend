from setuptools import setup, find_packages
import sys, os

version = '0.1'

setup(
	name='ckanext-suspend',
	version=version,
	description="",
	long_description="""\
	""",
	classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
	keywords='',
	author='Andrew Dean',
	author_email='andrew at xvt.com.au',
	url='',
	license='',
	packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
	include_package_data=True,
	zip_safe=False,
	install_requires=[
		# -*- Extra requirements: -*-
	],
	entry_points=\
	"""
        [ckan.plugins]
	suspend=ckanext.suspend.plugin:SuspendPlugin
	""",
)
