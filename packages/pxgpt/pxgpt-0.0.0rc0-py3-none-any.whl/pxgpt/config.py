from pathlib import Path

from diot import Diot
from simpleconf import ProfileConfig

DEFAULT_CONFIG = Diot(
    log_level="INFO",
    history_directory="~/.config/pxgpt/history",
    history_into_memory=True,
    credentials=Diot(
        openai_api_key=None,
    ),
    embeddings=Diot(),
    model=Diot(
        type="GPT4All",
        model="models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin",
    ),
    ingest=Diot(
        chunk_size=500,
        chunk_overlap=50,
        source_directory=None,
        n_workers=0,
        persist_directory=None,
        target_source_chunks=4,
    ),
)

CONFIG_SCHEMA = {
    "log_level": Diot(
        default=DEFAULT_CONFIG.log_level,
        kind="choice",
        choices=["NOTSET", "DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help=(
            "Log level for the logger in the terminal. Note that the server "
            "needs to be restarted for the change to take effect."
        ),
    ),
    "ingest.source_directory": Diot(
        default=None,
        kind="str",
        help=(
            "The directory to store the source files. "
            "If not set, then a chat chain is used, "
            "instead of a retrieval QA chain."
        ),
    ),
    "ingest.chunk_size": Diot(
        default=500,
        kind="int",
        help="Maximum size of chunks while ingesting the source documents",
    ),
    "ingest.chunk_overlap": Diot(
        default=50,
        kind="int",
        help="Overlap between chunks while ingesting the source documents",
    ),
    "ingest.n_workers": Diot(
        default=0,
        kind="int",
        help=(
            "Number of workers to use while ingesting the source documents. "
            "0 to use all available CPUs"
        ),
    ),
    "ingest.persist_directory": Diot(
        default=None,
        kind="str",
        help=(
            "The directory to store the vectorstore. If not set, "
            "`.pxgpt-<model>-db` under the source_directory is created and used"
        )
    ),
    "credentials.openai_api_key": Diot(
        default=None,
        kind="password",
        placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx",
        help="The API key for OpenAI API.",
    ),
    "model.type": Diot(
        default="GPT4All",
        kind="choice",
        choices=["GPT4All", "LlamaCpp", "OpenAI", "ChatOpenAI"],
        help=(
            "The type of the language model to use. "
            "When you choose GPT4All, you can also set `model_allow_download` "
            "to True to download the model from the internet automatically. "
            "When using openai models, if you are not sure about the model type"
            " you can just use `OpenAI` and the model will be automatically "
            "detected."
        ),
    ),
    # "model.<more>": Diot(
    #     default=None,
    #     kind="more",
    #     help=(
    #         "Model specific parameters passed to the language model. "
    #         "Not that `verbose`, `callbacks` and `streaming` are not allowed. "
    #         "You can use `model.allow_download` to download the model from the "
    #         "internet automatically for GPT4All, for example."
    #     ),
    # ),
    # model=Diot(
    #     default="models/gpt4all/ggml-gpt4all-j-v1.3-groovy.bin",
    #     kind="str",
    #     help=(
    #         "The path to the model file or the name of the model. "
    #         "If you allow download for some models, you can specify an "
    #         "unexisting path. The directories will be created automatically. "
    #     ),
    # ),
    "ingest.target_source_chunks": Diot(
        default=4,
        kind="int",
        help=(
            "The number of sources to use for each search. "
        ),
    ),
    "history_directory": Diot(
        default="~/.config/pxgpt/history",
        kind="str",
        help="The directory to store the history files",
    ),
    "history_into_memory": Diot(
        default=True,
        kind="bool",
        help=(
            "Whether to load the history files into memory. "
            "You can turn it off for small models."
        ),
    ),
}

# Used to save modified configs
MY_CONFIG_FILE = Path("./.pxgpt.config.yml")

CONFIG_FILES = [
    {"default": DEFAULT_CONFIG},
    Path("~/.config/pxgpt/config.yml").expanduser(),
    Path("~/.pxgpt.config.yml").expanduser(),
    MY_CONFIG_FILE,
]


config = ProfileConfig.load(*CONFIG_FILES, ignore_nonexist=True)
