import openai
from .utils import build_message_dict, get_answer_from_model


class ContextualGPT:
    def __init__(self, system_task, api_key):
        self._system_task = system_task
        self.conversation = [build_message_dict("system", self._system_task)]
        self.api_key = api_key

        openai.api_key = self.api_key

    @property
    def system_task(self):
        return self._system_task

    @system_task.setter
    def system_task(self, task):
        self._system_task = task

    def ask(self, question, verbose=True):
        self.conversation.append(build_message_dict("user", question))

        answer = get_answer_from_model(
            self.conversation,
            question,
        )
        print(answer) if verbose else None

        self.conversation.append(build_message_dict("assistant", answer))

    def ask_previous(self, question):
        self.conversation.pop()
        self.ask(question)

    def flush_conversation(self):
        self.conversation = [build_message_dict("system", self.task)]
