from typing import Any, Dict, List
import re

import openai
import diskcache

# from gptclass.gpt_client import chat_completion

cache = diskcache.Cache("~/.cache/gptclass")


@cache.memoize()
def chat_completion(messages) -> str:
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return completion.choices[0].message.content


def function_writer(name: str, n_args: int, kwargs: List[str]) -> str:
    kwargs_part = ""
    if len(kwargs) > 0:
        kwargs_part = (
            " and named parameters: " + ", ".join([f'"{w}"' for w in kwargs]) + "."
        )
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
            "content": f"""
                write a function named '{name}' that receives {n_args} parameter(s){kwargs_part}
                """.strip(),
        },
    ]
    generated_code = chat_completion(conversation)
    matches = re.search("```(python)?(.+?)```", generated_code, flags=re.DOTALL)
    if matches:
        generated_code = matches.group(2)
    return generated_code.strip()


def function_caller(name: str):
    def f(*args, **kwargs):
        code = function_writer(name, len(args), kwargs.keys())
        locals: Dict[str, Any] = {}
        exec(code, globals(), locals)
        for key, value in locals.items():
            globals()[key] = value
        func = locals[name]
        return func(*args, **kwargs)

    return f


def function_explainer(name: str):
    def f(*args, **kwargs) -> None:
        print(function_writer(name, len(args), kwargs.keys()))

    return f
