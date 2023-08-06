import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.md')) as readme:
    README = readme.read()


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf-schema-adapter',
    version='3.0.6',
    packages=['drf_auto_endpoint', 'export_app', 'export_app.management',
              'export_app.management.commands'],
    include_package_data=True,
    license='MIT License',
    description='Making using Django with frontend libraries and frameworks DRYer',
    long_description_content_type="text/markdown",
    long_description=README,
    url='https://github.com/drf-forms/drf-schema-adapter',
    author='Emmanuelle Delescolle, Adrien Brunet, Mauro Bianchi, Mattia Larentis, Aaron Elliot Ross',
    author_email='info@levit.be',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Framework :: Django :: 3.2',
        'Framework :: Django :: 4.0',
        'Framework :: Django :: 4.1',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
    ],
    install_requires=[
        'Django>=3.2',
        'djangorestframework>=3.12,<4.0',
        'django-filter>=0.13.0',
        'Inflector>=3.0.1',
        # This is the actual requirement for python 3.11 until release of Inflector 3.0.2
        # 'Inflector @ git+https://github.com/ixmatus/inflector@ef5c19dc2aa8df5e6b4c452ff2d9b54ec41a04a8#egg=Inflector',
    ]
)
