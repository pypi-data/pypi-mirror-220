import argx
from simpleconf import ProfileConfig


def main():
    """The main function"""
    parser = argx.ArgumentParser()

    profile_names = ["--profile", "-p"]
    profile_args = {
        "dest": "profile",
        "help": "Name of the profile to use from the config file",
        "default": "default",
    }

    # ingest
    parser_ingest = parser.add_command(
        "ingest", help="Ingest documents into the database"
    )
    parser_ingest.add_argument(*profile_names, **profile_args)
    parser_ingest.add_argument(
        "--force",
        "-f",
        action="store_true",
        default=False,
        help=(
            "Force ingestion, even if the document exists. "
            "You may want to use this if you have updated the documents or "
            "configurations for ingestion."
        ),
    )
    # chat
    parser_chat = parser.add_command(
        "chat", help="Chat with the model in the terminal"
    )
    parser_chat.add_argument(
        "--asyn",
        action="store_true",
        help=(
            "Use async calls to the model? "
            "Don't use it if you don't know what it is."
        ),
        default=False,
    )
    parser_chat.add_argument(*profile_names, **profile_args)
    # docs
    parser_docs = parser.add_command(
        "docs", help="Show ingested and pending documents under a profile"
    )
    parser_docs.add_argument(*profile_names, **profile_args)
    # serve
    parser_serve = parser.add_command(
        "serve", help="Serve a web interface to chat with the model"
    )
    parser_serve.add_argument(
        "--port",
        "-p",
        help="Port to serve the web interface on",
        default=7758,
        type=int,
    )
    # profiles
    parser.add_command(
        "profiles", help="List available profiles"
    )
    # zzz
    parser_zzz = parser.add_command(
        "zzz",
        help=(
            "A command used to solve that async not supported by some LLMs. "
            "Don't run this command manually."
        )
    )
    parser_zzz.add_argument(*profile_names, **profile_args)

    args = parser.parse_args()

    if args.COMMAND == 'ingest':
        from .ingest import ingest_cli
        ingest_cli(args.profile, args.force)

    elif args.COMMAND == 'chat':
        from .chat import chat_cli
        chat_cli(args.profile, args.asyn)

    elif args.COMMAND == 'serve':
        from .serve import serve
        serve(args.port)

    elif args.COMMAND == 'profiles':
        from .config import config
        profiles = ProfileConfig.profiles(config)
        print("\nAvailable profiles:\n")
        for profile in profiles:
            print(f"- {profile}")
        print()

    elif args.COMMAND == 'docs':
        from .docs import docs_cli
        docs_cli(args.profile)

    elif args.COMMAND == 'zzz':
        from .zzz import zzz
        zzz(args.profile)
