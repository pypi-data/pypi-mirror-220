"""Provides the entrance of the ingest command."""

from .manager import Manager


def docs_cli(profile: str) -> None:
    """The entrance of the command.

    Args:
        profile: The profile.
    """
    manager = Manager(profile, serving=True)
    if not manager.config.ingest.source_directory:
        print("Error: No source directory specified, nothing to show.")
        return

    docs = manager.get_docs()
    print("\nIngested documents:")
    for doc in docs['ingested']:
        print(f"- {doc['name']}: {doc['path']}")

    print("\nPending documents:")
    for doc in docs['pending']:
        print(f"- {doc['name']}: {doc['path']}")
