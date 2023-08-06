### PromptSec SDK

This library provides an SDK from PromptSec (https://prompt-security.com).

### Installing
```bash
pip install promptsec
```

There are two common scenarios for using the library. You can use the one that most suits your code style.

### Scenario #1: Monkey patching
This is the most convenient way to use the library. Just add one line to the top of your main python file:
```python
#import promptsec.langchain.monkey_patch
```

### Scenario #2: Use patched LLM implementation
Alternatively, if for any reason you don't want to use monkey patching, you can just replace all occurrences of:
```python
from langchain.llms import OpenAI # import OpenAI model
```
To become:
```python
from promptsec.langchain.llms import OpenAI # import OpenAI model
```
Basically, import `promptsec.langchain.llms.*` instead of `langchain.llms.*` and that's it.

## Initialize the library and provide a prompt-security API key
When your app starts, tell the library the API key you obtained from Prompt Security:
```python
from promptsec import ps_init
ps_init('my-api-key')
```

You can obtain the API key from http://prompt-security/sdk
