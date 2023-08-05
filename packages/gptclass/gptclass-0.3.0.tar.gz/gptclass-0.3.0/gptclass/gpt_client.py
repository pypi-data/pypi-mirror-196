from typing import List, Dict

import openai
import diskcache

cache = diskcache.Cache("~/.cached/gptclass")


@cache.memoize()
def chat_completion(messages: List[Dict[str, str]]) -> str:
    completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
    return completion.choices[0].message.content
