# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pxgpt', 'pxgpt.rings']

package_data = \
{'': ['*'], 'pxgpt': ['frontend/build/*', 'frontend/build/assets/*']}

install_requires = \
['argx>=0.2.9,<0.3.0',
 'faiss-cpu>=1.7.4,<2.0.0',
 'langchain>=0.0.234,<0.0.235',
 'pandas>=2.0.3,<3.0.0',
 'prompt-toolkit>=3.0.39,<4.0.0',
 'py>=1.11.0,<2.0.0',
 'pyarrow>=12.0.1,<13.0.0',
 'pymupdf>=1.22.5,<2.0.0',
 'python-simpleconf[yaml]>=0.6.0,<0.7.0',
 'quart>=0.18.4,<0.19.0',
 'scikit-learn>=1.3.0,<2.0.0']

extras_require = \
{'all': ['gpt4all>=1.0.3,<2.0.0',
         'llama-cpp-python>=0.1.70,<0.2.0',
         'openai>=0.27.8,<0.28.0'],
 'gpt4all': ['gpt4all>=1.0.3,<2.0.0'],
 'llama-cpp': ['llama-cpp-python>=0.1.70,<0.2.0'],
 'openai': ['openai>=0.27.8,<0.28.0', 'tiktoken>=0.4.0,<0.5.0']}

entry_points = \
{'console_scripts': ['pxgpt = pxgpt.cli:main']}

