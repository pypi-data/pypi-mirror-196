# pygptwrapper - A Python Wrapper for the ChatGPT API
pygptwrapper is a Python library that provides a simple way to interact with the ChatGPT API, which is a powerful language model trained by OpenAI that can generate human-like text based on input prompts.

This library makes it easy to integrate the ChatGPT API into your Python applications, allowing you to generate text in real-time, create chatbots, or automate text generation tasks. It provides context-based model using newly introduced model ```gpt-3.5-turbo```.

# Installation
To install pygptwrapper, you can use pip:

```python
pip install pygptwrapper
```

# Usage
Here's a basic example of how to use pygptwrapper:

```python
from pygptwrapper import ContextualGPT

# Instantiate the ContextualGPT object with a task and api_key
gpt = ContextualGPT(
    task="You are a chatbot assistant. You will give recommendations for restaurants."
    api_key=api_key
)
```

# Initiate a conversation with instanciated bot
```python
text = gpt.ask(question="What is the meaning of life?")
print(text)
```
This will generate a response from the ChatGPT API based on the input prompt. Notice that contextual conversation is stored in ```gpt.conversation```.