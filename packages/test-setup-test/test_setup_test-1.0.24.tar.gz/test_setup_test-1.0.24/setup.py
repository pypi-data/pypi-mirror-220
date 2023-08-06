# setup.py
from setuptools import setup

setup(
    name='test_setup_test',
    version='1.0.24',
    author='Divy TEST',
    author_email='divy.jain@bombaysoftwares.com',
    description='utils_bs_test',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    maintainers=['Maintainer 1', 'Maintainer 2'],

    license='MIT',
    project_urls={
        "Bug Tracker": "https://github.com/utils-bs-test",
        "Source Code": "https://github.com/abc",
        "Documentation": "https://github.com/abc"
    },
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Topic :: Software Development",
        "Topic :: Scientific/Engineering",
        "Operating System :: OS Independent",
    ]
)