setup_kwargs = {
    'name': 'pxgpt',
    'version': '0.0.0rc1',
    'description': 'Your personal, powerful and private GPT.',
    'long_description': '<div style="display: flex; align-items: center; justify-content: center; gap: .2rem">\n  <img src="pxgpt/frontend/public/assets/favicon.png" alt="px" style="width: 32px; height: 32px;" />\n  <div style="font-size: 24px; font-weight: bold">GPT</div>\n</div>\n<hr />\n<p style="text-align: center">Your personal, powerful and private GPT</p>\n\n\n\n## Features\n\n- Ingest of your own documents and talk to them.\n- Store your data locally on your device.\n- Choose from a variety of models, including OpenAI.\n- Support conversation history and memory.\n- Switch between profiles with different settings.\n- Support both web interface and command line interface.\n- Support Llama v2!\n\n## Installation\n\n```shell\n# With all supported models\n$ pip install -U pxgpt[all]\n\n# With support for GPT4all only\n$ pip install -U pxgpt[gpt4all]\n\n# With support for llama-cpp only\n$ pip install -U pxgpt[llama-cpp]\n\n# With support for openai only\n$ pip install -U pxgpt[openai]\n```\n\nThen copy the configuration from `.pxgpt.config-example.yml` to `.pxgpt.config.yml` and modify it to your needs.\n\n## Usage\n\n### Chat from CLI\n\n```shell\n$ 23:45:06 ❯ pxgpt chat\n\nWelcome to chat via the pxGPT CLI v0.0.0rc0!\nHit \'Ctrl+c\' or \'Ctrl+d\' to exit.\n[2023-07-20 20:03:22,716] INFO Switched profile to llamacpp-chat\n[2023-07-20 20:03:22,719] INFO Creating LLM (LlamaCpp)\nllama.cpp: loading model from models/llamacpp/llama-2-7b.ggmlv3.q4_0.bin\nllama_model_load_internal: format     = ggjt v3 (latest)\nllama_model_load_internal: n_vocab    = 32000\nllama_model_load_internal: n_ctx      = 512\nllama_model_load_internal: n_embd     = 4096\nllama_model_load_internal: n_mult     = 256\nllama_model_load_internal: n_head     = 32\nllama_model_load_internal: n_layer    = 32\nllama_model_load_internal: n_rot      = 128\nllama_model_load_internal: freq_base  = 10000.0\nllama_model_load_internal: freq_scale = 1\nllama_model_load_internal: ftype      = 2 (mostly Q4_0)\nllama_model_load_internal: n_ff       = 11008\nllama_model_load_internal: model size = 7B\nllama_model_load_internal: ggml ctx size =    0.08 MB\nllama_model_load_internal: mem required  = 5185.72 MB (+ 1026.00 MB per state)\nllama_new_context_with_model: kv self size  =  256.00 MB\n[2023-07-20 20:03:24,552] INFO Entering chat mode\nLoaded conversation:  2023-07-20_20-03-17\nUse the up/down arrow keys to navigate history.\nUse /help to see the list of commands.\n\n>>> Hello Llama 2, if you could choose a superpower, what would it be and why?\n I will answer this question in two parts. The first part is the super power that I will choose. The second part is why I chose this super power.\nIn the first part, the super power that I will choose is the ability to fly. This is because flying has many benefits. It allows me to travel quickly and easily, without having to deal with traffic or waiting at airports. Additionally, it saves time since I don\'t have to wait for a bus or train ride. Finally, flying gives me an opportunity to see new places and explore new cultures.\nIn the second part of my answer, I will explain why I chose this super power. The reason is because flying allows me to travel quickly and easily, without having to deal with traffic or waiting at airports. Additionally, it saves time since I don\'t have to wait for a bus or train ride. Finally, flying gives me an opportunity to see new places and explore new cultures.\n\n>>> /help\nCommands:\n  - /help: List the commands\n  - /new: Start a new conversation\n  - /switch: Switch to a conversation\n  - /list: List all conversations\n  - /path: Show the path of the current conversation file\n  - /delete: Delete a conversation\n  - /rename: Rename a conversation\n  - /ingest: Ingest documents from the source directory\n  - /docs: List ingested and uningested documents in the source directory\n  - /exit: Exit the CLI\n\n>>>\n```\n\n### Chat from the web interface\n\n```shell\n$ pxgpt serve\n# Open http://localhost:7758 in your browser\n```\n\n![Web-interface](web-interface.png)\n\n### Configuration\npx\nThe configuration files are loaded from the following paths:\n\n- `~/.config/pxgpt/config.yml`\n- `~/.pxgpt.config.yml`\n- `./.pxgpt.config.yml`\n\n#### Profiles\n\nNote that you need to define profiles in the configuration file. For example:\n\n```yaml\nopenai:  # The profile\n    model:\n        type: ChatOpenAI\n```\n\nThe configuration items are inherited from the `default` profile. For example:\n\n```yaml\ndefault:\n    credentials:\n        openai_api_key: sk-xxxxxxxxxxx\n\nopenai:\n    model:\n        type: ChatOpenAI\n```\n\nThen when you use `openai` profile, the configurations are expanded as:\n\n```yaml\nopenai:\n    credentials:\n        openai_api_key: sk-xxxxxxxxxxx\n    model:\n        type: ChatOpenAI\n```\n\nHigher-level configurations override lower-level configurations. For example:\n\nIf you define the `default` profile in `~/.config/pxgpt/config.yml` and the `openai` profile in `./.pxgpt.config.yml`, then the `openai` profile will inherit the `default` profile, as well.\n\n#### Configuration items\n\n- `log_level`: The log level for the logger in your teminal\n- `history_directory`: The directory to store the conversation history\n- `history_into_memory`: Whether to load the conversation history into memory\n  - You can turn this off if you are using small models\n- `credentials`: The credentials for the models.\n  For example, for OpenAI, you need to provide the `openai_api_key`.\n- `model`: Type of the model and arguments for it.\n  - `type`: The type of the model, supported models are: `GPT4All`, `LlamaCpp`, `ChatOpenAI` and `OpenAI`\n  - `<other>`: The arguments for the model. Passed to `langchain` llms.\n    - For `GPT4All`, you can pass the arguments listed in [here][1].\n    - For `LlamaCpp`, you can pass the arguments listed in [here][2].\n    - For `ChatOpenAI`, you can pass the arguments listed in [here][3].\n    - For `OpenAI`, you can pass the arguments listed in [here][4].\n- `qmodel`: The arguments for model used to condense questions\n  - `type`: Same as `model.type`, with and `Echo` model added, which is useful for models that don\'t do question condensing very well.\n  - `<other>`: Same as `model.<other>`.\n- `ingest`: The arguments for the ingestion.\n  - `source_directory`: The directory to ingest documents from.\n    - If not provided, we will enter the chat mode.\n  - `persist_directory`: The directory to save the vectorstore database.\n    - If not provided, will use `<source_directory>/.pxgpt-<model>-db`.\n  - `target_source_chunks`: The number of chunks to return against the query.\n  - `n_workers`: The number of workers to use for ingestion.\n  - `chunk_size` and `chunk_overlap`: The chunk size and overlap for the ingestion.\n- `embeddings`: The arguments for the embeddings.\n  - For `GPT4All`, you can pass the arguments listed in [here][5].\n  - For `LlamaCpp`, you can pass the arguments listed in [here][6].\n  - For `OpenAI` or `ChatOpenAI`, you can pass the arguments listed in [here][7].\n\n### Ingest documents\n\n```shell\n$ pxgpt ingest  # default profile\n$ pxgpt ingest --profile openai-docs\n# Will ingest documents under `ingest.source_directory` under `openai-docs` profile\n```\n\n## Credits\n\n`pxgpt` is Inspired by [privateGPT][8], with the addition of openai API support, history and memory support, and a web interface.\n\n## TODO\n\n- [ ] Support ingestion management (upload/download/delete/ingest documents) from the web interface\n- [ ] Support profile management (add/remove/modify) from the web interface\n- [ ] Use markdown to format the response on the web interface\n- [ ] Build a docker image\n- [ ] Support more models\n\n## Q & A\n\n[QA.md](QA.md)\n\n[1]: https://api.python.langchain.com/en/latest/llms/langchain.llms.gpt4all.GPT4All.html#langchain.llms.gpt4all.GPT4All\n[2]: https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html#langchain.llms.llamacpp.LlamaCpp\n[3]: https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html#langchain.chat_models.openai.ChatOpenAI\n[4]: https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAI.html#langchain.llms.openai.OpenAI\n[5]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.gpt4all.GPT4AllEmbeddings.html#langchain.embeddings.gpt4all.GPT4AllEmbeddings\n[6]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.llamacpp.LlamaCppEmbeddings.html#langchain.embeddings.llamacpp.LlamaCppEmbeddings\n[7]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html#langchain.embeddings.openai.OpenAIEmbeddings\n[8]: https://github.com/imartinez/privateGPT\n',
    'author': 'pwwang',
    'author_email': 'pwwang@pwwang.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
