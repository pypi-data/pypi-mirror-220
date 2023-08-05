# Django Literature 

[![Github Build](https://github.com/SSJenny90/django-literature/actions/workflows/build.yml/badge.svg)](https://github.com/SSJenny90/django-literature/actions/workflows/build.yml)
[![Github Docs](https://github.com/SSJenny90/django-literature/actions/workflows/docs.yml/badge.svg)](https://github.com/SSJenny90/django-literature/actions/workflows/docs.yml)
[![CodeCov](https://codecov.io/gh/SSJenny90/django-literature/branch/main/graph/badge.svg?token=0Q18CLIKZE)](https://codecov.io/gh/SSJenny90/django-literature)
![GitHub](https://img.shields.io/github/license/SSJenny90/django-literature)
![GitHub last commit](https://img.shields.io/github/last-commit/SSJenny90/django-literature)
![PyPI](https://img.shields.io/pypi/v/django-literature)

Streamline the handling of citable literature in your Django web applications.

Documentation
-------------

The full documentation is at https://ssjenny90.github.io/django-literature/

About
---------

Django Literature is designed to facilitate the management and organization of citable literature within your Django project by providing a set of tools and models that enable you to easily handle literature citations, references, and related metadata in your projects.

Features
-----------

- **Literature Models**: The package offers pre-built Django models for literature references, authors, journals, and other relevant entities. These models allow developers to store and manage literature-related information in their applications' databases.

- **Integration**: Django Literature easily integrates with existing models in a Django project, enabling the association of literature references with other data objects, such as articles, blog posts, or research papers.

- **Efficient Querying**: Django Literature provides intuitive query methods that allow developers to retrieve literature references based on various criteria, such as author, title, journal, or publication year. This makes it easy to search and filter the literature database.

- **Citation Generation**: The package offers utilities to generate citations in various formats, such as APA, MLA, or Chicago style. This feature simplifies the process of programmatically generating citations for references within the Django application.

- **Admin Interface**: Django Literature includes an admin interface that allows authorized users to manage literature references conveniently. The interface provides CRUD (Create, Read, Update, Delete) operations for literature objects and ensures data integrity.

Quickstart
----------

Install Django Literature::

    pip install django-literature

Add it to your `INSTALLED_APPS`:


    INSTALLED_APPS = (
        ...
        'literature',
        ...
    )

Add Django Literature's URL patterns:

    urlpatterns = [
        ...
        path('', include("literature.urls")),
        ...
    ]


Running Tests
-------------

Does the code actually work?

    source <YOURVIRTUALENV>/bin/activate
    (myenv) $ pip install tox
    (myenv) $ tox


Development commands
---------------------

    pip install -r requirements_dev.txt
    invoke -l


Credits
-------

