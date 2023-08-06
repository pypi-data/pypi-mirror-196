# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['slapdash', 'slapdash.examples']

package_data = \
{'': ['*'], 'slapdash': ['frontend/*']}

install_requires = \
['aiofiles>=22.1.0,<23.0.0',
 'fastapi>=0.88.0,<0.89.0',
 'python-socketio>=4.6.1,<5.0.0',
 'requests>=2.28.1,<3.0.0',
 'uvicorn>=0.20.0,<0.21.0',
 'websockets>=10.4,<11.0']

extras_require = \
{'examples': ['matplotlib']}

setup_kwargs = {
    'name': 'slapdash',
    'version': '1.0.1',
    'description': 'Create device and application control dashboards instantly',
    'long_description': "# Slapdash\n\n**<https://github.com/cathaychris/slapdash/>**\n\nThe Slapdash library lets you create a control dashboard with ease. It takes device driver classes written in simple python and automatically generates\n\n- A web server exposing the class via a RESTful API, that can be accessed with HTTP requests or using the provided clients;\n- An automatically generated fronted rendered in a web page that directly connects to the web server for immediate access;\n- and modularly permits the bootstrapping of other interfaces such as RPC. Bring-Your-Own-Interface.\n\nFor example, it will turn this:\n\n```python\nclass Device:\n\n    _current = 0.0\n    _voltage = 0.0\n    _power = False\n\n    @property\n    def current(self):\n        # run code to get current\n        return self._current\n\n    @current.setter\n    def current(self, value):\n        # run code to set current\n        self._current = value\n\n    @property\n    def voltage(self):\n        # run code to get voltage\n        return self._voltage\n\n    @voltage.setter\n    def voltage(self, value):\n        # run code to set voltage\n        self._voltage = value\n\n    @property\n    def power(self):\n        # run code to get power state\n        return self._power\n\n    @power.setter\n    def power(self, value):\n        # run code to set power state\n        self._power = value\n\n    def reset(self):\n        self.current = 0.0\n        self.voltage = 0.0\n```\n\ninto this:\n\n![](./docs/images/fast-api-example.png)\n\nTry running this example with\n\n```python\nfrom slapdash.examples import run_example\nrun_example('doc_example')\n```\n\n# Credits\n\nSlapdash was developed in the [TIQI group](https://tiqi.ethz.ch/) at ETH Zürich, primarily by [Matt Grau](https://www.odu.edu/directory/matt-grau).\n",
    'author': 'Matt Grau',
    'author_email': 'graum@phys.ethz.ch',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
