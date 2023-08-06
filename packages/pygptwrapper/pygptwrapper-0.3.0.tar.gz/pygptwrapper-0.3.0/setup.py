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
    'version': '0.3.0',
    'description': 'Python Wrapper for the ChatGPT API',
    'long_description': '# pygptwrapper - A Python Wrapper for the ChatGPT API\npygptwrapper is a Python library that provides a simple way to interact with the ChatGPT API, which is a powerful language model trained by OpenAI that can generate human-like text based on input prompts.\n\nThis library makes it easy to integrate the ChatGPT API into your Python applications, allowing you to generate text in real-time, create chatbots, or automate text generation tasks. It provides context-based model using newly introduced model ```gpt-3.5-turbo```.\n\n# Installation\nTo install pygptwrapper, you can use pip:\n\n```\npip install pygptwrapper\n```\n\n# Usage\nHere\'s a basic example of how to use pygptwrapper:\n\n```\nfrom pygptwrapper import ContextualGPT\n\n# Instantiate the ContextualGPT object with a ```task``` and ```api_key```\ngpt = ContextualGPT(\n    task="You are a chatbo assistant. You will give recommendations for restaurants."\n    api_key=api_key\n)\n```\n\n# Initiate a conversation with instanciated bot\n```\ntext = gpt.ask(question="What is the meaning of life?")\nprint(text)\n```\nThis will generate a response from the ChatGPT API based on the input prompt. Notice that contextual conversation is stored in ```gpt.conversation```.',
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
