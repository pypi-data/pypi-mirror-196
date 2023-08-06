import openai

MODEL = "gpt-3.5-turbo"


def build_message_dict(role, content):
    return {
        "role": role,
        "content": content,
    }


def get_answer_from_model(conversation, question):
    openai_object = openai.ChatCompletion.create(
        model=MODEL,
        messages=conversation,
    )
    return openai_object["choices"][0]["message"]["content"]
