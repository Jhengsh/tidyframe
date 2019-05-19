from setuptools import setup, find_packages

LONG_DESCRIPTION = """
Overview
--------------

+ Clean Pandas DataFrame to tidy DataFrame
+ Goal: Help you to create **tidy Pandas Dataframe**
+ Wapper SQLAlchemy function to help you create table, insert table, drop table easily
+ Make tranform nest dictionary easily
+ Make select columns, reorder columns easily
+ Make coalesce columns easily
+ Wapper window function from DataFrame

"""

CLASSIFIERS = [
    'Development Status :: 5 - Production/Stable',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research', 'Programming Language :: Python',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7', 'Programming Language :: Cython',
    'Topic :: Scientific/Engineering'
]

setup(
    name='tidyframe',
    version=open('VERSION').read().strip(),
    author='Hsueh-Hung Cheng',
    author_email='jhengsh.email@gmail.com',
    url='https://github.com/Jhengsh/tidyframe',
    description='Clean pandas DataFrame to Tidy DataFrame',
    long_description=LONG_DESCRIPTION,
    classifiers=CLASSIFIERS,
    keywords=['pandas', 'tidy'],
    packages=find_packages(),
    license='MIT',
    platforms='any',
    python_requires='!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*,!=3.4.*',
    install_requires=["pandas", "funcy", "SQLAlchemy"],
)
