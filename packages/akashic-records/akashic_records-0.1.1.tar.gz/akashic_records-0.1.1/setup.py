# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['akashic_records', 'akashic_records._meta']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.2,<0.28.0', 'sorcery>=0.2.2,<0.3.0']

setup_kwargs = {
    'name': 'akashic-records',
    'version': '0.1.1',
    'description': '',
    'long_description': '# akashic_records\n\n`akashic_records` is a Python library that dynamically generates functions using OpenAI code completion based on what is imported and how it is used.\nInstallation\n\nTo install the akashic_records library, you can use pip:\n\n```bash\npip install akashic_records\n```\n\n## Usage\n\nTo use the `akashic_records` library, you need to import the function you want to generate. The library generates the function on the fly based on the name you import. For example, to generate a quicksort function, you can import the quick_sort function like this:\n\nSince this library depends on [`openai`](https://github.com/openai/openai-python), you need to set your API key on start.\n```python\nimport openai\nopenai.api_key = \'<YOUR_KEY>\'\n\nfrom akashic_records import quick_sort\n\n# Use the generated function\narr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nresult = quick_sort(arr)\nprint(result)  # Output: [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]\n```\n\nThis library (ab)uses type hints to give more information to the completion process.\n```python\nimport openai\nopenai.api_key = \'<YOUR_KEY>\'\n\nfrom akashic_records import merge_sort\n\n# Use the generated function\narr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nresult: """\nSorts the input list using the mergesort algorithm.\n\nParameters:\n-----------\narr : list\n    The input list to be sorted.\n\nReturns:\n--------\nlist\n    The sorted list.\n""" = merge_sort(arr)\nprint(result)  # Output: [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]\n```\n\n### Wait, how did you do that?\n\nThe very neat [sorcery](https://github.com/alexmojaki/sorcery) package by [Alex Hall](https://github.com/alexmojaki).\n\n## What\'s with the name?\n\nThe name `akashic_records` is inspired by the spiritual belief of the [Akashic Records](https://en.wikipedia.org/wiki/Akashic_records). In this belief, the Akashic Records are a repository all universal events, thoughts, words, emotions and intent ever to have occurred in the past, present, or future in terms of all entities and life forms.\n\nThis seemed fitting for a library that in some sense contains the implementation of "every function".\n',
    'author': 'David Buckley',
    'author_email': 'david@davidbuckley.ca',
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
