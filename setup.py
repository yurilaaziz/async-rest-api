import os

from setuptools import setup, find_packages

try:
    here = os.path.abspath(os.path.dirname(__file__))
    README = open(os.path.join(here, "README.md")).read()
    with open(os.path.join(here, "requirements/base.txt")) as f:
        required = [l.strip('\n') for l in f if
                    l.strip('\n') and not l.startswith('#')]
except IOError:
    required = []
    README = ""

setup(
    name="barberousse",
    packages=find_packages(),
    version='0.0.1',
    license='GPLv3+',
    description="Asynchronous Job Runner Framework with builtin REST APi",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Amine Ben Asker",
    author_email="ben.asker.amine@gmail.com",
    url="https://github.com/yurilaaziz/barberousse",
    download_url='https://github.com/yurilaaziz/barberousse/releases/tag/0.1',
    keywords="Asynchronous Job Runner, Task Runner, Celery",
    install_requires=required,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
