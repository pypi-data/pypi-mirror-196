# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_batteries']

package_data = \
{'': ['*']}

install_requires = \
['django>=4.1.7,<5.0.0']

setup_kwargs = {
    'name': 'django-batteries',
    'version': '0.0.1',
    'description': 'Set of most common utils for django/drf projects',
    'long_description': "# Django-batteries\n\nThis package contains useful utilities for django/drf project\n\n## Models\n\nContains set of abstract models to enforce DRY principle for most common use cases\n\n### TimeStampedModel\n\n- `created`\n- `modified`\n\n### TimeFramedModel\n\n- `start`\n- `end`\n\n  For time bound entities\n\n### DescriptionModel\n\n- `description`\n\n### TitleModel\n\n- `title`\n\n### TitleDescriptionModel\n\n- `title`\n- `description`\n\n## Fields\n\n### Monitor field\n\nA DateTimeField that monitors another field on the same model and sets itself to the current date/time whenever the monitored field\nchanges.\nuse it like this in your models:\nclass MyMode(models.Model):\n\n    title = models.Charfield(max_length=50)\n    title_changed = MonitorField(_('title changed'), monitor='title')\n\n## Tests\n",
    'author': 'Oleksandr Korol',
    'author_email': 'zibertua@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.11,<4.0',
}


setup(**setup_kwargs)
