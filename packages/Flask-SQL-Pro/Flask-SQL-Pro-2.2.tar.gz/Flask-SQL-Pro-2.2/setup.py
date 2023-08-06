from setuptools import setup, find_packages

setup(
    name='Flask-SQL-Pro',
    version='2.2',
    description='旨在为写sql的程序拆分sql语句出程序中,分类管理。目前支持增删改查、分页、事务,以及flask项目中多数据库连接。',
    long_description=open('README.rst').read(),
    author='miaokela',
    author_email='2972799448@qq.com',
    maintainer='miaokela',
    maintainer_email='2972799448@qq.com',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'flask',
        'flask_sqlalchemy',
        'pyyaml',
    ],
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy'
    ],
)
