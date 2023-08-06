# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

from aldryn_translation_tools import __version__


REQUIREMENTS = [
    'django-cms>=3.11',
    'django-parler>=1.9.2',
    'python-slugify>=1.2.6',
]


setup(
    name='djangocms-aldryn-translation-tools',
    version=__version__,
    description='Collection of helpers and mixins for translated projects.',
    long_description=open('README.rst').read(),
    long_description_content_type='text/x-rst',
    author='Divio AG',
    author_email='info@divio.ch',
    url='https://github.com/CZ-NIC/djangocms-aldryn-translation-tools',
    packages=find_packages(exclude=['tests']),
    license='BSD License',
    platforms=['OS Independent'],
    install_requires=REQUIREMENTS,
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
    include_package_data=True,
    zip_safe=False,
    python_requires='>=3.7',
)
