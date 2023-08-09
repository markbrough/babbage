from setuptools import setup, find_packages

exec(open('babbage/version.py', 'r').read())

with open('README.md') as f:
    long_description = f.read()

setup(
    name='babbage',
    version=__version__,
    description="A light-weight analytical engine for OLAP processing",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    keywords='sql sqlalchemy olap cubes analytics',
    author='Friedrich Lindenberg',
    author_email='friedrich@pudo.org',
    url='http://github.com/openspending/babbage',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    namespace_packages=[],
    include_package_data=True,
    package_data={
        '': ['babbage/schema/model.json', 'babbage/schema/parser.ebnf']
    },
    zip_safe=False,
    install_requires=[
        'normality >= 0.2.2',
        'PyYAML >= 3.10',
        'six >= 1.7.3',
        'flask == 2.*', # Higher versions break tests
        'jsonschema >= 2.5.1',
        'sqlalchemy == 1.*', # Higher versions break tests
        'psycopg2 >= 2.6',
        'python-dateutil',
        'grako == 3.10.1'  # Versions > 3.10.1 break our tests
    ],
    tests_require=[
        'tox'
    ],
    test_suite='tests',
    entry_points={}
)
