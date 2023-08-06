# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['foodunits', 'foodunits.utils']

package_data = \
{'': ['*']}

install_requires = \
['Pattern>=3.6', 'fuzzywuzzy>=0.18.0', 'pycountry>=22.3.5']

setup_kwargs = {
    'name': 'foodunits',
    'version': '0.1.0',
    'description': 'Validate or convert food units',
    'long_description': '# foodunits\n\nValidate and convert food units with ease!\n\n## Installation\nYou can install foodunits using pip:\n```bash\n$ pip install foodunits\n```\n\n## Usage\n`foodunits` provides functionality to validate and convert food units. It supports both imperial and metric units, including common units such as "liter," "fluid ounce," "pint," "gram," "pound," as well as specific food-related units like "slice," "can," "bottle," and more.\n\n### Validation\nThe validation feature checks whether a string represents a valid food unit. It is case, space, singular-plural, and full name-symbol insensitive. Only the spelling matters. It returns a boolean value indicating the validity of the unit. Here are some examples:\n\n"Value + Unit" type strings can also be validated, such as "5 mls" or "five milliliters".\n\n```python\nfrom foodunits import units_validator\n\nunits_validator("fluid ounce")  # True\nunits_validator("fl oz")  # True\nunits_validator("5 fl ozs")  # True\nunits_validator("5 fl  ozs ")  # True\nunits_validator("five fl ozs")  # True\nunits_validator("flud ounce")  # False\nunits_validator("f oz")  # False\nunits_validator("5 l oz")  # False\nunits_validator("fiv fl ozs")  # False\n```\n\n### Conversation\nThe conversion feature allows you to convert between volumetric and mass food units, both in imperial and metric systems. For example:\n\n```python\nfrom foodunits import units_convertor\n\nunits_convertor("1 fluid ounce", to_unit="ml")\n# Output: {"converted value": 29.573, "unit": "ml"}\n\nunits_convertor("1 1/2 fluid ounce", to_unit="ml")\n# Output: {"converted value": 44.360, "unit": "ml"}\n```\n\nIf you want to convert between volume and mass and have the correct conversion based on the food ingredient, you can provide the ingredient name. Currently, the package supports 100+ major ingredients. If the ingredient you input is not supported, you can provide a value for the "ingredient_density" argument. Here\'s an example:\n```python\nunits_convertor("2.5", to_unit="g", from_unit="fl oz", ingredient="skimmed milk")\n# Output: {"converted value": 76.152, "unit": "g"}\n```\n\nFor cookery units like cup, tablespoon, and teaspoon, which depend on the country, you need to specify the country name or code:\n"2.5 cups", "skimmed milk", "United States" -> "g"\n```python\nunits_convertor("2.5 cups", to_unit="g", ingredient="skimmed milk", country="United States")\n# Output: {"converted value": 618.0, "unit": "g"}\n```\n\nNote: The decimal parameter can be used to specify the number of decimal places in the converted value.\n\nMake sure to import the relevant functions from the foodunits package to use them in your code.\n\n## Contributing\n\nInterested in contributing? Check out the contributing guidelines. Please note that this project is released with a Code of Conduct. By contributing to this project, you agree to abide by its terms.\n\n## License\n\n`foodunits` was created by Ben Zhang. It is licensed under the terms of the MIT license.\n\n## Credits\n\n`foodunits` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter). Inspired by [`validators`](https://github.com/python-validators/validators) and [`UnitConverter`](https://github.com/mattgd/UnitConverter)\n',
    'author': 'Ben Zhang',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': None,
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.9',
}


setup(**setup_kwargs)
