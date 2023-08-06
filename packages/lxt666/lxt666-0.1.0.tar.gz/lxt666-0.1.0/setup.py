# 编写完包源码后，python setup.py sdist生成pip压缩包
# 解压压缩包，python setup.py install  安装自己的包，就可以引用了


from distutils.core import setup
from setuptools import find_packages

setup(name='lxt666',  # 包名
      version='0.1.0',  # 版本号
      description='',
      long_description='',
      author='garich',
      author_email='piggymaster@163.com',
      url='',
      license='',
      install_requires=[],
      classifiers=[
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'Natural Language :: Chinese (Simplified)',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Utilities'
      ],
      keywords='',
      packages=find_packages('src'),  # 必填
      package_dir={'': 'src'},  # 必填
      include_package_data=True,
      )