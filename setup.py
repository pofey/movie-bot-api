# -*- coding: utf-8 -*-
from setuptools import setup

# Get README.rst contents
readme = ''
with open('README.rst') as f:
    readme = f.read()
requirements = []
with open('requirements.txt') as handle:
    for line in handle.readlines():
        if not line.startswith('#'):
            package = line.strip().split('=', 1)[0]
            requirements.append(package)
setup(
    name='movie-bot-api',
    version='0.0.53',
    author='yee',
    author_email='yipengfei329@gmail.com',
    license='MIT',
    url='https://github.com/pofey/movie-bot-api',
    description='智能影音机器人MovieBot的接口SDK',
    python_requires='>=3.8',
    long_description=readme,
    long_description_content_type="text/x-rst",
    keywords=['movie bot', 'movie robot'],
    packages=['moviebotapi', 'moviebotapi.core'],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese (Simplified)',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Internet',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities'
    ]
)
