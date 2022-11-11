# -*- coding: utf-8 -*-
from setuptools import setup

# Get README.rst contents
with open('README.md', 'r', encoding="utf-8") as f:
    readme = f.read()
requirements = []
with open('requirements.txt') as handle:
    for line in handle.readlines():
        if not line.startswith('#'):
            package = line.strip().split('=', 1)[0]
            requirements.append(package)
setup(
    name='movie-bot-api',
    version='0.0.10',
    author='yee',
    author_email='yipengfei329@gmail.com',
    license='MIT',
    url='https://github.com/pofey/movie-bot-api',
    description='智能影音机器人MovieBot的接口SDK',
    python_requires='>=3.8',
    long_description=readme,
    long_description_content_type="text/markdown",
    keywords=['movie bot', 'movie robot'],
    packages=['moviebotapi', 'moviebotapi.core'],
    install_requires=requirements,
    include_package_data=True,
    classifiers=[
        'License :: MIT License',
        'Intended Audience :: Developers',
        'Natural Language :: Chinese',
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
