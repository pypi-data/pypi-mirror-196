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
    'version': '0.2.1',
    'description': '',
    'long_description': '# akashic_records\n\n`akashic_records` is a Python package that dynamically generates functions using OpenAI code completion based on what is imported and how it is used.\nInstallation\n\nTo install the akashic_records package, you can use pip:\n\n```bash\npip install akashic_records\n```\n\n## Usage\n\nBehaviour of the `akashic_records` package is based on _what_ you import from it, and _how_ you use it.\n\nThe package generates functions on the fly based on the name you import and the way you call it.\n\n```python\nfrom akashic_records import quick_sort\n\narr = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nresult = quick_sort(arr)\nprint(result)  # Output: [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]\n```\n\nThe package will end up making requests to the OpenAI completations endpoint with the `code-davinci-002` model.\n\nThe above code will end up generating this prompt:\n```\ndef quick_sort(arr: list):\n```\n\nNote that the parameter name matches the name of the argument that was passed in. If a constant is passed in instead of an identifier, generic names such as `p0` and `p1` will be used. To have a useful name with a constant argument, use keyword arguments.\n\n## Return type and docstrings\n\nThis package (ab)uses type hints to give more information to the completion process.\n\n```python\nfrom typing import Annotated\nfrom akashic_records import merge_sort\n\nunsorted_list = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]\nresult: Annotated[list, """\nSorts the input list using the mergesort algorithm.\n\nParameters:\n-----------\nunsorted_list : list\n    The input list to be sorted.\n\nReturns:\n--------\nlist\n    The sorted list.\n"""] = merge_sort(unsorted_list)\nprint(result)  # Output: [1, 1, 2, 3, 3, 4, 5, 5, 5, 6, 9]\n```\n\nGenerates the following prompt:\n```\ndef merge_sort(unsorted_list: list) -> list:\n    """\n    Sorts the input list using the mergesort algorithm.\n\n    Parameters:\n    -----------\n    unsorted_list : list\n        The input list to be sorted.\n\n    Returns:\n    --------\n    list\n        The sorted list.\n    """\n```\n\nIf you would like to include a docstring but not a return type, only use a string for the type annotation instead of using `typing.Annotated`.\n\n### How does the parameter name/type hint thing work?\n\nThe very neat [sorcery](https://github.com/alexmojaki/sorcery) package by [Alex Hall](https://github.com/alexmojaki).\n\n## Options\n\nThe OpenaAI completaions endpoint has many options. Some of these are available for tweaking.\n\n```\nfrom akashic_records import config\n\nconfig.n = 3 # https://platform.openai.com/docs/api-reference/completions/create#completions/create-n\nconfig.max_tokens = 512 # https://platform.openai.com/docs/api-reference/completions/create#completions/create-max_tokens\nconfig.temperature = 0.2 # https://platform.openai.com/docs/api-reference/completions/create#completions/create-temperature\n```\n\nSome additional options are available to control the prompt generation process.\n```\nfrom akashic_records import config\n\nconfig.type_hint = True # Set to False to disable all type hints in prompts\n\n# The package isn\'t always able to get a working completion from the API.\n# In the event that something goes wrong (syntax error in the generated code, runtime error trying to run it, etc)\n# The package will try to generate new completions.\n# The `attempts` value controls how many times it will try.\nconfig.attempts = 5 # Set to -1 for unlimited tries.\n```\n\n## What\'s with the name?\n\nThe name `akashic_records` is inspired by the spiritual belief of the [Akashic Records](https://en.wikipedia.org/wiki/Akashic_records). In this belief, the Akashic Records are a repository all universal events, thoughts, words, emotions and intent ever to have occurred in the past, present, or future in terms of all entities and life forms.\n\nThis seemed fitting for a package that in some sense contains the implementation of "every function".\n',
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
