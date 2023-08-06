# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pxgpt', 'pxgpt.rings']

package_data = \
{'': ['*'], 'pxgpt': ['frontend/build/*', 'frontend/build/assets/*']}

install_requires = \
['argx>=0.2.9,<0.3.0',
 'chromadb>=0.3.29,<0.4.0',
 'langchain>=0.0.232,<0.0.233',
 'prompt-toolkit>=3.0.39,<4.0.0',
 'python-simpleconf[yaml]>=0.6.0,<0.7.0',
 'quart>=0.18.4,<0.19.0']

extras_require = \
{'all': ['gpt4all>=1.0.3,<2.0.0',
         'llama-cpp-python>=0.1.70,<0.2.0',
         'openai>=0.27.8,<0.28.0'],
 'gpt4all': ['gpt4all>=1.0.3,<2.0.0'],
 'llama-cpp': ['llama-cpp-python>=0.1.70,<0.2.0'],
 'openai': ['openai>=0.27.8,<0.28.0']}

entry_points = \
{'console_scripts': ['pxgpt = pxgpt.cli:main']}

setup_kwargs = {
    'name': 'pxgpt',
    'version': '0.0.0rc0',
    'description': 'Your personal, powerful and private GPT.',
    'long_description': '# <img src="pxgpt/frontend/public/assets/favicon.png" alt="p" width=28 />GPT: Your personal, powerful and private GPT\n\n## Features\n\n- Ingest of your own documents and talk to them.\n- Store your data locally on your device.\n- Choose from a variety of models, including OpenAI.\n- Support conversation history and memory.\n- Switch between profiles with different settings.\n- Support both web interface and command line interface.\n\n## Installation\n\n```shell\n# With all supported models\n$ pip install -U pxgpt[all]\n\n# With support for GPT4all only\n$ pip install -U pxgpt[gpt4all]\n\n# With support for llama-cpp only\n$ pip install -U pxgpt[llama-cpp]\n\n# With support for openai only\n$ pip install -U pxgpt[openai]\n```\n\n## Usage\n\n### Chat from CLI\n\n```shell\n$ 23:45:06 ❯ pxgpt chat\n\nWelcome to chat via the pxgpt CLI v0.0.0!\nHit \'Ctrl+c\' or \'Ctrl+d\' to exit.\n[2023-07-18 23:45:09,969] INFO Creating LLM (GPT4All)\nFound model file at  models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin\ngptj_model_load: loading model from \'models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin\' - please wait ...\ngptj_model_load: n_vocab = 50400\ngptj_model_load: n_ctx   = 2048\ngptj_model_load: n_embd  = 4096\ngptj_model_load: n_head  = 16\ngptj_model_load: n_layer = 28\ngptj_model_load: n_rot   = 64\ngptj_model_load: f16     = 2\ngptj_model_load: ggml ctx size = 5401.45 MB\ngptj_model_load: kv self size  =  896.00 MB\ngptj_model_load: ................................... done\ngptj_model_load: model size =  3609.38 MB / num tensors = 285\n[2023-07-18 23:45:11,741] INFO Entering chat mode\nLoaded conversation:  2023-07-16_23-11-27\nUse the up/down arrow keys to navigate history.\nUse /help to see the list of commands.\n\n>>> Hello?\n  Hi there! How may I help you today?\n\n>>> /help\nCommands:\n  - /help: List the commands\n  - /new: Start a new conversation\n  - /switch: Switch to a conversation\n  - /list: List all conversations\n  - /path: Show the path of the current conversation file\n  - /delete: Delete a conversation\n  - /rename: Rename a conversation\n  - /ingest: Ingest documents from the source directory\n  - /docs: List ingested and uningested documents in the source directory\n  - /exit: Exit the CLI\n\n>>>\n```\n\n### Chat from the web interface\n\n```shell\n$ pxgpt serve\n# Open http://localhost:7758 in your browser\n```\n\n![Web-interface](web-interface.png)\n\n### Configuration\n\nThe configuration files are loaded from the following paths:\n\n- `~/.config/pxgpt/config.yml`\n- `~/.pxgpt.config.yml`\n- `./.pxgpt.config.yml`\n\n#### Profiles\n\nNote that you need to define profiles in the configuration file. For example:\n\n```yaml\nopenai:  # The profile\n    model:\n        type: ChatOpenAI\n```\n\nThe configuration items are inherited from the `default` profile. For example:\n\n```yaml\ndefault:\n    credentials:\n        openai_api_key: sk-xxxxxxxxxxx\n\nopenai:\n    model:\n        type: ChatOpenAI\n```\n\nThen when you use `openai` profile, the configurations are expanded as:\n\n```yaml\nopenai:\n    credentials:\n        openai_api_key: sk-xxxxxxxxxxx\n    model:\n        type: ChatOpenAI\n```\n\nHigher-level configurations override lower-level configurations. For example:\n\nIf you define the `default` profile in `~/.config/pxgpt/config.yml` and the `openai` profile in `./.pxgpt.config.yml`, then the `openai` profile will inherit the `default` profile, as well.\n\n#### Configuration items\n\n- `log_level`: The log level for the logger in your teminal\n- `history_directory`: The directory to store the conversation history\n- `history_into_memory`: Whether to load the conversation history into memory\n  - You can turn this off if you are using small models\n- `credentials`: The credentials for the models.\n  For example, for OpenAI, you need to provide the `openai_api_key`.\n- `model`: Type of the model and arguments for it.\n  - `type`: The type of the model, supported models are: `GPT4All`, `LlamaCpp`, `ChatOpenAI` and `OpenAI`\n  - `<other>`: The arguments for the model. Passed to `langchain` llms.\n    - For `GPT4All`, you can pass the arguments listed in [here][1].\n    - For `LlamaCpp`, you can pass the arguments listed in [here][2].\n    - For `ChatOpenAI`, you can pass the arguments listed in [here][3].\n    - For `OpenAI`, you can pass the arguments listed in [here][4].\n- `qmodel`: The arguments for model used to condense questions\n  - `type`: Same as `model.type`, with and `Echo` model added, which is useful for models that don\'t do question condensing very well.\n  - `<other>`: Same as `model.<other>`.\n- `ingest`: The arguments for the ingestion.\n  - `source_directory`: The directory to ingest documents from.\n    - If not provided, we will enter the chat mode.\n  - `persist_directory`: The directory to save the vectorstore database.\n    - If not provided, will use `<source_directory>/.pxgpt-<model>-db`.\n  - `target_source_chunks`: The number of chunks to return against the query.\n  - `n_workers`: The number of workers to use for ingestion.\n  - `chunk_size` and `chunk_overlap`: The chunk size and overlap for the ingestion.\n- `embeddings`: The arguments for the embeddings.\n  - For `GPT4All`, you can pass the arguments listed in [here][5].\n  - For `LlamaCpp`, you can pass the arguments listed in [here][6].\n  - For `OpenAI` or `ChatOpenAI`, you can pass the arguments listed in [here][7].\n\n### Ingest documents\n\n```shell\n$ pxgpt ingest  # default profile\n$ pxgpt ingest --profile openai-docs\n# Will ingest documents under `ingest.source_directory` under `openai-docs` profile\n```\n\n## Credits\n\n`pxgpt` is Inspired by [privateGPT][8], with the addition of openai API support, history and memory support, and a web interface.\n\n## TODO\n\n- [ ] Support ingestion management (upload/download/delete/ingest documents) from the web interface\n- [ ] Support profile management (add/remove/modify) from the web interface\n- [ ] Build a docker image\n- [ ] Support more models\n\n## Q & A\n\n[QA.md](QA.md)\n\n[1]: https://api.python.langchain.com/en/latest/llms/langchain.llms.gpt4all.GPT4All.html#langchain.llms.gpt4all.GPT4All\n[2]: https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html#langchain.llms.llamacpp.LlamaCpp\n[3]: https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html#langchain.chat_models.openai.ChatOpenAI\n[4]: https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAI.html#langchain.llms.openai.OpenAI\n[5]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.huggingface.HuggingFaceEmbeddings.html#langchain.embeddings.huggingface.HuggingFaceEmbeddings\n[6]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.llamacpp.LlamaCppEmbeddings.html#langchain.embeddings.llamacpp.LlamaCppEmbeddings\n[7]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html#langchain.embeddings.openai.OpenAIEmbeddings\n[8]: https://github.com/imartinez/privateGPT\n',
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
