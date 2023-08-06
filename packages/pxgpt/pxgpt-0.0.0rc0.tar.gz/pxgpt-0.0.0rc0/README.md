# <img src="pxgpt/frontend/public/assets/favicon.png" alt="p" width=28 />GPT: Your personal, powerful and private GPT

## Features

- Ingest of your own documents and talk to them.
- Store your data locally on your device.
- Choose from a variety of models, including OpenAI.
- Support conversation history and memory.
- Switch between profiles with different settings.
- Support both web interface and command line interface.

## Installation

```shell
# With all supported models
$ pip install -U pxgpt[all]

# With support for GPT4all only
$ pip install -U pxgpt[gpt4all]

# With support for llama-cpp only
$ pip install -U pxgpt[llama-cpp]

# With support for openai only
$ pip install -U pxgpt[openai]
```

## Usage

### Chat from CLI

```shell
$ 23:45:06 ❯ pxgpt chat

Welcome to chat via the pxgpt CLI v0.0.0!
Hit 'Ctrl+c' or 'Ctrl+d' to exit.
[2023-07-18 23:45:09,969] INFO Creating LLM (GPT4All)
Found model file at  models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin
gptj_model_load: loading model from 'models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin' - please wait ...
gptj_model_load: n_vocab = 50400
gptj_model_load: n_ctx   = 2048
gptj_model_load: n_embd  = 4096
gptj_model_load: n_head  = 16
gptj_model_load: n_layer = 28
gptj_model_load: n_rot   = 64
gptj_model_load: f16     = 2
gptj_model_load: ggml ctx size = 5401.45 MB
gptj_model_load: kv self size  =  896.00 MB
gptj_model_load: ................................... done
gptj_model_load: model size =  3609.38 MB / num tensors = 285
[2023-07-18 23:45:11,741] INFO Entering chat mode
Loaded conversation:  2023-07-16_23-11-27
Use the up/down arrow keys to navigate history.
Use /help to see the list of commands.

>>> Hello?
  Hi there! How may I help you today?

>>> /help
Commands:
  - /help: List the commands
  - /new: Start a new conversation
  - /switch: Switch to a conversation
  - /list: List all conversations
  - /path: Show the path of the current conversation file
  - /delete: Delete a conversation
  - /rename: Rename a conversation
  - /ingest: Ingest documents from the source directory
  - /docs: List ingested and uningested documents in the source directory
  - /exit: Exit the CLI

>>>
```

### Chat from the web interface

```shell
$ pxgpt serve
# Open http://localhost:7758 in your browser
```

![Web-interface](web-interface.png)

### Configuration

The configuration files are loaded from the following paths:

- `~/.config/pxgpt/config.yml`
- `~/.pxgpt.config.yml`
- `./.pxgpt.config.yml`

#### Profiles

Note that you need to define profiles in the configuration file. For example:

```yaml
openai:  # The profile
    model:
        type: ChatOpenAI
```

The configuration items are inherited from the `default` profile. For example:

```yaml
default:
    credentials:
        openai_api_key: sk-xxxxxxxxxxx

openai:
    model:
        type: ChatOpenAI
```

Then when you use `openai` profile, the configurations are expanded as:

```yaml
openai:
    credentials:
        openai_api_key: sk-xxxxxxxxxxx
    model:
        type: ChatOpenAI
```

Higher-level configurations override lower-level configurations. For example:

If you define the `default` profile in `~/.config/pxgpt/config.yml` and the `openai` profile in `./.pxgpt.config.yml`, then the `openai` profile will inherit the `default` profile, as well.

#### Configuration items

- `log_level`: The log level for the logger in your teminal
- `history_directory`: The directory to store the conversation history
- `history_into_memory`: Whether to load the conversation history into memory
  - You can turn this off if you are using small models
- `credentials`: The credentials for the models.
  For example, for OpenAI, you need to provide the `openai_api_key`.
- `model`: Type of the model and arguments for it.
  - `type`: The type of the model, supported models are: `GPT4All`, `LlamaCpp`, `ChatOpenAI` and `OpenAI`
  - `<other>`: The arguments for the model. Passed to `langchain` llms.
    - For `GPT4All`, you can pass the arguments listed in [here][1].
    - For `LlamaCpp`, you can pass the arguments listed in [here][2].
    - For `ChatOpenAI`, you can pass the arguments listed in [here][3].
    - For `OpenAI`, you can pass the arguments listed in [here][4].
- `qmodel`: The arguments for model used to condense questions
  - `type`: Same as `model.type`, with and `Echo` model added, which is useful for models that don't do question condensing very well.
  - `<other>`: Same as `model.<other>`.
- `ingest`: The arguments for the ingestion.
  - `source_directory`: The directory to ingest documents from.
    - If not provided, we will enter the chat mode.
  - `persist_directory`: The directory to save the vectorstore database.
    - If not provided, will use `<source_directory>/.pxgpt-<model>-db`.
  - `target_source_chunks`: The number of chunks to return against the query.
  - `n_workers`: The number of workers to use for ingestion.
  - `chunk_size` and `chunk_overlap`: The chunk size and overlap for the ingestion.
- `embeddings`: The arguments for the embeddings.
  - For `GPT4All`, you can pass the arguments listed in [here][5].
  - For `LlamaCpp`, you can pass the arguments listed in [here][6].
  - For `OpenAI` or `ChatOpenAI`, you can pass the arguments listed in [here][7].

### Ingest documents

```shell
$ pxgpt ingest  # default profile
$ pxgpt ingest --profile openai-docs
# Will ingest documents under `ingest.source_directory` under `openai-docs` profile
```

## Credits

`pxgpt` is Inspired by [privateGPT][8], with the addition of openai API support, history and memory support, and a web interface.

## TODO

- [ ] Support ingestion management (upload/download/delete/ingest documents) from the web interface
- [ ] Support profile management (add/remove/modify) from the web interface
- [ ] Build a docker image
- [ ] Support more models

## Q & A

[QA.md](QA.md)

[1]: https://api.python.langchain.com/en/latest/llms/langchain.llms.gpt4all.GPT4All.html#langchain.llms.gpt4all.GPT4All
[2]: https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html#langchain.llms.llamacpp.LlamaCpp
[3]: https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html#langchain.chat_models.openai.ChatOpenAI
[4]: https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAI.html#langchain.llms.openai.OpenAI
[5]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.huggingface.HuggingFaceEmbeddings.html#langchain.embeddings.huggingface.HuggingFaceEmbeddings
[6]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.llamacpp.LlamaCppEmbeddings.html#langchain.embeddings.llamacpp.LlamaCppEmbeddings
[7]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html#langchain.embeddings.openai.OpenAIEmbeddings
[8]: https://github.com/imartinez/privateGPT
