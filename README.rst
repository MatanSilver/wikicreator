wikicreator

Wikicreator is a static site generator written in python.
It was originally created or VirZOOM, Inc.so to ease updating the manual pages.
There are currently no theming capabilities unless you actually clone this
repo and modify the templates used. The structure of the default site is such
that if you add entries to the config.yaml file and then write corresponding
document.md files in your project root, the pages will appear in the rendered
sidebar. The resulting page is a single html file and accompanying css that can
be served by a CDN.

The project was scaffolded using the cookiecutter package from pypi. Using the
--init flag will use the cookiecutter-wikicreator repo to create a skeleton site.
