""" Module providing setup tools. """
from setuptools import setup,find_packages
import app_info

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name=app_info.NAME,
    version=app_info.VERSION,
    author=app_info.AUTHOR,
    author_email=app_info.AUTHOR_EMAIL,
    description=app_info.DESCRIPTION,
    long_description=long_description,
    long_description_content_type='text/markdown',
    url=app_info.URL,
    packages=find_packages(),
    py_modules=['macloot','app_info','oui','mac'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.7',
    install_requires=[
        'requests',
    ],
    entry_points={
        'console_scripts': [
            'macloot=macloot:main',
        ],
    }
)
