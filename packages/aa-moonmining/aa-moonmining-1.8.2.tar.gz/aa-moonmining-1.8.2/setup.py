import os

from setuptools import find_packages, setup

from moonmining import __version__

# read the contents of your README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="aa-moonmining",
    version=__version__,
    packages=find_packages(),
    include_package_data=True,
    license="MIT",
    description="Alliance Auth app for tracking moon extractions and scouting new moons.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/ErikKalkoken/aa-moonmining",
    author="Erik Kalkoken",
    author_email="kaloken87@gmail.com",
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 3.2",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    python_requires="~=3.8",
    install_requires=[
        "allianceauth>=2.9",
        "django-bootstrap-form",
        "django-navhelper",
        "allianceauth-app-utils>=1.14.2",
        "django-eveuniverse>=0.18",
        "django-datatables-view>=1.20",
        "PyYAML",
    ],
)
