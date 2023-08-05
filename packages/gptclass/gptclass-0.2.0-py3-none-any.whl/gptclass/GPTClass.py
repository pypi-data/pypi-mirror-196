from typing import Any
import textwrap

from .gpt_client import chat_completion


def function_writer(name: str, n_parameters: int) -> str:
    conversation = [
        {
            "role": "system",
            "content": textwrap.dedent(
                """You are a python code generator that returns the code that satisfies the provided description. The answer should contain no explanation about the code, how it is working or any description. The output should be just code.""".strip()
            ),
        },
        {
            "role": "user",
            "content": f"write a function named '{name}' that receives {n_parameters} parameter(s)",
        },
    ]
    generated_code = chat_completion(conversation)
    return generated_code


def function_builder(name: str):
    def f(*args):
        code = function_writer(name, len(args))
        cleaned_code = code.replace("```python", "").replace("```", "").strip()
        locals: dict[str, Any] = {}
        exec(cleaned_code, globals(), locals)
        func = locals[name]
        return func(*args)

    return f


class GPTClass:
    def __getattr__(self, name: str):
        return function_builder(name)
