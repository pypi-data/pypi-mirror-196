from typing import Any, Dict
import re

from .gpt_client import chat_completion


def function_writer(name: str, n_parameters: int) -> str:
    conversation = [
        {
            "role": "system",
            "content": re.sub(
                r"\s+",
                " ",
                """
                    You are a python code generator that returns the code that satisfies the
                    provided description.
                    The generated python code should contain all auxiliary functions.
                    The answer should contain no explanation about the code, how it is working
                    or any description.
                    The output should be just code.
                """,
            ).strip(),
        },
        {
            "role": "user",
            "content": f"write a function named '{name}' that receives {n_parameters} parameter(s)",
        },
    ]
    generated_code = chat_completion(conversation)
    if "```python" in generated_code:
        cleaned_code = generated_code.split("```python")[1].split("```")[0].strip()

    return cleaned_code


def function_caller(name: str):
    def f(*args):
        code = function_writer(name, len(args))
        locals: Dict[str, Any] = {}
        exec(code, globals(), locals)
        for key, value in locals.items():
            globals()[key] = value
        func = locals[name]
        return func(*args)

    return f


def function_explainer(name: str):
    def f(*args) -> None:
        print(function_writer(name, len(args)))

    return f
