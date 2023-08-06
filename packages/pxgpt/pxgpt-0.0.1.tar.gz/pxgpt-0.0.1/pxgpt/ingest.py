"""Provides the entrance of the ingest command."""

from .manager import Manager


def ingest_cli(profile: str, force: bool) -> None:
    """The entrance of the command.

    Args:
        profile: The profile.
    """
    manager = Manager(profile)
    if not manager.config.ingest.source_directory:
        print("No source directory specified, nothing to ingest.")
        return

    manager.ingest(force=force)
