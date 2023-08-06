# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pygptwrapper']

package_data = \
{'': ['*']}

install_requires = \
['openai>=0.27.1,<0.28.0']

setup_kwargs = {
    'name': 'pygptwrapper',
    'version': '0.1.0',
    'description': 'Python Wrapper for the ChatGPT API',
    'long_description': '# pyGPT - A Python Wrapper for the ChatGPT API\npyGPT is a Python library that provides a simple way to interact with the ChatGPT API, which is a powerful language model trained by OpenAI that can generate human-like text based on input prompts.\n\nThis library makes it easy to integrate the ChatGPT API into your Python applications, allowing you to generate text in real-time, create chatbots, or automate text generation tasks.\n\n# Installation\nTo install pyGPT, you can use pip:\n\n```\npip install pyGPT\n```',
    'author': 'Your Name',
    'author_email': 'you@example.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
