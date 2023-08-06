# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pytest_pyspec']

package_data = \
{'': ['*']}

install_requires = \
['pytest>=7.2.1,<8.0.0']

entry_points = \
{'pytest11': ['pytest_pyspec = pytest_pyspec.plugin']}

setup_kwargs = {
    'name': 'pytest-pyspec',
    'version': '0.5.0',
    'description': 'A plugin that transforms the pytest output into a result similar to the RSpec. It enables the use of docstrings to display results and also enables the use of the prefixes "describe", "with" and "it".',
    'long_description': '\nThe **pytest-pyspec** plugin transforms the pytest output into a result similar to the RSpec.\n\nJust nest your tests using classes and include _docstring_ for each class and test. You can create any nested levels.\n\nThe following test sample:\n\n```python\nimport pytest\n\nclass TestHouse:\n    "a House"\n    \n    def test_door(self):\n        "has door"\n        assert 1 == 1\n        \n    class TestTwoFloors:\n        """with two floors\n        \n        A house with two floor has stairs\n        """\n        def test_stairs(self):\n            "has stairs"\n            assert 1 == 1\n\n        def test_second_floor(self):\n            "has second floor"\n            assert 1 == 1\n\n        def test_third_floor(self):\n            "has third floor"\n            assert 1 == 2\n```\n\nGenerates the following output:\n\n```\ntest/test_sample.py \n\nA house\n  ✓ Has door\n\nA house\n  With two floors\n    ✓ Has stairs\n    ✓ Has second floor\n    ✗ Has third floor\n```\n\n## Installing and running **pySpec**\n\n```bash\npip install pytest-pyspec\npytest --pyspec\n```\n',
    'author': 'Felipe Curty',
    'author_email': 'felipecrp@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/felipecrp/pytest-pyspec',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
