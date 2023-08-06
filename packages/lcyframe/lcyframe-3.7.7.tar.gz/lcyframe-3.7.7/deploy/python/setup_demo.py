# -*- coding:utf-8 -*-
import os
from setuptools import setup, find_packages

name = "lcyframe"
version = "3.7.6"

setup(name=name,
      version=version,
      description="A Fast ApiServer Frame for python3",
      long_description="",
      classifiers=[],
      keywords=name,
      author="lcylln",
      author_email="123220663@qq.com",
      url='',
      license='',
      platforms='any',
      packages=find_packages(),
      zip_safe=False,
      include_package_data=True,
      entry_points={
            "console_scripts": [
                "test = lcyframe.commands:test1",
                "test2 = lcyframe.commands:test2",
            ]
      },
     # entry_points={
     #        'console_scripts': [
     #            '%s = %s.__main__:main' % (name, name),
     #        ]
     #    },
      install_requires=[
          'tornado==5.0',
      ],

)

# pip安装成功后，会在当前python环境的/bin下生成一个lcyframe可执行文件，内容如下。
"""
#!/Users/apple/python/caih/python39-with-lcyframe/bin/python
# EASY-INSTALL-ENTRY-SCRIPT: 'lcyframe==3.7.5','console_scripts','lcyframe'
import re
import sys

# for compatibility with easy_install; see #2198
__requires__ = 'lcyframe==3.7.5'

try:
    from importlib.metadata import distribution
except ImportError:
    try:
        from importlib_metadata import distribution
    except ImportError:
        from pkg_resources import load_entry_point


def importlib_load_entry_point(spec, group, name):
    dist_name, _, _ = spec.partition('==')
    matches = (
        entry_point
        for entry_point in distribution(dist_name).entry_points
        if entry_point.group == group and entry_point.name == name
    )
    return next(matches).load()


globals().setdefault('load_entry_point', importlib_load_entry_point)


if __name__ == '__main__':
    sys.argv[0] = re.sub(r'(-script\.pyw?|\.exe)?$', '', sys.argv[0])
    sys.exit(load_entry_point('lcyframe==3.7.5', 'console_scripts', 'lcyframe')())

"""
