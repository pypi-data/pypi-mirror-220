# coding=UTF-8
import sys
from pathlib import Path
from setuptools import Extension, setup  # noqa: E402


  


install_requires = [
    "numpy",
    "pandas>=1.1",
    "pyluach",
    "python-dateutil",
    "pytz",
    "toolz",
    "korean_lunar_calendar",
]

installs_for_two = [
    'pyOpenSSL',
    'ndg-httpsclient',
    'pyasn1'
]

if sys.version_info[0] < 3:
    install_requires += installs_for_two

packages = [
 "exchange_calendars",
 "exchange_calendars.pandas_extensions",
 "exchange_calendars.utils",
]

setup(
    name='tej-exchange-calendars',
    description='Modified exchange-calendars from exchange-calendars3.3.',
    keywords=['tej', 'big data', 'data', 'financial', 'economic','stock','TEJ',],
    entry_points={
            "console_scripts": [
                "ecal = exchange_calendars.ecal:main",
            ],
        },
    long_description='Modified exchange-calendars from exchange-calendars3.3.',
    version='0.0.5',
    author='tej',
    author_email='tej@tej.com.tw',
    maintainer='tej api Development Team',
    maintainer_email='tej@tej.com',
    url='https://api.tej.com.tw',
    license='MIT',
    install_requires=install_requires,
    tests_require=[
        'unittest2',
        'flake8',
        'nose',
        'httpretty',
        'mock',
        'factory_boy',
        'jsondate'
    ],
    test_suite="nose.collector",
    
    packages=packages,
    
    python_requires=">=3.7"
)