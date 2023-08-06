<div style="display: flex; align-items: center; justify-content: center; gap: .2rem">
  <img src="pxgpt/frontend/public/assets/favicon.png" alt="px" style="width: 32px; height: 32px;" />
  <div style="font-size: 24px; font-weight: bold">GPT</div>
</div>
<hr />
<p style="text-align: center">Your personal, powerful and private GPT</p>



## Features

- Ingest of your own documents and talk to them.
- Store your data locally on your device.
- Choose from a variety of models, including OpenAI.
- Support conversation history and memory.
- Switch between profiles with different settings.
- Support both web interface and command line interface.
- Support Llama v2!

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

Then copy the configuration from `.pxgpt.config-example.yml` to `.pxgpt.config.yml` and modify it to your needs.

## Usage

### Chat from CLI

```shell
$ 23:45:06 ❯ pxgpt chat

Welcome to chat via the pxGPT CLI v0.0.0rc0!
Hit 'Ctrl+c' or 'Ctrl+d' to exit.
[2023-07-20 20:03:22,716] INFO Switched profile to llamacpp-chat
[2023-07-20 20:03:22,719] INFO Creating LLM (LlamaCpp)
llama.cpp: loading model from models/llamacpp/llama-2-7b.ggmlv3.q4_0.bin
llama_model_load_internal: format     = ggjt v3 (latest)
llama_model_load_internal: n_vocab    = 32000
llama_model_load_internal: n_ctx      = 512
llama_model_load_internal: n_embd     = 4096
llama_model_load_internal: n_mult     = 256
llama_model_load_internal: n_head     = 32
llama_model_load_internal: n_layer    = 32
llama_model_load_internal: n_rot      = 128
llama_model_load_internal: freq_base  = 10000.0
llama_model_load_internal: freq_scale = 1
llama_model_load_internal: ftype      = 2 (mostly Q4_0)
llama_model_load_internal: n_ff       = 11008
llama_model_load_internal: model size = 7B
llama_model_load_internal: ggml ctx size =    0.08 MB
llama_model_load_internal: mem required  = 5185.72 MB (+ 1026.00 MB per state)
llama_new_context_with_model: kv self size  =  256.00 MB
[2023-07-20 20:03:24,552] INFO Entering chat mode
Loaded conversation:  2023-07-20_20-03-17
Use the up/down arrow keys to navigate history.
Use /help to see the list of commands.

>>> Hello Llama 2, if you could choose a superpower, what would it be and why?
 I will answer this question in two parts. The first part is the super power that I will choose. The second part is why I chose this super power.
In the first part, the super power that I will choose is the ability to fly. This is because flying has many benefits. It allows me to travel quickly and easily, without having to deal with traffic or waiting at airports. Additionally, it saves time since I don't have to wait for a bus or train ride. Finally, flying gives me an opportunity to see new places and explore new cultures.
In the second part of my answer, I will explain why I chose this super power. The reason is because flying allows me to travel quickly and easily, without having to deal with traffic or waiting at airports. Additionally, it saves time since I don't have to wait for a bus or train ride. Finally, flying gives me an opportunity to see new places and explore new cultures.

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
px
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
- [ ] Use markdown to format the response on the web interface
- [ ] Build a docker image
- [ ] Support more models

## Q & A

[QA.md](QA.md)

[1]: https://api.python.langchain.com/en/latest/llms/langchain.llms.gpt4all.GPT4All.html#langchain.llms.gpt4all.GPT4All
[2]: https://api.python.langchain.com/en/latest/llms/langchain.llms.llamacpp.LlamaCpp.html#langchain.llms.llamacpp.LlamaCpp
[3]: https://api.python.langchain.com/en/latest/chat_models/langchain.chat_models.openai.ChatOpenAI.html#langchain.chat_models.openai.ChatOpenAI
[4]: https://api.python.langchain.com/en/latest/llms/langchain.llms.openai.OpenAI.html#langchain.llms.openai.OpenAI
[5]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.gpt4all.GPT4AllEmbeddings.html#langchain.embeddings.gpt4all.GPT4AllEmbeddings
[6]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.llamacpp.LlamaCppEmbeddings.html#langchain.embeddings.llamacpp.LlamaCppEmbeddings
[7]: https://api.python.langchain.com/en/latest/embeddings/langchain.embeddings.openai.OpenAIEmbeddings.html#langchain.embeddings.openai.OpenAIEmbeddings
[8]: https://github.com/imartinez/privateGPT
