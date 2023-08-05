# GPTClass
**GPTClass** is a Python class that uses OpenAI's GPT to do what you need with minimal information.

## Installation
```bash
pip install gptclass
```

## Usage
```python
>>> import openai
>>> openai.api_key = "..."

>>> from gptclass import GPTClass
>>> jack = GPTClass()

>>> jack.add(1, 2)
3
>>> jack.n_unique([1, 2, 5, 5])
3
>>> jack.prime_numbers_below(10)
[2, 3, 5, 7]
>>> jack.count_vowels("Today I had a nice coffee!")
10
>>> jack.from_celsius_to_fahrenheit(25)
77.0
```

## Notes
- Inspired on: [davinci-functions](https://github.com/odashi/davinci-functions/tree/main)

## Warning
- The code produced may not be reliable and should be validated before executing it.