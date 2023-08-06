'''
Author: Alex
LastEditors: Alex yxfacw@163.com
Date: 2023-07-18 18:05:25
Description:  
'''
from pkg_resources import parse_version
from configparser import ConfigParser
from setuptools import setup
import setuptools
assert parse_version(setuptools.__version__) >= parse_version('36.2')

# note: 相关参数在 setup.ini 中设置
config = ConfigParser(delimiters=['='])
config.read('setup.ini')
cfg = config['DEFAULT']

cfg_keys = 'version description keywords author author_email'.split()
expected = cfg_keys + \
    "name branch license status min_python audience language".split()
for o in expected:
    assert o in cfg, "missing expected setting: {}".format(o)
setup_cfg = {o: cfg[o] for o in cfg_keys}

statuses = ['1 - Planning', '2 - Pre-Alpha', '3 - Alpha',
            '4 - Beta', '5 - Production/Stable', '6 - Mature', '7 - Inactive']
py_versions = '3.6 3.7 3.8 3.9 3.10'.split()

requirements = cfg.get('requirements', '').split()
min_python = cfg['min_python']

setup(
    name=cfg['name'],
    license=open('LICENSE').read(),
    classifiers=[
        'Development Status :: ' + statuses[int(cfg['status'])],
        'Intended Audience :: ' + cfg['audience'].title(),
        'License :: OSI Approved :: MIT License',
        'Natural Language :: ' + cfg['language'].title(),
    ] + ['Programming Language :: Python :: '+o for o in py_versions[py_versions.index(min_python):]],
    url=cfg['git_url'],
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=requirements,
    dependency_links=cfg.get('dep_links', '').split(),
    python_requires='>=' + cfg['min_python'],
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    zip_safe=False,
    entry_points={'console_scripts': cfg.get('console_scripts', '').split()},
    **setup_cfg)
